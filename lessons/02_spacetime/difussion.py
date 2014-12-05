import numpy                       
import matplotlib.pyplot as plt    
#%matplotlib inline
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 16

nx = 41
dx = 2./(nx-1)
nt = 20   
nu = 0.3   #the value of viscosity
sigma = .2 
dt = sigma*dx**2/nu 

x = numpy.linspace(0,2,nx)

u = numpy.ones(nx)      
u[.5/dx : 1/dx+1]=2  

un = numpy.ones(nx)

for n in range(nt):  
    un = u.copy() 
    u[1:-1] = un[1:-1] + nu*dt/dx**2*(un[2:] -2*un[1:-1] +un[0:-2]) 
        
plt.plot(numpy.linspace(0,2,nx), u, color='#003366', ls='--', lw=3)
plt.ylim(0,2.5);
plt.show()

#from JSAnimation_master.JSAnimation.IPython_display import display_animation
from matplotlib import animation

nt = 50

u = numpy.ones(nx)      
u[.5/dx : 1/dx+1]=2  

un = numpy.ones(nx)

fig = plt.figure(figsize=(8,5))
ax = plt.axes(xlim=(0,2), ylim=(1,2.5))
line = ax.plot([], [], color='#003366', ls='--', lw=3)[0]

def diffusion(i):
    line.set_data(x,u)
    
    un = u.copy() 
    u[1:-1] = un[1:-1] + nu*dt/dx**2*(un[2:] -2*un[1:-1] +un[0:-2]) 
    

ani = animation.FuncAnimation(fig, diffusion,
                        frames=nt, interval=100)
plt.show()
