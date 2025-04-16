import numpy as np
from scipy.integrate import solve_ivp

from NonIsotermalReactor import balance_reactor_nonisothermal
from RateConstant import calculate_rate_constant
from ReactionUtils import reaction_rate
from Stoichiometry import calculate_concentrations


def nonisothermal_batch_reactor_simulate(k, C_A0, C_B0, C_I, order, stoichiometry, excess_B,
                                         A, E, T0, T_ref, delta_H_rxn, C_p_dict,
                                         mode_energy, U=None, A_ICQ=None, T_cool=None, m_c=None, Cp_ref=None,
                                        use_initial_conditions=True, tiempo_inicio=2700, conversion_inicial=0.034, temperatura_inicial=448):
    Cp_total = (
            C_p_dict.get("A", 0) +
            (C_B0 / C_A0) * C_p_dict.get("B", 0) +
            (C_I / C_A0) * C_p_dict.get("I", 0)
    )

    if mode_energy == "adiabatic":
        if not use_initial_conditions:
            # Solo resolvemos dX_A/dt
            def dX_dt(t, y):
                X_A = y[0]
                T = T0 + (-delta_H_rxn * X_A) / Cp_total
                k_T = calculate_rate_constant(A=A, E=E, T=T, T_ref=T_ref)
                k = k_T
                r_A = reaction_rate(X_A, k, C_A0, C_B0, order, stoichiometry, excess_B)
                dX_A_dt = r_A / C_A0
                return dX_A_dt


            sol = solve_ivp(dX_dt, [0, 3000], [0.0], dense_output=True, max_step=1.0)

            t_eval = np.linspace(0, sol.t[-1], 100)
            X_A_eval = sol.sol(t_eval)[0]
            T_eval = [T0 + (-delta_H_rxn * x) / Cp_total for x in X_A_eval]
            T_final = T_eval[-1]
            k_final = calculate_rate_constant(A=A, E=E, T=T_final, T_ref=T_ref)
            concentrations = calculate_concentrations(C_A0, C_B0, X_A_eval, stoichiometry)
            T2a = None
            return t_eval, X_A_eval, T_eval, concentrations, sol.t[-1], k_final, T2a
        else:
            # Modo con condiciones iniciales
            print("MODO CON CONDICIONES INCIALES ACTIVADO")
            X0 = conversion_inicial
            T_init = temperatura_inicial if temperatura_inicial is not None else T0

            def evento_conversion_max(t, y):
                return 1.0 - y[0]

            evento_conversion_max.terminal = True
            evento_conversion_max.direction = 1

            def dX_dt(t, y):
                X_A = min(max(y[0], 0.0), 1.0)
                T = T_init + (-delta_H_rxn * (X_A - X0)) / Cp_total
                k_T = calculate_rate_constant(A=A, E=E, T=T, T_ref=T_ref)
                r_A = reaction_rate(X_A, k_T, C_A0, C_B0, order, stoichiometry, excess_B)
                return r_A / C_A0


            sol = solve_ivp(dX_dt, [tiempo_inicio, tiempo_inicio + 1000], [X0], dense_output=True, max_step=1.0,
                            events=evento_conversion_max)
            t_eval = np.linspace(sol.t[0], sol.t[-1], 100)
            X_A_eval = sol.sol(t_eval)[0]
            T_eval = [T_init + (-delta_H_rxn * (x - X0)) / Cp_total for x in X_A_eval]

        T_final = T_eval[-1]
        k_final = calculate_rate_constant(A=A, E=E, T=T_final, T_ref=T_ref)
        concentrations = calculate_concentrations(C_A0, C_B0, X_A_eval, stoichiometry)
        Ta2 = None

        return t_eval, X_A_eval, T_eval, concentrations, sol.t[-1], k_final, Ta2

    else:
        # Modo no adiabático o ICQ – se resuelve el sistema completo

        y0 = [0.0, T0]

        def evento_conversion_max(t, y):
            return 1.0 - y[0]

        evento_conversion_max.terminal = True
        evento_conversion_max.direction = -1  # Se anula cuando X_A se aproxima desde abajo

        sol = solve_ivp(
            lambda t, y: balance_reactor_nonisothermal(
                t, y, k, A,
                C_A0=C_A0, C_B0=C_B0, C_I=C_I, order=order, stoichiometry=stoichiometry,
                excess_B=excess_B, C_p_dict=C_p_dict, delta_H_rxn=delta_H_rxn,
                T_ref=T_ref, E=E,
                U=U, A_ICQ=A_ICQ, T_cool=T_cool, m_c=m_c, Cp_ref=Cp_ref
            ),
            [0, 4000],
            [0.0, T0],  # X_A = 0, T = T0
            dense_output=True,
            events=evento_conversion_max,
            max_step=1.0
        )
        t_final = sol.t_events[0][0] if sol.t_events[0].size > 0 else sol.t[-1]
        t_eval = np.linspace(0, t_final, 1000)
        X_A_eval = sol.sol(t_eval)[0]
        T_eval = sol.sol(t_eval)[1]
        concentrations = calculate_concentrations(C_A0, C_B0, X_A_eval, stoichiometry)
        T_final = T_eval[-1]
        k_final = calculate_rate_constant(A=A, E=E, T=T_final, T_ref=T_ref)
        Ta2 = T_eval - (T_eval - T_cool) * np.exp(-U * A_ICQ / (m_c * Cp_ref))

        return t_eval, X_A_eval, T_eval, concentrations, sol.t[-1], k_final, Ta2
