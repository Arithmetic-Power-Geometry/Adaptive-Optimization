"""Phase 6: gated memory search; 1200 runs, hard cap 240 evaluations."""
import csv, numpy as np
from scipy.optimize import differential_evolution, minimize
CAP=240
class Budget(Exception): pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=float('inf');self.trace=[]
 def __call__(self,x):
  if self.n>=CAP:raise Budget()
  v=float(self.f(np.asarray(x)));self.n+=1;self.best=min(self.best,v)
  if self.n in (20,40,80,120,180,240):self.trace.append((self.n,self.best))
  return v
def objective(name,d,seed,rotated):
 r=np.random.default_rng(55000+100*d+seed)
 Q,_=np.linalg.qr(r.normal(size=(d,d)))
 if not rotated:Q=np.eye(d)
 shift=r.uniform(-.6,.6,d)
 def f(x):
  z=Q@(np.asarray(x)-shift)
  if name=='sphere':return np.sum(z*z)
  if name=='ellipsoid':return np.sum(10.**np.linspace(0,4,d)*z*z)
  if name=='rastrigin':return 10*d+np.sum(z*z-10*np.cos(2*np.pi*z))
  return np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2)
 return f
def poll(m,x0,seed,method):
 d=len(x0);r=np.random.default_rng(seed);x=x0.copy();fx=m(x);step=np.full(d,1.);memory=np.zeros(d);stale=0;probes=accepts=0
 while m.n<CAP:
  improved=False
  do=(method=='Memory' and stale>=1) or (method=='GatedMemory' and stale>=2 and np.linalg.norm(memory)>0.2)
  if do and np.linalg.norm(memory)>1e-12:
   direction=memory/np.linalg.norm(memory)
   for sign in (1.,-1.):
    if m.n>=CAP:break
    y=np.clip(x+sign*np.mean(step)*direction,-3,3)
    if np.array_equal(y,x):continue
    fy=m(y);probes+=1
    if fy<fx:
     memory=.7*memory+.3*(y-x);x,fx=y,fy;improved=True;accepts+=1;break
  if not improved:
   for j in r.permutation(d):
    for sign in r.permutation([-1.,1.]):
     if m.n>=CAP:break
     y=x.copy();y[j]=np.clip(y[j]+sign*step[j],-3,3)
     if y[j]==x[j]:continue
     fy=m(y)
     if fy<fx:
      memory=.7*memory+.3*(y-x);x,fx=y,fy;step[j]=min(1.15*step[j],6);improved=True;break
    if m.n>=CAP:break
  if improved:stale=0
  else:
   stale+=1;step*=.5
   if np.max(step)<1e-6 and m.n<CAP:
    x=r.uniform(-3,3,d);fx=m(x);step[:]=1;memory[:]=0;stale=0
 return probes,accepts
def save(path,rows):
 with open(path,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
if __name__=='__main__':
 rows=[];traces=[]
 for d in (2,5,10):
  for name in ('sphere','ellipsoid','rastrigin','rosenbrock'):
   for rotated in (0,1):
    for seed in range(10):
     x0=np.random.default_rng(8000+seed+100*d).uniform(-2,2,d)
     f=objective(name,d,seed,rotated)
     for method in ('Adaptive','Memory','GatedMemory','DE','Powell'):
      m=Meter(f);probes=accepts=0
      try:
       if method in ('Adaptive','Memory','GatedMemory'):probes,accepts=poll(m,x0,seed,method)
       elif method=='DE':differential_evolution(m,[(-3,3)]*d,rng=np.random.default_rng(seed),popsize=5,maxiter=1000,polish=False,tol=0,atol=0,init='latinhypercube')
       else:minimize(m,x0,method='Powell',bounds=[(-3,3)]*d,options={'maxfev':CAP,'xtol':1e-6,'ftol':1e-9})
      except Budget:pass
      rows.append(dict(dimension=d,function=name,rotated=rotated,seed=seed,method=method,evaluations=m.n,best=m.best,probes=probes,accepted_probes=accepts))
      for n,v in m.trace:traces.append(dict(dimension=d,function=name,rotated=rotated,seed=seed,method=method,evaluations=n,best=v))
 save('raw_results.csv',rows);save('trajectories.csv',traces)
 summary=[]
 for d in (2,5,10):
  for name in ('sphere','ellipsoid','rastrigin','rosenbrock'):
   for rotated in (0,1):
    for method in ('Adaptive','Memory','GatedMemory','DE','Powell'):
     g=[r for r in rows if (r['dimension'],r['function'],r['rotated'],r['method'])==(d,name,rotated,method)]
     summary.append(dict(dimension=d,function=name,rotated=rotated,method=method,median_best=float(np.median([r['best'] for r in g])),mean_evaluations=float(np.mean([r['evaluations'] for r in g])),mean_probes=float(np.mean([r['probes'] for r in g])),successes_le_1e_3=sum(r['best']<=1e-3 for r in g),trials=10))
 save('summary.csv',summary)
 for row in summary:print(row)
