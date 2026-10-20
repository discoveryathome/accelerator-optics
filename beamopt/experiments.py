"""Held-out transfer and tracking; never use these outcomes to select the candidate."""
import argparse
import copy
import json
from pathlib import Path
import numpy as np
from . import matrix,xsuite_backend
from .search import search
from .verify import check


def main():
    p=argparse.ArgumentParser();p.add_argument('--spec',default='configs/nominal.json')
    p.add_argument('--out',default='results');args=p.parse_args()
    spec=json.loads(Path(args.spec).read_text());out=Path(args.out)
    candidate=json.loads((out/'candidate.json').read_text())['strengths_m_inv']
    configurations={'reference':spec['reference_strengths_m_inv'],
                    'baseline':spec['baseline_strengths_m_inv'],'candidate':candidate}
    checks={'candidate':check(out/'candidate.json',args.spec)}
    for name,k in configurations.items():
        ev=matrix.evaluate(k,spec);xe=xsuite_backend.evaluate(k,spec)
        checks[name+'_optics']=dict(matrix=matrix.serializable(ev),xsuite=matrix.serializable(xe),
                                    feasible=matrix.feasible(k,spec))
        for key in ['tune','beta','maps','chromaticity','offmomentum_peak']:
            np.testing.assert_allclose(ev[key],xe[key],rtol=2e-6,atol=2e-5)
    (out/'verification.json').write_text(json.dumps(checks,indent=2)+'\n')
    tracking=[]
    # Identical physical injection for every candidate: use the known reference covariance.
    # The separately matched experiment isolates periodic-envelope effects.
    ref_twiss=matrix.evaluate(configurations['reference'],spec)
    for name,k in configurations.items():
        for scenario in ['matched','common_injection','mismatch','errors']:
            initial=matrix.evaluate(k,spec) if scenario=='matched' else ref_twiss
            for seed in spec['tracking']['seeds']:
                row=xsuite_backend.track(k,spec,initial,seed,scenario)
                row['configuration']=name;tracking.append(row)
                print(f'tracking {name} {scenario} seed={seed} survival={row["survival"]:.6f}',flush=True)
    (out/'tracking.json').write_text(json.dumps(tracking,indent=2)+'\n')
    transfer=[]
    # Test both zero-shot settings and adaptation of the method. Geometries held fixed per task.
    for family,drifts in [('longer',[2.1]*8),('alternating',[1.8,2.2]*4)]:
        held=copy.deepcopy(spec);held['id']=family;held['drifts_m']=drifts
        # Derive held-out target from its symmetric reference, never from its optimized result.
        held['constraints']['tune_target']=matrix.evaluate(held['reference_strengths_m_inv'],held)['tune'].tolist()
        held['constraints']['chromaticity_abs_max']=(np.abs(matrix.evaluate(held['reference_strengths_m_inv'],held)['chromaticity'])*1.05).tolist()
        for name,k in configurations.items():
            try:
                ev=matrix.evaluate(k,held)
                transfer.append(dict(family=family,mode='zero-shot',configuration=name,
                                     feasible=matrix.feasible(k,held),peak_beta_m=ev['objective']))
            except ValueError:
                transfer.append(dict(family=family,mode='zero-shot',configuration=name,feasible=False,peak_beta_m=None))
        for method in ['random','slsqp']:
            for seed in spec['search']['seeds']:
                run=search(held,seed,method)
                k=run['best_strengths'];ev=matrix.evaluate(k,held);xe=xsuite_backend.evaluate(k,held)
                for key in ['maps','tune','chromaticity','beta']:
                    np.testing.assert_allclose(ev[key],xe[key],atol=2e-5,rtol=2e-6)
                transfer.append(dict(family=family,mode='reoptimized',configuration=method,
                                     feasible=matrix.feasible(k,held),peak_beta_m=ev['objective'],run=run))
        (out/f'{family}-spec.json').write_text(json.dumps(held,indent=2)+'\n')
    (out/'generalization.json').write_text(json.dumps(transfer,indent=2)+'\n')

if __name__=='__main__':
    main()
