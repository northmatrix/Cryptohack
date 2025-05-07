from sympy.ntheory import sqrt_mod

B = 1
A = 486662
p = 2**255 - 19

g_x = 9
g_y = sqrt_mod(g_x**3 + 486662 * g_x**2 + g_x, p)
print((g_x, g_y))
