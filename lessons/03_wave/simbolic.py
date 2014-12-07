import sympy
sympy.init_printing()

rho, u_max, u_star, rho_max, rho_star, A, B = \
sympy.symbols('rho u_max u_star rho_max rho_star A B')


eq1 = sympy.Eq( 0, u_max*rho_max*(1 - A*rho_max-B*rho_max**2) )
eq2 = sympy.Eq( 0, u_max*(1 - 2*A*rho_star-3*B*rho_star**2) )
eq3 = sympy.Eq( u_star, u_max*(1 - A*rho_star - B*rho_star**2) )

eq4 = sympy.Eq(eq2.lhs - 3*eq3.lhs, eq2.rhs - 3*eq3.rhs)
eq4

eq4.simplify()

eq4

eq4.expand()

rho_sol = sympy.solve(eq4,rho_star)[0]
rho_sol

B_sol = sympy.solve(eq1,B)[0]
B_sol

quadA = eq2.subs([(rho_star, rho_sol), (B,B_sol)])
quadA

quadA.simplify()

A_sol = sympy.solve(quadA, A)

A_sol[0]

A_sol[1]

aval = A_sol[0].evalf(subs={u_star: 1.5, u_max:2.0, rho_max:15.0} )
print(aval)

print(A_sol[1].evalf(subs={u_star: 1.5, u_max:2.0, rho_max:15.0} ))

bval = B_sol.evalf(subs={rho_max:15.0, A:aval} )
print(bval)

sympy.init_printing(use_latex=False)

rhom = 15.0

um = 2.0

us = 1.5

eq5 = sympy.Eq( 0, u_max*(1 - 2*A*rho-3*B*rho**2) )

rho_sol = sympy.solve(eq5,rho)

print(rho_sol)

print(rho_sol[0].evalf(subs={A: aval, u_max:2.0, B: bval} ))
print(rho_sol[1].evalf(subs={A: aval, u_max:2.0, B: bval} ))

#print(rhos_sol.evlaf(subs=))

#def f(rho):
    #return um*rho
