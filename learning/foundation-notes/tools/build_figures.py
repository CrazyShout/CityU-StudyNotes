"""Reproducible teaching figures; all examples are explicitly synthetic."""
from pathlib import Path
import os, json, hashlib

BASE = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(BASE / '.cache/matplotlib'))
import numpy as np
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

ASSETS = BASE / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)
BLUE, GOLD, INK, GREY = '#2878a5', '#bd7c20', '#253746', '#78818a'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14,
                     'axes.titlesize': 15, 'axes.labelsize': 14,
                     'legend.fontsize': 11, 'figure.facecolor': 'white',
                     'axes.spines.top': False, 'axes.spines.right': False})
figures = []
def save(fig, name, question, params):
    fig.savefig(ASSETS / name, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    figures.append({'file': 'assets/' + name, 'question': question, 'parameters': params,
                    'kind': 'synthetic_teaching_example',
                    'sha256': hashlib.sha256((ASSETS/name).read_bytes()).hexdigest()})
def grid(ax):
    ax.grid(alpha=.16)
    ax.set_axisbelow(True)

t = np.linspace(0, 4, 100)
fig, ax = plt.subplots(figsize=(6.2, 4.3), layout='constrained')
ax.plot(t, 2*t+1, color=BLUE, lw=2.3)
ax.scatter([0,1,2,3,4], [1,3,5,7,9], color=BLUE, s=42, zorder=4)
ax.plot([1,2,2], [3,3,5], '--', color=GOLD, lw=2)
ax.annotate('+1 min', (1.5,3), xytext=(1.5,1.8), ha='center', color=GOLD)
ax.annotate('+2 L', (2,4), xytext=(2.25,3.7), color=GOLD)
ax.annotate('V(0) = 1 L', (0,1), xytext=(.25,1.1), fontsize=12)
ax.set(title='A constant inflow: V(t) = 2t + 1', xlabel='Time t (min)', ylabel='Volume V (L)', xlim=(-.15,4.2), ylim=(0,10))
grid(ax)
save(fig,'tank-function.png','How do input, output and slope connect?',{'initial_litres':1,'litres_per_minute':2,'time_range_minutes':[0,4]})

fig, axs = plt.subplots(2,1,figsize=(6.2,7.2),layout='constrained')
ax=axs[0]
ax.plot([-.1,0,0,.5,.5,.6],[0,0,2,2,0,0],color=BLUE,lw=2.2)
ax.fill_between([.1,.3],0,2,color=GOLD,alpha=.35,hatch='//')
ax.text(.2,.8,'Area = 0.4',ha='center',fontsize=12)
ax.set(title='Uniform density on [0, 0.5]',xlabel='Waiting time x (min)',ylabel='Density (1/min)',xlim=(-.1,.6),ylim=(0,2.6))
grid(ax)
ax=axs[1];x=np.linspace(-3.5,3.5,500)
ax.plot(x,norm.pdf(x),color=BLUE,lw=2.2)
inside=np.linspace(-1,1,200)
ax.fill_between(inside,0,norm.pdf(inside),color=GOLD,alpha=.35,hatch='//')
ax.text(0,.14,'Area ≈ 0.6827',ha='center',fontsize=12)
ax.set(title='A curved density: standard normal',xlabel='Value z (unitless)',ylabel='Density',ylim=(0,.5))
grid(ax)
save(fig,'density-area.png','Why is probability an area rather than a height?',{'uniform_interval':[0,.5],'uniform_shaded_interval':[.1,.3],'normal_mean':0,'normal_std':1,'normal_shaded_interval':[-1,1],'normal_shaded_probability':float(norm.cdf(1)-norm.cdf(-1))})

fig,axs=plt.subplots(2,1,figsize=(6.2,7.2),layout='constrained')
x=np.linspace(-2,2,200);axs[0].plot(x,np.exp(x),color=BLUE,lw=2.2)
axs[0].scatter([0,1],[1,np.e],color=GOLD,zorder=4)
axs[0].annotate('(0, 1)',(0,1),xytext=(-8,12),textcoords='offset points',ha='right',fontsize=12)
axs[0].annotate('(1, e)',(1,np.e),xytext=(-8,12),textcoords='offset points',ha='right',fontsize=12)
axs[0].set(title='Exponent: y = exp(x)',xlabel='Exponent x',ylabel='Positive output y')
x=np.linspace(.08,4,400);axs[1].plot(x,np.log(x),color=BLUE,lw=2.2)
axs[1].scatter([1,np.e],[0,1],color=GOLD,zorder=4)
axs[1].annotate('(1, 0)',(1,0),xytext=(8,-22),textcoords='offset points',fontsize=12)
axs[1].annotate('(e, 1)',(np.e,1),xytext=(8,-22),textcoords='offset points',fontsize=12)
axs[1].axhline(0,color=GREY,lw=.8)
axs[1].set(title='Reverse question: y = ln(x)',xlabel='Positive input x',ylabel='Logarithm y',xlim=(0,4.1))
for ax in axs:grid(ax)
save(fig,'exp-log.png','What does it mean for exp and ln to be inverse functions?',{'exp_range':[-2,2],'log_range':[.08,4],'marked_pairs':[[0,1],[1,float(np.e)]]})

fig,ax=plt.subplots(figsize=(6.2,4.6),layout='constrained')
t=np.linspace(.65,3.1,400);ax.plot(t,1/t,color=BLUE,lw=2.2,label='Height = 1/t')
a=np.linspace(1,2,160);ax.fill_between(a,0,1/a,color=BLUE,alpha=.2,label='Area from 1 to 2 = ln 2')
b=np.linspace(2,2.2,50);ax.fill_between(b,0,1/b,color=GOLD,alpha=.4,hatch='//',label='Added area: 2 to 2.2')
ax.plot([2,2,2.2,2.2],[0,.5,.5,0],color=GOLD,ls='--',lw=1.5)
ax.text(1.45,.3,'ln 2 ≈ 0.6931',ha='center',fontsize=12)
ax.annotate('Height at 2: 1/2',(2,.5),xytext=(2.35,.8),arrowprops={'arrowstyle':'->','color':GOLD},fontsize=11)
ax.set(title='The local growth of ln(x)',xlabel='Positive coordinate t',ylabel='Height 1/t',xlim=(.65,3.1),ylim=(0,1.7));grid(ax);ax.legend(loc='upper right')
save(fig,'log-area.png','Why is the derivative of ln(x) equal to 1/x?',{'start':1,'x':2,'increment':.2,'log_x':float(np.log(2)),'added_area':float(np.log(2.2)-np.log(2)),'rectangle_approximation':.1})

fig,ax=plt.subplots(figsize=(6.2,4.6),layout='constrained')
x=np.linspace(1.5,3.1,200);ax.plot(x,x*x,color=BLUE,lw=2.3,label='Curve: x²')
ax.plot(x,4+4*(x-2),color=INK,lw=1.8,label='Tangent slope = 4')
for h,color,style in [(1,GOLD,'--'),(.25,GREY,':')]:
    ax.plot(x,4+(4+h)*(x-2),color=color,ls=style,lw=1.8,label=f'Secant h={h:g}: slope {4+h:g}')
    ax.scatter([2+h],[(2+h)**2],color=color,s=35,zorder=4)
ax.scatter([2],[4],color=INK,s=42,zorder=5)
ax.set(title='Closer points reveal the local slope',xlabel='Input x',ylabel='Output f(x)',xlim=(1.5,3.1),ylim=(1.8,10))
ax.legend(loc='upper left');grid(ax)
save(fig,'secant-tangent.png','How does an average slope approach a derivative?',{'function':'x^2','base_x':2,'secant_h':[1,.25],'derivative_at_base':4})

p=np.linspace(.005,.995,800);L=p**4*(1-p)**6;ell=4*np.log(p)+6*np.log1p(-p)
fig,axs=plt.subplots(2,1,figsize=(6.2,7.1),layout='constrained')
for ax,y,title,ylabel in [(axs[0],L,'Likelihood of the fixed label sequence','L(p)'),(axs[1],ell,'Natural log of the same likelihood','ln L(p)')]:
    ax.plot(p,y,color=BLUE,lw=2.2);ax.axvline(.4,color=GOLD,ls='--',lw=1.8,label='Maximum at p = 0.4')
    ax.set(title=title,xlabel='Candidate class probability p',ylabel=ylabel,xlim=(0,1));grid(ax);ax.legend(loc='lower center')
axs[0].ticklabel_format(axis='y',style='sci',scilimits=(0,0),useMathText=True)
save(fig,'likelihood-peak.png','Why do likelihood and log-likelihood select the same parameter?',{'class_1_count':4,'class_2_count':6,'p_range':[.005,.995],'maximum_p':.4,'L_max':.4**4*.6**6,'log_L_max':float(4*np.log(.4)+6*np.log(.6)),'binomial_coefficient_included':False})

X=np.array([[1,1],[2,3],[3,2],[4,4]],dtype=float)
fig,ax=plt.subplots(figsize=(6.2,3.5),layout='constrained');ax.axis('off')
table=ax.table(cellText=X.astype(int),rowLabels=['1','2','3','4'],colLabels=['Feature 1','Feature 2'],bbox=[.03,.18,.4,.62],cellLoc='center')
table.auto_set_font_size(False);table.set_fontsize(13)
for col in [0,1]:table[(2,col)].set_facecolor('#f1dfbe')
ax.text(.21,.91,'Data matrix X: 4 × 2',ha='center',fontsize=14)
ax.annotate('',xy=(.68,.48),xytext=(.48,.48),arrowprops={'arrowstyle':'->','color':GOLD,'lw':2})
ax.text(.58,.64,'Record 2',ha='center',fontsize=12)
ax.text(.83,.74,'Column vector',ha='center',fontsize=13)
vector=ax.table(cellText=[[2],[3]],bbox=[.79,.28,.1,.34],cellLoc='center')
vector.auto_set_font_size(False);vector.set_fontsize(16)
ax.text(.76,.45,'x₂ =',ha='right',va='center',fontsize=16)
ax.text(.82,.13,'Shape: 2 × 1',ha='center',fontsize=12)
save(fig,'records-vectors.png','How does one matrix row become one mathematical feature vector?',{'X':X.astype(int).tolist(),'selected_row_1based':2})

fig,ax=plt.subplots(figsize=(6.2,4.8),layout='constrained')
ax.scatter(X[:,0],X[:,1],c=BLUE,s=64,zorder=4)
for a,b in X:ax.annotate(f'({a:g}, {b:g})',(a,b),xytext=(5,9),textcoords='offset points',fontsize=12)
ax.axhline(2.5,color=GREY,ls='--',lw=1);ax.axvline(2.5,color=GREY,ls='--',lw=1)
ax.scatter([2.5],[2.5],marker='x',s=85,c=GOLD,linewidths=2,label='Mean (2.5, 2.5)',zorder=5)
ax.set(title='Covariance uses deviations from the mean',xlabel='Feature 1 (unitless)',ylabel='Feature 2 (unitless)',xlim=(.4,4.7),ylim=(.4,4.7));ax.set_aspect('equal');grid(ax);ax.legend(loc='lower right')
save(fig,'covariance-data.png','What is being multiplied when covariance is computed?',{'X':X.astype(int).tolist(),'mean':X.mean(0).tolist(),'covariance_ddof0':np.cov(X,rowvar=False,ddof=0).tolist()})

A=np.array([[2,1],[0,1]]);square=np.array([[0,0],[1,0],[1,1],[0,1]])
fig,axs=plt.subplots(2,1,figsize=(6.2,6.4),layout='constrained')
for ax,pts,title,color,area in [(axs[0],square,'Input: unit square',BLUE,1),(axs[1],square@A.T,'After A = [[2, 1], [0, 1]]',GOLD,2)]:
    ax.add_patch(Polygon(pts,closed=True,facecolor=color,alpha=.18,edgecolor='none'))
    q=np.vstack([pts,pts[0]]);ax.plot(q[:,0],q[:,1],color=color,lw=2.2)
    center=pts.mean(0);ax.text(*center,f'Area = {area}',ha='center',va='center',fontsize=13)
    ax.set(title=title,xlabel='First coordinate',ylabel='Second coordinate',xlim=(-.3,3.3),ylim=(-.35,1.45));ax.set_aspect('equal');grid(ax)
save(fig,'determinant-area.png','How does a determinant describe area scaling?',{'A':A.tolist(),'input_vertices':square.tolist(),'output_vertices':(square@A.T).tolist(),'determinant':2})

data={'scope':'Author-created mathematical teaching examples, not measurements or assignment results',
      'generator':'tools/build_figures.py','figures':figures,
      'reused_figure':{'path':'../../CS5489/course-notes/assets/covariance-shapes.png',
                       'source':'Lecture2b cell 36; existing checked redraw',
                       'condition':'Mean zero, unit marginal variances, squared Mahalanobis distance 4; not a 95% region'}}
(BASE/'figure-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(f'Generated {len(figures)} reproducible teaching figures and figure-data.json.')
