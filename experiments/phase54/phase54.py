"""Phase54 paired Gaussian diagnostics on PSD quadratic models; synthetic, not COCO."""
import numpy as np,csv
from pathlib import Path
p=Path(__file__).parent;rows=[]
for rank in (2,4,8,20):
 for gn in (0.,1.,5.):
  for rep in range(100):
   rng=np.random.default_rng(540000+rank*1000+int(gn)*100+rep)
   Q,_=np.linalg.qr(rng.normal(size=(20,rank)))
   g=rng.normal(size=20);g*=gn/max(np.linalg.norm(g),1e-100)
   z=rng.normal(size=(32,20));curv=np.sum((z@Q)**2,axis=1);lin=z@g
   plus=curv/2+lin;minus=curv/2-lin
   central=plus+minus;one=2*plus;antisym=plus-minus
   rc=2*np.mean(central)**2/np.var(central,ddof=1)
   ro=2*np.mean(one)**2/np.var(one,ddof=1)
   rows.append(dict(rank=rank,gradient_norm=gn,rep=rep,central_rank=rc,one_sided_rank=ro,gradient_norm_squared_est=np.mean(antisym**2)/4,central_rel_error=abs(rc-rank)/rank,one_rel_error=abs(ro-rank)/rank,calls=65))
with (p/'raw_results.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=[]
for rank in (2,4,8,20):
 for gn in (0.,1.,5.):
  rr=[x for x in rows if x['rank']==rank and x['gradient_norm']==gn]
  summary.append(dict(rank=rank,gradient_norm=gn,n=len(rr),median_central_rel_error=float(np.median([x['central_rel_error'] for x in rr])),median_one_rel_error=float(np.median([x['one_rel_error'] for x in rr])),mean_gradient_norm_squared_est=float(np.mean([x['gradient_norm_squared_est'] for x in rr])),true_gradient_norm_squared=gn*gn))
with (p/'summary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
print('1200 paired trials complete')
