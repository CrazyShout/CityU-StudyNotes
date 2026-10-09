"""Extract only required printed diagrams; draw clearly labelled teaching/clean graph figures."""
from pathlib import Path
import argparse,json,subprocess,hashlib,os,tempfile
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'cs5489-midterm-mpl'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--poppler',required=True,help='Path to pdftoppm')
p.add_argument('--source-dir',type=Path,required=True,help='External archive directory containing Sxxx.pdf source files')
args=p.parse_args()
CACHE=args.source_dir.resolve()
assert CACHE.is_dir(), 'External source directory does not exist'
OUT=ROOT/'assets';OUT.mkdir(exist_ok=True)
# Boxes are measured on the verified 110-dpi page render; extract at 220 dpi.
crops=[
 ('mt008-loss','S013',4,(110,365,515,370)),
 ('mt010-distribution','S013',5,(240,370,435,400)),
 ('mt012-l1-boundary','S013',6,(105,650,315,285)),
 ('mt026-loss','S012',4,(305,775,285,160)),
 ('mt031-rbf-points','S010',3,(250,255,355,130)),
 ('mt039-loss','S010',4,(290,865,330,165)),
 ('mt051-loss','S015',10,(310,235,285,150)),
 ('mt060-data','S016',6,(255,245,405,355)),
 ('answer-mt060-large-c','S016',6,(145,680,210,165)),
 ('answer-mt060-small-c','S016',6,(145,900,210,155)),
]
provenance=[]
catalog={item['id']:item for item in json.loads((ROOT/'SourceCatalog.json').read_text())['files']}
for sid in {entry[1] for entry in crops}:
    src=CACHE/(sid+'.pdf')
    assert src.is_file(), f'Missing original source {src.name}'
    assert hashlib.sha256(src.read_bytes()).hexdigest()==catalog[sid]['sha256'], f'Source hash mismatch: {sid}'
for name,sid,page,box in crops:
    src=CACHE/(sid+'.pdf');x,y,w,h=[int(2*v) for v in box]
    subprocess.run([args.poppler,'-f',str(page),'-l',str(page),'-r','220',
                    '-x',str(x),'-y',str(y),'-W',str(w),'-H',str(h),
                    '-singlefile','-png',str(src),str(OUT/name)],
                   check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    provenance.append({'file':name+'.png','source_id':sid,'source_page':page,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'box_at_110dpi':box,'kind':'printed question/answer figure crop'})

plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
def save(fig,name,info):
    fig.savefig(OUT/(name+'.png'),dpi=180,bbox_inches='tight',facecolor='white')
    plt.close(fig);provenance.append({'file':name+'.png',**info})

z=np.linspace(-6,6,1001)
fig,ax=plt.subplots(figsize=(6.2,3.6))
ax.plot(z,np.maximum(0,1-z),'k-',lw=1.8,label='hinge (SVM)')
ax.plot(z,np.logaddexp(0,-z)/np.log(2),'--',color='#3d6175',lw=1.8,label='logistic (LR, source scale)')
ax.plot(z,np.exp(-z),':',color='#945120',lw=2.1,label='exponential (AdaBoost)')
ax.axvline(0,color='#777',lw=.9,ls='--');ax.set(xlim=(-6,6),ylim=(0,9),xlabel='Signed score z = y f(x)',ylabel='Loss')
ax.text(-5.6,8.45,'Incorrectly classified',fontsize=9);ax.text(.5,8.45,'Correctly classified',fontsize=9)
ax.legend(loc='center right',fontsize=8);ax.grid(alpha=.2)
save(fig,'mt065-loss-comparison',{'source_id':'S030','source_page':6,'kind':'clean redraw of printed curves','formulae':['max(0,1-z)','log(1+exp(-z))/log(2)','exp(-z)'],'note':'LR normalization inferred from the printed curve: L(0)≈1 and a steeper far-negative tail than hinge. Handwritten annotations excluded.'})

fig,ax=plt.subplots(figsize=(6.3,2.05));ax.set(xlim=(-.8,6.2),ylim=(-.65,1.1));ax.axis('off')
for x,label in [(0,r'$g_1$'),(1.25,r'$z$'),(2.5,r'$g_2$'),(3.75,r'$f$'),(5,r'$L$')]:
    ax.add_patch(Circle((x,0),.24,fill=False,lw=1.3));ax.text(x,0,label,ha='center',va='center',fontsize=15)
for start,end in [(-.7,-.24),(.24,1.01),(1.49,2.26),(2.74,3.51),(3.99,4.76)]:
    ax.annotate('',(end,0),(start,0),arrowprops={'arrowstyle':'->','lw':1.3})
ax.text(-.75,0,r'$x$',ha='right',va='center',fontsize=15)
for x,label in [(0,r'$A$'),(2.5,r'$W$'),(5,r'$y$')]:
    ax.text(x,.86,label,ha='center',fontsize=15);ax.annotate('',(x,.24),(x,.72),arrowprops={'arrowstyle':'->','lw':1.3})
save(fig,'mt067-network',{'source_id':'S030','source_page':10,'kind':'clean redraw of printed forward graph','nodes':['x','g1','z','g2','f','L'],'parameter_arrows':['A -> g1','W -> g2','y -> L'],'note':'No student gradient labels or marking included.'})

fig,axes=plt.subplots(1,2,figsize=(6.4,2.5))
for ax in axes:ax.set_ylim(-.4,.4);ax.set_yticks([]);ax.grid(axis='x',alpha=.2)
axes[0].scatter([-1,1],[0,0],c='#b4433b',marker='+',s=120,label='+1')
axes[0].scatter([0],[0],facecolors='none',edgecolors='#286798',s=65,label='-1')
axes[0].set(xlim=(-1.5,1.5),xlabel='Input x',title='No single threshold')
axes[1].scatter([1],[0],c='#b4433b',marker='+',s=120)
axes[1].scatter([0],[0],facecolors='none',edgecolors='#286798',s=65)
axes[1].axvline(.5,color='#444',ls='--');axes[1].set(xlim=(-.3,1.3),xlabel=r'Mapped feature $\Phi(x)=x^2$',title='Linear threshold at 0.5')
axes[0].legend(loc='upper left',fontsize=8)
save(fig,'answer-kernel-map',{'kind':'teaching example for MT048','inputs':[-1,0,1],'labels':[1,-1,1],'feature':'x^2','threshold':.5})

r=np.linspace(-3,3,601);fig,ax=plt.subplots(figsize=(4.8,3))
ax.plot(r,np.where(r<0,4*r*r,r*r),color='#285f7f');ax.axvline(0,color='#888',lw=.7);ax.set(xlabel='r = prediction - truth',ylabel='Loss',title='Underprediction costs more')
ax.text(-2.8,7,'Too few bikes\nb = 4',fontsize=9);ax.text(.9,7,'Extra bikes\na = 1',fontsize=9);ax.set_ylim(0,12)
save(fig,'answer-asymmetric-loss',{'kind':'teaching plot for MT050','coefficients':{'underprediction':4,'overprediction':1}})

fig,ax=plt.subplots(figsize=(5.5,2.5));ax.set(xlim=(-6,2),ylim=(-.4,.6),xlabel='Input x');ax.set_yticks([])
ax.axvline(-5,color='#333',ls='--',label='Boundary x = -5')
ax.scatter([-1],[0],facecolors='none',edgecolors='#286798',s=70);ax.scatter([1],[0],c='#b4433b',marker='+',s=110)
ax.text(-1,.15,'True -1; predicted +1\nz = -0.4; loss = 0',ha='center',fontsize=8)
ax.text(1,-.25,'True +1\nz = 0.6; loss = 0',ha='center',fontsize=8)
ax.text(-4.1,.4,'Predict +1 on this side',fontsize=9);ax.legend(loc='lower left',fontsize=8)
save(fig,'answer-zero-loss-error',{'kind':'teaching counterexample for MT051','inputs':[-1,1],'labels':[-1,1],'w':.1,'b':.5,'loss':'max(0,-1-y*f(x))'})

fig,ax=plt.subplots(figsize=(5,3));h=np.where(np.abs(r)<1,.5*r*r,np.abs(r)-.5)
ax.plot(r,h,color='#285f7f',lw=1.8);ax.scatter([-1,0,1],[.5,0,.5],color='#333',s=15)
ax.axvline(-1,color='#aaa',ls=':',lw=.9);ax.axvline(1,color='#aaa',ls=':',lw=.9)
ax.set(xlabel='Residual r = truth - prediction',ylabel='Huber loss',ylim=(0,2.7))
save(fig,'answer-huber',{'kind':'plot of the exact supplied Huber formula for MT063/MT064','delta':1})

fig,axes=plt.subplots(1,2,figsize=(6.3,2.7))
for ax,name,title in zip(axes,['answer-mt060-large-c','answer-mt060-small-c'],['Large C (source sketch)','Smaller positive C (source sketch)']):
    ax.imshow(plt.imread(OUT/(name+'.png')));ax.axis('off');ax.set_title(title,fontsize=9)
fig.tight_layout(pad=.3)
save(fig,'answer-mt060-pair',{'kind':'side-by-side layout of the two original answer crops','source_id':'S016','source_page':6,'components':['answer-mt060-large-c.png','answer-mt060-small-c.png']})

(OUT/'figure-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(provenance),'figures with source/calculate provenance.')
