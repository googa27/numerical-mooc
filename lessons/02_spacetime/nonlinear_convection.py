import numpy                       
import matplotlib.pyplot as plt                 
#%matplotlib inline
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 16

##problem parameters
nx = 41
dx = 2./(nx-1)
nt = 10    
dt = .02  

##initial conditions
u = numpy.ones(nx)      
u[.5/dx : 1/dx+1]=2  

x = numpy.linspace(0,2,nx)

plt.plot(numpy.linspace(0,2,nx), u, color='#003366', ls='--', lw=3)
plt.ylim(0,2.5)
plt.show()

for n in range(1, nt):  
    un = u.copy() 
    u[1:] = un[1:]-un[1:]*dt/dx*(un[1:]-un[0:-1]) 
    u[0] = 1.0

plt.plot(numpy.linspace(0,2,nx), u, color='#003366', ls='--', lw=3)
plt.ylim(0,2.5)
plt.show()
