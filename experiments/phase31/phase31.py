"""Phase31: pre-registered fixed-pilot measure-switching study."""
import csv,json,platform,hashlib
from pathlib import Path
import numpy as np,scipy
from scipy.optimize import minimize
from scipy.stats import beta
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
 if method=='COBYQA':stage(m,x0,B);return m,0,0,False
 stage(m,x0,80)
 rng=np.random.default_rng(seed+100000)
 tau=m.best
 # Fixed diagnostic sample of 12 iid points in K, not adaptive threshold.
 successes=0
 for _ in range(12):
  if m(rng.uniform(-5,5,size=len(x0)))<tau:successes+=1
 # One-sided 95% Clopper-Pearson lower bound, zero successes -> 0.
 lower=float(beta.ppf(.05,successes,13-successes)) if successes else 0.0
 # Prespecified gate: if lower bound > 0.02, spend up to 20 more global probes.
 switch=method=='MeasureGate' and lower>.02
 if method=='AlwaysGlobal' or switch:
  for _ in range(20):m(rng.uniform(-5,5,size=len(x0)))
 # Pilot-only comparator resumes COBYQA immediately; all methods retain incumbent.
 stage(m,m.x.copy(),B-m.n)
 return m,successes,lower,switch

def main():
 rows=[]
 for family in ('ackley','rastrigin','griewank','rosenbrock'):
  for d in (2,5,10):
   for seed in range(2100,2104):
    f,x0=problem(family,d,seed)
    for method in ('COBYQA','PilotOnly','AlwaysGlobal','MeasureGate'):
     m,s,p,sw=solve(f,x0,seed,method)
     rows.append(dict(function=family,dimension=d,seed=seed,method=method,budget=B,evaluations=m.n,best=m.best,pilot_successes=s,lower95=p,extra_global=sw if method=='MeasureGate' else method=='AlwaysGlobal'))
 with (P/'raw_results.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 summary=[]
 for family in ('ackley','rastrigin','griewank','rosenbrock'):
  for d in (2,5,10):
   g=[r for r in rows if r['function']==family and r['dimension']==d];ref={r['seed']:r['best'] for r in g if r['method']=='COBYQA'}
   for method in ('COBYQA','PilotOnly','AlwaysGlobal','MeasureGate'):
    v=[r for r in g if r['method']==method]
    summary.append(dict(function=family,dimension=d,method=method,runs=len(v),wins=sum(r['best']<ref[r['seed']]-1e-10 for r in v),losses=sum(r['best']>ref[r['seed']]+1e-10 for r in v),ties=sum(abs(r['best']-ref[r['seed']])<=1e-10 for r in v),mean_evaluations=float(np.mean([r['evaluations'] for r in v])),extra_global_count=sum(bool(r['extra_global']) for r in v)))
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seeds=[2100,2103],pilot=12,first_stage=80,extra_probes=20,threshold=.02,one_sided_alpha=.05),indent=2)+'\n')
 print('RUNS',len(rows))
 for method in ('COBYQA','PilotOnly','AlwaysGlobal','MeasureGate'):
  v=[r for r in summary if r['method']==method]
  print(method,'wins',sum(r['wins'] for r in v),'losses',sum(r['losses'] for r in v),'ties',sum(r['ties'] for r in v),'mean_evals',round(np.mean([r['mean_evaluations'] for r in v]),2),'extra_global',sum(r['extra_global_count'] for r in v),flush=True)
 for fn in ('phase31.py','raw_results.csv','summary.csv','environment.json'):
  print('SHA256',fn,hashlib.sha256((P/fn).read_bytes()).hexdigest())
if __name__=='__main__':main()
