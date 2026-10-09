"""Recompute the small Lecture 2–5 derivations; no course data or training runs.

Run with the notebook dependencies. --check compares the saved evidence without
writing it; the default writes this revision's dedicated calculation record.
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.special import logsumexp
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/reviews/derivation-bridges-2026-10-09/calculations.json'
checks = []


def check(name, actual, expected, atol=1e-10):
    actual, expected = np.asarray(actual, dtype=float), np.asarray(expected, dtype=float)
    np.testing.assert_allclose(actual, expected, atol=atol, rtol=1e-9, err_msg=name)
    checks.append({'name': name, 'actual': actual.tolist(), 'expected': expected.tolist(),
                   'max_abs_error': float(np.max(np.abs(actual - expected)))})


def score(x, mu, var, prior):
    return norm.logpdf(x, loc=mu, scale=np.sqrt(var)).sum(axis=-1) + np.log(prior)


def expanded(x, m1, m2, v1, v2, p1, p2):
    a = .5 / v1 - .5 / v2
    b = m2 / v2 - m1 / v1
    c = np.log(p2/p1) + np.sum(m1*m1/(2*v1)-m2*m2/(2*v2)-.5*np.log(v2/v1))
    return np.sum(a*x*x+b*x, axis=-1)+c


def gaussian_checks():
    for v2, roots in [(1., [5.]), (4., [(10-np.sqrt(16+24*np.log(2)))/3,
                                      (10+np.sqrt(16+24*np.log(2)))/3])]:
        r = np.array(roots)[:, None]
        check(f'1D variance {v2}: boundary scores', score(r, 6, v2, .5)-score(r, 4, 1, .5), np.zeros(len(r)))
    check('Unequal-variance displayed roots', roots, [1.4291, 5.2376], atol=5e-5)
    rng = np.random.default_rng(42)
    for d in [1, 2, 5]:
        for setting in range(4):
            x = rng.normal(size=(7, d))
            m1, m2 = rng.normal(size=(2, d))
            v1, v2 = rng.uniform(.2, 3, size=(2, d))
            p1 = .15 + .2*setting
            check(f'{d}D setting {setting}: expansion versus Gaussian log densities',
                  expanded(x,m1,m2,v1,v2,p1,1-p1),
                  score(x,m2,v2,1-p1)-score(x,m1,v1,p1))
    x = rng.normal(size=(8, 2)); m1=np.zeros(2);m2=np.array([1.,2.])
    check('2D setting I: full line including C',expanded(x,m1,m2,np.array([1.,4.]),np.array([1.,4.]),.5,.5),x[:,0]+.5*x[:,1]-1)
    check('2D setting II: full parabola including C',expanded(x,m1,m2,np.array([1.,4.]),np.array([1.,9.]),.5,.5),
          x[:,0]+5*x[:,1]**2/72+2*x[:,1]/9-13/18-.5*np.log(9/4))
    v=np.full(2,1.7);p1,p2=.3,.7
    raw=score(x,m1,v,p1)-score(x,m2,v,p2)
    log_joint=np.column_stack([score(x,m1,v,p1),score(x,m2,v,p2)])
    posterior=log_joint-logsumexp(log_joint,axis=1,keepdims=True)
    check('L3 shared variance: posterior denominator cancellation',posterior[:,0]-posterior[:,1],raw)
    check('L3 shared variance: w and b',x@((m1-m2)/1.7)+(m2@m2-m1@m1)/(2*1.7)+np.log(p1/p2),raw)
    check('L2/L3 comparison directions',expanded(x,m1,m2,v,v,p1,p2),-raw)


def svm_checks():
    x=np.array([[-1.,2.,0.],[-2.,1.,3.],[1.,0.,2.],[3.,2.,1.]])
    y=np.array([-1.,-1.,1.,1.]);alpha=np.array([.5,.3,.2,.6]);b=2.7
    v=(alpha*y)@x
    check('SVM multiplier equality',alpha@y,0)
    lag=.5*v@v-np.sum(alpha*(y*(x@v+b)-1))
    check('SVM substitution of all four terms',lag,alpha.sum()-.5*v@v)
    pair_sum=sum(alpha[i]*alpha[j]*y[i]*y[j]*(x[i]@x[j]) for i in range(4) for j in range(4))
    check('SVM norm expansion into all ordered pairs',pair_sum,v@v)
    for scale in [1.,2.,3.]:
        a=1/(2*scale**2);w=2*a*scale
        primal=.5*w*w;dual=2*a-.5*(2*a*scale)**2
        check(f'SVM points +/-{scale}: recovered w',w,1/scale)
        check(f'SVM points +/-{scale}: constraints tight',np.array([-1.,1.])*(np.array([-scale,scale])*w),[1,1])
        check(f'SVM points +/-{scale}: primal equals dual',primal,dual)
        for trial in [0.,.5*a,2*a]:
            assert 2*trial-2*trial**2*scale**2 <= primal+1e-12


def ols_checks():
    cases=[([0,1,2],[1,2,2]),([0,1,2],[2,3,3]),([0,2,4],[1,2,2]),([1,1,2],[1,2,4])]
    for n,(xs,ys) in enumerate(cases):
        x=np.array(xs,dtype=float);y=np.array(ys,dtype=float);u=x-x.mean();v=y-y.mean()
        w=(u@v)/(u@u);b=y.mean()-w*x.mean();design=np.vstack([x,np.ones(len(x))])
        scalar=np.array([w,b]);matrix=np.linalg.solve(design@design.T,design@y)
        numeric=np.linalg.lstsq(design.T,y,rcond=None)[0]
        check(f'OLS {n}: scalar versus matrix',scalar,matrix)
        check(f'OLS {n}: scalar versus least-squares solver',scalar,numeric)
        check(f'OLS {n}: zero gradient',2*design@(design.T@scalar-y),[0,0])
        if n==0:
            check('OLS worked coefficients',scalar,[.5,7/6])
            check('OLS worked MSE',np.mean((y-design.T@scalar)**2),1/18)
            check('OLS worked normal matrix',design@design.T,[[5,3],[3,3]])
    x=np.full(3,2.);y=np.array([1.,2.,3.]);design=np.vstack([x,np.ones(3)])
    numeric=design.T@np.linalg.lstsq(design.T,y,rcond=None)[0]
    assert np.linalg.matrix_rank(design)==1
    for w in [-3.,0.,5.]:
        b=y.mean()-w*x[0]
        check(f'OLS equal inputs: equivalent slope {w}',w*x+b,numeric)


def krr_checks():
    def verify(name,phi,y,star,alpha):
        m,n=phi.shape;k=phi.T@phi
        w=np.linalg.solve(phi@phi.T+alpha*np.eye(m),phi@y)
        a=np.linalg.solve(k+alpha*np.eye(n),y)
        check(f'{name}: stationarity to residual coefficients',a,(y-phi.T@w)/alpha)
        check(f'{name}: recovered feature weights',w,phi@a)
        check(f'{name}: primal versus kernel prediction',star.T@w,(phi.T@star).T@a)
        assert np.linalg.eigvalsh(k+alpha*np.eye(n)).min()>0
        return w,a
    w,a=verify('Linear worked example',np.array([[0.,1.]]),np.array([0.,2.]),np.array([[2.]]),1.)
    check('Linear worked w and a',np.r_[w,a],[1,0,1])
    x=np.array([0.,1.,1.,2.]);star=np.array([-.5,.5,3.])
    phi=np.vstack([np.ones(4),np.sqrt(2)*x,x*x]);ps=np.vstack([np.ones(3),np.sqrt(2)*star,star*star])
    check('Polynomial feature inner products',phi.T@phi,(1+np.outer(x,x))**2)
    check('Polynomial new-input kernel values',phi.T@ps,(1+np.outer(x,star))**2)
    assert np.linalg.matrix_rank(phi.T@phi)<len(x)
    for alpha in [.2,1.]:
        verify(f'Polynomial alpha={alpha}',phi,np.array([1.,2.,2.,4.]),ps,alpha)
    phi=np.array([[1.,2.,3.],[1.,2.,3.],[1.,1.,1.]])
    assert np.linalg.matrix_rank(phi)<phi.shape[0]
    verify('Repeated-feature rank deficiency',phi,np.array([2.,1.,4.]),np.array([[2.5],[2.5],[1.]]),.5)


def network(x,a,w,c,b,y,lam):
    u=x@a+c;h=np.maximum(u,0);z=h@w+b;lp=z-logsumexp(z,axis=1,keepdims=True);p=np.exp(lp)
    loss=-np.sum(y*lp)/len(x)+lam*(np.sum(a*a)+np.sum(w*w))/2
    gz=(p-y)/len(x);gh=gz@w.T;gu=gh*(u>0)
    grads={'x':gu@a.T,'a':x.T@gu+lam*a,'w':h.T@gz+lam*w,'c':gu.sum(axis=0),'b':gz.sum(axis=0)}
    return loss,grads,{'u':u,'h':h,'z':z,'p':p,'gz':gz,'gh':gh,'gu':gu}


def backprop_checks():
    cases=[('identity',np.array([[1.,2.]]),np.eye(2),np.eye(2),np.zeros(2),np.zeros(2),np.array([[0.,1.]]),0.),
           ('nonidentity',np.array([[1.,2.]]),np.eye(2),np.array([[1.,-1.],[1.,2.]]),np.zeros(2),np.zeros(2),np.array([[0.,1.]]),0.),
           ('transfer',np.array([[1.,2.]]),np.eye(2),np.array([[1.,-1.],[1.,3.]]),np.zeros(2),np.zeros(2),np.array([[0.,1.]]),0.),
           ('batch-regularized',np.array([[1.,2.],[2.,.5],[.5,1.5]]),np.array([[.8,-.2],[.3,.7]]),np.array([[1.,-.5],[.2,.6]]),np.array([.1,-.1]),np.array([.1,-.2]),np.array([[0.,1.],[1.,0.],[0.,1.]]),.2)]
    for name,x,a,w,c,b,y,lam in cases:
        args={'x':x,'a':a,'w':w,'c':c,'b':b,'y':y,'lam':lam}
        loss,grad,t=network(**args)
        assert np.min(np.abs(t['u']))>1e-4 # No finite difference crosses a ReLU corner.
        gw=np.zeros_like(w);gh=np.zeros_like(t['h'])
        for j in range(w.shape[0]):
            for k in range(w.shape[1]):
                gw[j,k]=sum(t['h'][i,j]*t['gz'][i,k] for i in range(len(x)))+lam*w[j,k]
            for i in range(len(x)):
                gh[i,j]=sum(t['gz'][i,k]*w[j,k] for k in range(w.shape[1]))
        check(f'{name}: component versus matrix weight gradient',gw,grad['w'])
        check(f'{name}: component versus matrix hidden gradient',gh,t['gh'])
        for key in ['x','a','w','c','b']:
            num=np.zeros_like(args[key]);step=1e-6
            for index in np.ndindex(num.shape):
                before=args[key][index]
                try:
                    args[key][index]=before+step;plus=network(**args)[0]
                    args[key][index]=before-step;minus=network(**args)[0]
                finally:args[key][index]=before
                num[index]=(plus-minus)/(2*step)
            check(f'{name}: finite-difference {key}',grad[key],num,atol=2e-8)
        if name=='nonidentity':
            check('Nonidentity logits',t['z'],[[3,3]])
            check('Nonidentity output gradient',t['gz'],[[.5,-.5]])
            check('Nonidentity hidden gradient',t['gh'],[[1,-.5]])
            check('Nonidentity W gradient',grad['w'],[[.5,-.5],[1,-1]])
            check('Nonidentity A gradient',grad['a'],[[1,-.5],[2,-1]])
        if name=='transfer':
            q=1/(1+np.exp(2))
            check('Transfer logits',t['z'],[[3,5]])
            check('Transfer output gradient',t['gz'],[[q,-q]])
            check('Transfer hidden gradient',t['gh'],[[2*q,-2*q]])
            check('Transfer W gradient',grad['w'],[[q,-q],[2*q,-2*q]])
            check('Transfer A gradient',grad['a'],[[2*q,-2*q],[4*q,-4*q]])
        if name=='batch-regularized':
            # Duplicating an entire batch leaves the average loss and parameter gradients unchanged.
            duplicate={**args,'x':np.tile(x,(2,1)),'y':np.tile(y,(2,1))}
            loss2,grads2,_=network(**duplicate)
            check('Batch average: duplicated loss',loss2,loss)
            for key in ['a','w','c','b']:
                check(f'Batch average: duplicated {key} gradient',grads2[key],grad[key])


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for fn in [gaussian_checks,svm_checks,ols_checks,krr_checks,backprop_checks]:fn()
    report={'seed':42,'scope':'Small instructional calculations only; no instructor data or course experiments.',
            'checks':checks,'count':len(checks)}
    if args.check:
        saved=json.loads(OUT.read_text())
        assert saved['count']==len(checks)
        for previous,current in zip(saved['checks'],checks):
            assert previous['name']==current['name']
            for key in ['actual','expected']:
                np.testing.assert_allclose(previous[key],current[key],atol=2e-8,rtol=1e-8)
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(checks)} derivation checks passed; evidence '+('verified.' if args.check else 'saved.'))


if __name__=='__main__':main()
