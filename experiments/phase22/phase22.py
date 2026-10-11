import numpy as np,csv,json,hashlib,platform
from scipy.optimize import minimize
from pathlib import Path
P=Path(__file__).parent; B=160
class Stop(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=np.inf
 def __call__(self,x):
  if self.n>=B:raise Stop()
  self.n+=1;y=float(self.f(np.asarray(x)));self.best=min(self.best,y);return y

def prob(family,d,seed):
 rng=np.random.default_rng(seed*17+d*100);Q,_=np.linalg.qr(rng.normal(size=(d,d)));shift=rng.uniform(-2,2,d)
 def f(x):
  z=Q@(x-shift)
  if family=='ackley':return -20*np.exp(-.2*np.sqrt(np.mean(z*z)))-np.exp(np.mean(np.cos(2*np.pi*z)))+20+np.e
  if family=='rastrigin':return 10*d+np.sum(z*z-10*np.cos(2*np.pi*z))
  if family=='griewank':return 1+np.sum(z*z)/4000-np.prod(np.cos(z/np.sqrt(np.arange(1,d+1))))
  return np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2)
 return f,rng.uniform(-3,3,d)

def helix(m,x0,seed,mode):
 # Helix-search: deterministic equiangular spiral subspace polling with
 # orthogonalized 2D directions; no gradients, no Hessians, no memory.
 rng=np.random.default_rng(seed+50000);x=x0.copy();fx=m(x);h=.7;d=len(x)
 phi=(np.sqrt(5)-1)/2;theta=0.;basis=np.eye(d)
 while m.n<B and h>1e-7:
  if mode=='Helix':
   # rotate within random orthogonal plane; angles irrationally advance
   a,b=rng.choice(d,2,replace=False);theta=(theta+2*np.pi*phi)%(2*np.pi)
   v=np.zeros(d);v[a]=np.cos(theta);v[b]=np.sin(theta)
   directions=[v,-v]
  else:
   a=rng.integers(d);v=basis[a];directions=[v,-v]
  improved=False
  for v in directions:
   if m.n>=B:break
   y=x+h*v;fy=m(y)
   if fy<fx:x=y;fx=fy;improved=True;break
  h=min(h*1.08,1.5) if improved else h*.7

def solve(f,x0,seed,method):
 m=Meter(f)
 try:
  if method=='COBYQA':minimize(m,x0,method='COBYQA',options={'maxfev':B,'maxiter':B})
  elif method=='Powell':minimize(m,x0,method='Powell',options={'maxfev':B})
  else:helix(m,x0,seed,method)
 except Stop:pass
 return m
rows=[]
for family in ['ackley','rastrigin','griewank','rosenbrock']:
 for d in [2,5,10]:
  for seed in range(1200,1208):
   f,x0=prob(family,d,seed)
   for method in ['Helix','RandomAxis','COBYQA','Powell']:
    m=solve(f,x0,seed,method);rows.append(dict(function=family,dimension=d,seed=seed,method=method,evaluations=m.n,best=m.best))
with (P/'raw_results.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=[]
for family in ['ackley','rastrigin','griewank','rosenbrock']:
 for d in [2,5,10]:
  sub=[r for r in rows if r['function']==family and r['dimension']==d];c={r['seed']:r['best'] for r in sub if r['method']=='COBYQA'};a={r['seed']:r['best'] for r in sub if r['method']=='RandomAxis'}
  for method in ['Helix','RandomAxis','COBYQA','Powell']:
   v=[r for r in sub if r['method']==method];summary.append(dict(function=family,dimension=d,method=method,median_best=float(np.median([r['best'] for r in v])),wins_vs_COBYQA=sum(r['best']<c[r['seed']]-1e-10 for r in v),wins_vs_RandomAxis=sum(r['best']<a[r['seed']]-1e-10 for r in v),mean_evals=float(np.mean([r['evaluations'] for r in v])),runs=len(v)))
with (P/'summary.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
(P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=__import__('scipy').__version__,budget=B,seeds=[1200,1207]),indent=2))
print('runs',len(rows))
for method in ['Helix','RandomAxis','COBYQA','Powell']:
 sub=[r for r in summary if r['method']==method];print(method,'winsCOBYQA',sum(r['wins_vs_COBYQA'] for r in sub),'winsAxis',sum(r['wins_vs_RandomAxis'] for r in sub),'mean_evals',np.mean([r['mean_evals'] for r in sub]))
for r in summary:
 if r['method'] in ['Helix','COBYQA']:print(r['function'],r['dimension'],r['method'],round(r['median_best'],5))
for f in ['phase22.py','raw_results.csv','summary.csv','environment.json']:print('sha256',f,hashlib.sha256((P/f).read_bytes()).hexdigest())
