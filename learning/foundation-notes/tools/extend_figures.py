"""Deterministic diagrams and independent arithmetic for the added foundations."""
from pathlib import Path
import os,json,math
OUT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(OUT/'.mpl-cache'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import binom
ASSETS=OUT/'assets';ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({'font.size':12,'axes.spines.top':False,'axes.spines.right':False})
data={'date':'2026-09-23','source':'Teaching examples supplementing current course prerequisites','figures':{},'all_checks_passed':True}
def save(fig,name,params):
    fig.savefig(ASSETS/name,dpi=170,bbox_inches='tight');plt.close(fig);data['figures'][name]=params
k=np.arange(4)
fig,ax=plt.subplots(figsize=(7,4),layout='constrained')
for p,offset in [(.2,-.18),(.5,.18)]:
    probs=binom.pmf(k,3,p);assert np.isclose(probs.sum(),1)
    ax.bar(k+offset,probs,width=.34,label=f'p={p}')
assert np.isclose(binom.sf(2,4,.5),5/16)
ax.set(xticks=k,xlabel='Number of active users K (out of 3)',ylabel='Probability P(K=k)',title='Independent users; common activity probability p');ax.legend()
save(fig,'binomial-users.png',{'n':3,'p':[.2,.5],'transfer_probability':5/16})
fig,ax=plt.subplots(figsize=(6.4,4.4),layout='constrained')
for v,label,col in [(np.array([2,1]),'v = (2, 1)','#2878a5'),(np.array([2,0]),'p = (2, 0)','#bd7c20')]:
    ax.annotate('',xy=v,xytext=(0,0),arrowprops={'arrowstyle':'->','color':col,'lw':2});ax.text(v[0]-.15,v[1]+.10,label,color=col,ha='right')
ax.plot([2,2],[0,1],'--',color='gray');ax.text(2.05,.45,'r = (0, 1)')
ax.set(xlim=(-.3,3.15),ylim=(-.3,1.55),xlabel='Coordinate 1',ylabel='Coordinate 2',title='Project v onto the horizontal direction u=(1, 0)');ax.set_aspect('equal');ax.grid(alpha=.2)
u=np.array([1,1]);v=np.array([3,1]);p=u*(u@v)/(u@u);r=v-p
assert np.allclose(p,[2,2]) and np.isclose(u@r,0)
u2=np.array([1,-1]);v2=np.array([4,2]);p2=u2*(u2@v2)/(u2@u2);assert np.allclose(p2,[1,-1])
save(fig,'vector-projection.png',{'illustration_u':[1,0],'illustration_v':[2,1],'worked_projection':p.tolist(),'transfer_projection':p2.tolist()})
fig,axs=plt.subplots(1,2,figsize=(9,4),layout='constrained')
A=np.array([[1.,1.],[2.,2.]]);y=np.array([3.,5.]);w=np.linalg.pinv(A)@y;fit=A@w;res=y-fit
assert np.allclose(w,[1.3,1.3]) and np.isclose(A[:,0]@res,0)
for ax in axs:ax.set(xlim=(-.3,3.6),ylim=(-.3,6.5),xlabel='Coordinate 1',ylabel='Coordinate 2');ax.grid(alpha=.2)
t=np.linspace(0,3.2,30)
axs[0].plot(t,2*t,alpha=.4);axs[0].annotate('',xy=(1,2),xytext=(0,0),arrowprops={'arrowstyle':'->','lw':3});axs[0].text(1.1,2,'a1 = a2 = (1, 2)');axs[0].set_title('Two columns, only one direction')
axs[1].plot(t,2*t,alpha=.4);axs[1].scatter([y[0],fit[0]],[y[1],fit[1]]);axs[1].plot([y[0],fit[0]],[y[1],fit[1]],'--')
axs[1].annotate('y=(3,5)',y,xytext=(3.1,4.25));axs[1].annotate('Aw=(2.6,5.2)',fit,xytext=(.6,5.7),arrowprops={'arrowstyle':'->'});axs[1].set_title('Least squares reaches the closest point')
save(fig,'rank-projection.png',{'A':A.tolist(),'y':y.tolist(),'minimum_norm_w':w.tolist(),'residual':res.tolist()})
fig,axs=plt.subplots(1,2,figsize=(9,4),layout='constrained')
x=np.linspace(-1.5,1.5,160);a,b=np.meshgrid(x,x);axs[0].contour(a,b,a*a+2*b*b,levels=[.3,1,1.36,3,5]);axs[0].annotate('',xy=(.8,.6),xytext=(1,1),arrowprops={'arrowstyle':'->','color':'#bd7c20','lw':2});axs[0].scatter([1,.8],[1,.6]);axs[0].text(1,1.1,'E=3');axs[0].text(.8,.4,'E=1.36');axs[0].set(xlabel='w1',ylabel='w2',title='One step with learning rate 0.1')
x=np.linspace(-1,3,200);axs[1].plot(x,x*x);axs[1].axvspan(1,3,alpha=.15,color='#2878a5');axs[1].scatter([0,1],[0,1]);axs[1].annotate('Best feasible point (1,1)',(1,1),xytext=(.4,5),arrowprops={'arrowstyle':'->'});axs[1].set(xlabel='x',ylabel='f(x)=x squared',title='Constraint x >= 1 (shaded region)')
assert np.isclose(.8**2+2*.6**2,1.36)
save(fig,'gradient-constraint.png',{'gradient_at_1_1':[2,4],'eta':.1,'next':[.8,.6],'objective_after':1.36,'constraint_optimum':1,'lambda':2})
(OUT/'extra-figure-data.json').write_text(json.dumps(data,indent=2)+'\n')
print('Verified and generated',len(data['figures']),'foundation figures')
