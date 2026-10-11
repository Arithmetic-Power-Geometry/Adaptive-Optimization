"""Phase 33: bounded-improvement value-of-information gate, preregistered ablation."""
import csv,json,hashlib,platform
from pathlib import Path
import numpy as np,scipy
from scipy.optimize import minimize
P=Path(__file__).resolve().parent;B=160;N=16;ALPHA=.05;COST=.01
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
 if method=='COBYQA':stage(m,x0,B);return m,0,0,0,False
 stage(m,x0,80);tau=m.best;rng=np.random.default_rng(seed+133000)
 values=[]
 for _ in range(N):
  y=m(rng.uniform(-5,5,len(x0)))
  values.append(min(1.,max(0.,(tau-y)/(1.+abs(tau)))))
 mean=float(np.mean(values));rad=np.sqrt(np.log(1/ALPHA)/(2*N));lower=max(0.,mean-rad)
 trigger=method=='VOIGate' and lower>COST
 if method=='AlwaysGlobal' or trigger:
  for _ in range(20):m(rng.uniform(-5,5,len(x0)))
 stage(m,m.x.copy(),B-m.n)
 return m,mean,lower,rad,trigger
def main():
 rows=[]
 for family in ('ackley','rastrigin','griewank','rosenbrock'):
  for d in (2,5,10):
   for seed in range(2300,2304):
    f,x=problem(family,d,seed)
    for method in ('COBYQA','PilotOnly','AlwaysGlobal','VOIGate'):
     m,mean,lower,rad,trigger=solve(f,x,seed,method)
     rows.append(dict(function=family,dimension=d,seed=seed,method=method,budget=B,evaluations=m.n,best=m.best,normalized_mean_gain=mean,lower95=lower,confidence_radius=rad,gate_fired=int(trigger)))
 with (P/'raw_results.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 ref={(r['function'],r['dimension'],r['seed']):r['best'] for r in rows if r['method']=='COBYQA'}
 summ=[]
 for method in ('COBYQA','PilotOnly','AlwaysGlobal','VOIGate'):
  v=[r for r in rows if r['method']==method]
  wins=sum(r['best']<ref[(r['function'],r['dimension'],r['seed'])]-1e-10 for r in v)
  losses=sum(r['best']>ref[(r['function'],r['dimension'],r['seed'])]+1e-10 for r in v)
  summ.append(dict(method=method,runs=len(v),wins=wins,losses=losses,ties=len(v)-wins-losses,mean_evaluations=float(np.mean([r['evaluations'] for r in v])),gate_fired=sum(r['gate_fired'] for r in v),mean_probe_gain=float(np.mean([r['normalized_mean_gain'] for r in v]))))
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summ[0]));w.writeheader();w.writerows(summ)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,budget=B,seed_start=2300,seed_stop=2303,diagnostic_probes=N,alpha=ALPHA,normalized_gain_threshold=COST,confidence_radius=float(np.sqrt(np.log(1/ALPHA)/(2*N)))),indent=2)+'\n')
 for row in summ:print(row,flush=True)
 for name in ('phase33.py','raw_results.csv','summary.csv','environment.json'):
  print('SHA256',name,hashlib.sha256((P/name).read_bytes()).hexdigest(),flush=True)
if __name__=='__main__':main()
