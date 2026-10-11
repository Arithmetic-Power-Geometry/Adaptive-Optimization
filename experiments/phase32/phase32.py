"""Phase 32: equal-volume stratification ablation; 160-call budget."""
import csv,hashlib,json,platform
from pathlib import Path
import numpy as np,scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent;B=160
class Stop(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=float('inf');self.x=None
 def __call__(self,x):
  if self.n>=B:raise Stop()
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
def stage(m,x,cap):
 used=0
 def fun(y):
  nonlocal used
  if used>=cap:raise Stop()
  used+=1;return m(y)
 try:minimize(fun,x,method='COBYQA',options={'maxfev':cap,'maxiter':cap})
 except Stop:pass
def solve(f,x0,seed,method):
 m=Meter(f)
 if method=='COBYQA':stage(m,x0,B);return m,0
 stage(m,x0,100);tau=m.best;k=0;rng=np.random.default_rng(seed+111000)
 for i in range(20):
  if method=='Stratified':
   y=rng.uniform(-5,5,len(x0));y[0]=-5+10*(i+rng.random())/20
  elif method=='Uniform':y=rng.uniform(-5,5,len(x0))
  else:y=m.x+rng.normal(size=len(x0))
  if m(y)<tau:k+=1
 stage(m,m.x.copy(),B-m.n)
 return m,k
def main():
 rows=[]
 for family in ('ackley','rastrigin','griewank','rosenbrock'):
  for d in (2,5,10):
   for seed in range(2200,2204):
    f,x=problem(family,d,seed)
    for method in ('COBYQA','Uniform','Stratified','Gaussian'):
     m,k=solve(f,x,seed,method)
     rows.append(dict(function=family,dimension=d,seed=seed,method=method,budget=B,evaluations=m.n,best=m.best,improving_probes=k))
 with (P/'raw_results.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 summary=[]
 for method in ('COBYQA','Uniform','Stratified','Gaussian'):
  v=[r for r in rows if r['method']==method]
  ref={(r['function'],r['dimension'],r['seed']):r['best'] for r in rows if r['method']=='COBYQA'}
  wins=sum(r['best']<ref[(r['function'],r['dimension'],r['seed'])]-1e-10 for r in v)
  losses=sum(r['best']>ref[(r['function'],r['dimension'],r['seed'])]+1e-10 for r in v)
  summary.append(dict(method=method,runs=len(v),wins=wins,losses=losses,ties=len(v)-wins-losses,mean_evaluations=np.mean([r['evaluations'] for r in v]),mean_improving_probes=np.mean([r['improving_probes'] for r in v])))
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seeds=[2200,2203],probe_count=20,first_stage=100,domain='[-5,5]^d'),indent=2)+'\n')
 for s in summary:print(s,flush=True)
 for fn in ('phase32.py','raw_results.csv','summary.csv','environment.json'):
  print(fn,hashlib.sha256((P/fn).read_bytes()).hexdigest(),flush=True)
if __name__=='__main__':main()
