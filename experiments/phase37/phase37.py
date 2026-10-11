"""Phase37: held-out rank-selection diagnostic, with explicit charged probes."""
import csv, json, hashlib, platform
from pathlib import Path
import numpy as np, scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent; B=120
class Budget(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=float('inf');self.x=None
 def __call__(self,x):
  if self.n>=B:raise Budget()
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

def run(f,x0,seed,method):
 m=Meter(f);d=len(x0);rng=np.random.default_rng(seed+51000)
 if method=='COBYQA':
  try:minimize(m,x0,method='COBYQA',options={'maxfev':B,'maxiter':B})
  except Budget:pass
  return m,0,0
 # Explicitly cost 16 function calls to obtain 8 finite differences for selection.
 # A single local gradient cannot identify intrinsic rank; this is a deliberately falsifiable heuristic.
 selected=8;score=0.
 if method=='Select8or16':
  V,_=np.linalg.qr(rng.normal(size=(d,8)))
  h=.05;g=[]
  for j in range(8):
   a=m(x0+h*V[:,j]);b=m(x0-h*V[:,j]);g.append((a-b)/(2*h))
  # Split-half energy ratio, fixed ex ante, with no oracle r information.
  g=np.asarray(g);score=float(np.sum(g[4:]**2)/(np.sum(g**2)+1e-30))
  selected=16 if score>.45 else 8
 elif method=='Embed16':selected=16
 A,_=np.linalg.qr(rng.normal(size=(d,selected)))
 anchor=x0 if m.x is None else m.x.copy()
 def reduced(z):return m(anchor+A@z)
 try:minimize(reduced,np.zeros(selected),method='COBYQA',options={'maxfev':B-m.n,'maxiter':B-m.n})
 except Budget:pass
 return m,selected,score

def main():
 rows=[]
 for family in ('sphere','rastrigin'):
  for d in (20,60):
   for r in (4,12,20):
    for seed in range(2700,2704):
     f,x=instance(family,d,r,seed)
     for method in ('COBYQA','Embed8','Embed16','Select8or16'):
      m,k,score=run(f,x,seed,method)
      rows.append(dict(family=family,ambient_d=d,intrinsic_r=r,seed=seed,method=method,evals=m.n,best=m.best,selected_k=k,diagnostic_score=score,budget=B))
 with (P/'raw_results.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 key=lambda z:(z['family'],z['ambient_d'],z['intrinsic_r'],z['seed'])
 summary=[]
 for r in (4,12,20):
  ref={key(z):z['best'] for z in rows if z['intrinsic_r']==r and z['method']=='COBYQA'}
  e8={key(z):z['best'] for z in rows if z['intrinsic_r']==r and z['method']=='Embed8'}
  for method in ('COBYQA','Embed8','Embed16','Select8or16'):
   v=[z for z in rows if z['intrinsic_r']==r and z['method']==method]
   dc=[z['best']-ref[key(z)] for z in v];de=[z['best']-e8[key(z)] for z in v]
   summary.append(dict(intrinsic_r=r,method=method,n=len(v),wins_cobyqa=sum(t< -1e-8 for t in dc),losses_cobyqa=sum(t>1e-8 for t in dc),ties_cobyqa=sum(abs(t)<=1e-8 for t in dc),wins_embed8=sum(t< -1e-8 for t in de),losses_embed8=sum(t>1e-8 for t in de),ties_embed8=sum(abs(t)<=1e-8 for t in de),mean_evals=float(np.mean([z['evals'] for z in v])),selected_16=sum(z['selected_k']==16 for z in v)))
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seed_range=[2700,2703],family=['sphere','rastrigin'],ambient_dimensions=[20,60],intrinsic_dimensions=[4,12,20],selection_threshold=.45,charged_diagnostic_calls=16),indent=2)+'\n')
 for z in summary:print(z,flush=True)
 for name in ('phase37.py','raw_results.csv','summary.csv','environment.json'):print('SHA256',name,hashlib.sha256((P/name).read_bytes()).hexdigest(),flush=True)
if __name__=='__main__':main()
