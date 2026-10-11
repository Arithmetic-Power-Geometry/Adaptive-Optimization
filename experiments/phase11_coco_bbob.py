"""Phase 11: official COCO/BBOB pilot. CI executes; no local COCO results are claimed."""
import argparse,csv,hashlib,json,platform
from pathlib import Path
import numpy as np
from scipy.optimize import minimize,differential_evolution
import cocoex
try:
 import cma
except ImportError:
 cma=None
class StopBudget(Exception): pass
class Meter:
 def __init__(self,p,budget):self.p=p;self.cap=budget;self.n=0;self.best=float('inf');self.trace=[]
 def __call__(self,x):
  if self.n>=self.cap:raise StopBudget()
  v=float(self.p(np.asarray(x)));self.n+=1;self.best=min(self.best,v)
  if self.n in (10,20,40,80,120,240,480):self.trace.append((self.n,self.best))
  return v
def poll(m,x0,seed,mode):
 rng=np.random.default_rng(seed);d=len(x0);x=x0.copy();fx=m(x)
 step=np.ones(d);memory=np.zeros(d);stale=0
 while m.n<m.cap:
  good=False
  if mode=='Memory' and stale and np.linalg.norm(memory)>1e-12:
   direction=memory/np.linalg.norm(memory)
   for s in (1,-1):
    if m.n>=m.cap:break
    y=np.clip(x+s*np.mean(step)*direction,-5,5)
    if np.array_equal(x,y):continue
    fy=m(y)
    if fy<fx:
     memory=.7*memory+.3*(y-x);x,fx=y,fy;good=True;break
  if not good:
   for j in rng.permutation(d):
    for s in rng.permutation([-1,1]):
     if m.n>=m.cap:break
     y=x.copy();y[j]=np.clip(y[j]+s*step[j],-5,5)
     if y[j]==x[j]:continue
     fy=m(y)
     if fy<fx:
      memory=.7*memory+.3*(y-x);x,fx=y,fy;step[j]=min(6,1.15*step[j]);good=True;break
    if m.n>=m.cap:break
  if good:stale=0
  else:
   stale+=1;step*=.5
   if max(step)<1e-6 and m.n<m.cap:
    x=rng.uniform(-5,5,d);fx=m(x);step[:]=1;memory[:]=0;stale=0
def run(problem,method,budget,seed):
 d=problem.dimension;m=Meter(problem,budget);x0=np.asarray(problem.initial_solution,dtype=float)
 try:
  if method in ('Adaptive','Memory'):poll(m,x0,seed,method)
  elif method=='Powell':minimize(m,x0,method='Powell',bounds=[(-5,5)]*d,options={'maxfev':budget})
  elif method=='DE':differential_evolution(m,[(-5,5)]*d,rng=np.random.default_rng(seed),popsize=5,maxiter=1000,polish=False,tol=0)
  elif method=='CMA':
   if cma is None:raise RuntimeError('pycma unavailable')
   es=cma.CMAEvolutionStrategy(x0,2.0,{'seed':seed+1,'bounds':[-5,5],'verbose':-9,'popsize':4+int(3*np.log(d))})
   while not es.stop() and m.n<budget:
    xs=es.ask();ys=[]
    for x in xs:
     if m.n>=budget:break
     ys.append(m(x))
    if len(ys)==len(xs):es.tell(xs,ys)
    else:break
 except StopBudget:pass
 return m
def main():
 a=argparse.ArgumentParser()
 a.add_argument('--instances',default='1-3');a.add_argument('--dimensions',default='2,5');a.add_argument('--budget-factor',type=int,default=40)
 a.add_argument('--out',default='phase11_results');a.add_argument('--methods',default='Adaptive,Memory,Powell,DE,CMA')
 args=a.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 suite=cocoex.Suite('bbob',f'instances: {args.instances}',f'dimensions: {args.dimensions}')
 methods=args.methods.split(',');rows=[];traces=[]
 for problem in suite:
  # A fresh Suite/Problem per method prevents COCO evaluation counters being shared across methods.
  for method in methods:
   fresh=cocoex.Suite('bbob',f'instances: {args.instances}',f'dimensions: {args.dimensions}')
   p=fresh.get_problem(problem.index)
   seed=100000+p.index
   meter=run(p,method,args.budget_factor*p.dimension,seed)
   row=dict(problem_id=p.id,function_id=p.id_function,instance=p.id_instance,dimension=p.dimension,method=method,budget=meter.cap,evaluations=meter.n,best=meter.best)
   rows.append(row)
   for n,v in meter.trace:traces.append(dict(problem_id=p.id,method=method,evaluations=n,best=v))
   print(json.dumps(row),flush=True)
 for name,data in [('raw.csv',rows),('traces.csv',traces)]:
  with (out/name).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 (out/'environment.json').write_text(json.dumps({'python':platform.python_version(),'numpy':np.__version__,'scipy':__import__('scipy').__version__,'cocoex':getattr(cocoex,'__version__','unreported'),'cma':getattr(cma,'__version__','missing'),'instances':args.instances,'dimensions':args.dimensions,'budget_factor':args.budget_factor,'methods':methods},indent=2))
 for f in out.iterdir():
  if f.is_file():print('SHA256',f.name,hashlib.sha256(f.read_bytes()).hexdigest())
if __name__=='__main__':main()
