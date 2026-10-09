"""Independent small checks for the newly explained exam examples; no course experiments."""
from pathlib import Path
import sys
sys.dont_write_bytecode = True
import argparse,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check',action='store_true',help='Run calculations without writing any files')
args=parser.parse_args()
checks=[]
def check(name,actual,expected,atol=1e-7):
    assert np.allclose(actual,expected,atol=atol,rtol=1e-6),(name,actual,expected)
    checks.append({'name':name,'actual':np.asarray(actual).tolist(),'expected':np.asarray(expected).tolist()})
check('MT009 Gram entries',2000**2,4_000_000)
check('MT022 full Gram entries',50000**2,2_500_000_000)
check('MT031 RBF example',[math.exp(-.01),math.exp(-1)],[.9900498337,.3678794412])
check('MT050 asymmetric losses',[4*(-1)**2,1**2,4*(-2)**2,2**2],[4,1,16,4])
x=np.array([-1.,1.]);labels=np.array([-1.,1.]);scores=.1*x+.5;signed=labels*scores
check('MT051 signed scores',signed,[-.4,.6]);check('MT051 both bad losses zero',np.maximum(0,-1-signed),[0,0])
K=np.array([[1.,1.],[1.,0.]]);v=np.array([1.,-2.])
check('MT055 indicator kernel negative quadratic form',v@K@v,-3)
check('MT055 sine negative diagonal',math.sin(3*math.pi/2),-1)
det=math.tanh(1)*math.tanh(4)-math.tanh(2)**2
check('MT055 tanh negative determinant',det,-.16826582059019524)
check('MT061 linear prediction storage',1000+1,1001)
check('MT062 RF variance',[.2+.8/5,.2+.8/20],[.36,.24])
def huber(r):return .5*r*r if abs(r)<1 else abs(r)-.5
check('MT063 Huber points',[huber(v) for v in [0,-1,1,-2,2]],[0,.5,.5,1.5,1.5])
for a in [-1.,1.]:
    h=1e-6
    check('MT063 smooth join '+str(a),(huber(a+h)-huber(a-h))/(2*h),a,atol=1e-6)
z=-4.
slopes=[math.exp(-z),1/(1+math.exp(z))/math.log(2),1.]
assert slopes[0]>slopes[1]>slopes[2]
checks.append({'name':'MT065 original-plot scaled negative-tail slope order','actual':slopes,'order':['AdaBoost','LR scaled to source','SVM']})
check('MT066 four factors',.2**4,.0016)
def scalar(x):
    u=np.cbrt(3*x*x)+math.tan(5*x)
    return 1/(1+math.exp(u))
def deriv(x):
    u=np.cbrt(3*x*x)+math.tan(5*x)
    return -math.exp(u)/(1+math.exp(u))**2*(2*x/(3*x*x)**(2/3)+5/(math.cos(5*x)**2))
for x in [-.2,.15,.4]:
    h=1e-6
    check('MT067 scalar derivative '+str(x),deriv(x),(scalar(x+h)-scalar(x-h))/(2*h),atol=1e-6)
rng=np.random.default_rng(42)
x=rng.normal(size=2);A=rng.normal(size=(2,2));W=rng.normal(size=(2,3));y=rng.normal(size=3)
def loss(a,w):
    f=w.T@np.tanh(a.T@x);return .5*np.sum((f-y)**2)
g1=A.T@x;hidden=np.tanh(g1);d2=W.T@hidden-y;d1=(W@d2)*(1-hidden**2)
for name,mat,grad in [('A',A,np.outer(x,d1)),('W',W,np.outer(hidden,d2))]:
    numerical=np.empty_like(mat)
    for idx in np.ndindex(mat.shape):
        h=1e-6;p=mat.copy();m=mat.copy();p[idx]+=h;m[idx]-=h
        numerical[idx]=(loss(p,W)-loss(m,W))/(2*h) if name=='A' else (loss(A,p)-loss(A,m))/(2*h)
    check('MT067 full two-layer '+name+' gradient',grad,numerical,atol=1e-6)
check('MT067 scalar network example gradients',[-2.,0.],[-2.,0.])
check('MT005 Bernoulli label variances',[.5*(1-.5),.9*(1-.9)],[.25,.09])
check('MT022 full double Gram GB',50000**2*8/1e9,20.)
check('MT036 full double covariance entries and GB',[10597**2,10597**2*8/1e9],[112296409,.898371272])
check('MT040 normalized posterior',np.array([.4*.1,.2*.9])/(.4*.1+.2*.9),[2/11,9/11])
pt=np.array([.8,.8]);means=np.array([[0.,0.],[1.,1.]])
dists=np.sum((pt-means)**2,axis=1)
densities=np.exp(-dists/2)/(2*np.pi)*.5
check('MT046 squared distances',dists,[1.28,.08])
check('MT046 density posterior vs sigmoid',densities[1]/densities.sum(),1/(1+math.exp(-.6)))
check('MT047 signed-score logistic losses',np.logaddexp(0,[-2.,2.]),[.126928011,2.126928011])
check('MT061 100 and 500 support-vector storage',[1001*100+1,1001*500+1],[100101,500501])
check('MT063 large-residual loss and slope',[.5*10**2,huber(10.),10.,(huber(10.00001)-huber(9.99999))/.00002],[50,9.5,10,1])
check('MT023 screening rates',[45/50,855/950,(45+855)/1000],[.9,.9,.9])
# Independent evaluation: compare Gaussian log densities against the expanded linear log-odds.
mu0=np.array([-1.,.3]);mu1=np.array([2.,-.4]);var=np.array([.8,1.4]);priors=np.array([.4,.6])
for point in [np.array([0.,0.]),np.array([1.2,-2.]),np.array([-.7,.8])]:
    logpdf=lambda mu:-.5*np.sum(np.log(2*np.pi*var)+(point-mu)**2/var)
    full=math.log(priors[1])+logpdf(mu1)-math.log(priors[0])-logpdf(mu0)
    linear=np.sum((mu1-mu0)/var*point+(mu0**2-mu1**2)/(2*var))+math.log(priors[1]/priors[0])
    check('MT059 shared-variance cancellation '+str(point.tolist()),linear,full)
grid=np.linspace(-5,5,100001)
for strength in [.5,2.,4.]:
    ridge_grid=grid[np.argmin(.5*(grid-3)**2+strength*grid**2)]
    lasso_grid=grid[np.argmin(.5*(grid-3)**2+strength*np.abs(grid))]
    check('MT019 ridge grid minimum '+str(strength),ridge_grid,3/(1+2*strength),atol=.00006)
    check('MT019 lasso grid minimum '+str(strength),lasso_grid,max(3-strength,0),atol=.00006)
u,v,t=math.tanh(1),math.tanh(2),math.tanh(4)
avec=np.array([-v/u,1.]);tanhK=np.array([[u,v],[v,t]])
assert avec@tanhK@avec<0
checks.append({'name':'MT055 direct tanh PSD counterexample','quadratic_form':float(avec@tanhK@avec)})
points=np.array([[1.,0.],[0.,1.],[0.,0.],[1.,1.]])
check('MT020 XOR interaction scores',points[:,0]+points[:,1]-2*points[:,0]*points[:,1]-.5,[.5,.5,-.5,-.5])
check('MT055 simple tanh quadratic form',u+t-2*v,-.1671317044568)
for probability in [0.,.1,.25,.5,.8,1.]:
    slope=probability*(1-probability)
    check('MT066 sigmoid slope identity '+str(probability),slope,.25-(probability-.5)**2)
    assert slope<=.25
if not args.check:
    (ROOT/'CalculationChecks.json').write_text(json.dumps({'status':'passed','checks':checks},ensure_ascii=False,indent=2)+'\n')
print('Passed',len(checks),'numeric checks, including independent finite differences.')
