import csv,json,hashlib,platform
from pathlib import Path
import numpy as np, scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent
B=120
class Stop(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=float('inf');self.x=None
 def __call__(self,x):
  if self.n>=B:raise Stop()
  v=float(self.f(np.asarray(x)));self.n+=1
  if v<self.best:self.best=v;self.x=np.asarray(x).copy()
  return v
def instance(family,d,r,seed):
 rng=np.random.default_rng(seed*53+d*17+r*101);Q,_=np.linalg.qr(rng.normal(size=(d,r)));shift=rng.uniform(-2,2,r);x0=rng.uniform(-1.5,1.5,d)
 def obj(x):
  z=Q.T@x-shift
  if family=='sphere':return float(z@z)
  if family=='rastrigin':return float(10*r+np.sum(z*z-10*np.cos(2*np.pi*z)))
  if family=='rosenbrock':return float(np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2))
  return float(-20*np.exp(-.2*np.sqrt(np.mean(z*z)))-np.exp(np.mean(np.cos(2*np.pi*z)))+20+np.e)
 return obj,x0
def coby(m,x,cap,transform=None):
 used=0
 def fun(y):
  nonlocal used
  if used>=cap:raise Stop()
  used+=1;return m(y if transform is None else transform(y))
 try:minimize(fun,x,method='COBYQA',options={'maxfev':cap,'maxiter':cap})
 except Stop:pass
def run(f,x0,seed,method):
 m=Meter(f);d=len(x0)
 if method=='COBYQA':coby(m,x0,B);return m
 rng=np.random.default_rng(seed+41000)
 def embed(k,cap):
  anchor=x0.copy() if m.x is None else m.x.copy()
  A,_=np.linalg.qr(rng.normal(size=(d,k)))
  coby(m,np.zeros(k),cap,lambda z:anchor+A@z)
 if method=='Embed4':embed(4,B)
 elif method=='Embed8':embed(8,B)
 elif method=='Split4to8':embed(4,60);embed(8,B-m.n)
 elif method=='Split8to4':embed(8,60);embed(4,B-m.n)
 return m
def main():
 rows=[]
 for family in ('sphere','rastrigin'):
  for d in (20,60):
   for r in (4,12,20):
    for seed in range(2500,2503):
     f,x=instance(family,d,r,seed)
     for method in ('COBYQA','Embed4','Embed8','Split4to8','Split8to4'):
      m=run(f,x,seed,method)
      rows.append(dict(family=family,dimension=d,effective_dimension=r,seed=seed,method=method,evaluations=m.n,best=m.best,budget=B))
 with (P/'raw_results.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 ref={(x['family'],x['dimension'],x['effective_dimension'],x['seed']):x['best'] for x in rows if x['method']=='COBYQA'}
 summary=[]
 for d in (20,60):
  for r in (4,12,20):
   for method in ('COBYQA','Embed4','Embed8','Split4to8','Split8to4'):
    v=[x for x in rows if x['dimension']==d and x['effective_dimension']==r and x['method']==method]
    diffs=[x['best']-ref[(x['family'],x['dimension'],x['effective_dimension'],x['seed'])] for x in v]
    summary.append(dict(dimension=d,effective_dimension=r,method=method,runs=len(v),wins=sum(z< -1e-8 for z in diffs),losses=sum(z>1e-8 for z in diffs),ties=sum(abs(z)<=1e-8 for z in diffs),median_best=float(np.median([x['best'] for x in v])),mean_evaluations=float(np.mean([x['evaluations'] for x in v]))))
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seed_range=[2500,2502],dimensions=[20,60],effective_dimensions=[4,12,20],methods=['COBYQA','Embed4','Embed8','Split4to8','Split8to4']),indent=2)+'\n')
 print('RUNS',len(rows))
 for r in (4,12,20):
  for method in ('Embed4','Embed8','Split4to8','Split8to4'):
   v=[x for x in summary if x['effective_dimension']==r and x['method']==method]
   print('r',r,method,'wins',sum(x['wins'] for x in v),'losses',sum(x['losses'] for x in v),'ties',sum(x['ties'] for x in v),flush=True)
 for name in ('phase35.py','raw_results.csv','summary.csv','environment.json'):print('SHA256',name,hashlib.sha256((P/name).read_bytes()).hexdigest(),flush=True)
if __name__=='__main__':main()
