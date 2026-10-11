"""Phase 27: budget-fair incumbent-preserving COBYQA restart ablation."""
import csv, hashlib, json, platform
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize

P=Path(__file__).resolve().parent
B=240
SEEDS=range(1700,1703)
METHODS=('COBYQA','RestartBest','RestartKick','MultiStart')
class Exhausted(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=np.inf;self.x=None
 def __call__(self,x):
  if self.n>=B:raise Exhausted()
  y=float(self.f(np.asarray(x)));self.n+=1
  if y<self.best:self.best=y;self.x=np.asarray(x).copy()
  return y

def problem(name,d,seed):
 rng=np.random.default_rng(seed*17+d*100)
 Q,_=np.linalg.qr(rng.normal(size=(d,d)))
 shift=rng.uniform(-2,2,d)
 def f(x):
  z=Q@(x-shift)
  if name=='ackley':return -20*np.exp(-.2*np.sqrt(np.mean(z*z)))-np.exp(np.mean(np.cos(2*np.pi*z)))+20+np.e
  if name=='rastrigin':return 10*d+np.sum(z*z-10*np.cos(2*np.pi*z))
  if name=='griewank':return 1+np.sum(z*z)/4000-np.prod(np.cos(z/np.sqrt(np.arange(1,d+1))))
  return np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2)
 return f,rng.uniform(-3,3,d)

def stage(m,x,cap):
 count=0
 def fun(y):
  nonlocal count
  if count>=cap:raise Exhausted()
  count+=1
  return m(y)
 try:minimize(fun,x,method='COBYQA',options={'maxfev':cap,'maxiter':cap})
 except Exhausted:pass

def solve(f,x0,seed,method):
 m=Meter(f)
 if method=='COBYQA':stage(m,x0,B)
 else:
  stage(m,x0,120)
  rng=np.random.default_rng(seed+85000)
  if method=='RestartBest':x=m.x.copy()
  elif method=='RestartKick':x=m.x+0.8*rng.normal(size=len(x0))/np.sqrt(len(x0))
  else:x=x0+0.8*rng.normal(size=len(x0))/np.sqrt(len(x0))
  stage(m,x,B-m.n)
 return m

def main():
 rows=[]
 for family in ('ackley','rastrigin','griewank','rosenbrock'):
  for d in (2,5,10):
   for seed in SEEDS:
    f,x0=problem(family,d,seed)
    for method in METHODS:
     m=solve(f,x0,seed,method)
     rows.append(dict(function=family,dimension=d,seed=seed,method=method,budget=B,evaluations=m.n,best=m.best))
 with (P/'raw_results.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 summary=[]
 for family in ('ackley','rastrigin','griewank','rosenbrock'):
  for d in (2,5,10):
   group=[r for r in rows if r['function']==family and r['dimension']==d]
   ref={r['seed']:r['best'] for r in group if r['method']=='COBYQA'}
   for method in METHODS:
    v=[r for r in group if r['method']==method]
    summary.append(dict(function=family,dimension=d,method=method,runs=len(v),median_best=float(np.median([r['best'] for r in v])),mean_evals=float(np.mean([r['evaluations'] for r in v])),wins=sum(r['best']<ref[r['seed']]-1e-10 for r in v),losses=sum(r['best']>ref[r['seed']]+1e-10 for r in v),ties=sum(abs(r['best']-ref[r['seed']])<=1e-10 for r in v)))
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seeds=[min(SEEDS),max(SEEDS)],methods=METHODS,seed_rule='seed+85000',split=120),indent=2)+'\n')
 print('RUNS',len(rows))
 for method in METHODS:
  v=[r for r in summary if r['method']==method]
  print(method,'wins',sum(r['wins'] for r in v),'losses',sum(r['losses'] for r in v),'ties',sum(r['ties'] for r in v),'mean_evals',round(np.mean([r['mean_evals'] for r in v]),2),flush=True)
 for family in ('ackley','rastrigin','griewank','rosenbrock'):
  print(family,{method:sum(r['wins'] for r in summary if r['function']==family and r['method']==method) for method in METHODS[1:]},flush=True)
 for fn in ('phase27.py','raw_results.csv','summary.csv','environment.json'):
  print('SHA256',fn,hashlib.sha256((P/fn).read_bytes()).hexdigest())
if __name__=='__main__':main()
