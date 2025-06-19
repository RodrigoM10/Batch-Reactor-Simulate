import numpy as np

from SimulateBR.IsothermalReactor import isothermal_reaction_time, calculate_conversion_at_time
from SimulateBR.RateConstant import calculate_rate_constant
from SimulateBR.Stoichiometry import calculate_concentrations


def isothermal_batch_reactor_simulate(C_A0, C_B0, C_C0, C_D0, order, stoichiometry, excess_B, X_eq,
                                      A, E, T, k,
                                      X_A_desired, t_reaction_det,
                                      reversible=False, Keq=None):
    if A is not None and E is not None:
        k = calculate_rate_constant(A=A, E=E, T=T)
        print(f"\n🔹 Constante k calculada por Arrhenius: {k:.4f}")

    if t_reaction_det is not None:
        print("calcular conversión a partir del tiempo de reacción (min):", t_reaction_det)
        t_eval = np.linspace(0, t_reaction_det, 100)
        X_A_eval = calculate_conversion_at_time(
            t_eval, k, C_A0, C_B0, C_C0, C_D0, order,
            stoichiometry, excess_B, X_eq,
            reversible, Keq
        )
        t_final = t_reaction_det
    else:
        print("calcular tiempo a partir de conversión deseada:", X_A_desired)
        t_eval, X_A_eval = isothermal_reaction_time(
            k, C_A0, C_B0, C_C0, C_D0, X_A_desired, order,
            stoichiometry, excess_B,
            reversible, Keq
        )
        t_final = t_eval[-1]

    concentrations = calculate_concentrations(C_A0, C_B0, C_C0, C_D0, X_A_eval, stoichiometry)

    return t_eval, X_A_eval, concentrations, t_final, k

