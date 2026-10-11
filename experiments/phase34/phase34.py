"""Phase34: dimension-stress experiment, with intrinsic-dimension negative control."""
import csv,json,hashlib,platform
from pathlib import Path
import numpy as np,scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent
B=100
class Limit(Exception): pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=float('inf');self.best_x=None
 def __call__(self,x):
  if self.n>=B:raise Limit()
  y=float(self.f(np.asarray(x)));self.n+=1
  if y<self.best:self.best=y;self.best_x=np.array(x,copy=True)
  return y

def instance(family,d,seed):
 rng=np.random.default_rng(seed*53+d*17)
 Q,_=np.linalg.qr(rng.normal(size=(d,4)))
 shift=rng.uniform(-2,2,4)
 # high-dimensional objectives depend on an unknown rank-4 linear projection
 def obj(x):
  z=Q.T@x-shift
  if family=='ridge_sphere':return float(np.dot(z,z))
  if family=='ridge_rastrigin':return float(40+np.sum(z*z-10*np.cos(2*np.pi*z)))
  if family=='ridge_rosenbrock':return float(np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2))
  return float(-20*np.exp(-.2*np.sqrt(np.mean(z*z)))-np.exp(np.mean(np.cos(2*np.pi*z)))+20+np.e)
 return obj,rng.uniform(-1.5,1.5,d)

def local(m,x0,method,budget):
 used=0
 def f(x):
  nonlocal used
  if used>=budget:raise Limit()
  used+=1;return m(x)
 try:minimize(f,x0,method=method,options={'maxfev':budget,'maxiter':budget} if method=='COBYQA' else {'maxfev':budget,'maxiter':budget,'disp':False})
 except Limit:pass

def run(f,x0,seed,method,k=8):
 m=Meter(f)
 if method in ('COBYQA','Powell'):
  local(m,x0,method,B);return m
 # Random embedding in k-dimensional subspace, same initial point.
 # A=Q from Gaussian d x k: uniform random subspace, not learned structure.
 rng=np.random.default_rng(seed+99991)
 A,_=np.linalg.qr(rng.normal(size=(len(x0),k)))
 def reduced(z):return m(x0+A@np.asarray(z))
 try:minimize(reduced,np.zeros(k),method='COBYQA',options={'maxfev':B,'maxiter':B})
 except Limit:pass
 return m

def main():
 rows=[]
 for family in ('ridge_sphere','ridge_rastrigin','ridge_rosenbrock','ridge_ackley'):
  for d in (20,40,60):
   for seed in range(2400,2402):
    f,x0=instance(family,d,seed)
    for method in ('COBYQA','Powell','Embed8'):
     m=run(f,x0,seed,method)
     rows.append(dict(function=family,dimension=d,seed=seed,method=method,evaluations=m.n,best=m.best,budget=B))
 with (P/'raw_results.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 ref={(r['function'],r['dimension'],r['seed']):r['best'] for r in rows if r['method']=='COBYQA'}
 summary=[]
 for method in ('COBYQA','Powell','Embed8'):
  for d in (20,40,60):
   v=[r for r in rows if r['method']==method and r['dimension']==d]
   wins=sum(r['best']<ref[(r['function'],r['dimension'],r['seed'])]-1e-8 for r in v)
   losses=sum(r['best']>ref[(r['function'],r['dimension'],r['seed'])]+1e-8 for r in v)
   summary.append(dict(method=method,dimension=d,runs=len(v),wins_vs_cobyqa=wins,losses_vs_cobyqa=losses,ties_vs_cobyqa=len(v)-wins-losses,median_best=float(np.median([r['best'] for r in v])),mean_evaluations=float(np.mean([r['evaluations'] for r in v]))))
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,intrinsic_dimension=4,embedding_dimension=8,seeds=[2400,2401],dimensions=[20,40,60]),indent=2)+'\n')
 for r in summary:print(r,flush=True)
 for name in ('phase34.py','raw_results.csv','summary.csv','environment.json'):print('SHA256',name,hashlib.sha256((P/name).read_bytes()).hexdigest(),flush=True)
if __name__=='__main__':main()
