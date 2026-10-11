"""Phase 40: general-dimension negative controls, reproducible and budgeted."""
import csv, json, hashlib, platform, time
from pathlib import Path
import numpy as np, scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent
B=80
class Limit(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=float('inf');self.x=None
 def __call__(self,x):
  if self.n>=B:raise Limit()
  x=np.asarray(x);v=float(self.f(x));self.n+=1
  if v<self.best:self.best=v;self.x=x.copy()
  return v

def instance(family,d,r,seed):
 rng=np.random.default_rng(seed*53+d*17+r*101)
 Q,_=np.linalg.qr(rng.normal(size=(d,r)));shift=rng.uniform(-2,2,r);x0=rng.uniform(-1.5,1.5,d)
 def f(x):
  z=Q.T@x-shift
  if family=='sphere':return float(z@z)
  if family=='rastrigin':return float(10*r+np.sum(z*z-10*np.cos(2*np.pi*z)))
  return float(np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2))
 return f,x0

def solve(f,x0,seed,method):
 m=Meter(f);d=len(x0);rng=np.random.default_rng(seed+71000)
 if method=='COBYQA':
  try:minimize(m,x0,method='COBYQA',options={'maxfev':B,'maxiter':B})
  except Limit:pass
 elif method=='Powell':
  try:minimize(m,x0,method='Powell',options={'maxfev':B,'maxiter':B})
  except Limit:pass
 else:
  stages=[(8,80)] if method=='Embed8' else [(8,40),(8,40)]
  for k,cap in stages:
   if m.n>=B:break
   A,_=np.linalg.qr(rng.normal(size=(d,k)))
   anchor=x0 if m.x is None else m.x.copy();used=0
   def reduced(z):
    nonlocal used
    if used>=cap:raise Limit()
    used+=1;return m(anchor+A@z)
   try:minimize(reduced,np.zeros(k),method='COBYQA',options={'maxfev':cap,'maxiter':cap})
   except Limit:pass
 return m

def main():
 rows=[];start=time.time()
 for family in ('sphere','rastrigin','rosenbrock'):
  for d in (8,20,40):
   for regime in ('low4','full'):
    r=4 if regime=='low4' else d
    for seed in (3100,3101,3102):
     f,x=instance(family,d,r,seed)
     for method in ('COBYQA','Powell','Embed8','Restart8'):
      m=solve(f,x,seed,method)
      rows.append(dict(family=family,dimension=d,regime=regime,effective_dimension=r,seed=seed,method=method,evaluations=m.n,best=m.best,budget=B))
 with (P/'raw_results.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 key=lambda z:(z['family'],z['dimension'],z['regime'],z['seed'])
 summ=[]
 for regime in ('low4','full'):
  for d in (8,20,40):
   v=[z for z in rows if z['regime']==regime and z['dimension']==d]
   baselines={method:{key(z):z['best'] for z in v if z['method']==method} for method in ('COBYQA','Powell','Embed8')}
   for method in ('COBYQA','Powell','Embed8','Restart8'):
    a=[z for z in v if z['method']==method];out=dict(regime=regime,dimension=d,method=method,n=len(a),median_best=float(np.median([z['best'] for z in a])),mean_calls=float(np.mean([z['evaluations'] for z in a])))
    for base in ('COBYQA','Powell','Embed8'):
     diff=[z['best']-baselines[base][key(z)] for z in a]
     out['wins_'+base]=sum(t< -1e-8 for t in diff);out['losses_'+base]=sum(t>1e-8 for t in diff);out['ties_'+base]=sum(abs(t)<=1e-8 for t in diff)
    summ.append(out)
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summ[0]));w.writeheader();w.writerows(summ)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seeds=[3100,3101,3102],families=['sphere','rastrigin','rosenbrock'],dimensions=[8,20,40],regimes=['low4','full'],methods=['COBYQA','Powell','Embed8','Restart8'],elapsed_seconds=round(time.time()-start,3)),indent=2)+'\n')
 for z in summ:print(z,flush=True)
 for fn in ('phase40.py','raw_results.csv','summary.csv','environment.json'):print('SHA256',fn,hashlib.sha256((P/fn).read_bytes()).hexdigest())
if __name__=='__main__':main()
