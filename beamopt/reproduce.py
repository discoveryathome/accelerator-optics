"""Quick fresh-checkout verification of retained results (does not rerun search)."""
import json
import time
from pathlib import Path
from .verify import check,reference,digest


def main():
    started=time.perf_counter();root=Path('results');rows=[]
    rows.append(reference('configs/nominal.json'))
    paths=[root/'candidate.json',root/'analytic-candidate.json',root/'reduced-candidate.json']
    paths+=sorted((root/'candidates').glob('*.json'))
    for path in paths:
        rows.append(check(path,'configs/nominal.json'))
    for path in sorted((root/'trial').glob('epigraph-*.json')):
        if path.name=='epigraph-search.json':continue
        family=path.stem.rsplit('-',1)[0].replace('epigraph-','')
        spec='configs/nominal.json' if family=='nominal' else f'results/{family}-spec.json'
        rows.append(check(path,spec))
    frontier=Path('discover/frontier.json')
    if frontier.exists():
        for artifact in json.loads(frontier.read_text()).get('artifacts',[]):
            if digest(artifact['path'])!=artifact['sha256']:
                raise ValueError('Artifact hash mismatch: '+artifact['path'])
    table=root/'frontier-cases.json'
    if table.exists():
        for row in json.loads(table.read_text()):
            result=check(row['candidate'],row['spec'])
            if abs(result['peak_beta_m']-row['peak_beta_m'])>1e-6:
                raise ValueError('Table score mismatch: '+row['case'])
            rows.append(result)
    print(json.dumps(dict(status='PASS',elapsed_s=time.perf_counter()-started,checks=rows),indent=2))

if __name__=='__main__':main()
