"""Phase 25: cost-accounted dual-engine derivative-free portfolio.
Held-out seeds 1500..1509, matched 240-evaluation caps.
"""
import csv,hashlib,json,platform
from pathlib import Path
import numpy as np,scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent; B=240
class Budget(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=np.inf;self.bestx=None
 def __call__(self,x):
  if self.n>=B:raise Budget()
  self.n+=1;y=float(self.f(np.asarray(x)))
  if y<self.best:self.best=y;self.bestx=np.array(x,copy=True)
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

def call(m,x,method,cap):
 if cap<=0:return
 # objective wrapper enforces per-stage and global budgets exactly
 stage=0
 def f(y):
  nonlocal stage
  if stage>=cap:raise Budget()
  stage+=1;return m(y)
 try:
  if method=='COBYQA':minimize(f,x,method='COBYQA',options={'maxfev':cap,'maxiter':cap})
  else:minimize(f,x,method='Powell',options={'maxfev':cap,'maxiter':cap,'xtol':1e-6,'ftol':1e-8})
 except Budget:pass

def solve(f,x0,method):
 m=Meter(f)
 if method in ('COBYQA','Powell'):call(m,x0,method,B)
 elif method=='DualStart':
  # budget split, two independent engines starting at same x0; return best ever.
  call(m,x0,'COBYQA',B//2);call(m,x0,'Powell',B-m.n)
 elif method=='DualWarm':
  # 120 COBYQA evaluations then Powell starts at its best point.
  call(m,x0,'COBYQA',B//2);call(m,m.bestx if m.bestx is not None else x0,'Powell',B-m.n)
 return m
rows=[]
for name in ('ackley','rastrigin','griewank','rosenbrock'):
 for d in (2,5,10):
  for seed in range(1500,1504):
   f,x0=problem(name,d,seed)
   for method in ('COBYQA','Powell','DualStart','DualWarm'):
    m=solve(f,x0,method)
    rows.append(dict(function=name,dimension=d,seed=seed,method=method,budget=B,evaluations=m.n,best=m.best))
with (P/'raw_results.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=[]
for name in ('ackley','rastrigin','griewank','rosenbrock'):
 for d in (2,5,10):
  sub=[r for r in rows if r['function']==name and r['dimension']==d]
  ref={k:{r['seed']:r['best'] for r in sub if r['method']==k} for k in ('COBYQA','Powell')}
  for method in ('COBYQA','Powell','DualStart','DualWarm'):
   g=[r for r in sub if r['method']==method]
   summary.append(dict(function=name,dimension=d,method=method,median_best=float(np.median([r['best'] for r in g])),mean_evals=float(np.mean([r['evaluations'] for r in g])),wins_vs_COBYQA=sum(r['best']<ref['COBYQA'][r['seed']]-1e-10 for r in g),wins_vs_Powell=sum(r['best']<ref['Powell'][r['seed']]-1e-10 for r in g),wins_vs_best_single=sum(r['best']<min(ref['COBYQA'][r['seed']],ref['Powell'][r['seed']])-1e-10 for r in g),runs=len(g)))
with (P/'summary.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
(P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seeds=[1500,1503],methods=['COBYQA','Powell','DualStart','DualWarm']),indent=2)+'\n')
print('runs',len(rows))
for method in ('COBYQA','Powell','DualStart','DualWarm'):
 g=[r for r in summary if r['method']==method]
 print(method,'wins_vs_COBYQA',sum(r['wins_vs_COBYQA'] for r in g),'wins_vs_Powell',sum(r['wins_vs_Powell'] for r in g),'wins_vs_best_single',sum(r['wins_vs_best_single'] for r in g),'mean_evals',np.mean([r['mean_evals'] for r in g]))
for f in ('phase25.py','raw_results.csv','summary.csv','environment.json'):
 print('sha256',f,hashlib.sha256((P/f).read_bytes()).hexdigest())
