"""Small independent numerical checks for Lecture 2–5, without training experiments.

Pass --report to save evidence. Optional --iris-file checks the local teacher data;
the report records its hash, never its path. No data files are distributed.
"""
from pathlib import Path
import argparse, hashlib, importlib.metadata, json
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import softmax
from scipy.stats import norm, multivariate_normal
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

checks={}
def equal(name, actual, expected, tol=1e-9):
    np.testing.assert_allclose(actual,expected,atol=tol,rtol=tol)
    checks[name]=np.asarray(actual).tolist()

def finite_gradient(fn, x):
    x=np.asarray(x,dtype=float); out=np.zeros_like(x)
    for ix in np.ndindex(x.shape):
        a=x.copy();b=x.copy();a[ix]+=1e-6;b[ix]-=1e-6
        out[ix]=(fn(a)-fn(b))/2e-6
    return out

def calculate(iris=None):
    equal('L2.gaussian_mle',[np.mean([2,4,6]),np.var([2,4,6])],[4,8/3])
    equal('L2.bayes_posterior',softmax(np.log([.4,.2])+np.log([.25,.75])),[.4,.6])
    equal('L2.stable_posterior',softmax([-1001,-1000]),[1/(1+np.e),np.e/(1+np.e)])
    roots=np.sort(np.roots([3/8,-5/2,7/2-np.log(2)]))
    equal('L2.boundaries',roots,[(10-np.sqrt(16+24*np.log(2)))/3,(10+np.sqrt(16+24*np.log(2)))/3])
    equal('L2.boundary_density_equality',norm.pdf(roots,4,1),norm.pdf(roots,6,2))
    equal('L2.shared_variance_boundary',norm.pdf(5,4,1),norm.pdf(5,6,1))
    equal('L2.quadratic_coefficient_x2',1/(2*4)-1/(2*9),5/72)
    covs=[np.eye(2),np.array([[1.,.5],[.5,1.]])]
    densities=np.array([multivariate_normal.pdf([1,1],mean=[0,0],cov=c) for c in covs])
    equal('L2.full_gaussian_equal_priors',densities/densities.sum(),[.3829,.6171],5e-5)
    s=densities*[.8,.2]
    equal('L2.full_gaussian_new_priors',s/s.sum(),[.7128,.2872],5e-5)
    equal('L2.bernoulli_smoothing',(.6*.6)/(.6*.6+.2*.4),9/11)
    equal('L2.multinomial_counts',.7**2/(.7**2+.2**2),49/53)
    counts=np.array([[2,1,0,1],[1,0,0,1],[0,0,2,1],[0,0,1,1]])
    tf=TfidfTransformer(norm='l1');features=tf.fit_transform(counts)
    model=MultinomialNB(alpha=1).fit(features,[0,0,1,1])
    equal('L2.tfidf_D1',features.toarray()[0],[.5089,.3227,0,.1684],5e-5)
    new=tf.transform([[2,0,0,1],[0,0,1,2]])
    equal('L2.tfidf_new_posteriors',model.predict_proba(new)[:,0],[.6339,.4021],5e-5)
    equal('L2.bayes_error_identical_distributions',[1-max(.5,.5),1-max(.2,.8)],[.5,.2])
    if iris:
        data=np.loadtxt(iris,delimiter=',',skiprows=1);X=data[:,:2];y=data[:,2].astype(int)
        tx,vx,ty,vy=train_test_split(X,y,test_size=.5,random_state=4487)
        nb=GaussianNB().fit(tx,ty)
        equal('L2.iris_train_class_counts',np.bincount(ty)[1:],[19,31])
        equal('L2.iris_nb_test_correct',np.sum(nb.predict(vx)==vy),42)
        # Original full-Gaussian demonstration uses alpha=0: verified separately below.
        score0=np.array([multivariate_normal.logpdf(vx,mean=tx[ty==c].mean(0),cov=np.cov(tx[ty==c],rowvar=False))+np.log(np.mean(ty==c)) for c in [1,2]]).T
        equal('L2.iris_full_gaussian_test_correct',np.sum(1+score0.argmax(1)==vy),45)
        dens=[norm.pdf(5,X[y==c,0].mean(),X[y==c,0].std()) for c in [1,2]]
        equal('L2.iris_1d_densities',dens,[.241986,.438306],1e-6)
        checks['iris_sha256']=hashlib.sha256(Path(iris).read_bytes()).hexdigest()

    equal('L3.logistic_losses',np.logaddexp(0,[2,-2]),[2.126928011,.126928011])
    x=np.array([[1.,2.],[-2,1]]);y=np.array([1.,-1.]);p=np.array([.2,-.3,.1]);C=2.
    f=lambda p: np.sum(np.logaddexp(0,-y*(x@p[:2]+p[2])))+p[:2]@p[:2]/C
    a=y/(1+np.exp(y*(x@p[:2]+p[2])))
    analytic=np.r_[2*p[:2]/C-x.T@a,-a.sum()]
    equal('L3.logistic_gradient',finite_gradient(f,p),analytic,2e-9)
    equal('L3.step_probability',1/(1+np.exp(-.25)),.5621765008857981)
    for C in [.25,1.]:
        model=SVC(C=C,kernel='linear',tol=1e-10).fit([[-1.],[1.]],[-1,1])
        alpha=np.abs(model.dual_coef_[0]);w=float(model.coef_[0,0]);b=float(model.intercept_[0]);yf=np.array([-1,1])*(np.array([-1,1])*w+b);xi=np.maximum(0,1-yf)
        equal(f'L3.soft_svm_C{C}',[w,b], [min(1,2*C),0])
        equal(f'L3.margin_complementarity_C{C}',alpha*(yf-1+xi),[0,0])
        equal(f'L3.slack_complementarity_C{C}',(C-alpha)*xi,[0,0])
    equal('L3.rbf_ln2',np.exp(-np.log(2)*np.array([[0,1],[1,0]])),[[1,.5],[.5,1]])
    equal('L3.invalid_gram',np.array([1,-1])@np.array([[1,2],[2,1]])@np.array([1,-1]),-2)
    equal('L3.parameter_count_d3',[3+1,2*3+1+1],[4,8])

    x=np.arange(3.);y=np.array([1.,2.,2.]);A=np.c_[x,np.ones(3)]
    w=np.linalg.lstsq(A,y,rcond=None)[0]
    equal('L4.ols_slope_intercept',w,[.5,7/6])
    equal('L4.ols_and_constant_SSE',[np.sum((y-A@w)**2),np.sum((y-y.mean())**2)],[1/6,2/3])
    equal('L4.ols_mse',np.mean((y-A@w)**2),1/18)
    singular=np.c_[x,x,np.ones(3)]
    equal('L4.rank_deficient_minimum_SSE',np.sum((y-singular@np.linalg.lstsq(singular,y,rcond=None)[0])**2),1/6)
    for a1,a2 in [(0,10),(4,0),(6,0),(10,0),(4,5),(10,5)]:
        f=lambda w:5*(1-w)**2+a1*abs(w)+a2*w*w
        numeric=minimize_scalar(f,bounds=(-3,3),method='bounded',options={'xatol':1e-12})
        expected=max(5-a1/2,0)/(5+a2)
        equal(f'L4.penalized_a1_{a1}_a2_{a2}',numeric.x,expected,2e-7)
    for target,expected in [([1.,2.],[-1,2*np.sqrt(2)]),([2.,1.],[1,np.sqrt(2)])]:
        A=np.array([[1,1/np.sqrt(2)],[0,1/np.sqrt(2)]])
        equal('L4.omp_first_'+str(target),np.argmax(abs(A.T@target)),1)
        equal('L4.omp_joint_'+str(target),np.linalg.lstsq(A,target,rcond=None)[0],expected)
    A=np.c_[np.arange(4),np.ones(4)]
    equal('L4.ransac_wide_refit',np.linalg.lstsq(A,[1,2,3,10],rcond=None)[0],[2.8,-.2])
    equal('L4.huber',[.5*.5**2,2-.5,3-.5],[.125,1.5,2.5])
    for n,r in [(5,.2),(20,.2),(10,.5)]:
        cov=(1-r)*np.eye(n)+r*np.ones((n,n));v=np.ones(n)/n
        equal(f'L4.forest_n{n}_rho{r}',v@cov@v,r+(1-r)/n)
    equal('L4.boost_SSE_eta_half',np.sum((np.array([3,1])-(np.array([2,2])+.5*np.array([1,-1])))**2),.5)
    equal('L4.boost_SSE_eta_quarter',np.sum((np.array([3,1])-(np.array([2,2])+.25*np.array([1,-1])))**2),1.125)

    equal('L5.softmax_probabilities',softmax(np.log([2,3,5])),[.2,.3,.5])
    equal('L5.softmax_scaled',softmax(2*np.log([2,3,5])),np.array([4,9,25])/38)
    g=np.log([2.,3.,5.]);ce=lambda z:-np.log(softmax(z)[2])
    equal('L5.softmax_CE_gradient',finite_gradient(ce,g),[.2,.3,-.5],1e-9)
    for u in [-2.,0.,2.]:
        equal('L5.tanh_derivative_'+str(u),finite_gradient(lambda x:np.tanh(x[0]),[u]),[1-np.tanh(u)**2],1e-9)
    f=lambda p:(p[2]*np.tanh(p[0]+p[1])+p[3]-1)**2
    p=np.array([0.,0.,2.,0.])
    equal('L5.scalar_all_gradients',finite_gradient(f,p),[-4,-4,0,-2],1e-9)
    equal('L5.scalar_half_loss_w1_gradient',finite_gradient(lambda p:f(p)/2,p)[0],-2,1e-9)
    p[0]=.4;equal('L5.scalar_loss_after_update',f(p),.0576,5e-5)
    theta=1.;v=0.;trajectory=[]
    for grad in [2.,-2.]:v=.9*v+.1*grad;theta-=v;trajectory.append([v,theta])
    equal('L5.momentum_opposed',trajectory,[[.2,.8],[-.02,.82]])
    equal('L5.momentum_same',.8-(.9*.2+.1*2),.42)
    equal('L5.perceptron_zero_update',np.zeros(2)+.5*(-1)*np.array([2,1]),[-1,-.5])
    equal('L5.network_parameter_counts',[(784+1)*10,(784+1)*50+(50+1)*10,(784+1)*200+(200+1)*10,(784+1)*1000+(1000+1)*10,(784+1)*500+(500+1)*500+(500+1)*10],[7850,39760,159010,795010,648010])
    return {'status':'passed','checks':checks,'check_groups':len(checks),'versions':{k:importlib.metadata.version(k) for k in ['numpy','scipy','scikit-learn']},'scope':'Explicit teaching examples, optional instructor iris data. No large training search or notebook execution.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path);p.add_argument('--iris-file',type=Path);a=p.parse_args();result=calculate(a.iris_file)
    if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f"Passed {result['check_groups']} calculation groups.")
