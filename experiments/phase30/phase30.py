"""Phase 30: Lebesgue-volume motivated uniform-probe restart portfolio.
All objective evaluations counted; same starting points; fixed predeclared design.
"""
import csv,hashlib,json,platform
from pathlib import Path
import numpy as np,scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent; B=160
class Exhausted(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=np.inf;self.x=None
 def __call__(self,x):
  if self.n>=B:raise Exhausted()
  y=float(self.f(np.asarray(x)));self.n+=1
  if y<self.best:self.best=y;self.x=np.array(x,copy=True)
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

def cobyqa(m,x,cap):
 used=0
 def fun(y):
  nonlocal used
  if used>=cap:raise Exhausted()
  used+=1;return m(y)
 try:minimize(fun,x,method='COBYQA',options={'maxfev':cap,'maxiter':cap})
 except Exhausted:pass

def solve(f,x0,seed,method):
 m=Meter(f)
 if method=='COBYQA':cobyqa(m,x0,B);return m
 rng=np.random.default_rng(seed+94000)
 if method=='Uniform':
  m(x0)
  while m.n<B:m(rng.uniform(-5,5,size=len(x0)))
  return m
 # Two-stage: 100 local evals, then 20 probes of measure-defined uniform cube;
 # if any probe improves the incumbent, restart at best probe; otherwise keep incumbent.
 cobyqa(m,x0,100)
 incumbent=m.x.copy()
 if method=='LebesgueProbe':
  for _ in range(20):m(rng.uniform(-5,5,size=len(x0)))
 else:
  for _ in range(20):m(incumbent+rng.normal(0,1,size=len(x0)))
 cobyqa(m,m.x.copy(),B-m.n)
 return m

def main():
 rows=[]
 for family in ('ackley','rastrigin','griewank','rosenbrock'):
  for d in (2,5,10):
   for seed in range(2000,2004):
    f,x0=problem(family,d,seed)
    for method in ('COBYQA','Uniform','LebesgueProbe','GaussianProbe'):
     m=solve(f,x0,seed,method)
     rows.append(dict(function=family,dimension=d,seed=seed,method=method,budget=B,evaluations=m.n,best=m.best))
 with (P/'raw_results.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 summary=[]
 for family in ('ackley','rastrigin','griewank','rosenbrock'):
  for d in (2,5,10):
   g=[r for r in rows if r['function']==family and r['dimension']==d]
   ref={r['seed']:r['best'] for r in g if r['method']=='COBYQA'}
   for method in ('COBYQA','Uniform','LebesgueProbe','GaussianProbe'):
    v=[r for r in g if r['method']==method]
    summary.append(dict(function=family,dimension=d,method=method,runs=len(v),median_best=float(np.median([r['best'] for r in v])),mean_evals=float(np.mean([r['evaluations'] for r in v])),wins=sum(r['best']<ref[r['seed']]-1e-10 for r in v),losses=sum(r['best']>ref[r['seed']]+1e-10 for r in v),ties=sum(abs(r['best']-ref[r['seed']])<=1e-10 for r in v)))
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seeds=[2000,2003],domain='[-5,5]^d',probe_count=20,first_stage=100),indent=2)+'\n')
 print('RUNS',len(rows))
 for method in ('COBYQA','Uniform','LebesgueProbe','GaussianProbe'):
  v=[r for r in summary if r['method']==method]
  print(method,'wins',sum(r['wins'] for r in v),'losses',sum(r['losses'] for r in v),'ties',sum(r['ties'] for r in v),'mean_evals',round(np.mean([r['mean_evals'] for r in v]),2),flush=True)
 for fn in ('phase30.py','raw_results.csv','summary.csv','environment.json'):
  print('SHA256',fn,hashlib.sha256((P/fn).read_bytes()).hexdigest())
if __name__=='__main__':main()
