import numpy as np
from SimulateBR.RateConstant import calculate_rate_constant
from SimulateBR.ReactionUtils import reaction_rate


def heat_rates_calculate(X_A_eval, T_eval, A, E, T_ref, delta_H_rxn, C_A0, C_B0, order, stoichiometry, excess_B,
                     U, A_ICQ, T_cool, m_c, Cp_ref):
    k_eval = [calculate_rate_constant(A=A, E=E, T=T, T_ref=T_ref) for T in T_eval]
    r_A = [reaction_rate(x, k, C_A0, C_B0, order, stoichiometry, excess_B) for x, k in zip(X_A_eval, k_eval)]

    Qgb_eval = np.array([-delta_H_rxn * r for r in r_A])
    Qrb_eval = np.array([(m_c * Cp_ref) * ((T - T_cool) * (1 - np.exp((-U * A_ICQ) / (m_c * Cp_ref)))) for T in T_eval])

    return Qgb_eval, Qrb_eval