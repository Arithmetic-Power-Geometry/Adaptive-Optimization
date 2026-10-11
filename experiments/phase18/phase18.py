"""Phase 18: held-out continuation versus fixed/adaptive restart, 180 oracle calls."""
import csv, json, hashlib, platform
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
P=Path(__file__).resolve().parent
B=90
class Budget(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=float('inf');self.bestx=None;self.history=[]
 def __call__(self,x):
  if self.n>=B:raise Budget()
  y=float(self.f(np.asarray(x)));self.n+=1
  if y<self.best:self.best=y;self.bestx=np.asarray(x).copy()
  self.history.append(self.best);return y
class Sub:
 def __init__(self,m,cap):self.m=m;self.cap=cap;self.n=0
 def __call__(self,x):
  if self.n>=self.cap:raise Budget()
  self.n+=1;return self.m(x)
def problem(name,d,seed):
 rng=np.random.default_rng(17*seed+100*d)
 Q,_=np.linalg.qr(rng.normal(size=(d,d)));shift=rng.uniform(-2,2,d)
 def f(x):
  z=Q@(x-shift)
  if name=='ackley':return -20*np.exp(-.2*np.sqrt(np.mean(z*z)))-np.exp(np.mean(np.cos(2*np.pi*z)))+20+np.e
  if name=='rastrigin':return 10*d+np.sum(z*z-10*np.cos(2*np.pi*z))
  if name=='griewank':return 1+np.sum(z*z)/4000-np.prod(np.cos(z/np.sqrt(np.arange(1,d+1))))
  return np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2)
 return f,rng.uniform(-3,3,d)
def run(f,x0,method,seed):
 m=Meter(f);d=len(x0);rng=np.random.default_rng(seed+2000)
 try:
  if method=='COBYQA':minimize(m,x0,method='COBYQA',options={'maxfev':B,'maxiter':B});return m,False
  start2=x0+rng.uniform(-1.5,1.5,d)
  s=Sub(m,54)
  try:minimize(s,x0,method='COBYQA',options={'maxfev':54,'maxiter':54})
  except Budget:pass
  # Plateau test: if less than 1% relative improvement in last 30 calls, restart.
  # Decision uses only incumbent observations; no extra oracle calls.
  plateau=len(m.history)>=31 and (m.history[-31]-m.history[-1]) <= .01*max(1,abs(m.history[-31]))
  restart=method=='FixedRestart' or (method=='PlateauRestart' and plateau)
  if restart:
   s2=Sub(m,B-m.n)
   try:minimize(s2,start2,method='COBYQA',options={'maxfev':B-m.n,'maxiter':B-m.n})
   except Budget:pass
  else:
   # A new COBYQA invocation from the incumbent is a *warm restart*, not true
   # uninterrupted continuation: this is a methodological limitation.
   incumbent=m.bestx.copy()
   s2=Sub(m,B-m.n)
   try:minimize(s2,incumbent,method='COBYQA',options={'maxfev':B-m.n,'maxiter':B-m.n})
   except Budget:pass
 except Budget:pass
 return m,restart
rows=[]
for name in ('ackley','rastrigin','rosenbrock'):
 for d in (2,5):
  for seed in range(800,803):
   f,x0=problem(name,d,seed)
   for method in ('COBYQA','FixedRestart','PlateauRestart'):
    m,restarted=run(f,x0,method,seed)
    rows.append(dict(function=name,dimension=d,seed=seed,method=method,budget=B,evaluations=m.n,best=m.best,restarted=int(restarted)))
with (P/'raw_results.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=[]
for name in ('ackley','rastrigin','rosenbrock'):
 for d in (2,5):
  g=[r for r in rows if r['function']==name and r['dimension']==d]
  base={r['seed']:r['best'] for r in g if r['method']=='COBYQA'}
  for method in ('COBYQA','FixedRestart','PlateauRestart'):
   v=[r for r in g if r['method']==method]
   summary.append(dict(function=name,dimension=d,method=method,median_best=float(np.median([r['best'] for r in v])),wins_vs_COBYQA=sum(r['best']<base[r['seed']]-1e-12 for r in v),restarts=sum(r['restarted'] for r in v),runs=len(v)))
with (P/'summary.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
(P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=__import__('scipy').__version__,budget=B,seeds=[800,802],design='3 functions x 2 dimensions x 3 seeds x 3 methods'),indent=2))
print('RUNS',len(rows))
for method in ('FixedRestart','PlateauRestart'):
 s=[r for r in summary if r['method']==method];print(method,'wins',sum(r['wins_vs_COBYQA'] for r in s),'restarts',sum(r['restarts'] for r in s))
for f in ('phase18.py','raw_results.csv','summary.csv','environment.json'):
 print('SHA256',f,hashlib.sha256((P/f).read_bytes()).hexdigest())
