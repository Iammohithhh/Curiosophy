"""Original explanatory figures. Run from any directory; requires matplotlib/numpy."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / 'content' / 'images'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':14,'axes.spines.top':False,
 'axes.spines.right':False,'axes.titleweight':'bold','figure.facecolor':'#faf9f6',
 'axes.facecolor':'#faf9f6','text.color':'#203842','axes.labelcolor':'#203842'})
TEAL, CORAL, BLUE = '#007f80', '#c34e32', '#4c64ae'
def save(fig,name):
    fig.savefig(OUT/name,dpi=170,bbox_inches='tight',facecolor=fig.get_facecolor())
    plt.close(fig)

fig,ax=plt.subplots(figsize=(10,5))
x=np.linspace(0,1,500); y=3.2*np.exp(-((x-.48)/.17)**2)-.8*x
ax.plot(x,y,lw=4,color=TEAL); ax.set(xlabel='Progress through molecular geometries',ylabel='Electronic energy (arbitrary units)',xticks=[],yticks=[])
ax.text(.02,.25,'Reactants',fontsize=15); ax.text(.72,-.5,'Products',fontsize=15)
i=np.argmax(y); ax.annotate('Transition state',xy=(x[i],y[i]),xytext=(.62,2.7),arrowprops={'arrowstyle':'->','color':BLUE},fontsize=15)
ax.hlines([y[0],y[i]],0,x[i],color='#a0a0a0',linestyle='dotted')
ax.annotate('',xy=(.18,y[i]),xytext=(.18,y[0]),arrowprops={'arrowstyle':'<->','color':CORAL,'lw':2})
ax.text(.20,1.5,'Barrier',color=CORAL)
ax.annotate('',xy=(.92,y[0]),xytext=(.92,y[-1]),arrowprops={'arrowstyle':'<->','color':BLUE,'lw':2})
ax.text(.63,.15,'Reaction energy',color=BLUE)
ax.set_title('A downhill reaction can still have a barrier',pad=22)
save(fig,'reaction-landscape.png')

fig,ax=plt.subplots(figsize=(11,4)); ax.set(xlim=(0,11),ylim=(0,4)); ax.axis('off')
labels=['Guess a\ndensity','Build energy\nand potential','Solve for\norbitals','Construct\nnew density']
for i,label in enumerate(labels):
    xx=.2+i*2.8
    ax.add_patch(FancyBboxPatch((xx,1.7),2.1,1.1,boxstyle='round,pad=.12',facecolor='#e0eeeb',edgecolor=TEAL,lw=1.8))
    ax.text(xx+1.05,2.25,label,ha='center',va='center',fontsize=14)
    if i<3: ax.annotate('',xy=(xx+2.6,2.25),xytext=(xx+2.22,2.25),arrowprops={'arrowstyle':'->','lw':2,'color':TEAL})
ax.plot([9.65,9.65,4.05],[1.55,.65,.65],color=CORAL,lw=2)
ax.annotate('',xy=(4.05,1.55),xytext=(4.05,.65),arrowprops={'arrowstyle':'->','lw':2,'color':CORAL})
ax.text(6.85,.2,'Mix and repeat until consistent',ha='center',color=CORAL,fontsize=14)
ax.text(5.5,3.5,'The functional changes the density it is evaluated on',ha='center',weight='bold',fontsize=17)
save(fig,'self-consistency.png')

fig,ax=plt.subplots(figsize=(10,5.8)); ax.axis('off'); ax.set(xlim=(0,10),ylim=(0,6))
rows=[('LDA','Density at this point'),('GGA','Density + local gradient'),('Meta-GGA','Also orbital kinetic-energy density'),('Hybrid','Also nonlocal orbital-pair exchange'),('Learned functional','Inputs depend on the architecture')]
for i,(name,desc) in enumerate(rows):
    yy=4.6-i
    ax.add_patch(FancyBboxPatch((.1,yy-.32),9.5,.75,boxstyle='round,pad=.08',facecolor='#e0eeeb' if i%2==0 else '#eeeae2',edgecolor='none'))
    ax.text(.35,yy,name,va='center',weight='bold',fontsize=15); ax.text(3.8,yy,desc,va='center',fontsize=14)
ax.text(.15,5.65,'What information does the approximation receive?',weight='bold',fontsize=17)
ax.text(.15,-.1,'More information can help. It does not guarantee better predictions.',fontsize=13,color=CORAL)
save(fig,'functional-information.png')

fig,ax=plt.subplots(figsize=(10,5))
x=np.linspace(1,10,200)
for p,c in [(3,TEAL),(4,BLUE),(7,CORAL)]: ax.loglog(x,x**p,lw=3,color=c,label=f'Schematic $M^{p}$')
ax.set(xlabel='Relative problem size M',ylabel='Relative operation count',title='An exponent describes growth, not a stopwatch')
ax.legend(frameon=False); ax.grid(alpha=.15); ax.set_xticks([1,2,5,10],['1','2','5','10'])
fig.text(.14,-.02,'All curves share an arbitrary starting cost. No measured timings are plotted.',fontsize=12)
save(fig,'scaling-is-not-runtime.png')

fig,axs=plt.subplots(1,2,figsize=(11,4.4)); x=np.linspace(0,1,1000); eps=.01; w=100
axs[0].plot(x,x*x,color=TEAL,label='Reference'); axs[0].plot(x,x*x+eps*np.sin(w*x),color=CORAL,label='With tiny wiggles')
axs[1].plot(x,2*x,color=TEAL); axs[1].plot(x,2*x+eps*w*np.cos(w*x),color=CORAL)
for ax,title in zip(axs,['Energy: error at most 0.01','Derivative: error up to 1']): ax.set(xlabel='x',title=title)
axs[0].legend(frameon=False,fontsize=11); fig.tight_layout()
save(fig,'energy-and-derivative.png')

fig,ax=plt.subplots(figsize=(9,4.7)); x=np.linspace(0,4,400)
ax.plot(x,1+.804-.804/(1+.21951*x*x/.804),color=TEAL,lw=3)
ax.axhline(1.804,color=CORAL,ls='--',label='PBE exchange cap: 1.804')
ax.set(xlabel='Reduced gradient s',ylabel='Exchange enhancement Fₓ(s)',title='PBE: add gradient information without unlimited enhancement',ylim=(.95,1.9))
ax.legend(frameon=False); save(fig,'pbe-enhancement.png')

fig,ax=plt.subplots(figsize=(9,4.7)); x=np.linspace(0,1,200)
ax.plot(x,-x,color=TEAL,lw=3,label='Exact ensemble: straight segment')
ax.plot(x,-x-.7*x*(1-x),color=CORAL,lw=3,label='Illustrative delocalization bias')
ax.set(xlabel='Fractional electron added α',ylabel='Energy relative to E(N) (arbitrary units)',title='A curved energy can reward spreading a charge')
ax.legend(frameon=False,fontsize=12); save(fig,'fractional-charge.png')
