"""Independent canonical (x, px/p0) thin-lens maps; no Xsuite imports.

At delta != 0 drift R12=L/(1+delta); quadrupole kick is -k1L*x.
This keeps det(M)=1 in normalized canonical coordinates.
"""
import numpy as np


def maps(strengths, drifts, delta=0.):
    for k, length in zip(strengths, drifts, strict=True):
        qx = np.array([[1., 0.], [-k, 1.]])
        qy = np.array([[1., 0.], [k, 1.]])
        d = np.array([[1., length / (1 + delta)], [0., 1.]])
        yield qx, qy, 0.
        yield d, d, length


def optics(strengths, drifts, delta=0.):
    seq = list(maps(strengths, drifts, delta))
    total = [np.eye(2), np.eye(2)]
    for mx, my, _ in seq:
        total = [mx @ total[0], my @ total[1]]
    tune, cov = [], []
    for m in total:
        c = np.trace(m) / 2
        if not np.isfinite(c) or abs(c) >= 1 - 1e-12:
            raise ValueError('Unstable or degenerate periodic map')
        sn = np.copysign(np.sqrt(1-c*c), m[0, 1])
        mu = np.arctan2(sn, c) % (2*np.pi)
        beta = m[0, 1] / sn
        alpha = (m[0, 0]-m[1, 1]) / (2*sn)
        cov.append(np.array([[beta, -alpha], [-alpha, (1+alpha*alpha)/beta]]))
        tune.append(mu/(2*np.pi))
    s, beta, alpha = [0.], [[c[0, 0] for c in cov]], [[-c[0, 1] for c in cov]]
    for mx, my, length in seq:
        cov = [mx @ cov[0] @ mx.T, my @ cov[1] @ my.T]
        s.append(s[-1]+length)
        beta.append([c[0, 0] for c in cov])
        alpha.append([-c[0, 1] for c in cov])
    # In drifts beta is a convex quadratic: its maximum is at an endpoint.
    return dict(tune=np.array(tune), maps=np.array(total), s=np.array(s),
                beta=np.array(beta), alpha=np.array(alpha),
                peak=np.max(beta, axis=0), trace=np.trace(total, axis1=1, axis2=2))


def evaluate(strengths, spec):
    drifts = spec['drifts_m']
    nominal = optics(strengths, drifts)
    h = spec['chromaticity_step']
    plus, minus = optics(strengths, drifts, h), optics(strengths, drifts, -h)
    diff = (plus['tune'] - minus['tune'] + .5) % 1 - .5
    nominal['chromaticity'] = diff/(2*h)
    off = [optics(strengths, drifts, d) for d in spec['momentum_grid']]
    nominal['offmomentum_peak'] = np.max([o['peak'] for o in off], axis=0)
    nominal['max_abs_trace'] = np.max(np.abs([o['trace'] for o in off]))
    nominal['objective'] = float(max(nominal['peak']))
    return nominal


def margins(strengths, spec, ev=None):
    """All entries must be >=0; no objective can compensate a failed gate."""
    k = np.asarray(strengths)
    ev = evaluate(k, spec) if ev is None else ev
    c = spec['constraints']
    signs = np.array([1, -1]*4)
    extra = []
    if "entrance_twiss_target" in c:
        actual = np.r_[ev["beta"][0], ev["alpha"][0]]
        difference = actual - np.asarray(c["entrance_twiss_target"])
        tolerance = np.asarray(c["entrance_twiss_tolerance"])
        extra = [tolerance - difference, tolerance + difference]
    return np.concatenate([
        k*signs-c['abs_k_min'], c['abs_k_max']-k*signs,
        c['tune_tolerance']-np.abs(ev['tune']-c['tune_target']),
        np.asarray(c['chromaticity_abs_max'])-np.abs(ev['chromaticity']),
        np.asarray(c['beta_max_each_m'])-ev['peak'],
        np.asarray(c['offmomentum_beta_max_each_m'])-ev['offmomentum_peak'],
        [c['max_abs_trace']-ev['max_abs_trace']],
        c['aperture_radius_m']-c['envelope_nsigma']*np.sqrt(
            spec['geometric_emittance_m']*ev['offmomentum_peak'])] + extra)


def feasible(strengths, spec, tol=1e-8):
    try:
        return bool(np.all(margins(strengths, spec) >= -tol))
    except (ValueError, FloatingPointError):
        return False


def serializable(ev):
    return {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in ev.items()}
