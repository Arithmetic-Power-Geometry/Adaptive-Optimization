"""Phase47: predeclared diagnostic-gated full-vs-embedding optimizer; held-out seeds.
Uses one common bounded objective, charges all probes, and records anytime traces.
"""
import csv,hashlib,json,platform
from pathlib import Path
import numpy as np,scipy
from scipy.optimize import minimize,LinearConstraint
P=Path(__file__).resolve().parent
D=20; B=160; K=8; METHODS=('Full','Embed8','Restart8','Gate8Full')
class Stop(Exception): pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=np.inf;self.x=None;self.trace=[]
 def __call__(self,x):
  if self.n>=B:raise Stop()
  x=np.asarray(x);v=float(self.f(x));self.n+=1
  if v<self.best:self.best=v;self.x=x.copy()
  self.trace.append(self.best);return v

def instance(family,r,seed):
 rng=np.random.default_rng(seed*53+D*17+r*101)
 Q,_=np.linalg.qr(rng.normal(size=(D,r)));shift=rng.uniform(-2,2,r);x0=rng.uniform(-1.5,1.5,D)
 def f(x):
  z=Q.T@x-shift
  return float(z@z) if family=='sphere' else float(10*r+np.sum(z*z-10*np.cos(2*np.pi*z)))
 return f,x0

def run(f,x0,seed,method):
 m=Meter(f);rng=np.random.default_rng(seed+151000)
 lb=np.full(D,-5.);ub=np.full(D,5.)
 def full(cap):
  used=0;anchor=x0.copy() if m.x is None else m.x.copy()
  def fun(x):
   nonlocal used
   if used>=cap:raise Stop()
   used+=1;return m(x)
  try:minimize(fun,anchor,method='COBYQA',bounds=list(zip(lb,ub)),options={'maxfev':cap,'maxiter':cap})
  except Stop:pass
 def embed(cap):
  A,_=np.linalg.qr(rng.normal(size=(D,K)));anchor=x0.copy() if m.x is None else m.x.copy();used=0
  def fun(z):
   nonlocal used
   if used>=cap:raise Stop()
   used+=1;return m(anchor+A@z)
  try:minimize(fun,np.zeros(K),method='COBYQA',constraints=[LinearConstraint(A,lb-anchor,ub-anchor)],options={'maxfev':cap,'maxiter':cap})
  except Stop:pass
 if method=='Full':full(B)
 elif method=='Embed8':embed(B)
 elif method=='Restart8':embed(B//2);embed(B//2)
 else:
  # Diagnostic: initial embedding for 60 calls, compare normalized gain in latter 30 vs first 30.
  # If progress stalled, switch to full COBYQA; otherwise restart in a new embedding.
  embed(60)
  t=m.trace
  gain1=max(0,t[0]-t[min(29,len(t)-1)]) if t else 0
  gain2=max(0,t[min(29,len(t)-1)]-t[-1]) if t else 0
  if gain2 < 0.1*gain1:full(B-m.n)
  else:embed(B-m.n)
 return m

def main():
 rows=[];traces=[]
 for family in ('sphere','rastrigin'):
  for regime,r in (('low4',4),('full',20)):
   for seed in range(3900,3903):
    f,x0=instance(family,r,seed)
    for method in METHODS:
     m=run(f,x0,seed,method)
     rows.append(dict(family=family,regime=regime,dimension=D,rank=r,seed=seed,method=method,calls=m.n,best=m.best,budget=B))
     for i,v in enumerate(m.trace,1):traces.append(dict(family=family,regime=regime,seed=seed,method=method,call=i,best=v))
 for name,data in [('raw_results.csv',rows),('traces.csv',traces)]:
  with (P/name).open('w',newline='') as h:
   w=csv.DictWriter(h,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 by={(z['family'],z['regime'],z['seed'],z['method']):z for z in rows};summary=[]
 for regime in ('low4','full'):
  for method in METHODS:
   rr=[z for z in rows if z['regime']==regime and z['method']==method]
   o=dict(regime=regime,method=method,n=len(rr),mean_calls=round(np.mean([z['calls'] for z in rr]),2))
   for base in METHODS:
    delta=[z['best']-by[(z['family'],regime,z['seed'],base)]['best'] for z in rr]
    o['W_'+base]=sum(v<-1e-8 for v in delta);o['L_'+base]=sum(v>1e-8 for v in delta);o['T_'+base]=sum(abs(v)<=1e-8 for v in delta)
   summary.append(o)
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,seeds=[3900,3901,3902],budget=B,dimension=D,methods=METHODS),indent=2)+'\n')
 for row in summary:print(row,flush=True)
 for name in ['phase47.py','raw_results.csv','summary.csv','traces.csv','environment.json']:
  print('HASH',name,hashlib.sha256((P/name).read_bytes()).hexdigest())
if __name__=='__main__':main()
