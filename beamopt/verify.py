"""Fail-closed checker. Never trust candidate-reported scores or constraints."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from . import matrix


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_candidate(path, spec_path):
    candidate = json.loads(Path(path).read_text())
    if set(candidate) != {'schema', 'spec_sha256', 'strengths_m_inv', 'claimed_peak_beta_m', 'provenance'}:
        raise ValueError('Unexpected or missing candidate fields')
    if candidate['schema'] != 'beamopt-candidate/v1' or candidate['spec_sha256'] != digest(spec_path):
        raise ValueError('Wrong schema or benchmark hash')
    strengths = np.asarray(candidate['strengths_m_inv'], dtype=float)
    if strengths.shape != (8,) or not np.all(np.isfinite(strengths)):
        raise ValueError('Require eight finite strengths')
    if not np.isfinite(candidate['claimed_peak_beta_m']):
        raise ValueError('Nonfinite claim')
    return candidate, strengths


def check(path, spec_path, use_xsuite=True):
    spec = json.loads(Path(spec_path).read_text())
    candidate, k = load_candidate(path, spec_path)
    ev = matrix.evaluate(k, spec)
    gate = matrix.margins(k, spec, ev)
    if np.min(gate) < -1e-8:
        raise ValueError(f'Constraint failed: minimum margin {np.min(gate)}')
    if abs(ev['objective']-candidate['claimed_peak_beta_m']) > 1e-6:
        raise ValueError('Claimed objective differs from recomputation')
    for m in ev['maps']:
        np.testing.assert_allclose(np.linalg.det(m), 1, atol=1e-10)
    checked = {}
    if use_xsuite:
        from . import xsuite_backend
        xe = xsuite_backend.evaluate(k, spec)
        for key, atol in [('maps',1e-7),('tune',1e-8),('beta',2e-6),('alpha',2e-6),
                          ('chromaticity',2e-5),('offmomentum_peak',2e-5)]:
            np.testing.assert_allclose(ev[key],xe[key],rtol=2e-6,atol=atol,err_msg=key)
            checked[key] = float(np.max(np.abs(ev[key]-xe[key])))
        if xe['dispersion_max'] > 1e-8 or xe['closed_orbit_max'] > 1e-8:
            raise ValueError('Unexpected dispersion or orbit')
    return dict(candidate=str(path), peak_beta_m=ev['objective'], min_constraint_margin=float(min(gate)),
                implementation_max_abs_errors=checked, status='PASS',
                evidence_level='author-checked', independent_review=False)


def reference(spec_path, use_xsuite=True):
    spec = json.loads(Path(spec_path).read_text())
    k = spec['reference_strengths_m_inv']
    ev = matrix.evaluate(k, spec)
    np.testing.assert_allclose(ev['peak'],4*(1+.5)/np.sin(np.pi/3),atol=1e-12)
    np.testing.assert_allclose(ev['tune'],[2/3,2/3],atol=1e-12)
    np.testing.assert_allclose(ev['chromaticity'],-4*np.tan(np.pi/6)/np.pi,atol=1e-8)
    if use_xsuite:
        from . import xsuite_backend
        xe = xsuite_backend.evaluate(k,spec)
        for key in ['peak','tune','chromaticity','maps','beta']:
            np.testing.assert_allclose(ev[key],xe[key],rtol=2e-6,atol=2e-5)
    return dict(status='PASS', reference='analytic symmetric 60 degree FODO',
                peak_beta_m=ev['objective'],tune=ev['tune'].tolist(),chromaticity=ev['chromaticity'].tolist())


def main():
    p = argparse.ArgumentParser()
    p.add_argument('candidate',nargs='?')
    p.add_argument('--spec',default='configs/nominal.json')
    p.add_argument('--reference',action='store_true')
    p.add_argument('--matrix-only',action='store_true')
    args = p.parse_args()
    result = reference(args.spec,not args.matrix_only) if args.reference else check(args.candidate,args.spec,not args.matrix_only)
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
