"""Phase53: one-sided versus central Gaussian curvature probes (synthetic PSD quadratics)."""
import numpy as np,csv,hashlib,platform,json
from pathlib import Path
p=Path(__file__).parent
rows=[]
for rank in [2,4,8,20]:
 for n in [8,16,32,64]:
  for rep in range(100):
   rng=np.random.default_rng(530000+rank*10000+n*100+rep)
   Q,_=np.linalg.qr(rng.normal(size=(20,rank)))
   z=rng.normal(size=(n,20)); curvature=np.sum((z@Q)**2,axis=1)
   for gradient in [0.,1.,5.]:
    g=rng.normal(size=20);g*=gradient/(np.linalg.norm(g)+1e-30)
    for method in ['one_sided','central']:
     y=curvature+(2*z@g if method=='one_sided' else 0)
     est=2*y.mean()**2/y.var(ddof=1)
     rows.append(dict(rank=rank,n=n,rep=rep,gradient_norm=gradient,method=method,calls=(n+1 if method=='one_sided' else 2*n+1),estimate=est,relative_error=abs(est-rank)/rank))
with (p/'raw_results.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=[]
for r in [2,4,8,20]:
 for n in [8,16,32,64]:
  for gradient in [0.,1.,5.]:
   for method in ['one_sided','central']:
    subset=[a for a in rows if a['rank']==r and a['n']==n and a['gradient_norm']==gradient and a['method']==method]
    summary.append(dict(rank=r,n=n,gradient_norm=gradient,method=method,calls=subset[0]['calls'],median_relative_error=float(np.median([a['relative_error'] for a in subset])),mean_relative_error=float(np.mean([a['relative_error'] for a in subset]))))
with (p/'summary.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
(p/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,rows=len(rows),seed_formula='530000+rank*10000+n*100+rep'),indent=2)+'\n')
for r in [2,4,8,20]:
 for gradient in [0.,1.,5.]:
  ss=[a for a in summary if a['rank']==r and a['n']==32 and a['gradient_norm']==gradient]
  print(r,gradient,[(a['method'],round(a['median_relative_error'],3),a['calls']) for a in ss])
for name in ['phase53.py','raw_results.csv','summary.csv','environment.json']:
 print('SHA256',name,hashlib.sha256((p/name).read_bytes()).hexdigest())
