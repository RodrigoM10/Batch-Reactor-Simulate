import numpy as np
from SimulateBR.RateConstant import calculate_rate_constant
from SimulateBR.ReactionUtils import reaction_rate
from SimulateBR.Equilibrium import calculate_keq_auto

def heat_rates_calculate(
    X_A_eval, T_eval, A, E, T_ref, delta_H_rxn,
    C_A0, C_B0, C_C0, C_D0, order, stoichiometry, excess_B,
    reversible, sim_params,
    U, A_ICQ, T_cool, m_c, Cp_ref
):
    k_eval = [
        calculate_rate_constant(A=A, E=E, T=T, T_ref=T_ref)
        for T in T_eval
    ]

    r_A = []
    for x, T, k in zip(X_A_eval, T_eval, k_eval):
        if reversible:
            try:
                Keq_T = calculate_keq_auto(sim_params, T)
            except Exception as e:
                print(f"⚠️ Error calculando Keq para T={T:.2f}: {e}")
                Keq_T = None
        else:
            Keq_T = None

        r = reaction_rate(
            X_A=x, k=k,
            C_A0=C_A0, C_B0=C_B0, C_C0=C_C0, C_D0=C_D0,
            order=order, stoichiometry=stoichiometry,
            excess_B=excess_B, reversible=reversible, Keq=Keq_T
        )
        r_A.append(r)

    Qgb_eval = np.array([-delta_H_rxn * r for r in r_A])
    Qrb_eval = np.array([
        (m_c * Cp_ref) * ((T - T_cool) * (1 - np.exp((-U * A_ICQ) / (m_c * Cp_ref))))
        for T in T_eval
    ])

    return Qgb_eval, Qrb_eval
