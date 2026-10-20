"""Refresh local author-checked result records after verification; never imply review."""
import json
from pathlib import Path
from .verify import digest


def main():
    cases=[]
    for name,candidate,spec in [
        ('nominal','results/analytic-candidate.json','configs/nominal.json'),
        ('longer','results/trial/epigraph-longer-7.json','results/longer-spec.json'),
        ('alternating','results/trial/epigraph-alternating-7.json','results/alternating-spec.json'),
        ('irregular','results/trial/epigraph-irregular-7.json','results/irregular-spec.json'),
        ('injection','results/trial/epigraph-injection-7.json','results/injection-spec.json')]:
        c=json.loads(Path(candidate).read_text())
        cases.append(dict(case=name,peak_beta_m=c['claimed_peak_beta_m'],candidate=candidate,spec=spec,
                          by='Codex trial author; independent review pending',source=candidate,updated='2026-10-20'))
    Path('results/frontier-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    sources=[p for p in Path('beamopt').glob('*.py')]+[Path('requirements.lock'),Path('configs/nominal.json')]
    sources += [Path('run.sh'), Path('results/frontier-cases.json')] + list(Path('tests').glob('*.py'))
    sources+=list({Path(r[key]) for r in cases for key in ['candidate','spec']})
    artifacts=[dict(path=str(p),sha256=digest(p)) for p in sorted(set(sources))]
    frontier=dict(schema='discover-frontier/v0',
        statement='Five retained feasible configurations cross-checked in Xsuite and independent thin-lens matrices. Nominal symmetric control peak beta is 6.8834461461 m; the fixed-injection irregular witness has 9.2106052934 m versus its 10.8226487083 m uniform-strength reference. These are local model witnesses, not global optima or real-machine improvements.',
        status='Author-checked local proposal; independent scientific review and maintainer consent pending.',
        evidence_level=['author-checked'],claim_kind=['model'],
        scope='Pinned uncoupled thin-lens periodic channels. Each case has a distinct fixed specification; scores across cases are not interchangeable. Tracking is a limited stress test, not part of an operational claim.',
        metric=dict(name='Nominal peak beta',value=str(cases[0]['peak_beta_m']),direction='lower-is-better',unit='m'),
        table=dict(path='results/frontier-cases.json',key=['case'],value='peak_beta_m',direction='lower-is-better',object='candidate',
                   check_row=['.venv/bin/python','-m','beamopt.verify','{candidate}','--spec','{spec}'],check_row_minutes=1,
                   by='by',source='source',updated='updated'),
        assumptions=[dict(id='review',statement='No independent contributor or consenting maintainer has reviewed these claims.',status='open'),
                     dict(id='fidelity',statement='No calibrated real-machine model, space charge, RF or validated error ensemble.',status='open'),
                     dict(id='optimality',statement='No global-optimality certificate for the general eight-variable problems.',status='open')],
        sources=['https://cds.cern.ch/record/1533020/files/CERN-2013-001-p171.pdf','https://xsuite.readthedocs.io/en/latest/twiss.html','docs/ASSESSMENT.md'],
        artifacts=artifacts,reproduce='.venv/bin/python -m beamopt.reproduce',
        reproduce_full='bash run.sh',reproduce_minutes=3,
        prerequisites=['Python 3.13','Install requirements.lock in .venv','CPU-only Xsuite; GPU not required'],
        review='docs/ASSESSMENT.md',updated_on='2026-10-20')
    Path('discover/frontier.json').write_text(json.dumps(frontier,indent=2)+'\n')

if __name__=='__main__':main()
