import numpy
import sympy
#%matplotlib inline
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 16

from sympy import init_printing
init_printing()

x = sympy.symbols('x')

x

5*x

x, nu, t = sympy.symbols('x nu t')
phi = sympy.exp(-(x-4*t)**2/(4*nu*(t+1))) + \
sympy.exp(-(x-4*t-2*numpy.pi)**2/(4*nu*(t+1)))
phi


phiprime = phi.diff(x)
phiprime

phiprime = phi.diff(x)
phiprime

from sympy.utilities.lambdify import lambdify

u = -2*nu*(phiprime/phi)+4
print(u)

ufunc = lambdify((t, x, nu), u)
print("The value of u at t=1, x=4, nu=3 is {}.".format(ufunc(1,4,3)))

import matplotlib.pyplot as plt

###variable declarations
nx = 101
nt = 100
dx = 2*numpy.pi/(nx-1)
nu = .07
dt = dx*nu

x = numpy.linspace(0, 2*numpy.pi, nx)
un = numpy.empty(nx)
t = 0

u = numpy.asarray([ufunc(t, x0, nu) for x0 in x])
u

plt.figure(figsize=(8,5), dpi=100)
plt.plot(x,u, color='#003366', ls='--', lw=3)
plt.xlim([0,2*numpy.pi])
plt.ylim([0,10]);
plt.show()

for n in range(nt):
    un = u.copy()
    
    u[1:-1] = un[1:-1] - un[1:-1] * dt/dx * (un[1:-1] - un[:-2]) + nu*dt/dx**2*\
                    (un[2:] - 2*un[1:-1] + un[:-2])

    u[0] = un[0] - un[0] * dt/dx * (un[0] - un[-1]) + nu*dt/dx**2*\
                (un[1] - 2*un[0] + un[-1])
    u[-1] = un[-1] - un[-1] * dt/dx * (un[-1] - un[-2]) + nu*dt/dx**2*\
                (un[0]- 2*un[-1] + un[-2])
        
u_analytical = numpy.asarray([ufunc(nt*dt, xi, nu) for xi in x])

plt.figure(figsize=(8,5), dpi=100)
plt.plot(x,u, color='#003366', ls='--', lw=3, label='Computational')
plt.plot(x, u_analytical, label='Analytical')
plt.xlim([0,2*numpy.pi])
plt.ylim([0,10])
plt.show()

from matplotlib import animation

u = numpy.asarray([ufunc(t, x0, nu) for x0 in x])

fig = plt.figure(figsize=(8,6))
ax = plt.axes(xlim=(0,2*numpy.pi), ylim=(0,10))
line = ax.plot([], [], color='#003366', ls='--', lw=3)[0]
line2 = ax.plot([], [], 'k-', lw=2)[0]
ax.legend(['Computed','Analytical'])

def burgers(n):
       
    un = u.copy()
        
    u[1:-1] = un[1:-1] - un[1:-1] * dt/dx * (un[1:-1] - un[:-2]) + nu*dt/dx**2*\
                    (un[2:] - 2*un[1:-1] + un[:-2])

    u[0] = un[0] - un[0] * dt/dx * (un[0] - un[-1]) + nu*dt/dx**2*\
                (un[1] - 2*un[0] + un[-1])
    u[-1] = un[-1] - un[-1] * dt/dx * (un[-1] - un[-2]) + nu*dt/dx**2*\
                (un[0]- 2*un[-1] + un[-2])
        
    u_analytical = numpy.asarray([ufunc(n*dt, xi, nu) for xi in x])
    line.set_data(x,u)
    line2.set_data(x, u_analytical)
    

ani = animation.FuncAnimation(fig, burgers,
                        frames=nt, interval=100)

plt.show()

x = sympy.symbols('x')
phi = (sympy.cos(x))**2*(sympy.sin(x))**3/  \
(x**5*sympy.exp(x))

phi

phiprime = phi.diff(x)
