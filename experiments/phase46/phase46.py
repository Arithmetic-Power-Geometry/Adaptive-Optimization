"""Phase 46: independent 20-seed, d20, bounded rank-regime mechanism replication."""
import csv,hashlib,platform,json
from pathlib import Path
import numpy as np,scipy
from scipy.optimize import minimize,LinearConstraint
P=Path(__file__).resolve().parent
D=20;B=240;SEEDS=range(3700,3703)
METHODS=('Full','Embed8','NewBest','SameBest','NewOrigin')
class Stop(Exception):pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=float('inf');self.x=None;self.trace=[]
 def __call__(self,x):
  if self.n>=B:raise Stop()
  x=np.asarray(x);v=float(self.f(x));self.n+=1
  if v<self.best:self.best=v;self.x=x.copy()
  self.trace.append(self.best)
  return v
def instance(family,r,seed):
 rng=np.random.default_rng(seed*53+D*17+r*101)
 Q,_=np.linalg.qr(rng.normal(size=(D,r)))
 shift=rng.uniform(-2,2,r);x0=rng.uniform(-1.5,1.5,D)
 def f(x):
  z=Q.T@x-shift
  if family=='sphere':return float(z@z)
  return float(10*r+np.sum(z*z-10*np.cos(2*np.pi*z)))
 return f,x0
def run(f,x0,seed,method):
 m=Meter(f);rng=np.random.default_rng(seed+131000)
 lb=np.full(D,-5.);ub=np.full(D,5.)
 if method=='Full':
  try:minimize(m,x0,method='COBYQA',bounds=list(zip(lb,ub)),options={'maxfev':B,'maxiter':B})
  except Stop:pass
  return m
 A0,_=np.linalg.qr(rng.normal(size=(D,8)))
 for i,cap in enumerate([B] if method=='Embed8' else [B//2,B//2]):
  A=A0 if i==0 or method=='SameBest' else np.linalg.qr(rng.normal(size=(D,8)))[0]
  anchor=x0 if i==0 or method=='NewOrigin' else m.x.copy()
  used=0
  def reduced(z):
   nonlocal used
   if used>=cap:raise Stop()
   used+=1;return m(anchor+A@z)
  try:minimize(reduced,np.zeros(8),method='COBYQA',constraints=[LinearConstraint(A,lb-anchor,ub-anchor)],options={'maxfev':cap,'maxiter':cap})
  except Stop:pass
 return m
def main():
 rows=[];traces=[]
 for family in ('sphere','rastrigin'):
  for regime,r in (('low4',4),('full',20)):
   for seed in SEEDS:
    f,x0=instance(family,r,seed)
    for method in METHODS:
     m=run(f,x0,seed,method)
     rows.append(dict(family=family,regime=regime,dimension=D,rank=r,seed=seed,method=method,calls=m.n,best=m.best,budget=B))
     for call,best in enumerate(m.trace,1):traces.append(dict(family=family,regime=regime,seed=seed,method=method,call=call,best=best))
 for name,data in (('raw_results.csv',rows),('traces.csv',traces)):
  with (P/name).open('w',newline='') as h:
   w=csv.DictWriter(h,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 by={(z['family'],z['regime'],z['seed'],z['method']):z for z in rows};summary=[]
 for regime in ('low4','full'):
  for method in METHODS:
   vv=[z for z in rows if z['regime']==regime and z['method']==method]
   line=dict(regime=regime,method=method,n=len(vv),mean_calls=round(np.mean([z['calls'] for z in vv]),2),median_best=float(np.median([z['best'] for z in vv])))
   for base in ('Full','Embed8','NewBest','SameBest','NewOrigin'):
    diff=[z['best']-by[(z['family'],regime,z['seed'],base)]['best'] for z in vv]
    line['W_'+base]=sum(x< -1e-8 for x in diff);line['L_'+base]=sum(x>1e-8 for x in diff);line['T_'+base]=sum(abs(x)<=1e-8 for x in diff)
   summary.append(line)
 with (P/'summary.csv').open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
 (P/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,seeds=[min(SEEDS),max(SEEDS)],budget=B,dimension=D,methods=METHODS),indent=2)+'\n')
 for z in summary:print(z,flush=True)
 for name in ('phase46.py','raw_results.csv','traces.csv','summary.csv','environment.json'):
  print('SHA256',name,hashlib.sha256((P/name).read_bytes()).hexdigest())
if __name__=='__main__':main()
