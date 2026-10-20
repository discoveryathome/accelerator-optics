"""Smooth epigraph reformulation of the peak-beta minimax objective.

The physical objective and acceptance gates are unchanged. A scalar t bounds every
beta sample. Unlike finite-differencing max(beta), the optimizer sees each smooth
active branch separately. Original baseline search is retained unchanged for comparison.
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from . import matrix
from .search import BudgetExhausted
from .verify import digest,check


def search(spec,seed,budget=None):
    rng=np.random.default_rng(seed);budget=budget or spec['search']['evaluation_budget']
    c=spec['constraints'];signs=np.array([1,-1]*4)
    bounds=[(c['abs_k_min'],c['abs_k_max']) if s>0 else (-c['abs_k_max'],-c['abs_k_min']) for s in signs]
    baseline=np.array(spec['baseline_strengths_m_inv']);cache={};history=[];count=0
    gate_size=len(matrix.margins(spec['reference_strengths_m_inv'],spec))
    best_value=np.inf;best_k=None;first_solver=None;started=time.perf_counter()
    def assess(k):
        nonlocal count,best_value,best_k
        key=np.asarray(k).tobytes()
        if key in cache:return cache[key]
        if count>=budget:raise BudgetExhausted()
        count+=1
        try:
            ev=matrix.evaluate(k,spec);g=matrix.margins(k,spec,ev);obj=ev['objective'];bet=ev['beta'].ravel()
            ok=bool(np.all(g>=-1e-8))
        except (ValueError,FloatingPointError):
            obj=1e6;g=np.full(gate_size,-1e3);bet=np.full(34,1e6);ok=False
        if ok and obj<best_value:best_value,best_k=float(obj),np.array(k)
        history.append(dict(evaluation=count,objective=float(obj),feasible=ok,incumbent=None if best_k is None else best_value))
        cache[key]=obj,g,bet
        return cache[key]
    assess(baseline)
    def constraint(x):
        _,g,bet=assess(x[:8]);return np.concatenate([g,x[-1]-bet])
    try:
        while count<budget:
            k=baseline if count==1 else np.clip(baseline+rng.normal(0,.025,8),np.array(bounds)[:,0],np.array(bounds)[:,1])
            start=np.r_[k,min(100.,assess(k)[0]+.1)]
            result=minimize(lambda x:x[-1],start,method='SLSQP',bounds=bounds+[(0.,100.)],
                            constraints=[dict(type='ineq',fun=constraint)],
                            options=dict(maxiter=120,ftol=1e-10,eps=2e-7))
            if first_solver is None:
                first_solver=dict(evaluations=count,success=bool(result.success),message=str(result.message),
                                  peak_beta_m=best_value,elapsed_s=time.perf_counter()-started)
    except BudgetExhausted:pass
    if best_k is None:raise ValueError('No feasible candidate')
    return dict(seed=seed,method='epigraph-slsqp',evaluations=count,elapsed_s=time.perf_counter()-started,
                best_strengths=best_k.tolist(),best_peak_beta_m=best_value,history=history,first_solver=first_solver)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--spec',nargs='+',default=['configs/nominal.json','results/longer-spec.json','results/alternating-spec.json'])
    parser.add_argument('--append',action='store_true')
    parser.add_argument('--output',default='results/trial/epigraph-search.json')
    args=parser.parse_args()
    root=Path('results');out=root/'trial'
    output=Path(args.output)
    rows=json.loads(output.read_text()) if args.append else []
    paths=[Path(p) for p in args.spec]
    for path in paths:
        spec=json.loads(path.read_text())
        for seed in spec['search']['seeds']:
            if any(r['family']==spec['id'] and r['seed']==seed for r in rows):continue
            run=search(spec,seed);run['family']=spec['id'];rows.append(run)
            candidate=dict(schema='beamopt-candidate/v1',spec_sha256=digest(path),strengths_m_inv=run['best_strengths'],
                           claimed_peak_beta_m=run['best_peak_beta_m'],provenance=dict(method=run['method'],seed=seed,budget=run['evaluations']))
            cp=out/f'epigraph-{spec["id"]}-{seed}.json';cp.write_text(json.dumps(candidate,indent=2)+'\n')
            run['verification']=check(cp,path)
            output.write_text(json.dumps(rows,indent=2)+'\n')
            print(f'{spec["id"]} seed={seed}: peak={run["best_peak_beta_m"]:.10f}; first_solver={run["first_solver"]}',flush=True)

if __name__=='__main__':main()
