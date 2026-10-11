"""Phase 26: derivative-information regime test. Budgeted, no gradients supplied."""
import csv, json, platform, hashlib
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent; B=240
class Exhausted(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=float('inf');self.x=None
 def __call__(self,x):
  if self.n>=B:raise Exhausted()
  y=float(self.f(np.asarray(x)));self.n+=1
  if y<self.best:self.best=y;self.x=np.asarray(x).copy()
  return y

def problem(name,d,seed):
 rng=np.random.default_rng(seed*17+d*100);Q,_=np.linalg.qr(rng.normal(size=(d,d)));shift=rng.uniform(-2,2,d)
 def f(x):
  z=Q@(x-shift)
  if name=='ackley':return -20*np.exp(-.2*np.sqrt(np.mean(z*z)))-np.exp(np.mean(np.cos(2*np.pi*z)))+20+np.e
  if name=='rastrigin':return 10*d+np.sum(z*z-10*np.cos(2*np.pi*z))
  if name=='griewank':return 1+np.sum(z*z)/4000-np.prod(np.cos(z/np.sqrt(np.arange(1,d+1))))
  return np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2)
 return f,rng.uniform(-3,3,d)

def stage(m,x,method,cap):
 used=0
 def fun(y):
  nonlocal used
  if used>=cap:raise Exhausted()
  used+=1;return m(y)
 try:
  if method=='COBYQA':minimize(fun,x,method='COBYQA',options={'maxfev':cap,'maxiter':cap})
  elif method=='BFGS':minimize(fun,x,method='BFGS',jac='2-point',options={'maxiter':cap,'gtol':1e-7})
  elif method=='L-BFGS-B':minimize(fun,x,method='L-BFGS-B',jac='2-point',options={'maxfun':cap,'maxiter':cap,'ftol':1e-12})
 except Exhausted:pass

def solve(f,x,method):
 m=Meter(f)
 if method=='WarmBFGS':
  stage(m,x,'COBYQA',min(60+8*len(x),B//2));stage(m,m.x if m.x is not None else x,'BFGS',B-m.n)
 else:stage(m,x,method,B)
 return m
rows=[]
for family in ('ackley','rastrigin','griewank','rosenbrock'):
 for d in (2,5,10):
  for seed in range(1600,1608):
   f,x=problem(family,d,seed)
   for method in ('COBYQA','BFGS','L-BFGS-B','WarmBFGS'):
    m=solve(f,x,method)
    rows.append(dict(function=family,dimension=d,seed=seed,method=method,evaluations=m.n,best=m.best))
with (P/'raw_results.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=[]
for family in ('ackley','rastrigin','griewank','rosenbrock'):
 for d in (2,5,10):
  g=[r for r in rows if r['function']==family and r['dimension']==d]
  c={r['seed']:r['best'] for r in g if r['method']=='COBYQA'}
  for method in ('COBYQA','BFGS','L-BFGS-B','WarmBFGS'):
   v=[r for r in g if r['method']==method]
   summary.append(dict(function=family,dimension=d,method=method,runs=len(v),median_best=float(np.median([r['best'] for r in v])),mean_evals=float(np.mean([r['evaluations'] for r in v])),wins_vs_COBYQA=sum(r['best']<c[r['seed']]-1e-10 for r in v),losses_vs_COBYQA=sum(r['best']>c[r['seed']]+1e-10 for r in v)))
with (P/'summary.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
(P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seeds=[1600,1607],n_runs=len(rows)),indent=2)+'\n')
for method in ('COBYQA','BFGS','L-BFGS-B','WarmBFGS'):
 v=[r for r in summary if r['method']==method]
 print(method,'wins',sum(r['wins_vs_COBYQA'] for r in v),'losses',sum(r['losses_vs_COBYQA'] for r in v),'mean_evals',round(np.mean([r['mean_evals'] for r in v]),1),flush=True)
for family in ('ackley','rastrigin','griewank','rosenbrock'):
 print(family,{method:sum(r['wins_vs_COBYQA'] for r in summary if r['function']==family and r['method']==method) for method in ('BFGS','L-BFGS-B','WarmBFGS')},flush=True)
for fn in ('phase26.py','raw_results.csv','summary.csv','environment.json'):
 print(fn,hashlib.sha256((P/fn).read_bytes()).hexdigest())
