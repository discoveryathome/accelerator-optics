"""Public-facing animation of modeled matched envelopes; no invented measurements."""
import json
from pathlib import Path
import numpy as np
import os
os.environ.setdefault("MPL_IGNORE_SYSTEM_FONTS", "1")
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,PillowWriter
from . import matrix
from .plots import dense_envelope


def rays_at(k,spec,positions,seed=808):
    e=matrix.evaluate(k,spec);rng=np.random.default_rng(seed);z=rng.normal(size=(4,64))
    coords=[]
    for j in range(2):
        b,a=e['beta'][0,j],e['alpha'][0,j];emit=spec['geometric_emittance_m']
        coords.append(np.array([np.sqrt(emit*b)*z[2*j],np.sqrt(emit/b)*(z[2*j+1]-a*z[2*j])]))
    result=np.zeros((len(positions),2,64))
    starts=np.r_[0,np.cumsum(spec['drifts_m'])]
    for frame,s in enumerate(positions):
        for plane in range(2):
            vec=coords[plane].copy()
            for i,(ki,length) in enumerate(zip(k,spec['drifts_m'],strict=True)):
                if s<starts[i]:break
                vec[1] -= (1 if plane==0 else -1)*ki*vec[0]
                distance=min(length,s-starts[i]);vec[0]+=distance*vec[1]
                if s<=starts[i+1]:break
            result[frame,plane]=vec[0]
    return result


def main():
    root=Path('results');spec=json.loads(Path('configs/nominal.json').read_text())
    configs={'Perturbed starting settings':spec['baseline_strengths_m_inv'],
             'Symmetry-guided settings':json.loads((root/'analytic-candidate.json').read_text())['strengths_m_inv']}
    peaks=[matrix.evaluate(k,spec)['objective'] for k in configs.values()]
    gain=100*(1-np.sqrt(peaks[1]/peaks[0]))
    positions=np.linspace(0,sum(spec['drifts_m']),96)
    fig,axs=plt.subplots(2,2,figsize=(11,6.3),sharex=True,sharey=True)
    fig.subplots_adjust(top=.79,bottom=.16,hspace=.27,wspace=.15)
    fig.suptitle(f'Retune eight magnets: {gain:.1f}% smaller maximum matched beam width',fontsize=16,y=.96)
    fig.text(.5,.885,'A reproducible home-computer exercise in focusing a particle beam',ha='center',fontsize=11)
    fig.text(.5,.045,'Idealized model • equal emittance • each beam matched to its settings\nThis animation does not establish better transmission or a new accelerator design.',ha='center',fontsize=9)
    scatters=[];data=[]
    for col,(name,k) in enumerate(configs.items()):
        s,b=dense_envelope(k,spec);data.append(rays_at(k,spec,positions))
        for plane in range(2):
            ax=axs[plane,col];env=1e3*6*np.sqrt(spec['geometric_emittance_m']*b[:,plane])
            ax.fill_between(s,-env,env,color='#d4eaf2',alpha=.9)
            ax.plot(s,env,color='#147c9b',lw=1.4);ax.plot(s,-env,color='#147c9b',lw=1.4)
            ax.axhline(20,color='#737373',ls='--',lw=1);ax.axhline(-20,color='#737373',ls='--',lw=1)
            for i,loc in enumerate(np.r_[0,np.cumsum(spec['drifts_m'])][:-1]):
                ax.axvline(loc,color='#d6912c' if i%2 else '#4168aa',lw=3,alpha=.35)
            ax.set(xlim=(-.25,16.25),ylim=(-22,22),ylabel=f'{["Horizontal","Vertical"][plane]} position [mm]')
            if plane==0:ax.set_title(name)
            else:ax.set_xlabel('Distance along repeated focusing channel [m]')
            scatters.append((col,plane,ax.scatter(np.zeros(64),np.zeros(64),s=5,c='#213f56',alpha=.65)))
            ax.grid(alpha=.15)
    def update(frame):
        for col,plane,sc in scatters:
            sc.set_offsets(np.column_stack([np.full(64,positions[frame]),1e3*data[col][frame,plane]]))
        return [sc for _,_,sc in scatters]
    update(44);fig.savefig(root/'public-demo.png',dpi=140)
    ani=FuncAnimation(fig,update,frames=len(positions),interval=65,blit=False)
    ani.save(root/'public-demo.gif',writer=PillowWriter(fps=15),dpi=90)
    plt.close(fig)

if __name__=='__main__':main()
