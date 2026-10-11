"""Phase 29: exponential zigzag turns, held-out controlled benchmark."""
import csv, json, platform, hashlib
from pathlib import Path
import numpy as np, scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent; B=160
class Exhausted(Exception): pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=float('inf')
 def __call__(self,x):
  if self.n>=B:raise Exhausted()
  y=float(self.f(np.asarray(x)));self.n+=1;self.best=min(self.best,y);return y

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
  except Exhausted:pass
  return m
 x=x0.copy();fx=m(x);h=.7;d=len(x);rng=np.random.default_rng(seed+91000)
 previous=np.zeros(d);previous[0]=1.;sign=1.;fails=0;turns=0
 while m.n<B and h>1e-7:
  if method in ('ZigZag','ExpoZigZag'):
   candidate=rng.normal(size=d);candidate-=previous*np.dot(candidate,previous)
   norm=np.linalg.norm(candidate)
   if norm<1e-10:candidate=np.roll(previous,1)
   else:candidate/=norm
   if method=='ExpoZigZag':
    # Exponentially shrinking angle, periodic reset; no post-hoc tuning.
    theta=np.pi/3*np.exp(-turns/8.0)+np.pi/18
    v=np.cos(theta)*previous+sign*np.sin(theta)*candidate
   else:v=(previous+sign*candidate)/np.sqrt(2)
   sign=-sign;turns+=1
  else:
   v=rng.normal(size=d);v/=np.linalg.norm(v)
  improved=False
  for direction in (v,-v):
   if m.n>=B:break
   y=x+h*direction;fy=m(y)
   if fy<fx:x=y;fx=fy;previous=direction.copy();improved=True;break
  h=min(1.5,h*1.08) if improved else h*.7
  fails=0 if improved else fails+1
  if fails>=d*4 and method in ('ZigZag','ExpoZigZag'):
   previous=np.eye(d)[int(rng.integers(d))];fails=0;turns=0
 return m

def main():
 rows=[]
 for family in ('ackley','rastrigin','griewank','rosenbrock'):
  for d in (2,5,10):
   for seed in range(1900,1904):
    f,x=problem(family,d,seed)
    for method in ('ExpoZigZag','ZigZag','RandomPoll','COBYQA'):
     m=solve(f,x,seed,method)
     rows.append(dict(function=family,dimension=d,seed=seed,method=method,evaluations=m.n,best=m.best))
 with (P/'raw_results.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 summary=[]
 for family in ('ackley','rastrigin','griewank','rosenbrock'):
  for d in (2,5,10):
   g=[r for r in rows if r['function']==family and r['dimension']==d]
   refs={method:{r['seed']:r['best'] for r in g if r['method']==method} for method in ('ZigZag','RandomPoll','COBYQA')}
   for method in ('ExpoZigZag','ZigZag','RandomPoll','COBYQA'):
    v=[r for r in g if r['method']==method]
    out=dict(function=family,dimension=d,method=method,median_best=float(np.median([r['best'] for r in v])),mean_evals=float(np.mean([r['evaluations'] for r in v])),runs=len(v))
    for comparator in refs:
     out['wins_vs_'+comparator]=sum(r['best']<refs[comparator][r['seed']]-1e-10 for r in v)
     out['losses_vs_'+comparator]=sum(r['best']>refs[comparator][r['seed']]+1e-10 for r in v)
    summary.append(out)
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seeds=[1900,1903],design='4 families x 3 dimensions x 4 seeds x 4 methods'),indent=2)+'\n')
 print('RUNS',len(rows))
 for method in ('ExpoZigZag','ZigZag','RandomPoll','COBYQA'):
  v=[r for r in summary if r['method']==method]
  print(method,'wins COBYQA',sum(r['wins_vs_COBYQA'] for r in v),'losses',sum(r['losses_vs_COBYQA'] for r in v),'wins ZigZag',sum(r['wins_vs_ZigZag'] for r in v),'losses ZigZag',sum(r['losses_vs_ZigZag'] for r in v),'mean_evals',round(np.mean([r['mean_evals'] for r in v]),2),flush=True)
 for fn in ('phase29.py','raw_results.csv','summary.csv','environment.json'):
  print('SHA256',fn,hashlib.sha256((P/fn).read_bytes()).hexdigest())
if __name__=='__main__':main()
