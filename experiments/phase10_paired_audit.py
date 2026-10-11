import csv, numpy as np
from pathlib import Path
p=Path(__file__).resolve().parent
rows=list(csv.DictReader((p/'phase9_raw_results.csv').open()))
by={}
for r in rows:
 k=(int(r['dimension']),r['function'],int(r['rotated']),int(r['seed']))
 by.setdefault(k,{})[r['method']]=r
assert len(by)==240 and len(rows)==960
rng=np.random.default_rng(10102026);out=[]
for budget in (40,80,120,180,240):
 for other in ('Memory','Powell','DE'):
  def hit(r):return bool(r['hit']) and int(r['hit'])<=budget
  a=np.array([hit(v['Adaptive']) for v in by.values()],dtype=int)
  b=np.array([hit(v[other]) for v in by.values()],dtype=int)
  d=b-a
  bs=d[rng.integers(0,len(d),size=(5000,len(d)))].mean(axis=1)
  lo,hi=np.quantile(bs,[.025,.975])
  out.append(dict(budget=budget,method=other,adaptive_hits=int(a.sum()),method_hits=int(b.sum()),difference_hits=int(d.sum()),difference_pp=float(100*d.mean()),bootstrap_low_pp=float(100*lo),bootstrap_high_pp=float(100*hi),method_only=int(((b==1)&(a==0)).sum()),adaptive_only=int(((a==1)&(b==0)).sum())))
with (p/'phase10_paired.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
