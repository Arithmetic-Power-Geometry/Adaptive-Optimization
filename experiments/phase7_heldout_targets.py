"""Phase 7 held-out target-hitting experiment; standalone and deterministic."""
import csv, numpy as np
from pathlib import Path
CAP=240
class Budget(Exception): pass
def instance(name,d,seed,rotation):
 rng=np.random.default_rng(55000+100*d+seed)
 Q,_=np.linalg.qr(rng.normal(size=(d,d)))
 if not rotation:Q=np.eye(d)
 shift=rng.uniform(-.6,.6,d)
 def f(x):
  z=Q@(np.asarray(x)-shift)
  if name=='ellipsoid':return np.sum(10.**np.linspace(0,4,d)*z*z)
  if name=='sphere':return np.sum(z*z)
  if name=='rastrigin':return 10*d+np.sum(z*z-10*np.cos(2*np.pi*z))
  return np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2)
 return f
def poll(m,x0,seed,mode):
 d=len(x0);rng=np.random.default_rng(seed);x=x0.copy();fx=m(x);step=np.full(d,1.0);memory=np.zeros(d);stale=0;probe_count=0;accepted_probes=0
 while m.n<CAP:
  improved=False
  do_probe=(mode=='Memory' and stale>=1) or (mode=='GatedMemory' and stale>=2 and np.linalg.norm(memory)>0.2)
  if do_probe and np.linalg.norm(memory)>1e-12:
   direction=memory/np.linalg.norm(memory)
   for sign in (1.,-1.):
    if m.n>=CAP:break
    y=np.clip(x+sign*np.mean(step)*direction,-3,3)
    if np.array_equal(y,x):continue
    fy=m(y);probe_count+=1
    if fy<fx:
     memory=.7*memory+.3*(y-x);x,fx=y,fy;improved=True;accepted_probes+=1;break
  if not improved:
   for j in rng.permutation(d):
    for sign in rng.permutation([-1.,1.]):
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
    x=rng.uniform(-3,3,d);fx=m(x);step[:]=1;memory[:]=0;stale=0
 return probe_count,accepted_probes
class Meter:
 def __init__(self,f,target):self.f=f;self.target=target;self.n=0;self.best=float('inf');self.hit=None
 def __call__(self,x):
  if self.n>=CAP:raise Budget()
  v=float(self.f(np.asarray(x)));self.n+=1;self.best=min(self.best,v)
  if self.hit is None and self.best<=self.target:self.hit=self.n
  return v
def save(path,rows):
 with open(path,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
if __name__=='__main__':
 rows=[]
 for d in (2,5):
  for name,target in [('sphere',1e-3),('ellipsoid',1.),('rastrigin',5.),('rosenbrock',5.)]:
   for rotated in (0,1):
    for seed in range(100,120):
     x0=np.random.default_rng(8000+seed+100*d).uniform(-2,2,d)
     for method in ('Adaptive','Memory','GatedMemory'):
      m=Meter(instance(name,d,seed,rotated),target);probes=accepted=0
      try:probes,accepted=poll(m,x0,seed,method)
      except Budget:pass
      rows.append(dict(dimension=d,function=name,rotated=rotated,seed=seed,method=method,target=target,hit_evaluations=m.hit or '',evaluations=m.n,best=m.best,probes=probes,accepted_probes=accepted))
 save('phase7_raw_results.csv',rows)
 summary=[]
 for d in (2,5):
  for name in ('sphere','ellipsoid','rastrigin','rosenbrock'):
   for rotated in (0,1):
    for method in ('Adaptive','Memory','GatedMemory'):
     g=[r for r in rows if (r['dimension'],r['function'],r['rotated'],r['method'])==(d,name,rotated,method)]
     hits=[int(r['hit_evaluations']) for r in g if r['hit_evaluations']!='']
     summary.append(dict(dimension=d,function=name,rotated=rotated,method=method,target=g[0]['target'],successes=len(hits),trials=len(g),median_hit_conditional=float(np.median(hits)) if hits else '',mean_probes=float(np.mean([r['probes'] for r in g])),median_final_best=float(np.median([r['best'] for r in g]))))
 save('phase7_summary.csv',summary)
 print('completed',len(rows),'runs')
