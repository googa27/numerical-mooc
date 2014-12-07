from math import sin, cos, log, ceil
import numpy
import matplotlib.pyplot as plt
#%matplotlib inline
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 16

# model parameters:
g = 9.8      # gravity in m s^{-2}
ms = 50.0  # trim velocity in m s^{-1}   
C_D = 0.15
r = 0.5# drag coefficient --- or D/L if C_L=1
A = numpy.pi*r**2    # for convenience, use C_L = 1
ve = 325.0
rho = 1.091
dmp = 20



### set initial conditions ###
h0 = 0.0    # start at the trim velocity (or add a delta)
v0 = 0.0 # initial angle of trajectory
mp0 = 100.0     # horizotal position is arbitrary  

def f(u):
    """Returns the right-hand side of the phugoid system of equations.
    
    Parameters
    ----------
    u : array of float
        array containing the solution at time n.
        
    Returns
    -------
    dudt : array of float
        array containing the RHS given u.
    """
    
    h = u[0]
    v = u[1]
    mp = u[2]
    return numpy.array([v,
                      -g + dmp*ve/(ms+mp) - rho*v*abs(v)*A*C_D/(2*(ms+mp)),
                      -dmp])

def euler_step(u, f, dt):
    """Returns the solution at the next time-step using Euler's method.
    
    Parameters
    ----------
    u : array of float
        solution at the previous time-step.
    f : function
        function to compute the right hand-side of the system of equation.
    dt : float
        time-increment.
    
    Returns
    -------
    u_n_plus_1 : array of float
        approximate solution at the next time step.
    """
    
    return u + dt * f(u)

T = 5.0                          # final time
dt = 0.1                           # time increment
N = int(T/dt) + 1                  # number of time-steps
t = numpy.linspace(0.0, T, N)      # time discretization

# initialize the array containing the solution for each time-step
u = numpy.empty((N, 3))
u[0] = numpy.array([h0, v0, mp0])# fill 1st element with initial values

# time loop - Euler method
for n in range(N-1):
    
    u[n+1] = euler_step(u[n], f, dt)

# get the glider's position with respect to the time
h = u[:,0]
v = u[:,1]
mp = u[:,2]


# visualization of the path
plt.figure(figsize=(8,6))
plt.grid(True)
plt.xlabel(r't', fontsize=18)
plt.ylabel(r'h', fontsize=18)
plt.title('Rocket height, flight time = %.2f' % T, fontsize=18)
plt.plot(t,h, 'k-',t,v,'r--',t,mp,'bs');
plt.show()


dmp = 0.0

h0 = u[-1,0]    # start at the trim velocity (or add a delta)
v0 = u[-1,1] # initial angle of trajectory
mp0 = u[-1,2]

T = 40.0                          # final time
dt = 0.1                           # time increment
N = int(T/dt) + 1                  # number of time-steps
t = numpy.linspace(0.0, T, N) 

# initialize the array containing the solution for each time-step
u = numpy.empty((N, 3))
u[0] = numpy.array([h0, v0, mp0])# fill 1st element with initial values

# time loop - Euler method
for n in range(N-1):
    
    u[n+1] = euler_step(u[n], f, dt)

# get the glider's position with respect to the time
h = u[:,0]
v = u[:,1]
mp = u[:,2]

# visualization of the path
plt.figure(figsize=(8,6))
plt.grid(True)
plt.xlabel(r't', fontsize=18)
plt.ylabel(r'h', fontsize=18)
plt.title('Rocket height, flight time = %.2f' % T, fontsize=18)
plt.plot(t,h, 'k-',t,v,'r--',t,mp,'bs');
plt.show()

