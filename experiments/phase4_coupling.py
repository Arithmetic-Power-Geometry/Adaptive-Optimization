import csv, numpy as np
from pathlib import Path
from scipy.optimize import direct, differential_evolution
CAP=240
class Budget(Exception): pass
class Meter:
 def __init__(self,f): self.f=f;self.n=0;self.best=float('inf');self.trace=[]
 def __call__(self,x):
  if self.n>=CAP:raise Budget()
  v=float(self.f(np.asarray(x)));self.n+=1;self.best=min(self.best,v)
  if self.n in (40,80,120,180,240):self.trace.append((self.n,self.best))
  return v
def instance(name,d,seed,rotated):
 rng=np.random.default_rng(9000+100*d+seed)
 Q,_=np.linalg.qr(rng.normal(size=(d,d)))
 if not rotated:Q=np.eye(d)
 shift=rng.uniform(-.7,.7,d)
 def f(x):
  z=Q@(np.asarray(x)-shift)
  if name=='ellipsoid':return np.sum(10.**np.linspace(0,4,d)*z*z)
  if name=='rastrigin':return 10*d+np.sum(z*z-10*np.cos(2*np.pi*z))
  return np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2)
 return f
def poll(m,d,seed,mode):
 rng=np.random.default_rng(seed);x=rng.uniform(-3,3,d);fx=m(x);step=np.full(d,1.5);Q=np.eye(d);stale=0;coupling=0.;tests=0;rotations=0
 if mode=='CouplingPoll' and m.n+3<=CAP:
  e=np.eye(d);h=.12;p=np.clip(x+h*e[0],-3,3);q=np.clip(x+h*e[1],-3,3);pq=np.clip(x+h*(e[0]+e[1]),-3,3)
  a,b,c=m(p),m(q),m(pq)
  coupling=abs(c-a-b+fx)/(abs(a-fx)+abs(b-fx)+1e-9);tests+=1
 while m.n<CAP:
  improved=False
  for j in rng.permutation(d):
   for sign in rng.permutation([-1.,1.]):
    if m.n>=CAP:break
    y=np.clip(x+sign*step[j]*Q[:,j],-3,3)
    if np.array_equal(y,x):continue
    fy=m(y)
    if fy<fx:
     x,fx=y,fy;improved=True;step[j]=min(1.15*step[j],6);break
   if m.n>=CAP:break
  if improved:stale=0
  else:
   stale+=1;step*=.5
   if mode=='RotatingPoll' and stale%2==0:
    Q,_=np.linalg.qr(rng.normal(size=(d,d)));step=np.maximum(step,.3);rotations+=1
   if mode=='CouplingPoll' and stale%2==0 and coupling>.15:
    Q,_=np.linalg.qr(rng.normal(size=(d,d)));step=np.maximum(step,.3);rotations+=1
   if np.max(step)<1e-6 and m.n<CAP:
    x=rng.uniform(-3,3,d);fx=m(x);step[:]=1.5
 return coupling,tests,rotations
def run(name,d,seed,rotated,method):
 m=Meter(instance(name,d,seed,rotated));info=(0.,0,0)
 try:
  if method in ('AdaptivePoll','RotatingPoll','CouplingPoll'):info=poll(m,d,seed,method)
  elif method=='DE':differential_evolution(m,[(-3,3)]*d,rng=np.random.default_rng(seed),popsize=5,maxiter=1000,polish=False,tol=0,atol=0)
  elif method=='DIRECT':direct(m,[(-3,3)]*d,maxfun=CAP,maxiter=CAP,locally_biased=False)
 except (Budget,SystemError):pass
 return m,info
def write(path,rows):
 with open(path,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
if __name__=='__main__':
 root=Path(__file__).resolve().parent;rows=[];trace=[]
 for d in (2,5):
  for name in ('ellipsoid','rastrigin','rosenbrock'):
   for rotated in (False,True):
    for seed in range(5):
     for method in ('AdaptivePoll','RotatingPoll','CouplingPoll','DE','DIRECT'):
      m,(c,t,r)=run(name,d,seed,rotated,method)
      rows.append(dict(dimension=d,function=name,rotated=int(rotated),seed=seed,method=method,evaluations=m.n,best=m.best,coupling=c,coupling_tests=t,rotations=r))
      for n,v in m.trace:trace.append(dict(dimension=d,function=name,rotated=int(rotated),seed=seed,method=method,evaluations=n,best=v))
 write(root/'phase4_raw_results.csv',rows);write(root/'phase4_trajectories.csv',trace)
 summary=[]
 for d in (2,5):
  for name in ('ellipsoid','rastrigin','rosenbrock'):
   for rotated in (False,True):
    for method in ('AdaptivePoll','RotatingPoll','CouplingPoll','DE','DIRECT'):
     g=[r for r in rows if (r['dimension'],r['function'],r['rotated'],r['method'])==(d,name,int(rotated),method)]
     summary.append(dict(dimension=d,function=name,rotated=int(rotated),method=method,median_best=float(np.median([r['best'] for r in g])),mean_evaluations=float(np.mean([r['evaluations'] for r in g])),trials=5))
 write(root/'phase4_summary.csv',summary)
 for row in summary:print(row)
