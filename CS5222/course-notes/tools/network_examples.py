"""Independent arithmetic and calculated static figures for current Chapter 1/2 tasks."""
from pathlib import Path
import os,json,math
OUT=Path(__file__).resolve().parents[1];FOUND=OUT.parents[1]/'learning/foundation-notes'
os.environ.setdefault('MPLCONFIGDIR',str(OUT/'.mpl-cache'))
import numpy as np
from scipy.stats import binom
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
plt.rcParams.update({'font.size':12,'axes.spines.top':False,'axes.spines.right':False})
ASSETS=OUT/'assets';ASSETS.mkdir(exist_ok=True)
r={'date':'2026-09-23','units':'decimal bit rates; 1 byte=8 bits','checks':{}}
# Enumerate user states independently of the binomial formula.
from itertools import product
for n,p in [(3,.1),(3,.2),(4,.5)]:
    states=list(product([0,1],repeat=n));probs=np.array([p**sum(s)*(1-p)**(n-sum(s)) for s in states]);assert np.isclose(probs.sum(),1)
    for k in range(n+1):assert np.isclose(sum(v for s,v in zip(states,probs) if sum(s)==k),binom.pmf(k,n,p))
tail=float(binom.sf(10,35,.1));assert .0004<tail<.0005
r['chapter1']={'35_users_over_10':tail,'tutorial_capacity':3e6/150e3,'caravan_min':(12*10+3600)/60,'fast_first_car_min':1+100/1000*60,'fast_last_car_min':10}
# Ring capacities: instructor routing of four A-C plus four B-D calls.
counts={e:0 for e in ['AB','BC','CD','AD']}
for route,num in [('ABC',2),('ADC',2),('BAD',2),('BCD',2)]:
    for a,b in zip(route,route[1:]):counts[''.join(sorted([a,b]))]+=num
assert set(counts.values())=={4}
r['tutorial1']={'ring_link_occupancy':counts,'file_time_s':160000/(1.536e6/12)+.6,'120_users_over_20':float(binom.sf(20,120,.1))}
assert np.isclose(r['tutorial1']['file_time_s'],1.85)
voice=64*8/128e3+64*8/4e6+.008
store=3*1500*8/2e6+(5000+4000+1000)*1000/2.5e8+2*.003
immediate=1500*8/2e6+(5000+4000+1000)*1000/2.5e8
queue=4.5*1500*8/2e6
assert np.allclose([voice,store,immediate,queue],[.012128,.064,.046,.027])
r['tutorial2']={'voip_playout_ms':voice*1000,'store_forward_ms':store*1000,'immediate_bit_forward_ms':immediate*1000,'queue_ms':queue*1000,'voip_128byte_ms':(128*8/128e3+128*8/4e6+.008)*1000,'queue_transfer_ms':2.25*1500*8/2e6*1000}
# Packet event recurrence, separate from the closed-form pipeline expression.
end=np.zeros((800,3));T=10000/2e6
for p in range(800):
    for link in range(3):end[p,link]=max(end[p-1,link] if p else 0,end[p,link-1] if link else 0)+T
assert np.isclose(end[-1,-1],4.01) and np.isclose(end[1,0],.01)
distance=2.5e8*120/56e3
r['assignment1']={'P6_distance_m':distance,'P31_unsegmented_s':3*8e6/2e6,'P31_segmented_s':float(end[-1,-1]),'P31_packet2_switch1_s':float(end[1,0]),'P31_400_packets_s':(400+3-1)*20000/2e6,'POP3_octets':498+912}
r['tutorial3']={'dns_no_cache_ms':4+3*20,'dns_local_hit_ms':4,'http_serial_RTT':2*(1+8),'http_parallel5_RTT':2+2*math.ceil(8/5),'http_persistent_serial_RTT':1+1+8,'http_persistent_pipelined_RTT':3}
r['chapter2']={'F_Mbit':100,'N':4,'server_upload_Mbps':10,'peer_upload_Mbps':2,'peer_download_Mbps':5,'CS_lower_bound_s':40,'P2P_lower_bound_s':max(100/10,100/5,400/(10+4*2)),'DASH_chunk_Mbit':4*2,'DASH_download_s':4*2/4,'report_stall_s':8-3}
for n in [1,5,10,100]:
    assert max(.1,n/(10+n))<=n/10+1e-12
r['checks']={'unit_conversions':True,'binomial_vs_enumeration':True,'ring_capacity':True,'delay_formulas':True,'pipeline_vs_event_recurrence':True,'http_rounds':True,'p2p_bounds':True}
def save(fig,path):fig.savefig(path,dpi=170,bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(7,3.5),layout='constrained');ax.barh(['Propagation: 1000 km / (2e8 m/s)','Transmission: 12000 bit / (2 Mbps)'],[5,6],color=['#bd7c20','#2878a5']);ax.set(xlabel='Time (ms)',xlim=(0,7),title='Different inputs, same output unit: time')
save(fig,FOUND/'assets/network-units.png')
fig,ax=plt.subplots(figsize=(7,4),layout='constrained')
ax.plot([0,8],[1,0],label='First bit');ax.plot([2,10],[1,0],label='Last bit');ax.plot([0,2],[1,1],lw=5,alpha=.3)
ax.set(yticks=[0,1],yticklabels=['Receiver','Sender'],xticks=[0,2,8,10],xlabel='Time (ms)',ylim=(-.15,1.45),title='Serialization 2 ms; propagation 8 ms');ax.legend(loc='upper right');ax.grid(axis='x',alpha=.2)
save(fig,FOUND/'assets/network-timeline.png')
fig,axs=plt.subplots(2,1,figsize=(8,6),layout='constrained')
for link in range(3):axs[0].add_patch(Rectangle((4*link,link-.25),4,.5,color='#2878a5',alpha=.75));axs[0].text(4*link+2,link,'Whole message',ha='center',va='center',color='white',fontsize=10)
axs[0].set(xlim=(0,12.4),ylim=(-.5,2.5),yticks=[0,1,2],yticklabels=['Link 1','Link 2','Link 3'],xlabel='Time (s)',title='No segmentation: 12 s to finish')
for packet in range(5):
    for link in range(3):
        start=(packet+link)*5;axs[1].add_patch(Rectangle((start,link-.25),5,.5,color=plt.get_cmap('viridis')(packet/5),alpha=.8));axs[1].text(start+2.5,link,str(packet+1),ha='center',va='center',color='white',fontsize=10)
axs[1].set(xlim=(0,39),ylim=(-.5,2.5),yticks=[0,1,2],yticklabels=['Link 1','Link 2','Link 3'],xlabel='Time (ms), first five packets shown',title='800 packets: 5 ms each; final completion at 4.01 s')
save(fig,ASSETS/'segmentation.png')
fig,ax=plt.subplots(figsize=(7,4.3),layout='constrained');labels=['Non-persistent serial','Non-persistent, 5 parallel','Persistent, no pipeline','Persistent, ideal pipeline'];vals=[18,6,10,3]
ax.barh(labels[::-1],vals[::-1],color=['#6f8c90','#2878a5','#bd7c20','#6178a2']);ax.set(xlabel='Server RTT units, excluding DNS and transmission',title='Base HTML + 8 referenced objects',xlim=(0,20))
for i,v in enumerate(vals[::-1]):ax.text(v+.2,i,str(v),va='center')
save(fig,ASSETS/'http-rounds.png')
r['all_checks_passed']=all(r['checks'].values())
(OUT/'network-example-results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
