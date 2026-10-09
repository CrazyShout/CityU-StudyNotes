"""Recompute the small teaching examples; no course datasets or experiments.

Run normally to save the report and the GBN/SR teaching diagram.
Use --check to compare current calculations with the saved report without writes.
"""
from pathlib import Path
import argparse,hashlib,json,importlib.metadata
import numpy as np
from scipy.special import softmax,logsumexp
from sklearn.linear_model import Ridge,Lasso
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'docs/reviews/all-notes-improvement-2026-10-09/calculations.json'
FIG=ROOT/'CS5222/course-notes/assets/chapter03-gbn-sr.png'

def calculate():
 A=np.array([[1,2,3],[4,5,6]]);B=np.array([[1,0],[0,1],[1,1]])
 assert (A@B==[[4,5],[10,11]]).all();B[:,1]=[1,1,0];assert (A@B==[[4,3],[10,9]]).all()
 points=np.array([0.,1.]);squared=(points[:,None]-points[None,:])**2
 k1=np.exp(-np.log(2)*squared);k2=np.exp(-np.log(4)*squared)
 np.testing.assert_allclose(k1,[[1,.5],[.5,1]]);np.testing.assert_allclose(k2,[[1,.25],[.25,1]])
 x=np.array([[1.],[2.]]);y=np.array([1.,2.])
 ridge=float(Ridge(alpha=10,fit_intercept=False).fit(x,y).coef_[0]);assert abs(ridge-1/3)<1e-12
 lasso=[float(Lasso(alpha=a/(2*len(y)),fit_intercept=False,tol=1e-12,max_iter=1000).fit(x,y).coef_[0]) for a in [6,10]]
 np.testing.assert_allclose(lasso,[.4,0],atol=1e-12)
 cols=np.array([[1,1/np.sqrt(2)],[0,1/np.sqrt(2)]]);target=np.array([2.,1.]);corr=cols.T@target
 assert np.argmax(abs(corr))==1
 weights=np.linalg.lstsq(cols,target,rcond=None)[0];np.testing.assert_allclose(weights,[1,np.sqrt(2)])
 xx=np.arange(4.);yy=np.array([1.,2.,3.,10.]);design=np.c_[xx,np.ones(4)];candidate=np.linalg.lstsq(design[[0,2]],yy[[0,2]],rcond=None)[0]
 residual=np.abs(yy-design@candidate);inliers=residual<=.5;assert inliers.tolist()==[True,True,True,False]
 refit=np.linalg.lstsq(design[inliers],yy[inliers],rcond=None)[0];wide=np.linalg.lstsq(design,yy,rcond=None)[0]
 np.testing.assert_allclose(refit,[1,1]);np.testing.assert_allclose(wide,[2.8,-.2])
 updated=np.array([2.,2.])+.25*np.array([1.,-1.]);sse=float(np.sum((np.array([3.,1.])-updated)**2));assert sse==1.125
 X=np.array([[1.,2.]])
 params=[np.eye(2),np.zeros((1,2)),np.eye(2),np.zeros((1,2))]
 def forward(ps,label):
  a,c,w,b=ps;u=X@a+c;h=np.maximum(u,0);z=h@w+b
  loss=float(logsumexp(z[0])-z[0,label]);p=softmax(z,axis=1)
  gz=p-np.eye(2)[[label]];gu=(gz@w.T)*(u>0)
  grads=[X.T@gu,gu.sum(0,keepdims=True),h.T@gz,gz.sum(0,keepdims=True)]
  return loss,p,grads
 mlp={}
 for label in [1,0]:
  loss,p,grads=forward(params,label);errors=[]
  for k,param in enumerate(params):
   num=np.zeros_like(param)
   for ix in np.ndindex(param.shape):
    plus=[v.copy() for v in params];minus=[v.copy() for v in params];plus[k][ix]+=1e-6;minus[k][ix]-=1e-6
    num[ix]=(forward(plus,label)[0]-forward(minus,label)[0])/2e-6
   errors.append(float(np.max(abs(num-grads[k]))));np.testing.assert_allclose(num,grads[k],atol=2e-9)
  mlp[f'class_{label+1}']={'loss':loss,'probabilities':p.tolist(),'gradients_A_c_W_b':[g.tolist() for g in grads],'max_finite_difference_error':max(errors)}
 q=1/(1+np.e);np.testing.assert_allclose(mlp['class_2']['gradients_A_c_W_b'][0],[[q,-q],[2*q,-2*q]])
 def rto(s):
  e=.875*100+.125*s;d=.75*10+.25*abs(s-e);return [e,d,e+4*d]
 np.testing.assert_allclose(rto(140),[105,16.25,170]);np.testing.assert_allclose(rto(80),[97.5,11.875,145])
 bad=np.array([[1.,2.],[2.,1.]]);v=np.array([1.,-1.]);assert v@bad@v==-2
 logistic=np.logaddexp(0,-np.array([2.,4.]));assert (logistic>0).all() and logistic[1]<logistic[0]
 residuals=np.array([.5,2.,-3.]);huber=np.where(abs(residuals)<=1,.5*residuals**2,abs(residuals)-.5)
 np.testing.assert_allclose(huber,[.125,1.5,2.5])
 variance=lambda n,rho:rho+(1-rho)/n
 np.testing.assert_allclose([variance(5,.2),variance(20,.2),variance(10,.5)],[.36,.24,.55])
 extra={'classification_losses_at_minus2_minus4':[[float(np.logaddexp(0,-z)),max(0,1-z),float(np.exp(-z))] for z in [-2,-4]],'binary_ce_at_three_quarters':float(-np.log(.75)),'zero_batch_counterexample_mean_gradient':[2.,-2.],'logistic_losses':logistic.tolist(),'invalid_gram_quadratic_form':float(v@bad@v),'huber':huber.tolist(),'asymmetric_at_plus_minus_2':[16,4],'forest_variances':[variance(5,.2),variance(20,.2),variance(10,.5)],'sigmoid_chain_bounds':[.25**5,.25**10],'chain_exercise':.2**4,'stored_parameters':{'d100_sv20':[101,20*101+1],'d50_sv10':[51,10*51+1]},'classifier_parameters_d3':[4,2*3+2]}
 return {'historical_teaching_extensions':extra,'matrix':{'product':[[4,5],[10,11]],'changed_second_column_product':(A@B).tolist()},'kernel':{'K_gamma_ln2':k1.tolist(),'K_gamma_ln4':k2.tolist(),'query_half_similarity':float(np.exp(-np.log(2)/4))},'ridge':{'alpha':10,'coefficient':ridge},'lasso':{'unaveraged_objective_alphas':[6,10],'coefficients':lasso},'omp':{'first_correlations':corr.tolist(),'joint_coefficients':weights.tolist()},'ransac':{'candidate_slope_intercept':candidate.tolist(),'absolute_residuals':residual.tolist(),'inliers_threshold_half':inliers.tolist(),'refit_threshold_half':refit.tolist(),'refit_threshold_7':wide.tolist()},'boosting':{'predictions':updated.tolist(),'sse':sse},'mlp':mlp,'network':{'single_hop_ms':1000*(.001+.002+500*8/2e6+1e6/2e8),'http_four_objects_rtts':{'serial':10,'persistent_nonpipelined':6},'dns_ms':{'worked_uncached':32,'worked_cached':2,'transfer_uncached':48,'transfer_cached':3},'video':{'size_mbit':18,'download_seconds':3,'buffer_gain_seconds':3},'rto_new_E_first_ms':{'sample_140':rto(140),'sample_80':rto(80)}}}

def draw():
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':14})
 fig,axes=plt.subplots(1,2,figsize=(8.4,5.8),layout='constrained')
 for ax,sr,title in zip(axes,[False,True],['Go-Back-N','Selective Repeat']):
  ax.set_xlim(-.28,1.3);ax.set_ylim(10,-.9);ax.axis('off');ax.set_title(title,fontsize=16)
  ax.plot([0,0],[0,9.5],c='#777',lw=1);ax.plot([1,1],[0,9.5],c='#777',lw=1)
  ax.text(0,-.35,'Sender',ha='center');ax.text(1,-.35,'Receiver',ha='center')
  def arrow(t,label,lost=False,ack=False):
   if ack:
    ax.annotate('',(0,t+.65),(1,t),arrowprops={'arrowstyle':'->','color':'#777','lw':1,'linestyle':':'})
    ax.text(.43,t+.54,label,fontsize=11.5,color='#555',ha='center',bbox={'facecolor':'white','edgecolor':'none','pad':.1})
   else:
    endx=.52 if lost else 1;endy=t+endx*.7
    ax.annotate('',(endx,endy),(0,t),arrowprops={'arrowstyle':'->','color':'#a43b31' if lost else '#276185','lw':1.3,'linestyle':'--' if lost else '-'})
    ax.text(.4,t+.13,label,fontsize=12,ha='center',bbox={'facecolor':'white','edgecolor':'none','pad':.2})
    if lost:ax.plot(endx,endy,marker='x',c='#a43b31',ms=8)
  arrow(.1,'0');arrow(.85,'ACK 0',ack=True);arrow(1.65,'1 lost',lost=True)
  arrow(2.6,'2');arrow(3.35,'ACK 2' if sr else 'ACK 0',ack=True)
  arrow(4.25,'3');arrow(5,'ACK 3' if sr else 'ACK 0',ack=True)
  ax.text(1.05,3.35,'buffer' if sr else 'discard',fontsize=11.5,ha='left')
  ax.text(1.05,5,'buffer' if sr else 'discard',fontsize=11.5,ha='left')
  ax.text(-.04,6,'timeout 1',fontsize=11.5,ha='left',bbox={'facecolor':'white','edgecolor':'none','pad':.2})
  arrow(6.45,'retry 1')
  if sr:
   arrow(7.2,'ACK 1',ack=True);ax.text(.5,8.8,'Deliver 1, 2, 3 in order',ha='center',fontsize=12)
  else:
   arrow(7.25,'retry 2');arrow(8.05,'retry 3');ax.text(.5,9.3,'Retransmit 1, 2, 3',ha='center',fontsize=12)
 fig.supxlabel('Event order runs downward; not a measured RTT scale',fontsize=12)
 FIG.parent.mkdir(parents=True,exist_ok=True);fig.savefig(FIG,dpi=220,bbox_inches='tight');plt.close(fig)

def compare(old,new):
 if isinstance(new,dict):
  assert old.keys()==new.keys()
  for k,v in new.items():compare(old[k],v)
 elif isinstance(new,list):
  assert len(old)==len(new)
  for a,b in zip(old,new):compare(a,b)
 elif isinstance(new,(int,float)):np.testing.assert_allclose(old,new,rtol=1e-8,atol=2e-9)
 else:assert old==new

def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args();result=calculate()
 if args.check:
  saved=json.loads(REPORT.read_text());compare(saved['results'],result);assert saved['figure_sha256']==hashlib.sha256(FIG.read_bytes()).hexdigest();print('Teaching calculations and figure identity verified; no files written.');return
 draw();REPORT.parent.mkdir(parents=True,exist_ok=True)
 REPORT.write_text(json.dumps({'status':'passed','scope':'explicit teaching data; no original experiment executed','results':result,'figure':'CS5222/course-notes/assets/chapter03-gbn-sr.png','figure_sha256':hashlib.sha256(FIG.read_bytes()).hexdigest(),'versions':{k:importlib.metadata.version(k) for k in ['numpy','scipy','matplotlib','scikit-learn']}},ensure_ascii=False,indent=2)+'\n');print('Saved teaching calculations and GBN/SR diagram.')
if __name__=='__main__':main()
