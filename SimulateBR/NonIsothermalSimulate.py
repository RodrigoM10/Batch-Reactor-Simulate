import numpy as np
from scipy.integrate import solve_ivp
from NonIsotermalReactor import balance_reactor_nonisothermal
from Stoichiometry import calculate_concentrations

def nonisothermal_batch_reactor_simulate(k, C_A0, C_B0, C_I, order, stoichiometry, excess_B,
                                         A, E, T0, T_ref, delta_H_rxn, C_p_dict,
                                         mode_energy, U=None, A_ICQ=None, T_cool=None):
    y0 = [0.0, T0]

    sol = solve_ivp(
        lambda t, y: balance_reactor_nonisothermal(
            t, y, k, A,
            C_A0=C_A0,
            C_B0=C_B0,
            order=order,
            stoichiometry=stoichiometry,
            excess_B=excess_B,
            C_p_dict=C_p_dict,
            delta_H_rxn=delta_H_rxn,
            T_ref=T_ref,
            E=E,
            mode_energy=mode_energy,
            U=U, A_ICQ=A_ICQ, T_cool=T_cool,
            C_I=C_I
        ),
        [0, 1000],
        y0,
        dense_output=True,
    )

    t_eval = np.linspace(0, sol.t[-1], 100)
    X_A_eval = sol.sol(t_eval)[0]
    T_eval = sol.sol(t_eval)[1]
    concentrations = calculate_concentrations(C_A0, C_B0, X_A_eval, stoichiometry)

    print("conversion:", X_A_eval, "temperatura:", T_eval, "tiempo:", t_eval)
    return t_eval, X_A_eval, T_eval, concentrations, sol.t[-1]

