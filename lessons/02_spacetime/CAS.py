import numpy
import sympy
from sympy.utilities.lambdify import lambdify

x = sympy.symbols('x')
phi = (sympy.cos(x))**2*(sympy.sin(x))**3/  \
(4*x**5*sympy.exp(x))

print('-----------------------------------------------')

print(phi)

print('-----------------------------------------------')

phiprime = phi.diff(x)

print(phiprime)

print('-----------------------------------------------')

ufunc = lambdify((x),phiprime)

print(ufunc(2.2))

