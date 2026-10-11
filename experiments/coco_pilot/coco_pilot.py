"""Official COCO/BBOB preregistered pilot. Requires coco-experiment and cma.
Not executed or validated in the current environment. Do not report results until CI succeeds.
"""
import argparse,csv,os
from pathlib import Path
import numpy as np
import cocoex
from scipy.optimize import minimize
import cma

def optimize(problem,method,seed,budget):
 d=problem.dimension
 rng=np.random.default_rng(seed)
 x0=np.zeros(d)
 count=0;best=float('inf')
 def objective(x):
  nonlocal count,best
  if count>=budget:raise RuntimeError('budget reached')
  count+=1;v=float(problem(np.asarray(x,dtype=float)))
  best=min(best,v)
  return v
 try:
  if method=='COBYQA':
   minimize(objective,x0,method='COBYQA',options={'maxfev':budget,'maxiter':budget})
  elif method=='Embed8':
   A,_=np.linalg.qr(rng.normal(size=(d,min(8,d))))
   minimize(lambda z:objective(x0+A@z),np.zeros(A.shape[1]),method='COBYQA',options={'maxfev':budget,'maxiter':budget})
  elif method=='Restart8':
   for cap in (budget//2,budget-budget//2):
    A,_=np.linalg.qr(rng.normal(size=(d,min(8,d))))
    start=x0.copy();used=0;local_best=float('inf')
    def reduced(z):
     nonlocal used,local_best,start
     if used>=cap:raise RuntimeError('stage cap')
     x=start+A@z
     v=objective(x);used+=1
     if v<local_best:local_best=v
     return v
    minimize(reduced,np.zeros(A.shape[1]),method='COBYQA',options={'maxfev':cap,'maxiter':cap})
  elif method=='CMAES':
   es=cma.CMAEvolutionStrategy(x0,2.0,{'seed':seed,'verbose':-9,'popsize':4+int(3*np.log(d))})
   while count<budget:
    candidates=es.ask();vals=[]
    for x in candidates:
     if count>=budget:break
     vals.append(objective(x))
    if len(vals)==len(candidates):es.tell(candidates,vals)
    else:break
 except RuntimeError as e:
  if str(e) not in ('budget reached','stage cap'):raise
 return count,best

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--dimensions',default='2,5,10,20')
 ap.add_argument('--instances',default='1-5')
 ap.add_argument('--budget-factor',type=int,default=100)
 ap.add_argument('--output',default='results/coco_pilot.csv')
 a=ap.parse_args()
 dims=[int(x) for x in a.dimensions.split(',')]
 suite=cocoex.Suite('bbob',f'instances: {a.instances}',f'dimensions: {",".join(map(str,dims))}')
 output=Path(a.output);output.parent.mkdir(parents=True,exist_ok=True)
 rows=[]
 for problem in suite:
  for method in ('COBYQA','Embed8','Restart8','CMAES'):
   # Each algorithm receives its own fresh COCO problem instance for logging isolation
   p=cocoex.Suite('bbob',f'instances: {a.instances}',f'dimensions: {",".join(map(str,dims))}').get_problem(problem.id)
   calls,best=optimize(p,method,1001,a.budget_factor*p.dimension)
   rows.append({'problem_id':problem.id,'dimension':p.dimension,'method':method,'calls':calls,'best':best})
 with output.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print('rows',len(rows))
if __name__=='__main__':main()
