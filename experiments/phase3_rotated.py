"""Phase 3: shifted, rotated functions; hard 300-evaluation cap. Python 3.13, NumPy 2.3.5, SciPy 1.17.0."""
import csv, numpy as np
from scipy.optimize import direct, differential_evolution
from pathlib import Path
CAP=300
class Stop(Exception): pass
class Count:
 def __init__(self,f):self.f=f;self.n=0;self.best=float('inf');self.trace=[]
 def __call__(self,x):
  if self.n>=CAP:raise Stop()
  y=float(self.f(np.asarray(x)));self.n+=1;self.best=min(self.best,y)
  if self.n in (30,100,200,300):self.trace.append((self.n,self.best))
  return y
def instance(name,d,seed):
 rng=np.random.default_rng(9000+100*d+seed)
 q,_=np.linalg.qr(rng.normal(size=(d,d))); shift=rng.uniform(-.7,.7,d)
 def f(x):
  z=q@(np.asarray(x)-shift)
  if name=="ellipsoid":return np.sum((10.**np.linspace(0,4,d))*z*z)
  if name=="rastrigin":return 10*d+np.sum(z*z-10*np.cos(2*np.pi*z))
  return np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2)
 return f
def poll(m,d,seed,rotating):
 rng=np.random.default_rng(seed);x=rng.uniform(-3,3,d);fx=m(x);step=np.full(d,1.5);Q=np.eye(d);stale=0
 while m.n<CAP:
  better=False
  for j in rng.permutation(d):
   for sign in rng.permutation([-1.,1.]):
    if m.n>=CAP:break
    y=np.clip(x+sign*step[j]*Q[:,j],-3,3)
    if np.array_equal(y,x):continue
    fy=m(y)
    if fy<fx:
     x,fx=y,fy;better=True;step[j]=min(1.15*step[j],6);break
   if m.n>=CAP:break
  if better:stale=0
  else:
   stale+=1;step*=.5
   if rotating and stale%2==0:
    Q,_=np.linalg.qr(rng.normal(size=(d,d)));step=np.maximum(step,.3)
   if max(step)<1e-6 and m.n<CAP:
    x=rng.uniform(-3,3,d);fx=m(x);step[:]=1.5
def evaluate(name,d,seed,method):
 m=Count(instance(name,d,seed))
 try:
  if method in ("AdaptivePoll","RotatingPoll"):poll(m,d,seed,method=="RotatingPoll")
  elif method=="DE":
   differential_evolution(m,[(-3,3)]*d,rng=np.random.default_rng(seed),popsize=5,maxiter=1000,polish=False,tol=0,atol=0)
  else:direct(m,[(-3,3)]*d,maxfun=CAP,maxiter=CAP,locally_biased=False)
 except (Stop,SystemError):pass
 return m
def save(name,rows):
 with open(Path(__file__).with_name(name),"w",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
if __name__=="__main__":
 rows=[];trace=[]
 for d in (2,5,10):
  for name in ("ellipsoid","rastrigin","rosenbrock"):
   for seed in range(5):
    for method in ("AdaptivePoll","RotatingPoll","DE","DIRECT"):
     m=evaluate(name,d,seed,method)
     rows.append(dict(dimension=d,function=name,seed=seed,method=method,evaluations=m.n,best=m.best))
     for n,v in m.trace:trace.append(dict(dimension=d,function=name,seed=seed,method=method,evaluations=n,best=v))
 save("phase3_raw_results.csv",rows);save("phase3_trajectories.csv",trace)
 summary=[]
 for d in (2,5,10):
  for name in ("ellipsoid","rastrigin","rosenbrock"):
   for method in ("AdaptivePoll","RotatingPoll","DE","DIRECT"):
    group=[r for r in rows if (r["dimension"],r["function"],r["method"])==(d,name,method)]
    summary.append(dict(dimension=d,function=name,method=method,median_best=float(np.median([r["best"] for r in group])),mean_evaluations=float(np.mean([r["evaluations"] for r in group])),runs=5))
 save("phase3_summary.csv",summary)
 for x in summary:print(x)
