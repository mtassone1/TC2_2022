# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:32:26 2022

@author: mante
"""

from IPython.display import display
from scipy import signal
import sympy as sy

sy.init_printing()  # LaTeX like pretty printing for IPython


def lti_to_sympy(lsys, symplify=True):
    """ Convert Scipy's LTI instance to Sympy expression """
    s = sy.Symbol('s')
    G = sy.Poly(lsys.num, s) / sy.Poly(lsys.den, s)
    return sy.simplify(G) if symplify else G


def sympy_to_lti(xpr, s=sy.Symbol('s')):
    """ Convert Sympy transfer function polynomial to Scipy LTI """
    num, den = sy.simplify(xpr).as_numer_denom()  # expressions
    p_num_den = sy.poly(num, s), sy.poly(den, s)  # polynomials
    c_num_den = [sy.expand(p).all_coeffs() for p in p_num_den]  # coefficients
    l_num, l_den = [sy.lambdify((), c)() for c in c_num_den]  # convert to floats
    return signal.lti(l_num, l_den)


pG, pH, pGH, pIGH = sy.symbols("G, H, GH, IGH")  # only needed for displaying

# Sample systems:
lti_G = signal.lti([0.091125, 0, 0, 0], [1, 1.1781, 3.530145, 2.447325, 3.530145, 1.1781, 1])
lti_H = signal.lti([0.2025, 0, 0],[1, 0.2781, 2.2025, 0.2781, 1])

# convert to Sympy:
Gs, Hs = lti_to_sympy(lti_G), lti_to_sympy(lti_H)


print("Converted LTI expressions:")
display(sy.Eq(pG, Gs))
display(sy.Eq(pH, Hs))

print("Multiplying Systems:")
GHs = sy.simplify(Gs*Hs).expand()  # make sure polynomials are canceled and expanded
display(sy.Eq(pGH, GHs))
