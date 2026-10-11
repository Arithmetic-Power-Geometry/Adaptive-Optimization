"""Phase 39: 80-call held-out comparison of full COBYQA, Embed8, Embed16, and two-stage Restart8."""
import csv,json,platform
from pathlib import Path
import numpy as np,scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent;B=80
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
 def obj(x):
  z=Q.T@x-shift
  if family=='sphere':return float(z@z)
  return float(10*r+np.sum(z*z-10*np.cos(2*np.pi*z)))
 return obj,x0
def solve(f,x0,seed,method):
 m=Meter(f);d=len(x0);rng=np.random.default_rng(seed+61000)
 if method=='COBYQA':
  try:minimize(m,x0,method='COBYQA',options={'maxfev':B,'maxiter':B})
  except Limit:pass
  return m
 stages=[(8,80)] if method=='Embed8' else ([(16,80)] if method=='Embed16' else [(8,40),(8,40)])
 for k,cap in stages:
  if m.n>=B:break
  A,_=np.linalg.qr(rng.normal(size=(d,k)))
  anchor=x0 if m.x is None else m.x.copy();used=0
  def fun(z):
   nonlocal used
   if used>=cap:raise Limit()
   used+=1;return m(anchor+A@z)
  try:minimize(fun,np.zeros(k),method='COBYQA',options={'maxfev':cap,'maxiter':cap})
  except Limit:pass
 return m
def main():
 rows=[]
 for family in ('sphere','rastrigin'):
  for d in (20,60):
   for r in (4,12,20):
    for seed in range(2900,2908):
     f,x=instance(family,d,r,seed)
     for method in ('COBYQA','Embed8','Embed16','Restart8'):
      m=solve(f,x,seed,method)
      rows.append(dict(family=family,ambient_d=d,intrinsic_r=r,seed=seed,method=method,evaluations=m.n,best=m.best,budget=B))
 with (P/'raw_results.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 key=lambda z:(z['family'],z['ambient_d'],z['intrinsic_r'],z['seed'])
 summ=[]
 for r in (4,12,20):
  ref={key(z):z['best'] for z in rows if z['intrinsic_r']==r and z['method']=='COBYQA'}
  e8={key(z):z['best'] for z in rows if z['intrinsic_r']==r and z['method']=='Embed8'}
  for method in ('COBYQA','Embed8','Embed16','Restart8'):
   v=[z for z in rows if z['intrinsic_r']==r and z['method']==method]
   a=[z['best']-ref[key(z)] for z in v];b=[z['best']-e8[key(z)] for z in v]
   summ.append(dict(r=r,method=method,n=len(v),wins_cobyqa=sum(t< -1e-8 for t in a),losses_cobyqa=sum(t>1e-8 for t in a),ties_cobyqa=sum(abs(t)<=1e-8 for t in a),wins_embed8=sum(t< -1e-8 for t in b),losses_embed8=sum(t>1e-8 for t in b),ties_embed8=sum(abs(t)<=1e-8 for t in b),mean_calls=float(np.mean([z['evaluations'] for z in v]))))
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summ[0]));w.writeheader();w.writerows(summ)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seeds=list(range(2900,2908)),families=['sphere','rastrigin'],ambient_d=[20,60],intrinsic_r=[4,12,20]),indent=2)+'\n')
 print('RUNS',len(rows))
 for z in summ:print(z)
if __name__=='__main__':main()
