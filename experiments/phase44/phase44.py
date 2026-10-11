"""Phase 44: matched restart mechanism ablation, common bounded domain."""
import csv,hashlib,json,platform
from pathlib import Path
import numpy as np,scipy
from scipy.optimize import minimize,LinearConstraint
P=Path(__file__).resolve().parent
METHODS=('COBYQA','Embed8','NewBest','SameBest','NewOrigin')
class Stop(Exception):pass
class Meter:
 def __init__(self,f,B):self.f=f;self.B=B;self.n=0;self.best=float('inf');self.x=None
 def __call__(self,x):
  if self.n>=self.B:raise Stop()
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
def run(f,x0,seed,method,B):
 m=Meter(f,B);d=len(x0);rng=np.random.default_rng(seed+121000)
 lb=np.full(d,-5.0);ub=np.full(d,5.0)
 if method=='COBYQA':
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
 rows=[]
 for family in ('sphere','rastrigin'):
  for d in (8,20):
   for regime in ('low4','full'):
    r=4 if regime=='low4' else d
    for seed in (3500,3501):
     f,x=instance(family,d,r,seed);B=12*d
     for method in METHODS:
      m=run(f,x,seed,method,B)
      rows.append(dict(family=family,dimension=d,regime=regime,rank=r,seed=seed,method=method,calls=m.n,best=m.best,budget=B))
 with (P/'raw_results.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 by={(z['family'],z['dimension'],z['regime'],z['seed'],z['method']):z for z in rows}
 out=[]
 for regime in ('low4','full'):
  for method in METHODS:
   vals=[z for z in rows if z['regime']==regime and z['method']==method]
   row={'regime':regime,'method':method,'n':len(vals),'mean_calls':float(np.mean([z['calls'] for z in vals]))}
   for base in ('COBYQA','Embed8','NewBest','SameBest','NewOrigin'):
    diffs=[z['best']-by[(z['family'],z['dimension'],z['regime'],z['seed'],base)]['best'] for z in vals]
    row.update({f'win_{base}':sum(v<-1e-8 for v in diffs),f'loss_{base}':sum(v>1e-8 for v in diffs),f'tie_{base}':sum(abs(v)<=1e-8 for v in diffs)})
   out.append(row)
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,methods=METHODS,seeds=[3500,3501],budget='12*d',families=['sphere','rastrigin'],dimensions=[8,20]),indent=2)+'\n')
 for z in out:print(z,flush=True)
 for f in ('phase44.py','raw_results.csv','summary.csv','environment.json'):
  print('SHA256',f,hashlib.sha256((P/f).read_bytes()).hexdigest())
if __name__=='__main__':main()
