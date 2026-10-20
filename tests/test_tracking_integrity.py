import copy
import json
from pathlib import Path
import numpy as np
from beamopt import xsuite_backend,matrix


def test_aperture_uses_specification():
    spec=json.loads(Path('configs/nominal.json').read_text())
    spec['constraints']['aperture_radius_m']=.012
    line=xsuite_backend.build(spec['reference_strengths_m_inv'],spec,apertures=True)
    assert line['aperture_0'].max_x==.012
    assert line['aperture_end'].min_y==-.012


def test_tracking_reports_real_losses_without_hiding_them():
    spec=json.loads(Path('configs/nominal.json').read_text())
    spec['constraints']['aperture_radius_m']=.004
    spec['tracking']['particles']=128
    spec['tracking']['periods']=8
    k=spec['reference_strengths_m_inv']
    result=xsuite_backend.track(k,spec,matrix.evaluate(k,spec),103)
    assert 0<result['survival']<1
    assert all(np.isfinite(result['max_rms_at_period_start_m']))
    # Fixed injected emittance is not replaced by the survivors' initial emittance.
    assert all(e>5e-7 for e in result['initial_emittance_m'])
