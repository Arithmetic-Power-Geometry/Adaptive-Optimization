"""Phase 21: APG curvature-filtered secant polling; independently seeded test."""
import numpy as np,csv,json,hashlib,platform
from pathlib import Path
from scipy.optimize import minimize
P=Path(__file__).resolve().parent; B=160
class Stop(Exception): pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=np.inf;self.bestx=None
 def __call__(self,x):
  if self.n>=B:raise Stop()
  y=float(self.f(np.asarray(x)));self.n+=1
  if y<self.best:self.best=y;self.bestx=np.asarray(x).copy()
  return y

def problem(name,d,seed):
 rng=np.random.default_rng(seed*17+100*d);Q,_=np.linalg.qr(rng.normal(size=(d,d)));shift=rng.uniform(-2,2,d)
 def f(x):
  z=Q@(x-shift)
  if name=='rastrigin':return 10*d+np.sum(z*z-10*np.cos(2*np.pi*z))
  if name=='ackley':return -20*np.exp(-.2*np.sqrt(np.mean(z*z)))-np.exp(np.mean(np.cos(2*np.pi*z)))+20+np.e
  if name=='griewank':return 1+np.sum(z*z)/4000-np.prod(np.cos(z/np.sqrt(np.arange(1,d+1))))
  return np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2)
 return f,rng.uniform(-3,3,d)

def apgcurv(m,x0,seed,variant):
 rng=np.random.default_rng(seed+21000);x=x0.copy();fx=m(x);h=.6
 try:
  while m.n+3<=B and h>1e-6:
   improved=False
   for j in rng.permutation(len(x)):
    if m.n+3>B:break
    e=np.zeros(len(x));e[j]=1
    fp=m(x+h*e);fm=m(x-h*e)
    g=(fp-fm)/(2*h);curv=(fp+fm-2*fx)/(h*h)
    if variant=='APGCurvature' and curv>1e-8:
     # Local power regularization suppresses large extrapolations; deterministic.
     step=np.clip(-g/curv,-2*h,2*h)
     if abs(step)>1e-12:
      y=x+step*e;fy=m(y)
      if fy<fx:x=y;fx=fy;improved=True;break
    # Reuse the two measured symmetric probes before spending further budget.
    if fp<fx or fm<fx:
     if fp<fm:x=x+h*e;fx=fp
     else:x=x-h*e;fx=fm
     improved=True;break
   h=min(h*1.15,1.5) if improved else h*.5
 except Stop:pass

def solve(f,x0,seed,method):
 m=Meter(f)
 try:
  if method=='COBYQA':minimize(m,x0,method='COBYQA',options={'maxfev':B,'maxiter':B})
  elif method=='Powell':minimize(m,x0,method='Powell',options={'maxfev':B})
  else:apgcurv(m,x0,seed,method)
 except Stop:pass
 return m
rows=[]
for family in ('ackley','rastrigin','griewank','rosenbrock'):
 for d in (2,5,10):
  for seed in range(1100,1106):
   f,x0=problem(family,d,seed)
   for method in ('APGCurvature','SymmetricPoll','COBYQA','Powell'):
    m=solve(f,x0,seed,method)
    rows.append(dict(function=family,dimension=d,seed=seed,method=method,evaluations=m.n,best=m.best))
with (P/'raw_results.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=[]
for family in ('ackley','rastrigin','griewank','rosenbrock'):
 for d in (2,5,10):
  g=[r for r in rows if r['function']==family and r['dimension']==d];b={r['seed']:r['best'] for r in g if r['method']=='COBYQA'};s={r['seed']:r['best'] for r in g if r['method']=='SymmetricPoll'}
  for method in ('APGCurvature','SymmetricPoll','COBYQA','Powell'):
   v=[r for r in g if r['method']==method]
   summary.append(dict(function=family,dimension=d,method=method,median_best=float(np.median([r['best'] for r in v])),wins_vs_COBYQA=sum(r['best']<b[r['seed']]-1e-10 for r in v),wins_vs_symmetric=sum(r['best']<s[r['seed']]-1e-10 for r in v),mean_evals=float(np.mean([r['evaluations'] for r in v])),runs=len(v)))
with (P/'summary.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
(P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=__import__('scipy').__version__,budget=B,seeds=[1100,1105]),indent=2))
print('RUNS',len(rows))
for method in ('APGCurvature','SymmetricPoll','COBYQA','Powell'):
 v=[r for r in summary if r['method']==method]
 print(method,'wins_COBYQA',sum(r['wins_vs_COBYQA'] for r in v),'wins_sym',sum(r['wins_vs_symmetric'] for r in v),'mean_evals',np.mean([r['mean_evals'] for r in v]))
for r in summary:
 if r['method'] in ('APGCurvature','COBYQA'):print(r['function'],r['dimension'],r['method'],r['median_best'])
for f in ('phase21.py','raw_results.csv','summary.csv','environment.json'):print('SHA256',f,hashlib.sha256((P/f).read_bytes()).hexdigest())
