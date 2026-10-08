"""Check the new Lecture 2 supplements and draw one teaching figure.

Requires requirements-notebooks.txt, but reads no Canvas data and runs no Tutorial.
Run with --check to verify the saved numerical report without writing files.
"""
from pathlib import Path
import argparse, hashlib, importlib.metadata, json
import numpy as np
from scipy.stats import norm, multivariate_normal
from scipy.special import softmax
from scipy.integrate import quad

NOTES=Path(__file__).resolve().parents[1]
ROOT=NOTES.parents[1]
REPORT=ROOT/'docs/reviews/lecture02-teaching-2026-10-09/calculations.json'
FIGURE=NOTES/'assets/lecture02-boundary-variance.png'
MEANS=np.array([4.,6.]); PRIORS=np.array([.5,.5])

def calculate():
    x=np.linspace(-6,16,441)
    shared=norm.logpdf(x,6,1)-norm.logpdf(x,4,1)
    unequal=norm.logpdf(x,6,2)-norm.logpdf(x,4,1)
    np.testing.assert_allclose(shared,2*x-10,atol=1e-12)
    np.testing.assert_allclose(unequal,3*x*x/8-5*x/2+7/2-np.log(2),atol=1e-12)
    roots=np.sort(np.roots([3/8,-5/2,7/2-np.log(2)]))
    exact=np.array([(10-np.sqrt(16+24*np.log(2)))/3,(10+np.sqrt(16+24*np.log(2)))/3])
    np.testing.assert_allclose(roots,exact,atol=1e-12)
    np.testing.assert_allclose(norm.pdf(roots,4,1),norm.pdf(roots,6,2),atol=1e-12)
    probes=np.array([0.,4.,8.]); difference=norm.logpdf(probes,6,2)-norm.logpdf(probes,4,1)
    assert (np.where(difference>0,2,1)==[2,1,2]).all()
    points=np.array([[-2.,1.],[0.,0.],[1.,2.],[3.,-1.],[5.,4.]])
    first=multivariate_normal.logpdf(points,[0,0],np.diag([1,4]))
    second_shared=multivariate_normal.logpdf(points,[1,2],np.diag([1,4]))
    second_changed=multivariate_normal.logpdf(points,[1,2],np.diag([1,9]))
    shared_expected=points[:,0]+points[:,1]/2-1
    changed_expected=points[:,0]+5*points[:,1]**2/72+2*points[:,1]/9-13/18-np.log(1.5)
    np.testing.assert_allclose(second_shared-first,shared_expected,atol=1e-12)
    np.testing.assert_allclose(second_changed-first,changed_expected,atol=1e-12)
    risks=[]
    for priors in [[.5,.5],[.2,.8]]:
        probabilities=norm.pdf(probes,4,1)[:,None]*np.array(priors)
        posterior=probabilities/probabilities.sum(axis=1,keepdims=True)
        np.testing.assert_allclose(posterior,np.tile(priors,(len(probes),1)))
        # Integrate min(pi_1 f_1, pi_2 f_2), independently of the posterior cancellation.
        risk,error=quad(lambda t:min(priors[0]*norm.pdf(t,4,1),priors[1]*norm.pdf(t,4,1)),-np.inf,np.inf)
        assert abs(risk-min(priors))<1e-10
        risks.append({'priors':priors,'minimum_expected_error':risk,'integration_error_bound':error})
    q7_scores=np.array([-1+np.log(.8),-2/3-.5*np.log(.75)+np.log(.2)])
    q7_library=np.array([multivariate_normal.logpdf([1,1],[0,0],np.eye(2)),multivariate_normal.logpdf([1,1],[0,0],[[1,.5],[.5,1]])])+np.log([.8,.2])
    np.testing.assert_allclose(q7_scores,q7_library+np.log(2*np.pi),atol=1e-12)
    return {'one_dimension':{'means_cm':MEANS.tolist(),'priors':PRIORS.tolist(),'shared_variances_cm2':[1,1],'changed_variances_cm2':[1,4],'shared_threshold_cm':5.,'changed_thresholds_cm':roots.tolist(),'probe_x_cm':probes.tolist(),'probe_predictions':[2,1,2]},'two_dimensions':{'means':[[0,0],[1,2]],'first_variances':[1,4],'second_variances_I':[1,4],'second_variances_II':[1,9],'shared_boundary_coefficients':[1,.5,-1],'changed_x2_squared_coefficient':5/72,'probe_points':points.tolist(),'score_differences_I':(second_shared-first).tolist(),'score_differences_II':(second_changed-first).tolist()},'identical_distributions':risks,'Q7':{'scores_without_common_gaussian_constant':q7_scores.tolist(),'posteriors':softmax(q7_scores).tolist()}}

def draw(results):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import transforms
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':14,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
    colors=['#2870a2','#b57319']; grid=np.linspace(0,10,801)
    fig,axes=plt.subplots(1,2,figsize=(8,3.7),layout='constrained')
    for ax,std2,roots,title in zip(axes,[1,2],[[5],results['one_dimension']['changed_thresholds_cm']],['Shared variances','Only class 2 becomes wider']):
        ax.plot(grid,norm.pdf(grid,4,1),color=colors[0],lw=2,ls='-',label='Class 1')
        ax.plot(grid,norm.pdf(grid,6,std2),color=colors[1],lw=2,ls='--',label='Class 2')
        ax.set(xlim=(0,10),ylim=(0,.49),xticks=[0,2,4,6,8,10],yticks=[0,.1,.2,.3,.4],xlabel='Petal length (cm)',ylabel='Density (1/cm)',title=title)
        ax.tick_params(labelsize=13);ax.grid(alpha=.13)
        ax.legend(loc='upper right',bbox_to_anchor=(1,.87),fontsize=12.5,frameon=False,handlelength=1,handletextpad=.4,labelspacing=.35)
        stops=[0]+roots+[10]
        transform=transforms.blended_transform_factory(ax.transData,ax.transAxes)
        for left,right in zip(stops[:-1],stops[1:]):
            mid=(left+right)/2;label=2 if norm.logpdf(mid,6,std2)>norm.logpdf(mid,4,1) else 1
            ax.axvspan(left,right,ymin=.92,ymax=1,facecolor=colors[label-1],alpha=.18,edgecolor=colors[label-1],hatch='///' if label==2 else None,lw=.5)
            ax.text(mid,.96,str(label),transform=transform,ha='center',va='center',fontsize=13,weight='bold')
        for j,root in enumerate(roots):
            height=norm.pdf(root,4,1);ax.vlines(root,0,.45,color='#444444',ls=':',lw=1.2)
            ax.plot(root,height,'o',color='#333333',ms=4)
            y=.095 if len(roots)==1 else (.095 if j==0 else .275)
            ax.annotate(f'{root:.4f}'.rstrip('0').rstrip('.'),xy=(root,height),xytext=(root+(.45 if j==0 else .75),y),fontsize=12.5,ha='center',arrowprops={'arrowstyle':'-','color':'#555','lw':.7},bbox={'facecolor':'white','edgecolor':'none','alpha':.85,'pad':.5})
    FIGURE.parent.mkdir(exist_ok=True);fig.savefig(FIGURE,dpi=210,bbox_inches='tight');plt.close(fig)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();results=calculate()
    if args.check:
        saved=json.loads(REPORT.read_text())
        def compare(previous,current):
            if isinstance(current,dict):
                assert previous.keys()==current.keys()
                for key,value in current.items():compare(previous[key],value)
            elif isinstance(current,list):
                assert len(previous)==len(current)
                for a,b in zip(previous,current):compare(a,b)
            elif isinstance(current,(int,float)):
                np.testing.assert_allclose(previous,current,rtol=1e-10,atol=1e-12)
            else:assert previous==current
        compare(saved['results'],results)
        assert saved['figure_sha256']==hashlib.sha256(FIGURE.read_bytes()).hexdigest()
        print('Checked boundary models, classification regions, two-dimensional coefficients, Bayes error and Q7; no files written.');return
    draw(results)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps({'status':'passed','model_source':'explicit teaching parameters; no instructor dataset or notebook executed','methods':['manual expansion versus scipy.stats log densities','polynomial roots versus completed square','2D Gaussian scores versus expanded coefficients','quadrature versus constant Bayes risk','Q7 full Gaussian densities versus existing reduced scores'],'results':results,'versions':{p:importlib.metadata.version(p) for p in ['numpy','scipy','matplotlib']},'figure':'CS5489/course-notes/assets/lecture02-boundary-variance.png','figure_sha256':hashlib.sha256(FIGURE.read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+'\n')
    print('Generated one figure and verified the new teaching calculations.')
if __name__=='__main__':main()
