"""Phase 45: held-out bounded matched restart ablation with actual evaluation traces."""
import argparse,csv,hashlib,json,platform
from pathlib import Path
import numpy as np,scipy
from scipy.optimize import minimize,LinearConstraint
P=Path(__file__).resolve().parent
METHODS=('Full','Embed8','NewBest','SameBest','NewOrigin')
class Stop(Exception):pass
class Meter:
 def __init__(self,f,B):self.f=f;self.B=B;self.n=0;self.best=float('inf');self.x=None;self.trace=[]
 def __call__(self,x):
  if self.n>=self.B:raise Stop()
  x=np.asarray(x);v=float(self.f(x));self.n+=1
  if v<self.best:self.best=v;self.x=x.copy()
  self.trace.append(self.best)
  return v

def instance(family,d,r,seed):
 rng=np.random.default_rng(seed*53+d*17+r*101)
 Q,_=np.linalg.qr(rng.normal(size=(d,r)));shift=rng.uniform(-2,2,r);x0=rng.uniform(-1.5,1.5,d)
 def f(x):
  z=Q.T@x-shift
  if family=='sphere':return float(z@z)
  if family=='rastrigin':return float(10*r+np.sum(z*z-10*np.cos(2*np.pi*z)))
  if family=='rosenbrock':return float(np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2))
  raise ValueError(family)
 return f,x0

def run(f,x0,seed,method,B):
 m=Meter(f,B);d=len(x0);rng=np.random.default_rng(seed+131000)
 lb=np.full(d,-5.0);ub=np.full(d,5.0)
 if method=='Full':
  try:minimize(m,x0,method='COBYQA',bounds=list(zip(lb,ub)),options={'maxfev':B,'maxiter':B})
  except Stop:pass
  return m
 A0,_=np.linalg.qr(rng.normal(size=(d,min(8,d))))
 stages=[B] if method=='Embed8' else [B//2,B-B//2]
 for i,cap in enumerate(stages):
  if i==0 or method=='SameBest':A=A0
  else:A,_=np.linalg.qr(rng.normal(size=(d,min(8,d))))
  anchor=x0 if i==0 or method=='NewOrigin' else m.x.copy()
  used=0
  def reduced(z):
   nonlocal used
   if used>=cap:raise Stop()
   used+=1;return m(anchor+A@z)
  try:minimize(reduced,np.zeros(A.shape[1]),method='COBYQA',constraints=[LinearConstraint(A,lb-anchor,ub-anchor)],options={'maxfev':cap,'maxiter':cap})
  except Stop:pass
 return m

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--dimension',type=int,required=True);args=parser.parse_args();d=args.dimension
 rows=[];traces=[]
 for family in ('sphere','rastrigin'):
  for regime in ('low4','full'):
   r=4 if regime=='low4' else d
   for seed in range(3600,3602):
    f,x=instance(family,d,r,seed);B=12*d
    for method in METHODS:
     m=run(f,x,seed,method,B)
     rows.append(dict(family=family,dimension=d,regime=regime,rank=r,seed=seed,method=method,calls=m.n,best=m.best,budget=B))
     for t,best in enumerate(m.trace,1):traces.append(dict(family=family,dimension=d,regime=regime,seed=seed,method=method,call=t,best=best))
 for name,data in ((f'raw_d{d}.csv',rows),(f'traces_d{d}.csv',traces)):
  with (P/name).open('w',newline='') as h:
   w=csv.DictWriter(h,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
  print(name,len(data),hashlib.sha256((P/name).read_bytes()).hexdigest(),flush=True)
if __name__=='__main__':main()
