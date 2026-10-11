"""Strict 300-evaluation exploratory benchmark. Not a claim of algorithmic novelty."""
import csv
from pathlib import Path
import numpy as np
from scipy.optimize import direct, differential_evolution
BUDGET=300
class StopBudget(Exception): pass
class Meter:
    def __init__(self, fun):
        self.fun=fun; self.n=0; self.best=float("inf"); self.trace=[]
    def __call__(self,x):
        if self.n>=BUDGET: raise StopBudget()
        v=float(self.fun(np.asarray(x)))
        self.n+=1; self.best=min(self.best,v)
        if self.n in (30,100,200,300): self.trace.append((self.n,self.best))
        return v
def problem(name,d):
    if name=="sphere": return lambda x:np.sum(x*x),(-5.,5.)
    if name=="rastrigin": return lambda x:10*d+np.sum(x*x-10*np.cos(2*np.pi*x)),(-5.12,5.12)
    if name=="ackley": return lambda x:-20*np.exp(-.2*np.sqrt(np.mean(x*x)))-np.exp(np.mean(np.cos(2*np.pi*x)))+20+np.e,(-5.,5.)
    if name=="rosenbrock": return lambda x:np.sum(100*(x[1:]-x[:-1]**2)**2+(1-x[:-1])**2),(-3.,3.)
def poll(m,lo,hi,d,seed,adaptive):
    rng=np.random.default_rng(seed)
    x=rng.uniform(lo,hi,d); fx=m(x); step=np.full(d,(hi-lo)/4)
    while m.n<BUDGET:
        improved=False
        for j in rng.permutation(d):
            for sign in rng.permutation([-1.,1.]):
                if m.n>=BUDGET: break
                y=x.copy(); y[j]=np.clip(y[j]+sign*step[j],lo,hi)
                if y[j]==x[j]: continue
                fy=m(y)
                if fy<fx:
                    x,fx=y,fy; improved=True
                    if adaptive: step[j]=min(step[j]*1.15,hi-lo)
                    break
            if m.n>=BUDGET: break
        if not improved:
            step*=.5
            if np.max(step)<1e-6 and m.n<BUDGET:
                x=rng.uniform(lo,hi,d); fx=m(x); step[:]=(hi-lo)/4
def run(method,m,lo,hi,d,seed):
    rng=np.random.default_rng(seed)
    try:
        if method=="AdaptivePoll": poll(m,lo,hi,d,seed,True)
        elif method=="FixedPoll": poll(m,lo,hi,d,seed,False)
        elif method=="Random":
            while True: m(rng.uniform(lo,hi,d))
        elif method=="DE":
            differential_evolution(m,[(lo,hi)]*d,rng=rng,popsize=5,maxiter=1000,polish=False,tol=0,atol=0)
        elif method=="DIRECT":
            direct(m,[(lo,hi)]*d,maxfun=BUDGET,maxiter=BUDGET,locally_biased=False)
    except (StopBudget,SystemError):
        # SciPy 1.17 DIRECT compiled wrapper converts an objective exception
        # to SystemError. All successful evaluations remain recorded by Meter.
        pass
    return m.n,m.best
def write(path,rows):
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
    rows=[]; traces=[]
    for d in (2,5,10):
        for name in ("sphere","rastrigin","ackley","rosenbrock"):
            f,(lo,hi)=problem(name,d)
            for seed in range(5):
                for method in ("AdaptivePoll","FixedPoll","Random","DE","DIRECT"):
                    m=Meter(f); n,best=run(method,m,lo,hi,d,seed)
                    rows.append(dict(dimension=d,function=name,seed=seed,method=method,evaluations=n,error=max(0,best)))
                    for step,val in m.trace:
                        traces.append(dict(dimension=d,function=name,seed=seed,method=method,evaluations=step,error=max(0,val)))
    root=Path(__file__).resolve().parent
    write(root/"raw_results.csv",rows);write(root/"trajectories.csv",traces)
    summary=[]
    for d in (2,5,10):
        for name in ("sphere","rastrigin","ackley","rosenbrock"):
            for method in ("AdaptivePoll","FixedPoll","Random","DE","DIRECT"):
                group=[r for r in rows if (r["dimension"],r["function"],r["method"])==(d,name,method)]
                summary.append(dict(dimension=d,function=name,method=method,
                    median_error=float(np.median([r["error"] for r in group])),
                    successes=sum(r["error"]<=1e-3 for r in group),trials=len(group),
                    max_evaluations=max(r["evaluations"] for r in group)))
    write(root/"summary.csv",summary)
    for r in summary: print(r)
if __name__=="__main__":main()
