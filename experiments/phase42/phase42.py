"""Phase 42: budget-matched held-out SciPy differential evolution comparison."""
import csv, json, hashlib, platform, argparse
from pathlib import Path
import numpy as np, scipy
from scipy.optimize import minimize, differential_evolution
P=Path(__file__).resolve().parent
B=120
class Stop(Exception): pass
class Meter:
 def __init__(self,f): self.f=f;self.n=0;self.best=float('inf');self.x=None
 def __call__(self,x):
  if self.n>=B: raise Stop()
  x=np.asarray(x);v=float(self.f(x));self.n+=1
  if v<self.best:self.best=v;self.x=x.copy()
  return v

def instance(family,d,r,seed):
 rng=np.random.default_rng(seed*53+d*17+r*101)
 Q,_=np.linalg.qr(rng.normal(size=(d,r)))
 shift=rng.uniform(-2,2,r);x0=rng.uniform(-1.5,1.5,d)
 def f(x):
  z=Q.T@x-shift
  if family=='sphere': return float(z@z)
  if family=='rastrigin': return float(10*r+np.sum(z*z-10*np.cos(2*np.pi*z)))
  return float(np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2))
 return f,x0

def run(f,x0,seed,method):
 m=Meter(f);d=len(x0);rng=np.random.default_rng(seed+91000)
 if method=='COBYQA':
  try:minimize(m,x0,method='COBYQA',options={'maxfev':B,'maxiter':B})
  except Stop:pass
 elif method=='DE':
  # population 5*d; strict cap, bounded [-5,5]^d, includes initial point
  try:differential_evolution(m,[(-5,5)]*d,popsize=5,maxiter=1000,polish=False,seed=seed,init='latinhypercube',x0=x0,tol=0,atol=0)
  except Stop:pass
 else:
  stages=[B] if method=='Embed8' else [B//2,B//2]
  for cap in stages:
   A,_=np.linalg.qr(rng.normal(size=(d,min(8,d))))
   anchor=x0 if m.x is None else m.x.copy();used=0
   def reduced(z):
    nonlocal used
    if used>=cap:raise Stop()
    used+=1;return m(anchor+A@z)
   try:minimize(reduced,np.zeros(A.shape[1]),method='COBYQA',options={'maxfev':cap,'maxiter':cap})
   except Stop:pass
 return m

def main():
 p=argparse.ArgumentParser();p.add_argument('--dimension',type=int,required=True);a=p.parse_args();d=a.dimension
 rows=[]
 for family in ('sphere','rastrigin','rosenbrock'):
  for regime in ('low4','full'):
   r=4 if regime=='low4' else d
   for seed in range(3300,3305):
    f,x0=instance(family,d,r,seed)
    for method in ('COBYQA','DE','Embed8','Restart8'):
     m=run(f,x0,seed,method)
     rows.append(dict(family=family,dimension=d,regime=regime,rank=r,seed=seed,method=method,evaluations=m.n,best=m.best,budget=B))
 path=P/f'raw_d{d}.csv'
 with path.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(d,len(rows),hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
if __name__=='__main__':main()
