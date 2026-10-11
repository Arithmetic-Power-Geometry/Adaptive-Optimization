"""Phase36: costed gradient-screened embedding against fixed random embeddings."""
import csv,json,platform,hashlib
from pathlib import Path
import numpy as np,scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent;B=120
class Budget(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=np.inf;self.x=None
 def __call__(self,x):
  if self.n>=B:raise Budget()
  x=np.asarray(x);v=float(self.f(x));self.n+=1
  if v<self.best:self.best=v;self.x=x.copy()
  return v
def instance(family,d,r,seed):
 rng=np.random.default_rng(seed*53+d*17+r*101);Q,_=np.linalg.qr(rng.normal(size=(d,r)));shift=rng.uniform(-2,2,r);x0=rng.uniform(-1.5,1.5,d)
 def obj(x):
  z=Q.T@x-shift
  if family=='sphere':return float(z@z)
  return float(10*r+np.sum(z*z-10*np.cos(2*np.pi*z)))
 return obj,x0
def solve(f,x0,seed,method):
 m=Meter(f);d=len(x0);rng=np.random.default_rng(seed+41000)
 if method=='COBYQA':
  try:minimize(m,x0,method='COBYQA',options={'maxfev':B,'maxiter':B})
  except Budget:pass
  return m
 k=8 if method in ('Embed8','Screen8') else 16
 if method=='Screen8':
  V,_=np.linalg.qr(rng.normal(size=(d,8)));h=0.05;diff=[]
  for j in range(8):
   a=m(x0+h*V[:,j]);b=m(x0-h*V[:,j]);diff.append((a-b)/(2*h))
  g=V@np.array(diff)
  if np.linalg.norm(g)>1e-12:
   u=g/np.linalg.norm(g);Z=rng.normal(size=(d,7));Z-=np.outer(u,u@Z)
   A,_=np.linalg.qr(np.column_stack([u,Z]))
  else:A,_=np.linalg.qr(rng.normal(size=(d,8)))
 else:A,_=np.linalg.qr(rng.normal(size=(d,k)))
 anchor=x0 if m.x is None else m.x.copy()
 def reduced(z):return m(anchor+A@z)
 try:minimize(reduced,np.zeros(k),method='COBYQA',options={'maxfev':B-m.n,'maxiter':B-m.n})
 except Budget:pass
 return m
def main():
 rows=[]
 for family in ('sphere','rastrigin'):
  for d in (20,60):
   for r in (4,12,20):
    for seed in range(2600,2603):
     f,x0=instance(family,d,r,seed)
     for method in ('COBYQA','Embed8','Embed16','Screen8'):
      m=solve(f,x0,seed,method)
      rows.append(dict(family=family,dimension=d,effective_dimension=r,seed=seed,method=method,evaluations=m.n,best=m.best,budget=B))
 with (P/'raw_results.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 ref={(z['family'],z['dimension'],z['effective_dimension'],z['seed']):z['best'] for z in rows if z['method']=='COBYQA'}
 emb={(z['family'],z['dimension'],z['effective_dimension'],z['seed']):z['best'] for z in rows if z['method']=='Embed8'}
 summary=[]
 for r in (4,12,20):
  for method in ('COBYQA','Embed8','Embed16','Screen8'):
   v=[z for z in rows if z['effective_dimension']==r and z['method']==method]
   dif=[z['best']-ref[(z['family'],z['dimension'],z['effective_dimension'],z['seed'])] for z in v]
   d8=[z['best']-emb[(z['family'],z['dimension'],z['effective_dimension'],z['seed'])] for z in v]
   summary.append(dict(r=r,method=method,n=len(v),wins_cobyqa=sum(t< -1e-8 for t in dif),losses_cobyqa=sum(t>1e-8 for t in dif),ties_cobyqa=sum(abs(t)<=1e-8 for t in dif),wins_embed8=sum(t< -1e-8 for t in d8),losses_embed8=sum(t>1e-8 for t in d8),ties_embed8=sum(abs(t)<=1e-8 for t in d8),mean_calls=float(np.mean([z['evaluations'] for z in v]))))
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seeds=[2600,2601,2602],families=['sphere','rastrigin'],ambient_dimensions=[20,60],effective_dimensions=[4,12,20],gradient_probes=16),indent=2)+'\n')
 print('RUNS',len(rows),flush=True)
 for z in summary:print(z,flush=True)
 for name in ('phase36.py','raw_results.csv','summary.csv','environment.json'):
  print('SHA256',name,hashlib.sha256((P/name).read_bytes()).hexdigest(),flush=True)
if __name__=='__main__':main()
