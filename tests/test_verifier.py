import copy
import json
from pathlib import Path
import numpy as np
import pytest
from beamopt import matrix
from beamopt.verify import check,digest,reference

SPEC=Path('configs/nominal.json')


def test_known_reference():
    assert reference(SPEC,False)['status']=='PASS'


def test_symplectic_and_periodic():
    spec=json.loads(SPEC.read_text())
    ev=matrix.evaluate(spec['baseline_strengths_m_inv'],spec)
    np.testing.assert_allclose(np.linalg.det(ev['maps']),1,atol=1e-12)
    np.testing.assert_allclose(ev['beta'][0],ev['beta'][-1],atol=1e-11)
    np.testing.assert_allclose(ev['alpha'][0],ev['alpha'][-1],atol=1e-11)


@pytest.mark.parametrize('mutation',['score','nan','bounds','sign','hash','shape','unstable'])
def test_reject_bad_candidate(tmp_path,mutation):
    spec=json.loads(SPEC.read_text()); k=spec['reference_strengths_m_inv']
    c=dict(schema='beamopt-candidate/v1',spec_sha256=digest(SPEC),strengths_m_inv=k,
           claimed_peak_beta_m=matrix.evaluate(k,spec)['objective'],provenance={})
    if mutation=='score': c['claimed_peak_beta_m']=1.
    if mutation=='nan': c['strengths_m_inv'][0]=float('nan')
    if mutation=='bounds': c['strengths_m_inv'][0]=.9
    if mutation=='sign': c['strengths_m_inv'][0]=-.5
    if mutation=='hash': c['spec_sha256']='0'*64
    if mutation=='shape': c['strengths_m_inv']=k[:-1]
    if mutation=='unstable': c['strengths_m_inv']=[.5]*8
    path=tmp_path/'bad.json';path.write_text(json.dumps(c))
    with pytest.raises((ValueError,AssertionError)):
        check(path,SPEC,False)


def test_chromaticity_gate_cannot_be_bought_by_beta():
    spec=json.loads(SPEC.read_text()); spec['constraints']['chromaticity_abs_max']=[.1,.1]
    assert not matrix.feasible(spec['reference_strengths_m_inv'],spec)


def test_aperture_gate():
    spec=json.loads(SPEC.read_text());spec['constraints']['aperture_radius_m']=.001
    assert not matrix.feasible(spec['reference_strengths_m_inv'],spec)


def test_reference_xsuite():
    assert reference(SPEC,True)['status']=='PASS'


def test_a_smaller_envelope_does_not_imply_preserved_reference_optics():
    # Closed-form stronger FODO has lower beta but shifts tunes/chromaticity.
    spec=json.loads(SPEC.read_text())
    k=[.51,-.51]*4
    reference_ev=matrix.evaluate(spec['reference_strengths_m_inv'],spec)
    candidate_ev=matrix.evaluate(k,spec)
    assert candidate_ev['objective']<reference_ev['objective']
    assert matrix.feasible(k,spec)
    strict=copy.deepcopy(spec)
    strict['constraints']['tune_tolerance']=1e-6
    strict['constraints']['chromaticity_abs_max']=(np.abs(reference_ev['chromaticity'])+1e-6).tolist()
    assert not matrix.feasible(k,strict)


def test_entrance_matching_is_an_independent_acceptance_gate():
    spec=json.loads(SPEC.read_text())
    ev=matrix.evaluate(spec['reference_strengths_m_inv'],spec)
    spec['constraints']['entrance_twiss_target']=np.r_[ev['beta'][0],ev['alpha'][0]].tolist()
    spec['constraints']['entrance_twiss_tolerance']=[1e-5]*4
    assert matrix.feasible(spec['reference_strengths_m_inv'],spec)
    # Previously acceptable focusing change now mismatches the fixed incoming beam.
    assert not matrix.feasible([.51,-.51]*4,spec)
