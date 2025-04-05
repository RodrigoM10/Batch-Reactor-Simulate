import numpy as np

from RateConstant import calculate_rate_constant
from ReactionUtils import reaction_rate


def balance_reactor_nonisothermal(t, y, k, A, C_A0, C_B0, C_I, order, stoichiometry, excess_B,
                                  C_p_dict, delta_H_rxn, E, T_ref,
                                  U=None, A_ICQ=None, T_cool=None, m_c=None, Cp_ref=None):
    if not isinstance(y, (list, np.ndarray)) or len(y) != 2:
        raise ValueError(
            f"El argumento 'y' debe ser una lista o arreglo con 2 elementos (no {type(y)}: {y})."
        )

    Cps = (
            C_p_dict.get("A", 0) +
            (C_B0 / C_A0) * C_p_dict.get("B", 0) +
            (C_I / C_A0) * C_p_dict.get("I", 0)
    )
    Cp_total = Cps * C_A0

    X_A, T = y
    # Limitar X_A dentro del rango físico permitido
    X_A = min(max(X_A, 0.0), 1.0)

    if A is None:
        raise ValueError("El parámetro A (factor preexponencial) es necesario para el cálculo de k.")
    k_T = calculate_rate_constant(A=A, E=E, T=T, T_ref=T_ref)
    k = k_T
    r_A = reaction_rate(X_A, k, C_A0, C_B0, order, stoichiometry, excess_B)
    dX_A_dt = r_A / C_A0

    Q_gb = -delta_H_rxn * r_A
    Q_rb = (m_c * Cp_ref) * ((T - T_cool) * (1 - np.exp((-U * A_ICQ) / (m_c * Cp_ref))))

    dT_dt = (Q_gb - Q_rb) / Cp_total if Cp_total > 0 else 0

    return [dX_A_dt, dT_dt]
