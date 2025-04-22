import numpy as np
from scipy.optimize import brentq

from Display import graph_equilibrium_line
from Stoichiometry import calculate_concentrations

R = 1.987  # Constante R en cal/(mol·K)


def vant_hoff_keq_calculate(K_eq_ref, T_ref, T_op, delta_H_rxn):
    K_eq = K_eq_ref * np.exp(delta_H_rxn / R * (1 / T_ref - 1 / T_op))
    return K_eq


def gibbs_keq_calculate(DG_dict, stoichiometry, T_op):
    delta_G_rxn_0 = (DG_dict.get("D", 0) * abs(stoichiometry.get("D", 0) / stoichiometry["A"]) +
                     DG_dict.get("C", 0) * abs(stoichiometry.get("C", 0) / stoichiometry["A"]) -
                     DG_dict.get("B", 0) * abs(stoichiometry.get("B", 0) / stoichiometry["A"]) -
                     DG_dict.get("A", 0))
    print(delta_G_rxn_0)
    return np.exp(-delta_G_rxn_0 / (R * T_op))


def equilibrium_conversion_calculate(stoichiometry, C_A0, C_B0):
    print("\n--- Determinación de la constante de equilibrio K_eq ---")
    k_eq_method = (
        input("¿Cómo desea determinar K_eq? (directa / vant_hoff / gibbs): ").strip().lower()
        .strip()
        .lower()
    )
    K_eq = None

    if k_eq_method == "directa":
        K_eq = float(input("Ingrese el valor de k_eq: "))
        T_op = float(input("Ingrese la temperatura de operación T (K): "))

    elif k_eq_method == "vant_hoff":
        print("\n--- Cálculo de constante de equilibrio usando Van't Hoff ---")
        K_eq_ref = float(input("Ingrese el valor de K_eq a T_ref: "))
        T_ref = float(input("Ingrese la temperatura de referencia T_ref (K): "))
        T_op = float(input("Ingrese la temperatura de operación T (K): "))
        delta_H_rxn = float(input("Ingrese el valor de ΔH_rxn (cal/mol): "))

        K_eq = vant_hoff_keq_calculate(K_eq_ref, T_ref, T_op, delta_H_rxn)
        print(f"🔹 K_eq calculado con Van't Hoff: {K_eq:.4f}")

    elif k_eq_method == "gibbs":
        DG_dict = {"A": -47860, "B": -46040, "C": -94630, "D": 0}
        T_op = 1000  # k
        K_eq = gibbs_keq_calculate(DG_dict, stoichiometry, T_op)
        print(f"🔹 K_eq calculado desde Gibbs: {K_eq:.4f}")

    else:
        raise ValueError("Método para determinar K_eq inválido.")

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

    print(f"✅ Conversión de equilibrio calculada: X_eq = {X_eq:.4f}")

    graph_equilibrium_line(X_eq, T_op=T_op)
    return X_eq
