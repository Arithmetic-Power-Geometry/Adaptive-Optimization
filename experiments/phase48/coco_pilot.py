"""Phase48 COCO pilot. Official results require cocoex and cma in CI.
python experiments/phase48/coco_pilot.py --mode coco --out results/phase48
"""
import argparse,csv,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize,differential_evolution,LinearConstraint
class BudgetEnd(Exception):pass
class Meter:
 def __init__(self,f,budget):self.f=f;self.budget=budget;self.n=0;self.best=float('inf');self.x=None;self.trace=[]
 def __call__(self,x):
  if self.n>=self.budget:raise BudgetEnd()
  y=float(self.f(np.asarray(x)));self.n+=1
  if y<self.best:self.best=y;self.x=np.asarray(x).copy()
  self.trace.append(self.best);return y
def solve(p,method,B,seed):
 d=p.dimension;lo=np.asarray(p.lower_bounds);hi=np.asarray(p.upper_bounds)
 x0=np.clip(np.asarray(p.initial_solution),lo,hi)
 m=Meter(p,B);rng=np.random.default_rng(seed)
 def full(cap):
  used=0;anchor=x0 if m.x is None else m.x.copy()
  def fun(x):
   nonlocal used
   if used>=cap:raise BudgetEnd()
   used+=1;return m(x)
  try:minimize(fun,anchor,method='COBYQA',bounds=list(zip(lo,hi)),options={'maxfev':cap,'maxiter':cap})
  except BudgetEnd:pass
 def embed(cap):
  if cap<=0:return
  A,_=np.linalg.qr(rng.normal(size=(d,min(d,8))))
  anchor=x0 if m.x is None else m.x.copy();used=0
  def fun(z):
   nonlocal used
   if used>=cap:raise BudgetEnd()
   used+=1;return m(anchor+A@z)
  try:minimize(fun,np.zeros(A.shape[1]),method='COBYQA',constraints=[LinearConstraint(A,lo-anchor,hi-anchor)],options={'maxfev':cap,'maxiter':cap})
  except BudgetEnd:pass
 if method=='COBYQA':full(B)
 elif method=='Embed8':embed(B)
 elif method=='Restart8':embed(B//2);embed(B-m.n)
 elif method=='Gate8Full':
  embed(min(60,B//2))
  if m.n:
   q=min(30,m.n-1);a=max(0,m.trace[0]-m.trace[q]);b=max(0,m.trace[q]-m.trace[-1])
   if b<.1*a:full(B-m.n)
   else:embed(B-m.n)
 elif method=='DE':
  try:differential_evolution(m,list(zip(lo,hi)),popsize=5,maxiter=10000,polish=False,seed=seed,x0=x0,tol=0,atol=0)
  except BudgetEnd:pass
 elif method=='CMAES':
  import cma
  es=cma.CMAEvolutionStrategy(x0,2.,{'bounds':[lo.tolist(),hi.tolist()],'seed':seed,'verbose':-9,'maxfevals':B})
  while not es.stop() and m.n<B:
   xs=es.ask();ys=[]
   for x in xs:
    if m.n>=B:break
    ys.append(m(x))
   if len(xs)==len(ys):es.tell(xs,ys)
   else:break
 else:raise ValueError(method)
 assert m.n==p.evaluations,(m.n,p.evaluations)
 return m
def main():
 a=argparse.ArgumentParser()
 a.add_argument('--mode',choices=['coco'],default='coco');a.add_argument('--dimension',type=int,default=20)
 a.add_argument('--instances',default='1-5');a.add_argument('--functions',default='1,2,3,4,5')
 a.add_argument('--budget-mult',type=int,default=50);a.add_argument('--methods',default='COBYQA,Embed8,Restart8,Gate8Full,DE,CMAES')
 a.add_argument('--out',default='results/phase48');z=a.parse_args()
 import cocoex
 low,high=map(int,z.instances.split('-'));funcs=[int(x) for x in z.functions.split(',')]
 methods=z.methods.split(',');B=z.dimension*z.budget_mult
 suite=cocoex.Suite('bbob','',f'dimensions:{z.dimension} instance_indices:{low}-{high} function_indices:{",".join(map(str,funcs))}')
 rows=[];traces=[]
 for fun in funcs:
  for inst in range(low,high+1):
   for method in methods:
    p=suite.get_problem_by_function_dimension_instance(fun,z.dimension,inst)
    try:
     seed=123000+fun*1000+inst*10
     m=solve(p,method,B,seed)
     rows.append(dict(problem=p.id,function=fun,instance=inst,method=method,budget=B,calls=m.n,best=m.best))
     traces.extend(dict(problem=p.id,method=method,call=i,best=v) for i,v in enumerate(m.trace,1))
    finally:p.free()
 suite.free()
 out=Path(z.out);out.mkdir(parents=True,exist_ok=True)
 for name,data in [('raw_results.csv',rows),('traces.csv',traces)]:
  with (out/name).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 (out/'protocol.json').write_text(json.dumps(vars(z),indent=2)+'\n')
 print('completed',len(rows),'official COCO runs')
if __name__=='__main__':main()
