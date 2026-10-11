"""Phase 41: independent mixed-rank dimensional stress test and charged portfolio ablation."""
import argparse,csv,json,platform,hashlib
from pathlib import Path
import numpy as np, scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent
B=80
METHODS=('COBYQA','Powell','Embed8','Restart8','Portfolio40')
class Limit(Exception): pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=float('inf');self.x=None
 def __call__(self,x):
  if self.n>=B:raise Limit()
  x=np.asarray(x);v=float(self.f(x));self.n+=1
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

def run(f,x0,seed,method):
 m=Meter(f);d=len(x0);rng=np.random.default_rng(seed+81000)
 def optimize_full(cap):
  used=0
  def wrapped(x):
   nonlocal used
   if used>=cap:raise Limit()
   used+=1;return m(x)
  try:minimize(wrapped,x0 if m.x is None else m.x.copy(),method='COBYQA',options={'maxfev':cap,'maxiter':cap})
  except Limit:pass
 def embed(k,cap):
  A,_=np.linalg.qr(rng.normal(size=(d,min(k,d))))
  anchor=x0 if m.x is None else m.x.copy();used=0
  def wrapped(z):
   nonlocal used
   if used>=cap:raise Limit()
   used+=1;return m(anchor+A@z)
  try:minimize(wrapped,np.zeros(A.shape[1]),method='COBYQA',options={'maxfev':cap,'maxiter':cap})
  except Limit:pass
 if method=='COBYQA':optimize_full(B)
 elif method=='Powell':
  try:minimize(m,x0,method='Powell',options={'maxfev':B,'maxiter':B})
  except Limit:pass
 elif method=='Embed8':embed(8,B)
 elif method=='Restart8':embed(8,40);embed(8,40)
 elif method=='Portfolio40':optimize_full(40);embed(8,40)
 return m

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--dimension',type=int,required=True);args=parser.parse_args();d=args.dimension
 rows=[]
 for family in ('sphere','rastrigin','rosenbrock'):
  for regime in ('low4','full'):
   r=4 if regime=='low4' else d
   for seed in (3200,3201,3202):
    f,x=instance(family,d,r,seed)
    for method in METHODS:
     m=run(f,x,seed,method)
     rows.append(dict(family=family,dimension=d,regime=regime,effective_dimension=r,seed=seed,method=method,evaluations=m.n,best=m.best,budget=B))
 dest=P/f'raw_d{d}.csv'
 with dest.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(d,len(rows),hashlib.sha256(dest.read_bytes()).hexdigest(),flush=True)
if __name__=='__main__':main()
