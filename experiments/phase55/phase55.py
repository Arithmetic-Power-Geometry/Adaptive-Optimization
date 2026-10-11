"""Phase55 finite-step nonlinear bias audit, 2700 synthetic trials."""
import numpy as np,csv,hashlib
from pathlib import Path
p=Path(__file__).parent
rows=[]
for d in [5,10,20,40,80]:
 for rank in [2,min(4,d),d]:
  for lam in [0.,.1,1.]:
   for h in [.1,.5,1.]:
    for rep in range(20):
     rng=np.random.default_rng(550000+d*10000+rank*1000+int(lam*10)*100+int(h*10)*20+rep)
     q,_=np.linalg.qr(rng.normal(size=(d,rank)))
     z=rng.normal(size=(64,d));base=np.sum((z@q)**2,axis=1)
     signal=base+lam*h*h/12*np.sum(z**4,axis=1)
     estimated=2*signal.mean()**2/signal.var(ddof=1)
     expected_mean_bias=lam*h*h*d/4
     rows.append(dict(d=d,rank=rank,lam=lam,h=h,rep=rep,estimate=estimated,relative_error=abs(estimated-rank)/rank,mean_signal=signal.mean(),mean_curvature=base.mean(),sample_bias=(signal-base).mean(),predicted_bias=expected_mean_bias,calls=129))
with open(p/'raw_results.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
summary=[]
for d in [5,10,20,40,80]:
 for rank in sorted(set([2,min(4,d),d])):
  for lam in [0.,.1,1.]:
   for h in [.1,.5,1.]:
    x=[r for r in rows if (r['d'],r['rank'],r['lam'],r['h'])==(d,rank,lam,h)]
    summary.append(dict(d=d,rank=rank,lam=lam,h=h,n=len(x),median_relative_error=float(np.median([r['relative_error'] for r in x])),mean_observed_bias=float(np.mean([r['sample_bias'] for r in x])),theoretical_bias=x[0]['predicted_bias']))
with open(p/'summary.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=summary[0]);w.writeheader();w.writerows(summary)
for d in [5,10,20,40,80]:
 x=[r for r in summary if r['d']==d and r['rank']==2 and r['lam']==1 and r['h']==1][0]
 print('d',d,'rank2 lam1 h1',x)
for name in ['phase55.py','raw_results.csv','summary.csv']:
 print('SHA256',name,hashlib.sha256((p/name).read_bytes()).hexdigest())
