import numpy as np, csv, hashlib, json
from scipy.optimize import minimize
from pathlib import Path
P=Path(__file__).parent; B=180
class Budget(Exception): pass
class Meter:
 def __init__(self,f):self.f=f;self.n=0;self.best=np.inf
 def __call__(self,x):
  if self.n>=B:raise Budget()
  self.n+=1;y=float(self.f(np.asarray(x)));self.best=min(self.best,y);return y

def problem(name,d,seed):
 rng=np.random.default_rng(seed*17+d*100);Q,_=np.linalg.qr(rng.normal(size=(d,d)));shift=rng.uniform(-2,2,d)
 def f(x):
  z=Q@(x-shift)
  if name=='rastrigin':return 10*d+np.sum(z*z-10*np.cos(2*np.pi*z))
  if name=='ackley':return -20*np.exp(-.2*np.sqrt(np.mean(z*z)))-np.exp(np.mean(np.cos(2*np.pi*z)))+20+np.e
  if name=='griewank':return 1+np.sum(z*z)/4000-np.prod(np.cos(z/np.sqrt(np.arange(1,d+1))))
  return np.sum(100*(z[1:]-z[:-1]**2)**2+(1-z[:-1])**2)
 return f,rng.uniform(-3,3,d)

def apg(m,x0,seed):
 # APG: arithmetic-power directional memory: weights proportional to
 # (gain/evaluation-distance)^p, p=2, with regularized mixture and poll safeguard.
 rng=np.random.default_rng(seed+9000);x=x0.copy();fx=m(x);h=.8;memory=[];p=2
 try:
  while m.n<B:
   dirs=[]
   if memory:
    gains=np.array([a[1] for a in memory]);weights=(gains+1e-9)**p;weights/=weights.sum()
    idx=rng.choice(len(memory),p=weights);v=memory[idx][0];dirs.extend([v,-v])
   j=rng.permutation(len(x))
   for k in j:
    e=np.zeros(len(x));e[k]=1;dirs.extend([e,-e])
   improved=False
   for v in dirs:
    if m.n>=B:break
    y=x+h*v;fy=m(y)
    if fy<fx:
     gain=fx-fy;x=y;fx=fy;memory.append((v.copy(),gain));memory=memory[-12:];improved=True;break
   if not improved:h*=.5
   else:h=min(h*1.12,1.5)
   if h<1e-7:break
 except Budget:pass

def run(f,x0,method,seed):
 m=Meter(f)
 try:
  if method=='APGPowerPoll':apg(m,x0,seed)
  elif method=='COBYQA':minimize(m,x0,method='COBYQA',options={'maxfev':B,'maxiter':B})
  elif method=='Powell':minimize(m,x0,method='Powell',options={'maxfev':B})
  else:minimize(m,x0,method='Nelder-Mead',options={'maxfev':B,'maxiter':B})
 except Budget:pass
 return m
rows=[]
for name in ['ackley','rastrigin','griewank','rosenbrock']:
 for d in [2,5,10]:
  for seed in range(900,910):
   f,x0=problem(name,d,seed)
   for method in ['APGPowerPoll','COBYQA','Powell','Nelder-Mead']:
    m=run(f,x0,method,seed)
    rows.append(dict(function=name,dimension=d,seed=seed,method=method,evaluations=m.n,best=m.best))
with (P/'raw_results.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
s=[]
for name in ['ackley','rastrigin','griewank','rosenbrock']:
 for d in [2,5,10]:
  g=[r for r in rows if r['function']==name and r['dimension']==d];base={r['seed']:r['best'] for r in g if r['method']=='COBYQA'}
  for method in ['APGPowerPoll','COBYQA','Powell','Nelder-Mead']:
   v=[r for r in g if r['method']==method];s.append(dict(function=name,dimension=d,method=method,median_best=float(np.median([r['best'] for r in v])),wins_vs_COBYQA=sum(r['best']<base[r['seed']]-1e-10 for r in v),runs=len(v)))
with (P/'summary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(s[0]));w.writeheader();w.writerows(s)
(P/'environment.json').write_text(json.dumps({'numpy':np.__version__,'scipy':__import__('scipy').__version__,'budget':B,'seeds':[900,909],'APG_power':2},indent=2))
print('RUNS',len(rows))
for method in ['APGPowerPoll','Powell','Nelder-Mead']:
 print(method,'wins',sum(r['wins_vs_COBYQA'] for r in s if r['method']==method),'of 120')
for name in ['ackley','rastrigin','griewank','rosenbrock']:
 print(name,[(r['dimension'],r['method'],round(r['median_best'],5)) for r in s if r['function']==name and r['method'] in ['APGPowerPoll','COBYQA']])
for f in ['phase19.py','raw_results.csv','summary.csv','environment.json']:
 print('SHA256',f,hashlib.sha256((P/f).read_bytes()).hexdigest())
