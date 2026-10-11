"""Phase 5 independent reproducer: rotated directional-memory polling, DE, Powell."""
import csv,numpy as np
from scipy.optimize import minimize,differential_evolution
CAP=300
class Stop(Exception):pass
def instance(name,d,seed):
 r=np.random.default_rng(9000+100*d+seed);Q,_=np.linalg.qr(r.normal(size=(d,d)));shift=r.uniform(-.7,.7,d)
 def f(x):
  z=Q@(np.asarray(x)-shift)
  if name=="ellipsoid":return float(np.sum(10.**np.linspace(0,4,d)*z*z))
  if name=="rastrigin":return float(10*d+np.sum(z*z-10*np.cos(2*np.pi*z)))
  return float(np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2))
 return f
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=float("inf");self.trace=[]
 def __call__(self,x):
  if self.n>=CAP:raise Stop()
  v=self.f(x);self.n+=1;self.best=min(self.best,v)
  if self.n in (30,60,100,150,200,250,300):self.trace.append((self.n,self.best))
  return v
def poll(m,d,seed,memory):
 r=np.random.default_rng(seed);x=r.uniform(-3,3,d);fx=m(x);step=np.full(d,1.5);direction=np.zeros(d);stale=0;probes=0
 while m.n<CAP:
  improved=False
  if memory and stale and np.linalg.norm(direction)>1e-12:
   delta=direction/np.linalg.norm(direction)*np.mean(step)
   for sign in (1.,-1.):
    if m.n>=CAP:break
    y=np.clip(x+sign*delta,-3,3)
    if np.array_equal(y,x):continue
    fy=m(y);probes+=1
    if fy<fx:
     direction=.7*direction+.3*(y-x);x,fx=y,fy;improved=True;break
  if not improved:
   for j in r.permutation(d):
    for sign in r.permutation([-1.,1.]):
     if m.n>=CAP:break
     y=x.copy();y[j]=np.clip(y[j]+sign*step[j],-3,3)
     if y[j]==x[j]:continue
     fy=m(y)
     if fy<fx:
      direction=.7*direction+.3*(y-x);x,fx=y,fy;step[j]=min(step[j]*1.15,6);improved=True;break
    if m.n>=CAP:break
  if improved:stale=0
  else:
   stale+=1;step*=.5
   if np.max(step)<1e-6 and m.n<CAP:
    x=r.uniform(-3,3,d);fx=m(x);step[:]=1.5;direction[:]=0
 return probes
def write(path,rows):
 with open(path,"w",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
if __name__=="__main__":
 rows=[];traces=[]
 for d in (2,5,10):
  for name in ("ellipsoid","rastrigin","rosenbrock"):
   for seed in range(5):
    for method in ("AdaptivePoll","MemoryPoll","DE","Powell"):
     m=Meter(instance(name,d,seed));probes=0
     try:
      if method in ("AdaptivePoll","MemoryPoll"):probes=poll(m,d,seed,method=="MemoryPoll")
      elif method=="DE":differential_evolution(m,[(-3,3)]*d,rng=np.random.default_rng(seed),popsize=5,maxiter=1000,polish=False,tol=0,atol=0)
      else:minimize(m,np.random.default_rng(seed).uniform(-3,3,d),method="Powell",bounds=[(-3,3)]*d,options={"maxfev":CAP,"xtol":1e-6,"ftol":1e-9})
     except Stop:pass
     rows.append(dict(dimension=d,function=name,seed=seed,method=method,evaluations=m.n,best=m.best,memory_probes=probes))
     for n,v in m.trace:traces.append(dict(dimension=d,function=name,seed=seed,method=method,evaluations=n,best=v))
 write("phase5_raw_results.csv",rows);write("phase5_trajectories.csv",traces)
 summary=[]
 for d in (2,5,10):
  for name in ("ellipsoid","rastrigin","rosenbrock"):
   for method in ("AdaptivePoll","MemoryPoll","DE","Powell"):
    g=[x for x in rows if (x["dimension"],x["function"],x["method"])==(d,name,method)]
    summary.append(dict(dimension=d,function=name,method=method,median_best=float(np.median([x["best"] for x in g])),mean_evaluations=float(np.mean([x["evaluations"] for x in g]))))
 write("phase5_summary.csv",summary)
 for x in summary:print(x)
