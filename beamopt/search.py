"""Budgeted multistart SLSQP and random-search control, identical hard gates."""
import argparse
import json
import time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from . import matrix
from .verify import digest


class BudgetExhausted(Exception):
    pass


def search(spec, seed, method='slsqp'):
    rng = np.random.default_rng(seed)
    budget = spec['search']['evaluation_budget']
    c = spec['constraints']
    signs = np.array([1,-1]*4)
    bounds = [(c['abs_k_min'],c['abs_k_max']) if s>0 else (-c['abs_k_max'],-c['abs_k_min']) for s in signs]
    baseline = np.array(spec['baseline_strengths_m_inv'])
    count, history, cache = 0, [], {}
    best_k, best_value = None, np.inf
    started = time.perf_counter()
    gate_size = len(matrix.margins(spec['reference_strengths_m_inv'],spec))
    def assess(k):
        nonlocal count,best_k,best_value
        key = np.asarray(k).tobytes()
        if key in cache:
            return cache[key]
        if count>=budget:
            raise BudgetExhausted()
        count += 1
        try:
            ev = matrix.evaluate(k,spec)
            g = matrix.margins(k,spec,ev)
            obj = ev['objective']
            ok = bool(np.all(g>=-1e-8))
        except (ValueError,FloatingPointError):
            obj,g,ok = 1e6,np.full(gate_size,-1e3),False
        if ok and obj < best_value:
            best_value,best_k = float(obj),np.array(k)
        history.append(dict(evaluation=count,objective=float(obj),feasible=ok,
                            incumbent=None if best_k is None else best_value))
        cache[key] = obj,g
        return obj,g
    assess(baseline)
    try:
        if method=='random':
            while True:
                # Equal budget, mixture of local and broad perturbations; no reference injection.
                scale = .01 if count%2 else .06
                k = np.clip(baseline+rng.normal(0,scale,8),np.array(bounds)[:,0],np.array(bounds)[:,1])
                assess(k)
        else:
            while count<budget:
                start = baseline if count==1 else np.clip(baseline+rng.normal(0,.025,8),np.array(bounds)[:,0],np.array(bounds)[:,1])
                minimize(lambda k:assess(k)[0],start,method='SLSQP',bounds=bounds,
                         constraints=[dict(type='ineq',fun=lambda k:assess(k)[1])],
                         options=dict(maxiter=120,ftol=1e-10,eps=2e-7))
    except BudgetExhausted:
        pass
    if best_k is None:
        raise ValueError('No feasible candidate found')
    return dict(seed=seed,method=method,evaluations=count,elapsed_s=time.perf_counter()-started,
                best_strengths=best_k.tolist(),best_peak_beta_m=best_value,history=history)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--spec',default='configs/nominal.json')
    p.add_argument('--out',default='results')
    args = p.parse_args()
    spec = json.loads(Path(args.spec).read_text())
    out = Path(args.out); out.mkdir(parents=True,exist_ok=True)
    runs=[]
    for method in ['random','slsqp']:
        for seed in spec['search']['seeds']:
            run=search(spec,seed,method); runs.append(run)
            print(f'{method} seed={seed}: beta={run["best_peak_beta_m"]:.8f}, n={run["evaluations"]}, seconds={run["elapsed_s"]:.2f}',flush=True)
    (out/'search.json').write_text(json.dumps(runs,indent=2)+'\n')
    best=min(runs,key=lambda r:r['best_peak_beta_m'])
    candidate=dict(schema='beamopt-candidate/v1',spec_sha256=digest(args.spec),
                   strengths_m_inv=best['best_strengths'],claimed_peak_beta_m=best['best_peak_beta_m'],
                   provenance=dict(method=best['method'],seed=best['seed'],budget=best['evaluations']))
    (out/'candidate.json').write_text(json.dumps(candidate,indent=2)+'\n')

if __name__=='__main__':
    main()
