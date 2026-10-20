"""Xsuite implementation, independent from matrix map and Twiss formulas."""
import numpy as np
import xtrack as xt
import xpart as xp
import xobjects as xo


def build(strengths, spec, apertures=False, errors=None):
    elements, names = [], []
    aperture = spec['constraints']['aperture_radius_m']
    errors = errors or {}
    for i, (k, length) in enumerate(zip(strengths, spec['drifts_m'], strict=True)):
        if apertures:
            elements.append(xt.LimitRect(min_x=-aperture, max_x=aperture, min_y=-aperture, max_y=aperture))
            names.append(f'aperture_{i}')
        k = k * (1+errors.get('relative_gradient', np.zeros(8))[i])
        elements.append(xt.Multipole(knl=[0., float(k), errors.get('k2l', 0.)]))
        names.append(f'q{i}')
        elements.append(xt.Drift(length=length))
        names.append(f'd{i}')
    if apertures:
        elements.append(xt.LimitRect(min_x=-aperture, max_x=aperture, min_y=-aperture, max_y=aperture))
        names.append('aperture_end')
    line = xt.Line(elements=elements, element_names=names)
    line.particle_ref = xp.Particles(p0c=spec['p0c_eV'], mass0=xp.PROTON_MASS_EV)
    line.build_tracker(_context=xo.ContextCpu())
    return line


def evaluate(strengths, spec):
    line = build(strengths, spec)
    tw = line.twiss(method='4d', delta_chrom=spec['chromaticity_step'])
    off = [line.twiss(method='4d', delta0=d, chrom=False) for d in spec['momentum_grid']]
    r = line.get_R_matrix(particle_on_co=tw.particle_on_co)['R_matrix']
    return dict(tune=np.array([tw.qx, tw.qy]), chromaticity=np.array([tw.dqx, tw.dqy]),
                beta=np.column_stack([tw.betx, tw.bety]),
                alpha=np.column_stack([tw.alfx, tw.alfy]), s=np.array(tw.s),
                maps=np.array([r[:2, :2], r[2:4, 2:4]]),
                peak=np.array([max(tw.betx), max(tw.bety)]),
                offmomentum_peak=np.array([max(max(t.betx) for t in off), max(max(t.bety) for t in off)]),
                dispersion_max=float(max(np.max(np.abs(tw.dx)),np.max(np.abs(tw.dy)))),
                closed_orbit_max=float(max(np.max(np.abs(tw.x)),np.max(np.abs(tw.y)))))


def track(strengths, spec, initial_twiss, seed, scenario='matched'):
    rng = np.random.default_rng(seed)
    n = spec['tracking']['particles']
    z = rng.normal(size=(5,n))
    # Deterministic hard truncation avoids unknown momentum tails outside the tested range.
    delta = np.clip(z[4]*spec['tracking']['sigma_delta'], -.02, .02)
    errors = {}
    if scenario == 'errors':
        errors = dict(relative_gradient=np.random.default_rng(seed+10000).normal(0, .001, 8), k2l=.15)
    line = build(strengths, spec, apertures=True, errors=errors)
    emit = spec['geometric_emittance_m']
    coords = []
    for j in range(2):
        b, a = initial_twiss['beta'][0,j], initial_twiss['alpha'][0,j]
        if scenario == 'mismatch':
            b *= 1.3 if j == 0 else .8
            a += .25
        coords.extend([np.sqrt(emit*b)*z[2*j], np.sqrt(emit/b)*(z[2*j+1]-a*z[2*j])])
    p = xp.Particles(p0c=spec['p0c_eV'], mass0=xp.PROTON_MASS_EV,
                     x=coords[0], px=coords[1], y=coords[2], py=coords[3], delta=delta)
    def emittance(x, px):
        return float(np.sqrt(max(0, np.linalg.det(np.cov(np.array([x,px]), ddof=0)))))
    initial_emit = [emittance(coords[0],coords[1]),emittance(coords[2],coords[3])]
    line.track(p, num_turns=spec['tracking']['periods'], turn_by_turn_monitor=True)
    mon = line.record_last_track
    live = np.asarray(p.state)>0
    # Lost particles are excluded only from moments; survival is reported separately.
    # Xsuite may reorder final particle slots after losses; monitor rows use particle_id.
    survivor_ids = np.asarray(p.particle_id)[live].astype(int)
    rms = []
    for a in [mon.x, mon.y]:
        rms.append(float(np.max(np.std(np.asarray(a)[survivor_ids,:],axis=0))) if live.any() else None)
    final_emit = [emittance(np.array(p.x)[live],np.array(p.px)[live]),
                  emittance(np.array(p.y)[live],np.array(p.py)[live])] if live.sum()>2 else [None,None]
    return dict(seed=seed, scenario=scenario, survival=float(live.mean()),
                max_rms_at_period_start_m=rms, initial_emittance_m=initial_emit,
                final_emittance_m=final_emit, emittance_ratio=[f/i if f is not None else None for f,i in zip(final_emit,initial_emit)])
