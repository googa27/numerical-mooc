import numpy as np
import matplotlib.pyplot as plt

T=20.0
dt=0.1
N=int(T/dt+1)

ms=50
g=9.81
ro=1.091
A=np.pi*0.5**2
ve=325
Cd=0.15



def step(t):
    #if t>0:
        #return 1
    #else:
        #return 0
    return 0.5*(np.sign(t)+1)

def fdmp(t):
    return 20.0*step(5-t)

def fmp(t):
    return (100-20.0*t)*step(5-t)

def f(u):
    h = u[0]
    v = u[1]
    print(mp,dmp,ro*v*abs(v)*A*Cd/2,h)
    return np.array([v,-g+dmp*ve/(ms+mp)-ro*v*abs(v)*A*Cd/2])

def euler_step(u,f,dt):
    return u+dt*f(u)


t=np.linspace(0.0,T,N)
h0=0
v0=0
u0=np.array([h0,v0])
u=np.empty((N,2))
u[0]=u0

for i in range(1,N):
    mp = fmp(t[i])
    dmp = fdmp(t[i])
    u[i]=euler_step(u[i-1],f,dt)

h = u[:,0]
v = u[:,1]

plt.plot(t,h)
plt.show()

for i,j in enumerate(v):
	if j==max(v):
		print('el indice de la velocidad maxima es',i)

for i,j in enumerate(h):
	if j==max(h):
		print('el indice de la altura maxima es',i)
#------------------------------------------------------------------

#x=np.linspace(4,23,43)

#print(x[5])

#ones_array = np.ones( (5,17) ) 
#zeros_array = np.zeros( ones_array.shape )

#p = 7.
#r = np.array([11.2, 4.7, 6.6])


#y=(np.sin(p/r))**3

#print(y[1])

#e = np.array([1.6,1.5,1.475])
#h = np.array([0.04,0.02,0.01])

#print(np.log((e[0]-e[1])/(e[1]-e[2]))/np.log(2))

