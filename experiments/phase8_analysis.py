"""Phase 8 paired analysis. Run after phase7_heldout_targets.py in same directory."""
import csv, numpy as np
from pathlib import Path
p=Path(__file__).parent
rows=list(csv.DictReader((p/'phase7_raw_results.csv').open()))
group={}
for r in rows:
 key=(r['dimension'],r['function'],r['rotated'],r['seed'])
 group.setdefault(key,{})[r['method']]=r
assert len(group)==320 and len(rows)==960
keys=list(group);rng=np.random.default_rng(20261011)
def hit(r,b):return bool(r['hit_evaluations']) and int(r['hit_evaluations'])<=b
curves=[];paired=[]
for budget in (40,80,120,180,240):
 for method in ('Adaptive','Memory','GatedMemory'):
  x=[group[k][method] for k in keys];hits=[int(r['hit_evaluations']) for r in x if hit(r,budget)]
  curves.append(dict(budget=budget,method=method,successes=len(hits),trials=len(x),rate=len(hits)/len(x),median_hit_given_success=np.median(hits) if hits else ''))
 for challenger in ('Memory','GatedMemory'):
  a=np.array([hit(group[k]['Adaptive'],budget) for k in keys],dtype=int)
  b=np.array([hit(group[k][challenger],budget) for k in keys],dtype=int)
  delta=b-a;idx=rng.integers(0,len(delta),(5000,len(delta)))
  low,high=np.quantile(delta[idx].mean(axis=1),[.025,.975])
  paired.append(dict(budget=budget,comparison=challenger+' minus Adaptive',difference_hits=int(delta.sum()),difference_rate=float(delta.mean()),ci95_low=float(low),ci95_high=float(high),challenger_only=int(((b==1)&(a==0)).sum()),adaptive_only=int(((b==0)&(a==1)).sum())))
def write(name,values):
 with (p/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(values[0]));w.writeheader();w.writerows(values)
write('phase8_budget_curves.csv',curves);write('phase8_paired.csv',paired)
print('Phase8 completed',len(rows),'existing runs,',len(group),'paired instances')
