"""Small independent checks for the three corrected decision rules."""
from pathlib import Path
import json
import sys
import numpy as np
from sklearn.svm import SVC

out=Path(__file__).with_name('calculations.json')
rows=[]
x=np.array([[-1.],[1.]]);y=np.array([-1.,1.])
for c in [.25,.5,1.,10.]:
    model=SVC(kernel='linear',C=c,tol=1e-10).fit(x,y)
    a=min(c,.5);w=2*a
    np.testing.assert_allclose(model.coef_,[[w]],atol=1e-8)
    np.testing.assert_allclose(model.intercept_,[0],atol=1e-8)
    np.testing.assert_allclose(np.abs(model.dual_coef_),[[a,a]],atol=1e-8)
    slack=np.maximum(0,1-y*(x[:,0]*w))
    primal=.5*w*w+c*slack.sum();dual=2*a-2*a*a
    np.testing.assert_allclose(primal,dual,atol=1e-10)
    rows.append({'case':'finite-C soft SVM','C':c,'alpha':[a,a],'w':w,'slack':slack.tolist(),'primal':primal,'dual':dual})

cols=np.array([[-1.,0.],[0.,1.]]) # feature columns, each with norm one
r=np.array([3.,2.]);corr=cols.T@r
selected=int(np.argmax(np.abs(corr)))
assert selected==0
residuals=[float(np.sum((r-cols[:,j]*corr[j])**2)) for j in range(2)]
np.testing.assert_allclose(corr,[-3,2]);np.testing.assert_allclose(residuals,[4,9])
rows.append({'case':'OMP absolute inner product','inner_products':corr.tolist(),'selected_column_0_based':selected,'residual_SSE_by_column':residuals})

target=np.array([3.,1.]);pred=np.array([2.,2.]);rate=.5
positive_gradient=pred-target # gradient of half-squared error
negative_gradient=target-pred
a=pred-rate*positive_gradient;b=pred+rate*negative_gradient
np.testing.assert_allclose(a,b);np.testing.assert_allclose(a,[2.5,1.5])
rows.append({'case':'boosting paired sign convention','loss':'half-squared error','subtract_positive':a.tolist(),'add_negative':b.tolist(),'SSE':float(np.sum((target-a)**2))})
report={'scope':'Four finite-C cases, normalized OMP sign case, and paired boosting updates. No course experiments.','cases':rows,'passed':True}
if '--check' in sys.argv:
    assert json.loads(out.read_text())==report
else:
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('6 corrected-rule cases passed; numerical results saved.')
