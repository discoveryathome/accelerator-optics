"""Standalone scientific plots from saved, recomputed results."""
import argparse
import json
from pathlib import Path
import os
os.environ.setdefault("MPL_IGNORE_SYSTEM_FONTS", "1")
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from . import matrix


def dense_envelope(k,spec):
    ev=matrix.evaluate(k,spec)
    s,beta=[0.],[ev['beta'][0]]
    for i,length in enumerate(spec['drifts_m']):
        # Immediately after lens i; inside its following drift.
        b=ev['beta'][2*i+1];a=ev['alpha'][2*i+1];g=(1+a*a)/b
        local=np.linspace(0,length,60)
        for t in local:
            s.append(ev['s'][2*i+1]+t);beta.append(b-2*a*t+g*t*t)
    return np.array(s),np.array(beta)


def main():
    p=argparse.ArgumentParser();p.add_argument('--spec',default='configs/nominal.json');p.add_argument('--out',default='results')
    args=p.parse_args();out=Path(args.out);spec=json.loads(Path(args.spec).read_text())
    k=json.loads((out/'candidate.json').read_text())['strengths_m_inv']
    configs={'Reference':spec['reference_strengths_m_inv'],'Perturbed baseline':spec['baseline_strengths_m_inv'],'Candidate':k}
    analytic=out/'analytic-candidate.json'
    if analytic.exists(): configs['Symmetry control']=json.loads(analytic.read_text())['strengths_m_inv']
    fig,axs=plt.subplots(2,2,figsize=(12,7),sharex=True,layout='constrained')
    for name,kk in configs.items():
        s,b=dense_envelope(kk,spec)
        for j in range(2):
            axs[0,j].plot(s,b[:,j],label=name)
            axs[1,j].plot(s,1e3*6*np.sqrt(spec['geometric_emittance_m']*b[:,j]),label=name)
    for j,plane in enumerate(['x','y']):
        axs[0,j].set_title(f'{plane} plane');axs[0,j].set_ylabel('Periodic beta [m]')
        axs[1,j].set_ylabel('Matched 6-sigma envelope [mm]');axs[1,j].set_xlabel('s [m]')
        axs[1,j].axhline(20,color='black',linestyle=':',label='Aperture half-width')
        for ax in axs[:,j]:ax.grid(alpha=.25)
    axs[0,0].legend();axs[1,0].legend()
    fig.suptitle('Fixed-geometry FODO channel: linear optics and matched envelope')
    for ext in ['png','svg']:fig.savefig(out/f'optics-envelope.{ext}',dpi=160)
    plt.close(fig)
    runs=json.loads((out/'search.json').read_text());fig,ax=plt.subplots(figsize=(8,4.8),layout='constrained')
    extra=out/'trial'/'epigraph-search.json'
    if extra.exists():runs += [r for r in json.loads(extra.read_text()) if r['family']=='nominal']
    colors={'random':'#b96928','slsqp':'#176f9a','epigraph-slsqp':'#268445'}
    for run in runs:
        h=run['history'];ax.plot([r['evaluation'] for r in h],[np.nan if r['incumbent'] is None else r['incumbent'] for r in h],
                               color=colors[run['method']],alpha=.7,label=f'{run["method"]}, seed {run["seed"]}')
    ref=matrix.evaluate(spec['reference_strengths_m_inv'],spec)['objective']
    ax.axhline(ref,color='black',linestyle='--',label='Textbook 60 degree reference')
    ax.set(xlabel='Unique full evaluations',ylabel='Best feasible peak beta [m]',title='Equal evaluation budgets; hard constraint gates')
    ax.legend(fontsize=8);ax.grid(alpha=.25);fig.savefig(out/'search.png',dpi=160);plt.close(fig)
    if (out/'tracking.json').exists():
        rows=json.loads((out/'tracking.json').read_text());fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
        scenarios=['matched','common_injection','mismatch','errors']
        for i,name in enumerate(['reference','baseline','candidate']):
            selected=[[r for r in rows if r['configuration']==name and r['scenario']==sc] for sc in scenarios]
            for j,key in enumerate(['survival','emittance_ratio']):
                vals=[[r[key] if j==0 else max(r[key]) for r in group] for group in selected]
                mean=np.mean(vals,axis=1);err=np.std(vals,axis=1)
                axs[j].errorbar(np.arange(4)+(i-1)*.12,mean,yerr=err,marker='o',label=name)
        for ax in axs:
            ax.set_xticks(range(4),scenarios,rotation=15);ax.grid(alpha=.25);ax.legend()
        axs[0].set_ylabel('Surviving fraction');axs[1].set_ylabel('Max projected emittance ratio (x or y)')
        fig.suptitle('Finite 1024-particle, 256-period tests; error bars: seed standard deviation')
        fig.savefig(out/'tracking.png',dpi=160);plt.close(fig)

if __name__=='__main__':
    main()
