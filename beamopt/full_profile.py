"""Check empirical RMS beam size throughout the lattice, not only at period starts."""
import json
from pathlib import Path
import numpy as np
import xpart as xp
from . import matrix,xsuite_backend


def profile(k,spec,initial,seed,scenario):
    rng=np.random.default_rng(seed);n=spec['tracking']['particles'];z=rng.normal(size=(5,n))
    delta=np.clip(z[4]*spec['tracking']['sigma_delta'],-.02,.02);coords=[];emit=spec['geometric_emittance_m']
    for j in range(2):
        b,a=initial['beta'][0,j],initial['alpha'][0,j]
        coords.extend([np.sqrt(emit*b)*z[2*j],np.sqrt(emit/b)*(z[2*j+1]-a*z[2*j])])
    errors={} if scenario=='common_injection' else dict(relative_gradient=np.random.default_rng(seed+10000).normal(0,.001,8),k2l=.15)
    line=xsuite_backend.build(k,spec,apertures=True,errors=errors)
    p=xp.Particles(p0c=spec['p0c_eV'],mass0=xp.PROTON_MASS_EV,x=coords[0],px=coords[1],y=coords[2],py=coords[3],delta=delta)
    s=np.array(line.get_table().s);snapshots=[];completed=0
    for start_period in [0,15,63,255]:
        if start_period>completed:line.track(p,num_turns=start_period-completed)
        line.track(p,num_turns=1,turn_by_turn_monitor='ONE_TURN_EBE');completed=start_period+1
        mon=line.record_last_track
        # This diagnostic aborts on losses; do not silently compare biased survivor envelopes.
        if not np.all(np.asarray(p.state)>0):raise ValueError('Profile diagnostic encountered losses; requires explicit survivor handling')
        rms=np.column_stack([np.std(mon.x,axis=0),np.std(mon.y,axis=0)])
        assert len(rms)==len(s),(rms.shape,s.shape)
        snapshots.append(dict(period=completed,rms_profile_m=rms.tolist(),peak_rms_m=np.max(rms,axis=0).tolist()))
    return dict(seed=seed,scenario=scenario,s_m=s.tolist(),survival=1.,snapshots=snapshots,
                worst_sampled_rms_m=np.max([q['peak_rms_m'] for q in snapshots],axis=0).tolist())


def main():
    root=Path('results');spec=json.loads((root/'injection-spec.json').read_text())
    initial=matrix.evaluate(spec['reference_strengths_m_inv'],spec)
    configs={'reference':spec['reference_strengths_m_inv'],
             'free_entrance':json.loads((root/'irregular/candidate.json').read_text())['strengths_m_inv'],
             'fixed_entrance':json.loads((root/'trial/epigraph-injection-7.json').read_text())['strengths_m_inv']}
    rows=[]
    for name,k in configs.items():
        for scenario in ['common_injection','errors']:
            for seed in [1009,2003,3001]:
                row=profile(k,spec,initial,seed,scenario);row['configuration']=name;rows.append(row)
                print(name,scenario,seed,row['worst_sampled_rms_m'],flush=True)
    (root/'trial/full-lattice-tracking.json').write_text(json.dumps(rows,indent=2)+'\n')

if __name__=='__main__':main()
