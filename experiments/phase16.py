"""Phase 16: independent, strict-evaluation-cap comparator experiment.
Quadratic problems with bounded deterministic oracle perturbations. Source is self-contained.
"""
import csv, hashlib, json, platform
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
OUT=Path(__file__).resolve().parent
CAP=160
METHODS=('Adaptive','NoiseAwareFD','Powell','COBYQA','BFGS')
NOISE=(0.,0.01)
class Budget(Exception):pass
class Meter:
 def __init__(self,f,delta):self.f=f;self.delta=delta;self.n=0;self.best=np.inf;self.bestx=None
 def __call__(self,x):
  if self.n>=CAP:raise Budget()
  x=np.asarray(x);true=float(self.f(x));self.n+=1
  if true<self.best:self.best=true;self.bestx=x.copy()
  return true+self.delta*np.sin(17.3*np.sum(np.sin(3.1*x))+11.7*np.sum(np.cos(2.7*x)))
def solve(f,x0,method,seed,delta):
 m=Meter(f,delta);x=x0.copy();rng=np.random.default_rng(seed);d=len(x);step=.5
 try:
  if method in ('Powell','COBYQA','BFGS'):
   opts={'maxfev':CAP} if method=='Powell' else ({'maxfev':CAP,'maxiter':CAP,'disp':False} if method=='COBYQA' else {'maxiter':CAP,'gtol':1e-8})
   minimize(m,x0,method=method,options=opts)
   return m
  fx=m(x)
  while m.n<CAP:
   improved=False
   if method=='NoiseAwareFD' and m.n+3<=CAP:
    v=np.zeros(d);v[rng.integers(d)]=1;h=.5 if delta>0 else .02
    fp=m(x+h*v);fm=m(x-h*v);g=(fp-fm)/(2*h)
    if abs(g)>delta/h:
     y=x-step*np.sign(g)*v;fy=m(y)
     if fy<fx-2*delta:x,fx=y,fy;improved=True
   if not improved:
    for j in rng.permutation(d):
     for sign in rng.permutation([-1,1]):
      if m.n>=CAP:break
      y=x.copy();y[j]+=sign*step;fy=m(y)
      if fy<fx-(2*delta if method=='NoiseAwareFD' else 0):x,fx=y,fy;improved=True;break
     if improved or m.n>=CAP:break
   if not improved:step*=.5
   if step<1e-6:break
 except Budget:pass
 return m
def main():
 rows=[]
 for d in (2,5,10):
  for geometry in ('diagonal','rotated'):
   for seed in range(600,608):
    rng=np.random.default_rng(70000+seed+10*d);Q,_=np.linalg.qr(rng.normal(size=(d,d)))
    if geometry=='diagonal':Q=np.eye(d)
    H=Q.T@np.diag(np.geomspace(1,100,d))@Q
    shift=rng.uniform(-1,1,d);x0=rng.uniform(-2,2,d)
    f=lambda x,H=H,shift=shift:float((x-shift)@H@(x-shift))
    for delta in NOISE:
     for method in METHODS:
      m=solve(f,x0,method,seed,delta)
      rows.append(dict(dimension=d,geometry=geometry,seed=seed,noise=delta,method=method,evaluations=m.n,best_true=m.best))
 summary=[]
 for d in (2,5,10):
  for geometry in ('diagonal','rotated'):
   for delta in NOISE:
    group=[r for r in rows if r['dimension']==d and r['geometry']==geometry and r['noise']==delta]
    base={r['seed']:r['best_true'] for r in group if r['method']=='Adaptive'}
    for method in METHODS:
     sub=[r for r in group if r['method']==method]
     summary.append(dict(dimension=d,geometry=geometry,noise=delta,method=method,runs=len(sub),median_true=float(np.median([r['best_true'] for r in sub])),wins_vs_adaptive=sum(r['best_true']<base[r['seed']] for r in sub),mean_evals=float(np.mean([r['evaluations'] for r in sub]))))
 for name,records in [('raw_results.csv',rows),('summary.csv',summary)]:
  with (OUT/name).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
 meta=dict(phase=16,design='3 dimensions x 2 geometries x 8 seeds x 2 noise levels x 5 methods',n_runs=len(rows),cap=CAP,seed_range=[600,607],python=platform.python_version(),numpy=np.__version__,scipy=__import__('scipy').__version__,methods=METHODS)
 (OUT/'environment.json').write_text(json.dumps(meta,indent=2))
 for name in ('phase16.py','raw_results.csv','summary.csv','environment.json'):
  print('SHA256',name,hashlib.sha256((OUT/name).read_bytes()).hexdigest())
 print('runs',len(rows));print(*summary,sep='\n')
if __name__=='__main__':main()
