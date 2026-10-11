"""Predeclared APG exponent ablation, new seeds 1000..1004, no tuning."""
import csv,hashlib,json,platform,sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
P=Path(__file__).resolve().parent;B=180
class Budget(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=float('inf')
 def __call__(self,x):
  if self.n>=B:raise Budget()
  self.n+=1;y=float(self.f(np.asarray(x)));self.best=min(self.best,y);return y

def problem(name,d,seed):
 rng=np.random.default_rng(seed*17+d*100);Q,_=np.linalg.qr(rng.normal(size=(d,d)));shift=rng.uniform(-2,2,d)
 def f(x):
  z=Q@(x-shift)
  if name=='rastrigin':return 10*d+np.sum(z*z-10*np.cos(2*np.pi*z))
  if name=='ackley':return -20*np.exp(-.2*np.sqrt(np.mean(z*z)))-np.exp(np.mean(np.cos(2*np.pi*z)))+20+np.e
  if name=='griewank':return 1+np.sum(z*z)/4000-np.prod(np.cos(z/np.sqrt(np.arange(1,d+1))))
  return np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2)
 return f,rng.uniform(-3,3,d)

def poll(m,x0,seed,p):
 rng=np.random.default_rng(seed+9000);x=x0.copy();fx=m(x);h=.8;memory=[]
 while m.n<B:
  dirs=[]
  if memory and p is not None:
   gains=np.array([a[1] for a in memory]);weights=(gains+1e-9)**p;weights/=weights.sum()
   v=memory[rng.choice(len(memory),p=weights)][0];dirs.extend([v,-v])
  for k in rng.permutation(len(x)):
   e=np.zeros(len(x));e[k]=1;dirs.extend([e,-e])
  improved=False
  for v in dirs:
   if m.n>=B:break
   y=x+h*v;fy=m(y)
   if fy<fx:
    memory.append((v.copy(),fx-fy));memory=memory[-12:];x=y;fx=fy;improved=True;break
  h=min(h*1.12,1.5) if improved else h*.5
  if h<1e-7:break

def solve(f,x0,method,seed):
 m=Meter(f)
 try:
  if method=='COBYQA':minimize(m,x0,method='COBYQA',options={'maxfev':B,'maxiter':B})
  else:poll(m,x0,seed,None if method=='NoMemory' else int(method[1:]))
 except Budget:pass
 return m
rows=[]
for name in ['ackley','rastrigin','griewank','rosenbrock']:
 for d in [2,5,10]:
  for seed in range(1000,1005):
   f,x0=problem(name,d,seed)
   for method in ['NoMemory','P0','P1','P2','P4','COBYQA']:
    m=solve(f,x0,method,seed)
    rows.append(dict(function=name,dimension=d,seed=seed,method=method,budget=B,evaluations=m.n,best=m.best))
with (P/'raw_results.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=[]
for name in ['ackley','rastrigin','griewank','rosenbrock']:
 for d in [2,5,10]:
  sub=[r for r in rows if r['function']==name and r['dimension']==d]
  base={r['seed']:r['best'] for r in sub if r['method']=='COBYQA'}
  p0={r['seed']:r['best'] for r in sub if r['method']=='P0'}
  for method in ['NoMemory','P0','P1','P2','P4','COBYQA']:
   g=[r for r in sub if r['method']==method]
   summary.append(dict(function=name,dimension=d,method=method,median_best=float(np.median([r['best'] for r in g])),wins_vs_COBYQA=sum(r['best']<base[r['seed']]-1e-10 for r in g),wins_vs_P0=sum(r['best']<p0[r['seed']]-1e-10 for r in g),mean_evals=float(np.mean([r['evaluations'] for r in g])),runs=len(g)))
with (P/'summary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
(P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=__import__('scipy').__version__,seeds=[1000,1004],budget=B,design='4 families x 3 dimensions x 5 seeds x 6 methods',methods=['NoMemory','P0','P1','P2','P4','COBYQA']),indent=2))
print('TOTAL',len(rows))
for method in ['NoMemory','P0','P1','P2','P4','COBYQA']:
 g=[r for r in summary if r['method']==method]
 print(method,'wins_vs_COBYQA',sum(r['wins_vs_COBYQA'] for r in g),'wins_vs_P0',sum(r['wins_vs_P0'] for r in g),'median_of_medians',np.median([r['median_best'] for r in g]),'mean_evals',np.mean([r['mean_evals'] for r in g]))
for fn in ['phase20.py','raw_results.csv','summary.csv','environment.json']:
 print('SHA256',fn,hashlib.sha256((P/fn).read_bytes()).hexdigest())
