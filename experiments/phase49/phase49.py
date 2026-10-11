"""Phase49 reproducible mock-suite ablation; synthetic tests, not official BBOB."""
import argparse,csv,json,platform
from pathlib import Path
import numpy as np
from scipy.optimize import minimize,differential_evolution,LinearConstraint
class Stop(Exception):pass
class Problem:
 def __init__(self,d,fun,inst):
  self.dimension=d;self.id=f'mock_f{fun:03d}_i{inst:02d}_d{d:02d}'
  self.lower_bounds=np.full(d,-5.);self.upper_bounds=np.full(d,5.);self.initial_solution=np.zeros(d);self.evaluations=0
  self.shift=np.random.default_rng(10000+fun*100+inst).uniform(-2,2,d);self.fun=fun
 def __call__(self,x):
  self.evaluations+=1;z=np.asarray(x)-self.shift
  return float(z@z) if self.fun==1 else float(10*self.dimension+np.sum(z*z-10*np.cos(2*np.pi*z)))
 def free(self):pass
class Meter:
 def __init__(self,p,B):self.p=p;self.B=B;self.n=0;self.best=float('inf');self.x=None;self.trace=[]
 def __call__(self,x):
  if self.n>=self.B:raise Stop()
  v=float(self.p(x));self.n+=1
  if v<self.best:self.best=v;self.x=np.asarray(x).copy()
  self.trace.append(self.best);return v
def run(p,method,B,seed):
 d=p.dimension;lo=p.lower_bounds;hi=p.upper_bounds;x0=p.initial_solution
 m=Meter(p,B);rng=np.random.default_rng(seed)
 def full(cap):
  used=0;anchor=x0.copy() if m.x is None else m.x.copy()
  def fn(x):
   nonlocal used
   if used>=cap:raise Stop()
   used+=1;return m(x)
  try:minimize(fn,anchor,method='COBYQA',bounds=list(zip(lo,hi)),options={'maxfev':cap,'maxiter':max(cap,1)})
  except Stop:pass
 def embed(cap):
  if cap<=0:return
  A,_=np.linalg.qr(rng.normal(size=(d,min(8,d))));anchor=x0.copy() if m.x is None else m.x.copy();used=0
  def fn(z):
   nonlocal used
   if used>=cap:raise Stop()
   used+=1;return m(anchor+A@z)
  try:minimize(fn,np.zeros(A.shape[1]),method='COBYQA',constraints=[LinearConstraint(A,lo-anchor,hi-anchor)],options={'maxfev':cap,'maxiter':max(cap,1)})
  except Stop:pass
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
  except Stop:pass
 else:raise ValueError(method)
 assert m.n<=B and p.evaluations==m.n
 return m
def main():
 a=argparse.ArgumentParser();a.add_argument('--mode',choices=['mock'],required=True);a.add_argument('--dimension',type=int,default=10);a.add_argument('--instances',default='1-20');a.add_argument('--functions',default='1,2');a.add_argument('--budget-mult',type=int,default=12);a.add_argument('--methods',default='COBYQA,Embed8,Restart8,Gate8Full,DE');a.add_argument('--out',default='results/phase49');z=a.parse_args()
 low,high=map(int,z.instances.split('-'));rows=[];traces=[]
 for fun in map(int,z.functions.split(',')):
  for inst in range(low,high+1):
   for method in z.methods.split(','):
    p=Problem(z.dimension,fun,inst);m=run(p,method,z.dimension*z.budget_mult,123000+fun*1000+inst*10)
    rows.append(dict(problem=p.id,function=fun,instance=inst,dimension=z.dimension,method=method,budget=m.B,calls=m.n,best=m.best,mode='mock'))
    traces.extend(dict(problem=p.id,method=method,call=i,best=v) for i,v in enumerate(m.trace,1))
 out=Path(z.out);out.mkdir(parents=True,exist_ok=True)
 for name,data in [('raw_results.csv',rows),('traces.csv',traces)]:
  with (out/name).open('w',newline='') as h:
   w=csv.DictWriter(h,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 (out/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,protocol=vars(z)),indent=2)+'\n')
 print('COMPLETE',len(rows),'runs',len(traces),'charged evaluations')
if __name__=='__main__':main()
