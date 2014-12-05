import numpy                       
import matplotlib.pyplot as plt                 
#%matplotlib inline
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 16

##problem parameters



nt = 6
nx = 81
dx = .25
dt = .0002   
gamma = 1.4

icl = numpy.array([1.0, 0.0,100.0*10**3 ])
icr = numpy.array([0.125, 0, 10.0*10**3 ])

def e(p):
    return p[2]/((gamma-1)*p[0])
def et(p):
    return e(p)+1/2*p[1]**2

def computeu(p):
    return p[0]*numpy.array([1, p[1], et(p)])

def f1(u):
    v = numpy.transpose(u)
    return v[1]
def f2(u):
    v = numpy.transpose(u)
    return v[1]**2/v[0]+(gamma-1)*(v[2]-1/2*v[1]**2/v[0])
def f3(u):
    v = numpy.transpose(u)
    return v[1]/v[0]*(v[2]+(gamma-1)*(v[2]-1/2*v[1]**2/v[0]))
    

    
##initial conditions
#u = numpy.ones(nx)      
#u[.5/dx : 1/dx+1]=2  

import matplotlib.pyplot as plt
from matplotlib import animation



def u_initial():
    ul = computeu(icl)
    ur = computeu(icr)
    u = numpy.zeros((nx,3))
    u[:]=ul.copy()
    u[10/dx:]=ur.copy()
    return u

def computef(u):
    return numpy.transpose(numpy.array([f1(u),f2(u),f3(u)]))

def maccormack(u, nt, dt, dx):
    un = numpy.zeros((nt,len(u)))
    un[:] = u.copy()
    ustar = u.copy()    

    for n in range(1,nt):
        F = computeF(u)
        
        ustar[1:-1] = u[1:-1]-dt/dx*(F[2:]-F[1:-1])+\
        e*(u[2:]-2*u[1:-1]+u[:-2])
        #ustar[-1]=un[0,0]#podria estar mal
        Fstar = computeF(ustar)

        un[n,1:] = 1/2*(u[1:]+ustar[1:]-dt/dx*(Fstar[1:]-Fstar[:-1]))

        u = un[n].copy()

    return un

def predictor(u):
    f = computef(u)
    upr = 1/2*(u[1:]+u[:-1])-dt/(2*dx)*(f[1:]-f[:-1])
    return upr


def corrector(u):
    upr = predictor(u)
    fpr = computef(upr)
    uc = u.copy()
    uc[1:-1] = u[1:-1]-dt/dx*(fpr[1:]-fpr[:-1])
    return uc

def richtmyer(u0,nt,dt,dx):
    un=u0
    u = numpy.zeros((nt,len(u0),len(u0[0])))
    u[:] = un.copy()  

    for n in range(1,nt):
        u[n]=corrector(un)
        un = u[n]

    return u


def animate(data):
    x = numpy.linspace(0,4,nx)
    y = data
    line.set_data(x,y)
    return line,

def pressure(u):
    return (gamma-1)*(u[2]-1/2*u[1]**2/u[0])

def velocity(u):
    return u[1]/u[0]

def density(u):
    return u[0]

def estado(u):
    return numpy.array([density(u),velocity(u),pressure(u)])

u0 = u_initial()
u = richtmyer(u0,nt,dt,dx)
upreg = u[5,50]


print('-------------------------------------------------------')
print('la velocidad es:',velocity(upreg))
print('-------------------------------------------------------')
print('la presion es:',pressure(upreg))
print('-------------------------------------------------------')
print('la densidad es:',density(upreg))
#u = u_initial()
#sigma = .5
#dt = sigma*dx

#un = maccormack(u,nt,dt,dx)

#fig = plt.figure();
#ax = plt.axes(xlim=(0,4),ylim=(-.5,2));
#line, = ax.plot([],[],lw=2);

#anim = animation.FuncAnimation(fig, animate, frames=un, interval=50)
#display_animation(anim, default_mode='once')
#plt.show()
