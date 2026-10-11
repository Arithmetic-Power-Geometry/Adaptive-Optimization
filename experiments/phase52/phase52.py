"""Phase52 Gaussian curvature-rank probe study; synthetic PSD quadratic matrices."""
import numpy as np,csv,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;d=20;reps=100;ns=(16,32,64,128,256);ranks=(2,4,8,20)
rows=[]
for rank in ranks:
 for rep in range(reps):
  rng=np.random.default_rng(520000+rank*1000+rep)
  Q,_=np.linalg.qr(rng.normal(size=(d,rank)))
  H=Q@Q.T
  for n in ns:
   z=rng.normal(size=(n,d));y=np.sum((z@Q)**2,axis=1)
   est=2*y.mean()**2/y.var(ddof=1)
   rows.append(dict(rank=rank,rep=rep,n=n,estimated_rank=est,absolute_error=abs(est-rank),relative_error=abs(est-rank)/rank,calls=2*n+1))
with (P/'raw_results.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summ=[]
for r in ranks:
 for n in ns:
  rr=[x for x in rows if x['rank']==r and x['n']==n]
  summ.append(dict(rank=r,n=n,calls=2*n+1,median_relative_error=float(np.median([x['relative_error'] for x in rr])),p90_relative_error=float(np.quantile([x['relative_error'] for x in rr],.9)),within_25pct=sum(x['relative_error']<=.25 for x in rr)/reps))
with (P/'summary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(summ[0]));w.writeheader();w.writerows(summ)
print(*summ,sep='\n')
for name in ('phase52.py','raw_results.csv','summary.csv'):
 print(name,hashlib.sha256((P/name).read_bytes()).hexdigest())
