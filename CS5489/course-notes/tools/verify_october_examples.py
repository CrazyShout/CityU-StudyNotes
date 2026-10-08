"""Deterministic teaching figures and independent numerical checks; no assignment training."""
from pathlib import Path
import os,json,hashlib
D=Path(__file__).resolve().parents[1]; C=D.parents[1]; N=C/'CS5222/course-notes'
os.environ.setdefault('MPLCONFIGDIR',str(D/'.cache/matplotlib'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import softmax,logsumexp
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
checks={}
def record(name,actual,expected):
 assert np.allclose(actual,expected,rtol=1e-6,atol=1e-7),(name,actual,expected)
 checks[name]={'actual':np.asarray(actual).tolist(),'expected':np.asarray(expected).tolist()}
def save(fig,folder,name):
 fig.tight_layout();fig.savefig(folder/'assets'/name,dpi=160,bbox_inches='tight');plt.close(fig)
logits=np.log([2.,3.,5.]);p=softmax(logits)
record('softmax',p,[.2,.3,.5]);record('shift invariance',softmax(logits+100),p)
record('scale logits',softmax(2*logits),np.array([4,9,25])/38)
fig,ax=plt.subplots(figsize=(6.5,3.4));ax.bar(['Class 1','Class 2','Class 3'],p,color=['#456b8d','#93764b','#448775']);ax.set(ylabel='Probability',ylim=(0,.65),title='Logits log(2), log(3), log(5)')
for i,v in enumerate(p):ax.text(i,v+.015,f'{v:.1f}',ha='center')
save(fig,D,'oct-softmax.png')
x=np.linspace(-5,5,601);sig=1/(1+np.exp(-x));t=np.tanh(x)
fig,axs=plt.subplots(1,2,figsize=(9,3.5))
for ax,ys in zip(axs,[[sig,t,np.maximum(x,0)],[sig*(1-sig),1-t*t,(x>0).astype(float)]]):
 for y,label,style in zip(ys,['Sigmoid','Tanh','ReLU'],['-','--',':']):ax.plot(x,y,style,label=label)
 ax.set_xlabel('Pre-activation u');ax.grid(alpha=.2);ax.legend(fontsize=9)
axs[0].set_ylabel('Activation');axs[1].set_ylabel('Local derivative (away from u=0)')
save(fig,D,'oct-activations.png')
record('layer parameter counts',[(a+1)*b+(b+1)*10 for a,b in [(784,50),(784,200),(784,1000)]],[39760,159010,795010])
record('two hidden count',(784+1)*500+(500+1)*500+(500+1)*10,648010)
X=np.array([[1.,2.],[3.,4.]]);G=np.array([[1.,-1.],[2.,0.]])
record('linear weight gradient',X.T@G,[[7,-1],[10,-2]]);record('broadcast bias gradient',G.sum(0),[3,-1])
record('exponent example',[3*2*2,3*4*np.log(2)],[12,8.317766166719343])
# A complete two-sample, one-hidden-layer network checked against finite differences.
rng=np.random.default_rng(42);X=rng.normal(size=(2,3));A=rng.normal(size=(3,4));c=np.array([[.7,-.4,.2,-.9]]);W=rng.normal(size=(4,2));b=np.array([[.2,-.1]]);Y=np.eye(2);lam=.07
U=X@A+c;H=np.where(U>0,U,.01*U);Z=H@W+b;P=softmax(Z,axis=1);Gz=(P-Y)/len(X)
Gu=(Gz@W.T)*np.where(U>0,1.,.01)
grads=[X.T@Gu+lam*A,Gu.sum(0,keepdims=True),H.T@Gz+lam*W,Gz.sum(0,keepdims=True)]
params=[A,c,W,b]
def loss():
 u=X@A+c;h=np.where(u>0,u,.01*u);z=h@W+b
 return np.mean(logsumexp(z,axis=1)-np.sum(Y*z,axis=1))+.5*lam*(np.sum(A*A)+np.sum(W*W))
errors=[]
for par,g in zip(params,grads):
 fd=np.empty_like(par)
 for ix in np.ndindex(par.shape):
  old=par[ix];par[ix]=old+1e-6;plus=loss();par[ix]=old-1e-6;minus=loss();par[ix]=old;fd[ix]=(plus-minus)/2e-6
 errors.append(float(np.max(np.abs(g-fd))));assert np.allclose(g,fd,atol=1e-7)
checks['full-network-finite-difference']={'max_abs_error_by_parameter':errors,'batch':2,'regularization':lam}
u=np.array([.5,2.,-1.]);n=1.6;up=np.array([3.,-2.,4.]);pos=u>0
def objective(exponent):
 a=.01*u.copy();a[pos]=u[pos]**exponent;return up@a
analytic=np.sum(up[pos]*u[pos]**n*np.log(u[pos]));fd=(objective(n+1e-6)-objective(n-1e-6))/2e-6
record('shared exponent finite difference',analytic,fd)
F=15000;count=100;us=30;d=2;upeer=.7
cs=[count*F/us,F/d];p2p=[F/us,F/d,count*F/(us+count*upeer)]
record('distribution',[max(cs),max(p2p)],[50000,15000])
fig,axs=plt.subplots(1,2,figsize=(9,3.8))
axs[0].bar(['Server supply','Slowest download'],cs,color=['#456b8d','#93764b']);axs[0].set_title('Client-server')
axs[1].bar(['First copy','Slowest\ndownload','Aggregate\nupload'],p2p,color=['#448775','#93764b','#456b8d']);axs[1].set_title('P2P')
for ax in axs:ax.set_ylabel('Minimum time constraint (s)');ax.tick_params(axis='x',labelsize=9)
save(fig,N,'oct-distribution.png')
record('checksum',(~(35+78+84))&255,58)
record('stop wait utilization',.008/30.008,.00026659557451346305)
record('minimum full pipeline',np.ceil(30.008/.008),3751)
fig,ax=plt.subplots(figsize=(8,6));ax.set(xlim=(-.2,1.35),ylim=(11,0));ax.axis('off')
for xx,label in [(0,'Sender'),(1,'Receiver')]:ax.plot([xx,xx],[.5,10.7],color='#555',lw=1);ax.text(xx,.2,label,ha='center',fontweight='bold')
def arrow(x0,t0,x1,t1,label,color,dy=0,dashed=False):
 ax.annotate('',xy=(x1,t1),xytext=(x0,t0),arrowprops={'arrowstyle':'->','lw':1.8,'color':color,'linestyle':'--' if dashed else '-'})
 ax.text((x0+x1)/2,(t0+t1)/2+dy,label,ha='center',fontsize=10,color=color,bbox={'facecolor':'white','edgecolor':'none','alpha':.92})
arrow(0,1,1,10,'Original A(0): delayed','#a45b44',0,True)
arrow(0,2.4,1,3.4,'Retransmit A(0)','#456b8d',-.3)
arrow(1,3.8,0,4.8,'ACK0','#448775',0)
arrow(0,5.4,1,6.4,'New B(1)','#456b8d',0)
arrow(1,6.8,0,7.8,'ACK1','#448775',.2)
ax.text(1.03,3.4,'Deliver A\nexpect 1',va='center',fontsize=9)
ax.text(1.03,6.4,'Deliver B\nexpect 0',va='center',fontsize=9)
ax.text(1.03,10,'Old A appears new!\nDuplicate delivery',va='center',fontsize=9,color='#a45b44')
ax.text(-.05,2.3,'Timeout',ha='right',fontsize=9);ax.text(.45,10.8,'Time runs downward; timing is illustrative, not to scale.',ha='center',fontsize=9)
save(fig,N,'oct-alternating-bit.png')
# Foundation view: one bias receives contributions from each sample.
fig,ax=plt.subplots(figsize=(7,3.4));ax.axis('off')
labels=[('Sample 1',.16,.8),('Sample 2',.16,.3),('Shared bias b',.75,.55)]
for label,x0,y0 in labels:ax.text(x0,y0,label,ha='center',va='center',bbox={'boxstyle':'round,pad=.5','fc':'#eef2f3','ec':'#6c8090'})
for y0,label in [(.8,'gradient 1'),(.3,'gradient 2')]:ax.annotate(label,xy=(.65,.55),xytext=(.32,y0),arrowprops={'arrowstyle':'->'},fontsize=10)
ax.text(.73,.14,'Add contributions\n(db has the shape of b)',ha='center',fontsize=11)
save(fig,D,'oct-batch-bias.png')
(D/'october-example-results.json').write_text(json.dumps(checks,indent=2)+'\n')
print('Passed',len(checks),'independent numerical checks; generated 5 figures.')
