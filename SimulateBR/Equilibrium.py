import numpy as np
from scipy.optimize import brentq

from SimulateBR.Stoichiometry import calculate_concentrations

R = 1.987  # Constante R en cal/(mol·K)


def vant_hoff_keq_calculate(K_eq_ref, T_ref, T, delta_H_rxn):
    K_eq = K_eq_ref * np.exp(delta_H_rxn / R * (1 / T_ref - 1 / T))
    return K_eq


def gibbs_keq_calculate(DG_dict, stoichiometry, T):
    delta_G_rxn_0 = sum(DG_dict.get(sp, 0) * nu for sp, nu in stoichiometry.items())
    return np.exp(-delta_G_rxn_0 / (R * T))


def equilibrium_conversion_calculate(K_eq, stoichiometry, C_A0, C_B0):

    def equilibrium_function(X):
        C_dict = calculate_concentrations(C_A0, C_B0, X, stoichiometry)
        num = 1.0  # productos
        den = 1.0  # reactivos
        for esp, nu in stoichiometry.items():
            if nu > 0:
                num *= C_dict[esp] ** nu
            elif nu < 0:
                den *= C_dict[esp] ** (-nu)
        return num / den - K_eq

    try:
        X_eq = brentq(equilibrium_function, 0.00001, 0.9999999)
    except ValueError:
        print("⚠️ No se pudo encontrar una solución para X_eq dentro del rango físico (0–1).")
        return None
    return X_eq

def calculate_keq_auto(sim_params, T=None):
    method = sim_params.get("k_eq_method")
    T_op = T if T is not None else sim_params.get("T_iso")

    if method == "direct":
        return sim_params["K_eq_direct"]

    elif method == "vant_hoff":
        return vant_hoff_keq_calculate(
            sim_params["K_eq_ref"],
            sim_params["T_ref"],
            T_op,
            sim_params["delta_H_rxn"]
        )

    elif method == "gibbs":
        return gibbs_keq_calculate(
            sim_params["DG_dict"],
            sim_params["stoichiometry"],
            T_op
        )

    else:
        raise ValueError(f"❌ Método para determinar K_eq inválido: {method}")