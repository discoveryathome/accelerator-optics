"""Reasoning-driven controls and held-out numerical checks, separate from original search."""
import copy
import json
import time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
from . import matrix
from .verify import digest,check


def control(spec, preserve=False):
    # Equal-spacing FODO theorem: sin(mu_cell/2)=k1L*Lcell/4.
    # On this small phase interval beta_max decreases as phase increases.
    # Enforce both tune and natural-chromaticity budgets analytically.
    ncell=4;Lcell=2*spec['drifts_m'][0]
    target=np.min(spec['constraints']['tune_target'])
    qmax=target if preserve else target+spec['constraints']['tune_tolerance']
    chmax=np.min(spec['constraints']['chromaticity_abs_max'])
    qchrom=ncell/np.pi*np.arctan(chmax*np.pi/ncell)
    q=min(qmax,qchrom)-1e-9
    magnitude=4/Lcell*np.sin(np.pi*q/ncell)
    k=np.array([magnitude,-magnitude]*4)
    ev=matrix.evaluate(k,spec)
    assert matrix.feasible(k,spec)
    return k,ev


def main():
    spec_path=Path('configs/nominal.json');spec=json.loads(spec_path.read_text())
    out=Path('results');trial=out/'trial';trial.mkdir(exist_ok=True)
    start=time.perf_counter();k,ev=control(spec)
    elapsed=time.perf_counter()-start
    c=dict(schema='beamopt-candidate/v1',spec_sha256=digest(spec_path),strengths_m_inv=k.tolist(),
           claimed_peak_beta_m=ev['objective'],provenance=dict(method='analytic-symmetric-control',evaluations=1,elapsed_s=elapsed))
    path=out/'analytic-candidate.json';path.write_text(json.dumps(c,indent=2)+'\n')
    verification=check(path,spec_path)
    configs={'reference':spec['reference_strengths_m_inv'],'baseline':spec['baseline_strengths_m_inv'],
             'slsqp_candidate':json.loads((out/'candidate.json').read_text())['strengths_m_inv'],
             'analytic_control':k.tolist()}
    rows=[]
    for name,kk in configs.items():
        e=matrix.evaluate(kk,spec)
        # Fully held-out grid, 100x denser than nominal momentum contract.
        grid=np.linspace(-.02,.02,401)
        dense=[matrix.optics(kk,spec['drifts_m'],d) for d in grid]
        chrom_steps={}
        for h in [1e-3,1e-4,1e-5,1e-6]:
            a=matrix.optics(kk,spec['drifts_m'],h)['tune']
            b=matrix.optics(kk,spec['drifts_m'],-h)['tune']
            chrom_steps[str(h)]=(((a-b+.5)%1-.5)/(2*h)).tolist()
        strict=copy.deepcopy(spec)
        strict['constraints']['tune_tolerance']=1e-6
        strict['constraints']['chromaticity_abs_max']=[4*np.tan(np.pi/6)/np.pi+1e-6]*2
        rows.append(dict(configuration=name,metrics=matrix.serializable(e),
                         nominal_feasible=matrix.feasible(kk,spec),
                         reference_preserving_feasible=matrix.feasible(kk,strict),
                         dense_delta_points=len(grid),dense_max_trace=float(np.max(np.abs([d['trace'] for d in dense]))),
                         dense_peak=np.max([d['peak'] for d in dense],axis=0).tolist(),
                         chromaticity_steps=chrom_steps))
    summary=dict(control_candidate=c,verification=verification,configurations=rows,
                 note='Symmetric control is a textbook-derived comparator, not a novel discovery. Strict-reference gates are a separate diagnostic, not a change to nominal scoring.')
    (trial/'controls.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({r['configuration']:{'peak':r['metrics']['objective'],'tune':r['metrics']['tune'],
                     'chromaticity':r['metrics']['chromaticity'],'strict_reference_feasible':r['reference_preserving_feasible']} for r in rows},indent=2))

if __name__=='__main__':
    main()
