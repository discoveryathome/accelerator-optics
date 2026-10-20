"""Figures for the fixed-injection diagnostic and aperture stress test."""
import json
import os
from pathlib import Path
os.environ.setdefault('MPL_IGNORE_SYSTEM_FONTS','1')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from . import matrix
from .plots import dense_envelope


def main():
    root=Path('results');spec=json.loads((root/'injection-spec.json').read_text())
    configs={'Reference':spec['reference_strengths_m_inv'],
             'Optimize width alone':json.loads((root/'irregular/candidate.json').read_text())['strengths_m_inv'],
             'Also preserve injection':json.loads((root/'trial/epigraph-injection-7.json').read_text())['strengths_m_inv']}
    colors=['#6b7280','#d27928','#14836e'];names=['reference','free_entrance','fixed_entrance']
    rows=json.loads((root/'trial/injection-tracking.json').read_text())['tracking']
    fig,axs=plt.subplots(2,2,figsize=(11,7.4),layout='constrained')
    values=[]
    for (name,k),color in zip(configs.items(),colors,strict=True):
        s,b=dense_envelope(k,spec);ev=matrix.evaluate(k,spec);values.append(ev['objective'])
        for plane in range(2):axs[0,plane].plot(s,6e3*np.sqrt(spec['geometric_emittance_m']*b[:,plane]),label=name,color=color,lw=2)
    for plane in range(2):
        axs[0,plane].axhline(20,color='black',ls=':',lw=1,label='Aperture half-width')
        axs[0,plane].set(xlabel='Distance [m]',ylabel='Matched 6-sigma envelope [mm]',title=['Horizontal plane','Vertical plane'][plane])
        axs[0,plane].grid(alpha=.2)
    axs[0,0].legend(fontsize=8)
    widths=100*np.sqrt(np.array(values)/values[0]);axs[1,0].bar(range(3),widths,color=colors,width=.65)
    axs[1,0].set(ylim=(0,110),ylabel='Maximum matched width [% of reference]',title='A smaller envelope is only part of the goal')
    for i,v in enumerate(widths):axs[1,0].text(i,v+2,f'{v:.1f}%',ha='center',fontsize=10)
    means=[];errs=[]
    for n in names:
        rr=[100*(max(r['emittance_ratio'])-1) for r in rows if r['configuration']==n and r['scenario']=='common_injection']
        means.append(np.mean(rr));errs.append(np.std(rr))
    axs[1,1].bar(range(3),means,color=colors,width=.65,yerr=errs,capsize=4)
    axs[1,1].axhline(0,color='black',lw=1);axs[1,1].set(ylabel='Projected emittance change [%]',title='Same injected beam; 3 fresh tracking seeds',ylim=(-2,25))
    for i,v in enumerate(means):axs[1,1].text(i,v+1.2,f'{v:+.1f}%',ha='center',fontsize=10)
    for ax in axs[1]:ax.set_xticks(range(3),['Reference','Width\nobjective','Fixed\ninjection'])
    fig.suptitle('Narrow the beam without sacrificing its quality\nSynthetic irregular lattice; Xsuite tracking with momentum spread',fontsize=15)
    fig.savefig(root/'injection-tradeoff.png',dpi=160);plt.close(fig)
    stress=json.loads((root/'trial/aperture-stress.json').read_text())
    fig,ax=plt.subplots(figsize=(8,4.8),layout='constrained')
    for name,label in [('reference','Textbook reference'),('baseline','Perturbed baseline'),('analytic','Symmetry control')]:
        means=[];errs=[]
        for a in [.006,.008,.012,.02]:
            rr=[100*r['survival'] for r in stress if r['configuration']==name and r['aperture_half_width_m']==a]
            means.append(np.mean(rr));errs.append(np.std(rr))
        ax.errorbar([6,8,12,20],means,yerr=errs,marker='o',label=label)
    ax.set(xlabel='Aperture half-width [mm]',ylabel='Surviving particles [%]',title='Recovery over perturbed settings; negligible gain over reference')
    ax.legend();ax.grid(alpha=.2);fig.savefig(root/'aperture-stress.png',dpi=160);plt.close(fig)

if __name__=='__main__':main()
