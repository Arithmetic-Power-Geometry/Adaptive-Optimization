"""Phase50: cost-matched anytime audit of existing Phase49 raw traces.
No new optimizer is introduced. Recompute all matched comparisons from archived traces.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import argparse
parser=argparse.ArgumentParser()
parser.add_argument("--raw",required=True,help="Path to Phase49 raw_results.csv")
parser.add_argument("--traces",required=True,help="Path to Phase49 traces.csv")
args=parser.parse_args()
raw=pd.read_csv(args.raw)
traces=pd.read_csv(args.traces)
rows=[]
for (fun,instance), group in raw.groupby(["function","instance"]):
    base=group.loc[group.method=="COBYQA"].iloc[0]
    b=traces[(traces.problem==base.problem)&(traces.method=="COBYQA")].sort_values("call").best.to_numpy()
    for _,rec in group.iterrows():
        v=traces[(traces.problem==rec.problem)&(traces.method==rec.method)].sort_values("call").best.to_numpy()
        assert len(v)==rec.calls and len(v)<=rec.budget
        for cap in (40,80,120):
            x=v[min(cap,len(v))-1];y=b[min(cap,len(b))-1];delta=x-y
            rows.append(dict(function=fun,instance=instance,method=rec.method,cap=cap,value=x,baseline=y,delta=delta,win=int(delta< -1e-8),loss=int(delta>1e-8),tie=int(abs(delta)<=1e-8)))
out=pd.DataFrame(rows)
summary=out.groupby(["function","cap","method"],as_index=False).agg(n=("win","size"),wins=("win","sum"),losses=("loss","sum"),ties=("tie","sum"),median_objective=("value","median"))
out.to_csv("results/phase50_anytime_matched.csv",index=False)
summary.to_csv("results/phase50_anytime_summary.csv",index=False)
print(summary.to_string(index=False))
print(raw.groupby(["function","method"]).calls.mean())
