import numpy                       
import matplotlib.pyplot as plt                 
#%matplotlib inline
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 16

##problem parameters
nx = 51
L = 11.0
dx = L/(nx-1)
nt = 101    
dt = .001
vm = 136.0
rhom = 250.0

##initial conditions
#u = numpy.ones(nx)      
#u[.5/dx : 1/dx+1]=2  

#x = numpy.linspace(0,2,nx)

#plt.plot(numpy.linspace(0,2,nx), u, color='#003366', ls='--', lw=3)
#plt.ylim(0,2.5)
#plt.show()

x = numpy.linspace(0,L,nx)
rho0 = numpy.ones(nx)*20
rho0[10:20] = 50

plt.plot(x, rho0, color='#003366', ls='--', lw=3)
plt.ylim(0,60)
plt.show()

u = u=numpy.ones((nt,nx))
u[0]=rho0

rho = rho0.copy()

def v(rho):
    return vm*(1-rho/rhom)

def F(rho):
    return rho*v(rho)
def dF(rho):
    return vm*(1-2*rho/rhom)

#for n in range(1, nt):  
    #rhon = rho.copy() 
    #rho[1:] = rhon[1:]-dt/dx*(F(rhon[1:])-F(rhon[0:-1])) 
    #rho[0] = 10.0
    #u[n]=rho

for n in range(1, nt):  
    rhon = rho.copy() 
    rho[1:] = rhon[1:]-dF(rho)[1:]*dt/dx*(rhon[1:]-rhon[0:-1]) 
    rho[0] = 20.0
    u[n]=rho

plt.plot(x, u[100], color='#003366', ls='--', lw=3)
plt.ylim(0,90)
plt.show()

#I calculate what is asked for taking into account the required unit changes

print(min(v(u[0])*10.0**3/60.0**2))

print(numpy.average(v(u[50])*10.0**3/60.0**2))

print(min(v(u[100])*10.0**3/60.0**2))

print(min(v(u[50])*10.0**3/60.0**2))
