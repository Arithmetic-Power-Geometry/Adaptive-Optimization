"""Official COCO BBOB pilot: golden/rational/random polling versus COBYQA.
Run in GitHub Actions with coco-experiment; results are NOT claimed until CI succeeds.
"""
import csv, os, numpy as np
from pathlib import Path
from scipy.optimize import minimize
import cocoex

OUT=Path(__file__).resolve().parent
BUDGET_MULTIPLIER=40
METHODS=("Golden","Rational","RandomAngle","COBYQA")
class Exhausted(Exception): pass
class Meter:
 def __init__(self,fun,budget):self.fun=fun;self.budget=budget;self.n=0;self.best=float("inf")
 def __call__(self,x):
  if self.n>=self.budget:raise Exhausted()
  self.n+=1;y=float(self.fun(np.asarray(x,dtype=float)));self.best=min(self.best,y);return y

def optimize(m,x0,method,seed):
 if method=="COBYQA":
  try:minimize(m,x0,method="COBYQA",options={"maxfev":m.budget,"maxiter":m.budget})
  except Exhausted:pass
  return
 d=len(x0);rng=np.random.default_rng(seed+50000)
 planes=[tuple(rng.choice(d,2,replace=False)) for _ in range(m.budget)]
 angles=np.random.default_rng(seed+72000).uniform(0,2*np.pi,m.budget)
 x=x0.copy();fx=m(x);h=.7;theta=0.;i=0
 while m.n<m.budget and h>1e-7:
  a,b=planes[i];i+=1
  if method=="Golden":theta=(theta+2*np.pi*((np.sqrt(5)-1)/2))%(2*np.pi)
  elif method=="Rational":theta=(theta+2*np.pi*3/8)%(2*np.pi)
  else:theta=angles[i-1]
  v=np.zeros(d);v[a]=np.cos(theta);v[b]=np.sin(theta)
  improved=False
  for direction in (v,-v):
   if m.n>=m.budget:break
   y=x+h*direction;fy=m(y)
   if fy<fx:x=y;fx=fy;improved=True;break
  h=min(h*1.08,1.5) if improved else h*.7

def main():
 suite=cocoex.Suite("bbob","","dimensions: 2,5,10 instance_indices: 1-3")
 rows=[]
 for p in suite:
  x0=np.array(p.initial_solution,dtype=float);d=len(x0)
  for method in METHODS:
   # Suite function and instance identity determine seed, not method.
   seed=int(p.id_function)*1000+int(p.id_instance)*10+d
   m=Meter(p,BUDGET_MULTIPLIER*d)
   optimize(m,x0,method,seed)
   rows.append(dict(problem=p.id,function=p.id_function,instance=p.id_instance,dimension=d,method=method,budget=m.budget,evaluations=m.n,best=m.best))
   print(p.id,method,m.n,m.best,flush=True)
 with (OUT/"coco_raw.csv").open("w",newline="") as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print("TOTAL",len(rows))

if __name__=="__main__":main()
