import numpy as np,csv,hashlib,json,platform
from scipy.optimize import minimize,differential_evolution
from pathlib import Path
P=Path(__file__).parent; B=180
class Stop(Exception): pass
class Meter:
 def __init__(self,fun):self.fun=fun;self.n=0;self.best=float('inf')
 def __call__(self,x):
  if self.n>=B:raise Stop()
  self.n+=1;y=float(self.fun(np.asarray(x)))
  self.best=min(self.best,y);return y

def objective(name,d,seed):
 rng=np.random.default_rng(seed*17+d*100);Q,_=np.linalg.qr(rng.normal(size=(d,d)));shift=rng.uniform(-2,2,d)
 def f(x):
  z=Q@(x-shift)
  if name=='rastrigin':return 10*d+np.sum(z*z-10*np.cos(2*np.pi*z))
  if name=='ackley':return -20*np.exp(-.2*np.sqrt(np.mean(z*z)))-np.exp(np.mean(np.cos(2*np.pi*z)))+20+np.e
  if name=='griewank':return 1+np.sum(z*z)/4000-np.prod(np.cos(z/np.sqrt(np.arange(1,d+1))))
  if name=='rosenbrock':return np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2)
 return f,rng.uniform(-3,3,d)

def solve(fun,x0,method,seed):
 d=len(x0);m=Meter(fun)
 try:
  if method=='COBYQA':minimize(m,x0,method='COBYQA',options={'maxfev':B,'maxiter':B});return m
  if method=='Powell':minimize(m,x0,method='Powell',options={'maxfev':B});return m
  if method=='DE':
   differential_evolution(m,[(-5,5)]*d,popsize=5,maxiter=1000,polish=False,rng=np.random.default_rng(seed),tol=0,atol=0);return m
  # Fixed-budget restart portfolio: 60% COBYQA initial, 40% COBYQA seeded restart.
  # Baseline controls: starts from same x0, 2nd restart sampled within local radius 1.5.
  rng=np.random.default_rng(seed+2000);start2=x0+rng.uniform(-1.5,1.5,d)
  class Sub:
   def __init__(self,cap):self.cap=cap;self.used=0
   def __call__(self,x):
    if self.used>=self.cap:raise Stop()
    self.used+=1;return m(x)
  for start,cap in [(x0,108),(start2,72)]:
   sub=Sub(cap)
   try:minimize(sub,start,method='COBYQA',options={'maxfev':cap,'maxiter':cap})
   except Stop:pass
 except Stop:pass
 return m
rows=[]
for name in ['ackley','rastrigin','griewank','rosenbrock']:
 for d in [2,5,10]:
  for seed in range(700,708):
   f,x0=objective(name,d,seed)
   for method in ['COBYQA','RestartCOBYQA','Powell','DE']:
    r=solve(f,x0,method,seed)
    rows.append(dict(function=name,dimension=d,seed=seed,method=method,budget=B,evaluations=r.n,best=r.best))
with (P/'raw_results.csv').open('w',newline='') as fh:
 w=csv.DictWriter(fh,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=[]
for name in ['ackley','rastrigin','griewank','rosenbrock']:
 for d in [2,5,10]:
  sub=[r for r in rows if r['function']==name and r['dimension']==d]
  base={r['seed']:r['best'] for r in sub if r['method']=='COBYQA'}
  for method in ['COBYQA','RestartCOBYQA','Powell','DE']:
   vals=[r for r in sub if r['method']==method]
   summary.append(dict(function=name,dimension=d,method=method,median_best=float(np.median([r['best'] for r in vals])),wins_vs_COBYQA=sum(r['best']<base[r['seed']]-1e-12 for r in vals),runs=len(vals)))
with (P/'summary.csv').open('w',newline='') as fh:
 w=csv.DictWriter(fh,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
(P/'environment.json').write_text(json.dumps({'python':platform.python_version(),'numpy':np.__version__,'scipy':__import__('scipy').__version__,'budget':B,'seeds':[700,707],'design':'4 functions x 3 dimensions x 8 seeds x 4 methods'},indent=2))
print('RUNS',len(rows))
for r in summary:print(r)
for name in ['phase17.py','raw_results.csv','summary.csv','environment.json']:
 print('SHA256',name,hashlib.sha256((P/name).read_bytes()).hexdigest())
