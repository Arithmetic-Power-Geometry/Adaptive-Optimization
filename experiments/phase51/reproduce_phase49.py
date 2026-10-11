"""Phase51 exact reproduction runner for the Phase49 200-run mock benchmark.
The output schema and algorithm are the locally re-executed Phase48 reference.
This is synthetic data, NOT official COCO/BBOB.
"""
import argparse,csv,json,platform
from pathlib import Path
import numpy as np
from scipy.optimize import minimize,differential_evolution,LinearConstraint
class BudgetEnd(Exception):pass
class Meter:
 def __init__(self,f,budget):self.f=f;self.budget=budget;self.n=0;self.best=float('inf');self.best_x=None;self.trace=[]
 def __call__(self,x):
  if self.n>=self.budget:raise BudgetEnd()
  y=float(self.f(np.asarray(x,dtype=float)));self.n+=1
  if y<self.best:self.best=y;self.best_x=np.asarray(x,dtype=float).copy()
  self.trace.append(self.best);return y
class MockProblem:
 def __init__(self,d,fun,inst):
  self.dimension=d;self.function=fun;self.instance=inst;self.id=f'mock_f{fun:03d}_i{inst:02d}_d{d:02d}'
  self.lower_bounds=np.full(d,-5.);self.upper_bounds=np.full(d,5.)
  self.initial_solution=np.zeros(d);self.evaluations=0
  self.shift=np.random.default_rng(10000+fun*100+inst).uniform(-2,2,d)
 def __call__(self,x):
  self.evaluations+=1;z=np.asarray(x)-self.shift
  return float(z@z) if self.function==1 else float(10*self.dimension+np.sum(z*z-10*np.cos(2*np.pi*z)))
 def free(self):pass
def run_method(problem,method,B,seed):
 d=problem.dimension;lb=np.asarray(problem.lower_bounds,dtype=float);ub=np.asarray(problem.upper_bounds,dtype=float)
 x0=np.clip(np.asarray(problem.initial_solution,dtype=float),lb,ub)
 m=Meter(problem,B);rng=np.random.default_rng(seed)
 def full(cap):
  used=0;anchor=x0.copy() if m.best_x is None else m.best_x.copy()
  def fn(x):
   nonlocal used
   if used>=cap:raise BudgetEnd()
   used+=1;return m(x)
  try:minimize(fn,anchor,method='COBYQA',bounds=list(zip(lb,ub)),options={'maxfev':cap,'maxiter':max(cap,1)})
  except BudgetEnd:pass
 def embed(cap,k=8):
  if cap<=0:return
  A,_=np.linalg.qr(rng.normal(size=(d,min(k,d))))
  anchor=x0.copy() if m.best_x is None else m.best_x.copy();used=0
  def fn(z):
   nonlocal used
   if used>=cap:raise BudgetEnd()
   used+=1;return m(anchor+A@z)
  try:minimize(fn,np.zeros(A.shape[1]),method='COBYQA',constraints=[LinearConstraint(A,lb-anchor,ub-anchor)],options={'maxfev':cap,'maxiter':max(cap,1)})
  except BudgetEnd:pass
 if method=='COBYQA':full(B)
 elif method=='Embed8':embed(B)
 elif method=='Restart8':embed(B//2);embed(B-m.n)
 elif method=='Gate8Full':
  stage=min(60,B//2);embed(stage)
  if m.n:
   q=min(30,m.n-1);early=max(0,m.trace[0]-m.trace[q]);late=max(0,m.trace[q]-m.trace[-1])
   if late<.1*early:full(B-m.n)
   else:embed(B-m.n)
 elif method=='DE':
  try:differential_evolution(m,list(zip(lb,ub)),popsize=5,maxiter=10000,polish=False,seed=seed,x0=x0,tol=0,atol=0)
  except BudgetEnd:pass
 else:raise ValueError(method)
 assert m.n<=B and problem.evaluations==m.n
 return m
def main():
 p=argparse.ArgumentParser();p.add_argument('--dimension',type=int,default=10);p.add_argument('--instances',default='1-20');p.add_argument('--functions',default='1,2');p.add_argument('--budget-mult',type=int,default=12);p.add_argument('--out',default='results/phase51');a=p.parse_args()
 funcs=[int(v) for v in a.functions.split(',')];lo,hi=map(int,a.instances.split('-'))
 methods=('COBYQA','Embed8','Restart8','Gate8Full','DE');B=a.dimension*a.budget_mult
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 rows=[];traces=[]
 for fun in funcs:
  for inst in range(lo,hi+1):
   for method in methods:
    problem=MockProblem(a.dimension,fun,inst)
    seed=123000+fun*1000+inst*10
    meter=run_method(problem,method,B,seed)
    rows.append(dict(problem=problem.id,function=fun,instance=inst,dimension=a.dimension,method=method,budget=B,calls=meter.n,best=meter.best,mode='mock'))
    traces.extend(dict(problem=problem.id,method=method,call=i,best=v) for i,v in enumerate(meter.trace,1))
    problem.free()
 for name,data in [('raw_results.csv',rows),('traces.csv',traces)]:
  with (out/name).open('w',newline='') as f:
   writer=csv.DictWriter(f,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
 (out/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,mode='mock',dimension=a.dimension,instances=a.instances,functions=funcs,methods=list(methods),budget=B),indent=2)+'\n')
 print('COMPLETE',len(rows),'runs',len(traces),'charged evaluations',out)
if __name__=='__main__':main()
