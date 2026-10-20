"""Audit all searched candidates and compare search with a symmetry-reduced optimizer."""
import json
import time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from . import matrix
from .verify import check,digest


def reduced_search(spec,seed,budget=1200):
    rng=np.random.default_rng(seed)
    c=spec['constraints'];count=0;cache={};best=[np.inf,None];history=[]
    started=time.perf_counter()
    def evaluate(x):
        nonlocal count
        key=np.asarray(x).tobytes()
        if key in cache:return cache[key]
        count+=1
        k=np.tile([x[0],-x[1]],4)
        try:
            ev=matrix.evaluate(k,spec);g=matrix.margins(k,spec,ev);obj=ev['objective']
            if np.all(g>=-1e-8) and obj<best[0]:best[:]=[obj,k.copy()]
        except ValueError:
            obj=1e6;g=np.full(27,-1e3)
        cache[key]=(obj,g);history.append(dict(evaluations=count,incumbent=None if best[1] is None else best[0]))
        return obj,g
    # The warm start is the two family means of the same perturbed baseline.
    start=np.array([np.mean(spec['baseline_strengths_m_inv'][::2]),-np.mean(spec['baseline_strengths_m_inv'][1::2])])
    result=minimize(lambda x:evaluate(x)[0],start,method='SLSQP',
                    bounds=[(c['abs_k_min'],c['abs_k_max'])]*2,
                    constraints=[dict(type='ineq',fun=lambda x:evaluate(x)[1])],
                    options=dict(maxiter=80,eps=2e-7,ftol=1e-10))
    return dict(seed=seed,method='two-family-slsqp',evaluations=count,
                elapsed_s=time.perf_counter()-started,success=bool(result.success),
                best_strengths=best[1].tolist(),best_peak_beta_m=float(best[0]),history=history,
                note='Stops at solver convergence; seed does not alter deterministic family-mean start.')


def main():
    root=Path('results');specpath=Path('configs/nominal.json');spec=json.loads(specpath.read_text())
    candidates=root/'candidates';candidates.mkdir(exist_ok=True)
    report=[]
    for run in json.loads((root/'search.json').read_text()):
        path=candidates/f'{run["method"]}-{run["seed"]}.json'
        c=dict(schema='beamopt-candidate/v1',spec_sha256=digest(specpath),
               strengths_m_inv=run['best_strengths'],claimed_peak_beta_m=run['best_peak_beta_m'],
               provenance={k:run[k] for k in ['method','seed','evaluations']})
        path.write_text(json.dumps(c,indent=2)+'\n')
        result=check(path,specpath);report.append(result)
    reduced=reduced_search(spec,7)
    c=dict(schema='beamopt-candidate/v1',spec_sha256=digest(specpath),
           strengths_m_inv=reduced['best_strengths'],claimed_peak_beta_m=reduced['best_peak_beta_m'],
           provenance=dict(method=reduced['method'],evaluations=reduced['evaluations']))
    path=root/'reduced-candidate.json';path.write_text(json.dumps(c,indent=2)+'\n')
    report.append(check(path,specpath))
    (root/'trial'/'candidate-audit.json').write_text(json.dumps(report,indent=2)+'\n')
    (root/'trial'/'reduced-search.json').write_text(json.dumps(reduced,indent=2)+'\n')
    print(json.dumps(reduced,indent=2))

if __name__=='__main__':main()
