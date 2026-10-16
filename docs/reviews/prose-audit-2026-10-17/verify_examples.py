"""Recalculate existing examples whose question wording/conditions were clarified.

Only explicit teaching numbers are used. No dataset, training or network probe.
"""
from pathlib import Path
import argparse
import json
import math
import numpy as np


def calculate():
    checks = []
    def record(name, actual, expected, atol=1e-7):
        assert np.allclose(actual, expected, rtol=1e-6, atol=atol), (name, actual, expected)
        checks.append({'case': name, 'actual': np.asarray(actual).tolist(),
                       'expected': np.asarray(expected).tolist()})
    x = 2
    x += 3
    x *= 2
    record('Lecture1 multiplication-assignment question', x, 10)
    point = np.array([1., 1.])
    covariances = [np.eye(2), np.array([[1., .5], [.5, 1.]])]
    scores = np.array([-.5*point @ np.linalg.solve(cov, point)
                       -.5*np.linalg.slogdet(cov)[1] + math.log(prior)
                       for cov, prior in zip(covariances, [.8, .2])])
    posterior = np.exp(scores - scores.max())
    posterior /= posterior.sum()
    record('Lecture2 Q7 covariance and prior conditions',
           [*scores, *posterior], [-1.22314355, -2.1323, .7128, .2872], atol=5e-5)
    p = np.array([2., 3., 5.]) / 10
    record('Lecture5 logit scaling', np.exp(2*np.log([2.,3.,5.]))/38, [4/38,9/38,25/38])
    record('Lecture5 true-class-2 gradient', p - [0,1,0], [.2,-.7,.5])
    record('Lecture5 parameter count with biases', (4+1)*3+(3+1)*2, 23)
    v, theta = 0., 1.
    for g in [2.,2.]:
        v = .9*v + .1*g
        theta -= v
    record('Lecture5 two momentum steps', [v,theta], [.38,.42])
    record('Tutorial1 nontrivial divisor counts', [sum(n%d==0 for d in range(2,n)) for n in [9,13]], [1,0])
    record('Tutorial3 alternate crop', (41-17)*(32-8), 576)
    record('Assignment2 input and exponent gradients', [3*2*.5,3*.5**2*math.log(.5)], [3,-.5198603854199589])
    record('Network Tutorial1 five packets, three links, in L/R units', 5+3-1, 7)
    record('Network Tutorial1 FDM setup plus serialization, seconds', .6+320000/(1.536e6/12), 3.1)
    record('Network Tutorial2 128-byte voice packets, milliseconds', 1000*(128*8/128000+128*8/4e6+.008), 16.256)
    record('Network Tutorial2 forwarding models, milliseconds', [3+4*2,4*3+4*2], [11,20])
    record('Network Tutorial2 FIFO waiting, milliseconds', (1-.75+2)*1500*8/2e6*1000, 13.5)
    record('Network Tutorial3 sequential DNS, milliseconds', [4+3*20,4], [64,4])
    record('Network Tutorial3 HTTP RTT coefficient excluding DNS', 2+2*math.ceil(6/4), 6)
    record('Chapter2 zero-peer-upload P2P lower bound, seconds', max(100/10,100/5,4*100/10), 40)
    holdings = [set('AB'),set('AC')]
    record('Chapter2 rarest-first counts after P2 leaves', [sum(c in h for h in holdings) for c in 'ABC'], [2,1,1])
    record('Chapter3 100-Mbps stop-and-wait throughput, Mbps', 8000/(.03+8000/1e8)/1e6, .26595744680851063)
    e = .875*100+.125*80
    d = .75*10+.25*abs(80-e)
    record('Chapter3 new-E-first RTO, milliseconds', [e,d,e+4*d], [97.5,11.875,145])
    record('Network Tutorial4 ten-peer capacity bounds, seconds',
           [max(10*15000/30,15000/2), max(15000/30,15000/2,10*15000/(30+10*.7))], [7500,7500])
    record('Network Tutorial4 DASH stored file counts', [4*2,4+2], [8,6])
    record('Network Assignment1 equal-delay distance, km', 2.5e8*240/56000/1000, 1071.4285714285713)
    record('Network Assignment1 400-packet pipeline, seconds', (400+3-1)*20000/2e6, 4.02)
    record('Network Assignment1 retained message octets', 498+912-498, 912)
    record('Research guide whole-chunk download and stall, seconds', [4*2/1, max(0,4*2/1-3)], [8,5])
    record('Math water tank inverse question', [1+2*2.5,(8-1)/2], [6,3.5])
    u, v = np.array([2.,3.]), np.array([4.,1.])
    record('Math inner product uTv', u@v, 11)
    record('Math outer product uuT', np.outer(u,u), [[4,6],[6,9]])
    a = np.array([[1.,1.],[2.,2.]])
    record('Math pseudoinverse maps target to minimum-norm solution', np.linalg.pinv(a)@[4,8], [2,2])
    record('Network foundation four-packet three-link pipeline, milliseconds', (4+3-1)*2, 12)
    return {'status':'passed', 'scope':'existing examples with clarified wording; no new experimental results',
            'cases':checks}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = calculate()
    if args.output:
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f"Passed {len(result['cases'])} independent teaching-example recalculations.")
