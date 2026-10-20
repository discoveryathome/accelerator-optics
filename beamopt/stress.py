"""Predeclared exploratory transfer checks; never select nominal candidates here."""
import copy
import json
from pathlib import Path
import numpy as np
import xtrack as xt
import xpart as xp
import xobjects as xo
from . import matrix,xsuite_backend


def configurations(spec):
    root=Path('results')
    return {'reference':spec['reference_strengths_m_inv'],
            'baseline':spec['baseline_strengths_m_inv'],
            'search':json.loads((root/'candidate.json').read_text())['strengths_m_inv'],
            'analytic':json.loads((root/'analytic-candidate.json').read_text())['strengths_m_inv']}


def main():
    spec=json.loads(Path('configs/nominal.json').read_text());configs=configurations(spec)
    out=Path('results/trial');length=.2;thick=[]
    for name,k in configs.items():
        elements=[]
        for ki,ld in zip(k,spec['drifts_m'],strict=True):
            elements.extend([xt.Quadrupole(length=length,k1=ki/length),xt.Drift(length=ld-length)])
        line=xt.Line(elements=elements)
        line.particle_ref=xp.Particles(p0c=spec['p0c_eV'],mass0=xp.PROTON_MASS_EV)
        line.build_tracker(_context=xo.ContextCpu())
        tw=line.twiss(method='4d',delta_chrom=spec['chromaticity_step'])
        thick.append(dict(configuration=name,quadrupole_length_m=length,period_length_m=line.get_length(),
                          tune=[float(tw.qx),float(tw.qy)],chromaticity=[float(tw.dqx),float(tw.dqy)],
                          endpoint_peak_beta_m=[float(max(tw.betx)),float(max(tw.bety))],
                          note='Element endpoints only; not a certified peak inside thick quadrupoles.'))
    (out/'finite-magnets.json').write_text(json.dumps(thick,indent=2)+'\n')
    rows=[];injection=matrix.evaluate(spec['reference_strengths_m_inv'],spec)
    for aperture in [.02,.012,.008,.006]:
        for name,k in configs.items():
            for seed in [401,503,607]:
                stress=copy.deepcopy(spec);stress['constraints']['aperture_radius_m']=aperture
                stress['tracking']['particles']=4096
                r=xsuite_backend.track(k,stress,injection,seed,scenario='common_injection')
                r.update(configuration=name,aperture_half_width_m=aperture,particles=4096)
                rows.append(r)
                print(f'aperture={aperture} {name} seed={seed} survival={r["survival"]:.5f}',flush=True)
                (out/'aperture-stress.json').write_text(json.dumps(rows,indent=2)+'\n')

if __name__=='__main__':main()
