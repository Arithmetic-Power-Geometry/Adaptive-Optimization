"""Phase 43: bounded-domain, charged-budget independent benchmark and restart ablation."""
import csv, json, hashlib, platform, argparse
from pathlib import Path
import numpy as np, scipy
from scipy.optimize import minimize, differential_evolution, LinearConstraint
P=Path(__file__).resolve().parent
METHODS=('COBYQA','DE','Embed8','Restart8')
class Budget(Exception):pass
class Meter:
 def __init__(self,f,budget):self.f=f;self.budget=budget;self.n=0;self.best=float('inf');self.x=None
 def __call__(self,x):
  if self.n>=self.budget:raise Budget()
  x=np.asarray(x,dtype=float);v=float(self.f(x));self.n+=1
  if v<self.best:self.best=v;self.x=x.copy()
  return v

def instance(family,d,r,seed):
 rng=np.random.default_rng(seed*53+d*17+r*101)
 Q,_=np.linalg.qr(rng.normal(size=(d,r)))
 shift=rng.uniform(-2,2,r);x0=rng.uniform(-1.5,1.5,d)
 def f(x):
  z=Q.T@x-shift
  if family=='sphere':return float(z@z)
  if family=='rastrigin':return float(10*r+np.sum(z*z-10*np.cos(2*np.pi*z)))
  return float(np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2))
 return f,x0

def run(f,x0,seed,method,budget):
 m=Meter(f,budget);d=len(x0);rng=np.random.default_rng(seed+101000)
 lb=np.full(d,-5.0);ub=np.full(d,5.0)
 if method=='COBYQA':
  try:minimize(m,x0,method='COBYQA',bounds=list(zip(lb,ub)),options={'maxfev':budget,'maxiter':budget})
  except Budget:pass
 elif method=='DE':
  try:differential_evolution(m,list(zip(lb,ub)),popsize=5,maxiter=1000,polish=False,seed=seed,init='latinhypercube',x0=x0,tol=0,atol=0)
  except Budget:pass
 else:
  caps=[budget] if method=='Embed8' else [budget//2,budget-budget//2]
  for cap in caps:
   if m.n>=budget:break
   A,_=np.linalg.qr(rng.normal(size=(d,min(8,d))))
   anchor=x0 if m.x is None else m.x.copy();used=0
   def reduced(z):
    nonlocal used
    if used>=cap:raise Budget()
    used+=1;return m(anchor+A@z)
   try:minimize(reduced,np.zeros(A.shape[1]),method='COBYQA',constraints=[LinearConstraint(A,lb-anchor,ub-anchor)],options={'maxfev':cap,'maxiter':cap})
   except Budget:pass
 return m

def main():
 p=argparse.ArgumentParser();p.add_argument('--dimension',type=int,required=True);a=p.parse_args();d=a.dimension
 budget=12*d
 rows=[]
 for family in ('sphere','rastrigin','rosenbrock'):
  for regime in ('low4','full'):
   r=4 if regime=='low4' else d
   for seed in (3400,3401,3402):
    f,x=instance(family,d,r,seed)
    for method in METHODS:
     m=run(f,x,seed,method,budget)
     rows.append(dict(family=family,dimension=d,regime=regime,rank=r,seed=seed,method=method,evaluations=m.n,best=m.best,budget=budget))
 dest=P/f'raw_d{d}.csv'
 with dest.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(d,len(rows),hashlib.sha256(dest.read_bytes()).hexdigest(),flush=True)
if __name__=='__main__':main()
