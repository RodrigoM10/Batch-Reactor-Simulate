import numpy as np

from RateConstant import calculate_rate_constant
from ReactionUtils import reaction_rate


def balance_reactor_nonisothermal(t, y, k, A, C_A0, C_B0, order, stoichiometry, excess_B,
                                  C_p_dict, delta_H_rxn, E, T_ref, mode_energy,
                                  U=None, A_ICQ=None, T_cool=None, C_I=0.0):
    if not isinstance(y, (list, np.ndarray)) or len(y) != 2:
        raise ValueError(
            f"El argumento 'y' debe ser una lista o arreglo con 2 elementos (no {type(y)}: {y})."
        )

    X_A, T = y

    if A is None:
        raise ValueError("El parámetro A (factor preexponencial) es necesario para el cálculo de k.")

    k_T = calculate_rate_constant(A=A, E=E, T=T, T_ref=T_ref)
    k = k_T

    r_A = reaction_rate(X_A, k, C_A0, C_B0, order, stoichiometry, excess_B)
    dX_A_dt = -r_A / C_A0

    C_A = C_A0 * (1 - X_A)
    C_B = C_B0 - (stoichiometry.get("B", 0) / stoichiometry["A"]) * C_A0 * X_A if "B" in stoichiometry else 0
    C_C = (stoichiometry.get("C", 0) / stoichiometry["A"]) * C_A0 * X_A if "C" in stoichiometry else 0

    Cp_total = (
            C_A * C_p_dict.get("A", 0) +
            (C_B / C_A) * C_p_dict.get("B", 0) +
            (C_C / C_A) * C_p_dict.get("C", 0) +
            (C_I / C_A) * C_p_dict.get("I", 0)
    )

    Q_gen = -delta_H_rxn * r_A

    if mode_energy == "adiabatic":
        dT_dt = Q_gen / Cp_total if Cp_total > 0 else 0
    elif mode_energy in ["non-adiabatic", "ICQ"] and U is not None and A_ICQ is not None and T_cool is not None:
        Q_rem = U * A_ICQ * (T - T_cool)
        dT_dt = (Q_gen - Q_rem) / Cp_total if Cp_total > 0 else 0
    else:
        dT_dt = 0

    return [dX_A_dt, dT_dt]
