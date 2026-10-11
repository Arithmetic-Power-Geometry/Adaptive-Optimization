"""Exploratory objective-evaluation comparison; CGCP has no novelty or globality claim."""
import csv, json, platform
from pathlib import Path
import numpy as np
from scipy.optimize import differential_evolution, direct

OUT=Path(__file__).resolve().parent
SEEDS=range(5)
DIMS=(2,5)
BUDGET=400

def functions(d):
    return {
        "sphere":(lambda x:float(np.sum(np.asarray(x)**2)),-5.,5.,0.),
        "rastrigin":(lambda x:float(10*d+np.sum(np.asarray(x)**2-10*np.cos(2*np.pi*np.asarray(x)))),-5.12,5.12,0.),
        "rosenbrock":(lambda x:float(np.sum(100*(np.asarray(x)[1:]-np.asarray(x)[:-1]**2)**2+(1-np.asarray(x)[:-1])**2)),-3.,3.,0.),
        "ackley":(lambda x:float(-20*np.exp(-.2*np.sqrt(np.mean(np.asarray(x)**2)))-np.exp(np.mean(np.cos(2*np.pi*np.asarray(x))))+20+np.e),-5.,5.,0.)
    }

class Meter:
    def __init__(self,fun,budget):
        self.fun,self.budget,self.n,self.best=fun,budget,0,float("inf")
    def __call__(self,x):
        if self.n>=self.budget: raise RuntimeError("budget exhausted")
        value=float(self.fun(np.asarray(x)))
        self.n+=1
        self.best=min(self.best,value)
        return value

def candidate(m,low,high,d,seed):
    rng=np.random.default_rng(seed)
    x=rng.uniform(low,high,d); fx=m(x)
    steps=np.full(d,(high-low)/4)
    while m.n<m.budget:
        improved=False
        for j in rng.permutation(d):
            for sign in (1.,-1.):
                if m.n>=m.budget: break
                y=x.copy()
                y[j]=np.clip(y[j]+sign*steps[j],low,high)
                if y[j]==x[j]: continue
                fy=m(y)
                if fy<fx:
                    x,fx=y,fy
                    steps[j]=min(steps[j]*1.15,high-low)
                    improved=True
                    break
            if m.n>=m.budget: break
        if not improved:
            steps*=.5
            if np.max(steps)<1e-6 and m.n<m.budget:
                x=rng.uniform(low,high,d)
                fx=m(x)
                steps[:]=(high-low)/4

def run_one(method,fun,low,high,d,seed):
    # DIRECT's maxfun is not an exact cap; track and publish the real count.
    m=Meter(fun,100000 if method=="DIRECT" else BUDGET)
    bounds=[(low,high)]*d
    if method=="CGCP": candidate(m,low,high,d,seed)
    elif method=="Random":
        rng=np.random.default_rng(seed)
        for _ in range(BUDGET): m(rng.uniform(low,high,d))
    elif method=="DE":
        population=max(5*d,10)
        iterations=max(0,BUDGET//population-1)
        differential_evolution(m,bounds,seed=seed,popsize=5,maxiter=iterations,
                               polish=False,tol=0,atol=0,updating="immediate")
    elif method=="DIRECT":
        direct(m,bounds,maxfun=BUDGET,maxiter=BUDGET,locally_biased=False)
    return {"method":method,"best":m.best,"evaluations":m.n}

def main():
    rows=[]
    for d in DIMS:
        for name,(fun,lo,hi,opt) in functions(d).items():
            for seed in SEEDS:
                for method in ("CGCP","Random","DE","DIRECT"):
                    r=run_one(method,fun,lo,hi,d,seed)
                    r.update({"dimension":d,"function":name,"seed":seed,
                              "known_optimum":opt,"error":max(0,r["best"]-opt)})
                    rows.append(r)
    with open(OUT/"raw_results.csv","w",newline="") as f:
        keys=["dimension","function","seed","method","evaluations","best","known_optimum","error"]
        writer=csv.DictWriter(f,fieldnames=keys);writer.writeheader();writer.writerows(rows)
    summary=[]
    for d in DIMS:
        for name in functions(d):
            for method in ("CGCP","Random","DE","DIRECT"):
                subset=[r for r in rows if r["dimension"]==d and r["function"]==name and r["method"]==method]
                summary.append({"dimension":d,"function":name,"method":method,
                                "median_error":float(np.median([r["error"] for r in subset])),
                                "mean_evaluations":float(np.mean([r["evaluations"] for r in subset])),
                                "successes_error_le_1e-3":sum(r["error"]<=1e-3 for r in subset),
                                "trials":len(subset)})
    with open(OUT/"summary.csv","w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(summary[0]));writer.writeheader();writer.writerows(summary)
    (OUT/"environment.json").write_text(json.dumps({
        "python":platform.python_version(),"numpy":np.__version__,
        "scipy":__import__("scipy").__version__,"seeds":list(SEEDS),
        "dimensions":list(DIMS),"evaluation_budget":BUDGET,
        "methods":["CGCP","Random","DE","DIRECT"]},indent=2)+"\n")
    for row in summary: print(row)
if __name__=="__main__":main()
