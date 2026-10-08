"""Recompute Lecture 2 teaching examples and two figures; never runs Tutorials.

Install requirements-notebooks.txt. Set COURSE_DATA_ROOT to the Canvas data root.
No raw datasets or instructor notebooks are copied into the repository.
"""
from pathlib import Path
import os, json, hashlib, platform, importlib.metadata, re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import norm, multivariate_normal
from scipy.special import logsumexp
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.datasets import load_files

NOTES = Path(__file__).resolve().parents[1]
ROOT = NOTES.parents[1]
DATA = Path(os.environ.get('COURSE_DATA_ROOT', ROOT/'data')).expanduser()
SOURCE = DATA/'CS5489/Lecture2/Lecture2'
for name in ['iris2.csv', 'Lecture2b.ipynb', 'email']:
    if not (SOURCE/name).exists():
        raise FileNotFoundError(f'Missing Canvas input {name}; see docs/DATA.md and COURSE_DATA_ROOT.')
ASSETS = NOTES/'assets'
REPORT = ROOT/'docs/reviews/lecture02-2026-10-08/calculations.json'
ASSETS.mkdir(exist_ok=True); REPORT.parent.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'figure.dpi':150,
    'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
BLUE, GOLD, INK = '#2870a2','#b57319','#243343'
def save(fig, name):
    fig.savefig(ASSETS/name, dpi=170, bbox_inches='tight'); plt.close(fig)
def normalized(z):
    z=np.asarray(z); return np.exp(z-logsumexp(z,axis=-1,keepdims=True))
def clean(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    raise TypeError(type(x))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

raw=np.loadtxt(SOURCE/'iris2.csv', delimiter=',',skiprows=1)
X,y=raw[:,:2],raw[:,2].astype(int)
mu=np.array([X[y==c,0].mean() for c in [1,2]])
std=np.array([X[y==c,0].std(ddof=0) for c in [1,2]])
prior=np.array([np.mean(y==c) for c in [1,2]])
point=5.; densities=norm.pdf(point,mu,std); scores=densities*prior
manual_density=np.exp(-((point-mu)**2)/(2*std**2))/np.sqrt(2*np.pi*std**2)
np.testing.assert_allclose(densities,manual_density)
fig,axes=plt.subplots(1,2,figsize=(9,3.5),layout='constrained')
for c,ax,color in zip([1,2],axes,[BLUE,GOLD]):
    v=X[y==c,0];grid=np.linspace(2.5,7.2,400)
    ax.hist(v,bins=np.arange(2.5,7.51,.2),density=True,color=color,alpha=.25,edgecolor=color,label='Observed lengths (n=50)')
    ax.plot(grid,norm.pdf(grid,mu[c-1],std[c-1]),color=color,lw=2,label='Fitted Gaussian')
    ax.set(title=['Versicolor (class 1)','Virginica (class 2)'][c-1],xlabel='Petal length (cm)',ylabel='Density (1/cm)',xlim=(2.5,7.2));ax.legend(fontsize=8)
save(fig,'lecture02-histogram-fit.png')
# Same instructor split, with indices retained to identify the annotated record.
it,iv=train_test_split(np.arange(len(y)),train_size=.5,test_size=.5,random_state=4487)
xt,xv,yt,yv=X[it],X[iv],y[it],y[iv]
gnb=GaussianNB().fit(xt,yt);pred=gnb.predict(xv)
error_indices=np.flatnonzero(pred!=yv);ei=int(error_indices[0]);focus=xv[ei]
grid0,grid1=np.meshgrid(np.linspace(2.5,7,220),np.linspace(1.5,4,180))
grid=np.c_[grid0.ravel(),grid1.ravel()];p2=gnb.predict_proba(grid)[:,1].reshape(grid0.shape)
fig,ax=plt.subplots(figsize=(7,4.8),layout='constrained')
ax.contourf(grid0,grid1,p2,levels=[0,.5,1],colors=[BLUE,GOLD],alpha=.09)
ax.contour(grid0,grid1,p2,levels=[.5],colors=INK,linestyles='--',linewidths=1.5)
for c,color,marker,name in [(1,BLUE,'o','True class 1'),(2,GOLD,'^','True class 2')]:
    ax.scatter(*xv[yv==c].T,color=color,marker=marker,s=33,label=name)
ax.scatter(*xv[error_indices].T,marker='s',facecolors='none',edgecolors=INK,s=100,lw=1.25,label='Wrong prediction')
ax.annotate(f'A: ({focus[0]:g}, {focus[1]:g}) cm',xy=focus,xytext=(3.0,3.75),arrowprops={'arrowstyle':'->','color':INK},fontsize=10)
ax.set(title='Gaussian NB: 42 / 50 test flowers classified correctly',xlabel='Petal length (cm)',ylabel='Sepal width (cm)',xlim=(2.5,7),ylim=(1.5,4));ax.legend(loc='lower right',fontsize=9);ax.grid(alpha=.15)
save(fig,'lecture02-test-errors.png')
probe=np.array([5.,3.]);marginal=norm.pdf(probe,gnb.theta_,np.sqrt(gnb.var_))
manual_post=marginal.prod(axis=1)*gnb.class_prior_;manual_post/=manual_post.sum()
np.testing.assert_allclose(manual_post,gnb.predict_proba(probe[None,:])[0])
full_mu=np.array([xt[yt==c].mean(0) for c in [1,2]])
full_cov=np.array([np.cov(xt[yt==c],rowvar=False) for c in [1,2]])
full_score=np.column_stack([multivariate_normal.logpdf(xv,mean=full_mu[j],cov=full_cov[j])+np.log(gnb.class_prior_[j]) for j in [0,1]])
# Two covariance matrices used in the worked bridge and changed-prior exercise.
point2=np.array([1.,1.]);covs=[np.eye(2),np.array([[1.,.5],[.5,1.]])]
distance=np.array([point2@np.linalg.solve(c,point2) for c in covs]);det=np.array([np.linalg.det(c) for c in covs])
base=-distance/2-np.log(det)/2
cov_demo={}
for key,pri in [('equal',[.5,.5]),('changed',[.8,.2])]:
    z=base+np.log(pri);p=normalized(z)
    direct=np.array([multivariate_normal.pdf(point2,mean=[0,0],cov=c) for c in covs])*pri
    np.testing.assert_allclose(p,direct/direct.sum())
    cov_demo[key]={'priors':pri,'scores_without_common_constant':z,'posterior':p}
# Exact small corpus specified in the revision plan; fixed vocabulary order.
documents=['free free offer today','free today','meeting meeting today','meeting today']
labels=np.array([1,1,0,0]);vocab=['free','offer','meeting','today']
vectorizer=CountVectorizer(vocabulary=vocab);counts=vectorizer.transform(documents).toarray()
df=(counts>0).sum(0);tf=counts/counts.sum(1,keepdims=True);idf_simple=np.log(len(documents)/df)
simple=tf*idf_simple
idf_smoothed=np.log((1+len(documents))/(1+df))+1
weighted=counts*idf_smoothed;l1=weighted/weighted.sum(1,keepdims=True)
transformer=TfidfTransformer(norm='l1');lib=transformer.fit_transform(counts).toarray()
np.testing.assert_allclose(l1,lib)
model=MultinomialNB(alpha=1).fit(lib,labels)
class_weight=np.array([l1[labels==c].sum(0) for c in model.classes_]);theta=(class_weight+1)/(class_weight.sum(1,keepdims=True)+len(vocab))
np.testing.assert_allclose(theta,np.exp(model.feature_log_prob_))
text_cases={}
for text in ['free free today','meeting today today']:
    count=vectorizer.transform([text]).toarray()[0];w=count*idf_smoothed;weight=w/w.sum()
    logjoint=np.log([.5,.5])+np.log(theta)@weight
    predicted=model.predict_proba(transformer.transform([count]))[0]
    np.testing.assert_allclose(normalized(logjoint),predicted)
    text_cases[text]={'counts':count,'tfidf_l1':weight,'logjoint_ham_spam':logjoint,'posterior_ham_spam':predicted}
# Instructor mail: saved predictions remain explicitly historical; inspect one
# real error under positive smoothing and cross-check the score directly.
mail=load_files(SOURCE/'email',encoding='utf8',decode_error='replace')
tr,te,ty,ey=train_test_split(mail.data,mail.target,train_size=.5,test_size=.5,random_state=11)
cv=CountVectorizer(stop_words='english',max_features=100);cx=cv.fit_transform(tr);tx=cv.transform(te)
b=BernoulliNB(alpha=.1).fit(cx,ty)
idx=12
assert te[idx].startswith('Get Up to 75% OFF at Online WatchesStore') and int(ey[idx])==1
binary=(tx[idx].toarray()[0]>0).astype(int);prob=np.exp(b.feature_log_prob_)
terms=binary*np.log(prob)+(1-binary)*np.log1p(-prob)
joint=np.log(b.class_prior_) + terms.sum(1) if hasattr(b,'class_prior_') else b.class_log_prior_+terms.sum(1)
np.testing.assert_allclose(normalized(joint),b.predict_proba(tx[idx])[0])
wordnames=cv.get_feature_names_out();present=np.flatnonzero(binary)
contributions=terms[1]-terms[0]
nbsource=json.loads((SOURCE/'Lecture2b.ipynb').read_text())
saved={}
for cell in [78,82,95]:
    streams=''.join(''.join(o.get('text',[])) for o in nbsource['cells'][cell-1].get('outputs',[]) if o.get('output_type')=='stream')
    saved[str(cell)]=float(streams.strip().splitlines()[-1])
assert saved=={'78':.64,'82':.72,'95':.68}
saved82=''.join(''.join(o.get('text',[])) for o in nbsource['cells'][81]['outputs'] if o.get('output_type')=='stream')
saved_predictions=np.fromstring(re.search(r'predictions:\s*\[([^]]+)\]',saved82).group(1),sep=' ',dtype=int)
assert int(saved_predictions[idx])==int(b.predict(tx[idx])[0])==0
mail_source=Path(mail.filenames[mail.data.index(te[idx])])

# Existing teaching examples computed from their inputs, not copied answers.
b_counts=np.array([[2,1],[0,2]]);b_theta=(b_counts+1)/5;b_scores=b_theta[:,0]*(1-b_theta[:,1])
m_counts=np.array([[6,2],[1,7]]);m_theta=(m_counts+1)/(m_counts.sum(1,keepdims=True)+2);m_scores=m_theta[:,0]**2
result={
 'source_hashes':{'iris2.csv':digest(SOURCE/'iris2.csv'),'Lecture2b.ipynb':digest(SOURCE/'Lecture2b.ipynb')},
 'versions':{'python':platform.python_version(),**{k:importlib.metadata.version(k) for k in ['numpy','scipy','scikit-learn','matplotlib']}},
 'iris_1d':{'means':mu,'std_mle':std,'priors':prior,'new_length_cm':point,'densities_per_cm':densities,'unnormalized_scores':scores,'posterior':scores/scores.sum()},
 'iris_2d':{'mean':gnb.theta_,'variance':gnb.var_,'priors':gnb.class_prior_,'probe_cm':probe,'marginal_densities':marginal,'posterior':manual_post,'nb_correct':int(np.sum(pred==yv)),'full_correct':int(np.sum(full_score.argmax(1)+1==yv)),'n_test':len(yv),'error_A':{'test_index_zero_based':ei,'data_row_zero_based':int(iv[ei]),'features_cm':focus,'true_label':int(yv[ei]),'predicted_label':int(pred[ei]),'posterior':gnb.predict_proba(focus[None,:])[0]}},
 'covariance_bridge':{'distance_squared':distance,'determinants':det,'base_scores':base,**cov_demo},
 'text_toy':{'vocabulary':vocab,'documents':documents,'labels_spam1_ham0':labels,'counts':counts,'document_frequency':df,'tf':tf,'idf_simple':idf_simple,'conceptual_tfidf':simple,'idf_smoothed':idf_smoothed,'tfidf_l1':l1,'class_weight_ham_spam':class_weight,'smoothed_theta_ham_spam':theta,'alpha':1,'predictions':text_cases},
 'mail_case':{'identity':'Original Lecture2b test record 12 (zero-based), watches advertisement','source_file':str(mail_source.relative_to(SOURCE)),'source_sha256':digest(mail_source),'excerpt':'Get Up to 75% OFF at Online WatchesStore','true_class':'spam','model':'Recomputed BernoulliNB alpha=0.1, instructor seed=11, max_features=100','present_vocabulary_terms':[{ 'word':str(wordnames[j]),'count':int(tx[idx,j]),'presence_log_ratio_spam_over_ham':float(contributions[j])} for j in present],'log_prior_ratio_spam_over_ham':float(b.class_log_prior_[1]-b.class_log_prior_[0]),'present_log_ratio_sum':float(contributions[present].sum()),'absent_log_ratio_sum':float(contributions[binary==0].sum()),'logjoint_ham_spam':joint,'posterior_ham_spam':normalized(joint),'class_order':mail.target_names},
 'instructor_saved_outputs':{'note':'Read from saved outputs, not new experiment scores','accuracy_by_cell':saved},
 'independent_bayes':{'priors':[.2,.8],'scores':densities*np.array([.2,.8]),'posterior':densities*np.array([.2,.8])/np.sum(densities*np.array([.2,.8]))},
 'existing_examples':{'bernoulli_smoothed_parameters_spam_ham':b_theta,'bernoulli_conditional_scores_spam_ham':b_scores,'bernoulli_spam_posterior':float(b_scores[0]/b_scores.sum()),'multinomial_spam_posterior':float(m_scores[0]/m_scores.sum())},
 'checks':'Manual formulas agree with independent NumPy/SciPy/scikit-learn paths; no tutorial execution.'}
REPORT.write_text(json.dumps(result,default=clean,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['iris_1d','iris_2d','covariance_bridge','text_toy','mail_case']},default=clean,ensure_ascii=False,indent=2))
