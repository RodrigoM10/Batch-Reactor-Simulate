import numpy as np
from scipy.optimize import brentq
from Stoichiometry import calculate_concentrations

R = 1.987  # cal/mol·K

def keq_vanthoff_differential(T, T_ref, K_eq_ref, delta_H_rxn):
    exponent = -delta_H_rxn / R * (1/T - 1/T_ref)
    return K_eq_ref * np.exp(exponent)


def nonIsothermal_equilibrium_conversion_calculate(K_eq_T, C_A0, C_B0, stoichiometry):

    def equilibrium_function(X):
        C_dict = calculate_concentrations(C_A0, C_B0, X, stoichiometry)
        num = 1.0
        den = 1.0
        for especie, nu in stoichiometry.items():
            if nu > 0:
                num *= C_dict[especie] ** nu
            elif nu < 0:
                den *= C_dict[especie] ** (-nu)
        return num / den - K_eq_T

    return brentq(equilibrium_function, 0.0001, 0.9999999)
