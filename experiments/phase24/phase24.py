"""Phase 24: independent held-out angle replication; same coordinate-plane schedule per instance."""
import csv, json, hashlib, platform
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent; B=160
class Limit(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=np.inf
 def __call__(self,x):
  if self.n>=B:raise Limit()
  self.n+=1; y=float(self.f(np.asarray(x)));self.best=min(self.best,y);return y

def problem(name,d,seed):
 rng=np.random.default_rng(seed*17+d*100);Q,_=np.linalg.qr(rng.normal(size=(d,d)));shift=rng.uniform(-2,2,d)
 def f(x):
  z=Q@(x-shift)
  if name=='ackley':return -20*np.exp(-.2*np.sqrt(np.mean(z*z)))-np.exp(np.mean(np.cos(2*np.pi*z)))+20+np.e
  if name=='rastrigin':return 10*d+np.sum(z*z-10*np.cos(2*np.pi*z))
  if name=='griewank':return 1+np.sum(z*z)/4000-np.prod(np.cos(z/np.sqrt(np.arange(1,d+1))))
  return np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2)
 return f,rng.uniform(-3,3,d)

def solve(f,x0,seed,method):
 m=Meter(f)
 if method=='COBYQA':
  try:minimize(m,x0,method='COBYQA',options={'maxfev':B,'maxiter':B})
  except Limit:pass
  return m
 d=len(x0); rng=np.random.default_rng(seed+50000); planes=[tuple(rng.choice(d,2,replace=False)) for _ in range(B)]
 # Separate RNG stream for random angles; planes identical in all angle variants.
 angles=np.random.default_rng(seed+72000).uniform(0,2*np.pi,B)
 x=x0.copy();fx=m(x);h=.7;theta=0.;i=0
 while m.n<B and h>1e-7:
  a,b=planes[i];i+=1
  if method=='Golden':theta=(theta+2*np.pi*((np.sqrt(5)-1)/2))%(2*np.pi)
  elif method=='Rational':theta=(theta+2*np.pi*(3/8))%(2*np.pi)
  elif method=='RandomAngle':theta=angles[i-1]
  v=np.zeros(d);v[a]=np.cos(theta);v[b]=np.sin(theta)
  improved=False
  for direction in (v,-v):
   if m.n>=B:break
   y=x+h*direction;fy=m(y)
   if fy<fx:x=y;fx=fy;improved=True;break
  h=min(h*1.08,1.5) if improved else h*.7
 return m

rows=[]
for family in ('ackley','rastrigin','griewank','rosenbrock'):
 for d in (2,5,10):
  for seed in range(1400,1420):
   f,x0=problem(family,d,seed)
   for method in ('Golden','Rational','RandomAngle','COBYQA'):
    m=solve(f,x0,seed,method)
    rows.append(dict(function=family,dimension=d,seed=seed,method=method,evaluations=m.n,best=m.best))
with (P/'raw_results.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=[]
for family in ('ackley','rastrigin','griewank','rosenbrock'):
 for d in (2,5,10):
  sub=[r for r in rows if r['function']==family and r['dimension']==d]
  controls={method:{r['seed']:r['best'] for r in sub if r['method']==method} for method in ('Golden','Rational','RandomAngle','COBYQA')}
  for method in ('Golden','Rational','RandomAngle','COBYQA'):
   v=[r for r in sub if r['method']==method]
   summary.append(dict(function=family,dimension=d,method=method,median_best=float(np.median([r['best'] for r in v])),mean_evals=float(np.mean([r['evaluations'] for r in v])),wins_vs_COBYQA=sum(r['best']<controls['COBYQA'][r['seed']]-1e-10 for r in v),wins_vs_Rational=sum(r['best']<controls['Rational'][r['seed']]-1e-10 for r in v),wins_vs_RandomAngle=sum(r['best']<controls['RandomAngle'][r['seed']]-1e-10 for r in v),runs=len(v)))
with (P/'summary.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
(P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seeds=[1400,1419],design='4 families x 3 dims x 20 seeds x 4 methods',plane_seed_rule='seed+50000',angle_seed_rule='seed+72000'),indent=2)+'\n')
print('RUNS',len(rows))
for method in ('Golden','Rational','RandomAngle','COBYQA'):
 v=[r for r in summary if r['method']==method]
 print(method,'wins_COBYQA',sum(r['wins_vs_COBYQA'] for r in v),'wins_Rational',sum(r['wins_vs_Rational'] for r in v),'wins_RandomAngle',sum(r['wins_vs_RandomAngle'] for r in v),'mean_evals',round(np.mean([r['mean_evals'] for r in v]),2))
for family in ('ackley','rastrigin','griewank','rosenbrock'):
 for method in ('Golden','Rational','RandomAngle'):
  v=[r for r in summary if r['function']==family and r['method']==method]
  print(family,method,'wins_COBYQA',sum(r['wins_vs_COBYQA'] for r in v))
for fn in ('phase24.py','raw_results.csv','summary.csv','environment.json'):
 print('SHA256',fn,hashlib.sha256((P/fn).read_bytes()).hexdigest())
