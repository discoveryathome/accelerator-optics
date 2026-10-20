"""Shared-injection tracking for the separate irregular-fixture contracts."""
import json
from pathlib import Path
from . import matrix,xsuite_backend
from .verify import check


def main():
    root=Path('results');specpath=root/'injection-spec.json';spec=json.loads(specpath.read_text())
    guarded=root/'trial/epigraph-injection-7.json';free=root/'irregular/candidate.json'
    configs={'reference':spec['reference_strengths_m_inv'],
             'free_entrance':json.loads(free.read_text())['strengths_m_inv'],
             'fixed_entrance':json.loads(guarded.read_text())['strengths_m_inv']}
    checks=[check(guarded,specpath),check(free,root/'irregular-spec.json')]
    initial=matrix.evaluate(spec['reference_strengths_m_inv'],spec);rows=[]
    for name,k in configs.items():
        for scenario in ['common_injection','mismatch','errors']:
            for seed in [1009,2003,3001]:
                r=xsuite_backend.track(k,spec,initial,seed,scenario)
                r['configuration']=name;rows.append(r)
                print(f'{name} {scenario} {seed}: survival={r["survival"]}',flush=True)
    (root/'trial/injection-tracking.json').write_text(json.dumps(dict(checks=checks,tracking=rows),indent=2)+'\n')

if __name__=='__main__':main()
