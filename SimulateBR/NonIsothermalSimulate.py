import numpy as np
from scipy.integrate import solve_ivp

from SimulateBR.Display import graph_equilibrium_vs_temperature, graph_conversion_with_equilibrium
from SimulateBR.Equilibrium import equilibrium_conversion_calculate, vant_hoff_keq_calculate, calculate_keq_auto
from SimulateBR.NonIsotermalReactor import balance_reactor_nonisothermal
from SimulateBR.RateConstant import calculate_rate_constant
from SimulateBR.ReactionUtils import reaction_rate
from SimulateBR.Stoichiometry import calculate_concentrations


def nonisothermal_batch_reactor_simulate(k, C_A0, C_B0, C_C0, C_D0, C_I, order, reversible, stoichiometry, excess_B,
                                         A, E, T0, T_ref, delta_H_rxn, C_p_dict, K_eq_ref,
                                         mode_energy, U=None, A_ICQ=None, T_cool=None, m_c=None, Cp_ref=None, sim_params=None ):
    if mode_energy == "adiabatic":
        Cp_total = (
                C_p_dict.get("A", 0) +
                ((C_B0 / C_A0) * C_p_dict.get("B", 0) if C_B0 is not None else 0) +
                ((C_C0 / C_A0) * C_p_dict.get("C", 0) if C_C0 is not None else 0) +
                ((C_D0 / C_A0) * C_p_dict.get("D", 0) if C_D0 is not None else 0) +
                ((C_I / C_A0) * C_p_dict.get("I", 0) if C_I is not None else 0)
        )

        def dX_dt(t, y):
            X_A = max(0.0, min(1.0, y[0]))
            T = T0 + (-delta_H_rxn * X_A) / Cp_total
            k = calculate_rate_constant(A=A, E=E, T=T, T_ref=T_ref)

            K_eq_T = None
            if reversible and K_eq_ref is not None:
                K_eq_T = calculate_keq_auto(sim_params, T=T)
                #K_eq_T = vant_hoff_keq_calculate(K_eq_ref, T_ref, T, delta_H_rxn)

                try:
                    X_eq_T = equilibrium_conversion_calculate(K_eq_T, stoichiometry, C_A0, C_B0, C_C0, C_D0)
                    if X_A >= X_eq_T:
                        return [0.0]
                except ValueError:
                    pass  # sigue si no se puede calcular equilibrio

            r_A = reaction_rate(
                X_A, k, C_A0, C_B0, C_C0, C_D0, order=order,
                stoichiometry=stoichiometry, excess_B=excess_B,
                reversible=reversible, Keq=K_eq_T
            )

            return [r_A / C_A0]

        # Solo incluir evento de equilibrio si es reversible
        events = None
        if reversible and K_eq_ref is not None:
            def equilibrium_event(t, y):
                X_A = y[0]
                T = T0 + (-delta_H_rxn * X_A) / Cp_total
                try:
                    #K_eq_T = vant_hoff_keq_calculate(K_eq_ref, T_ref, T, delta_H_rxn)
                    K_eq_T = calculate_keq_auto(sim_params, T=T)
                    X_eq_T = equilibrium_conversion_calculate(K_eq_T, stoichiometry, C_A0, C_B0, C_C0, C_D0)
                    return X_eq_T - X_A
                except:
                    return 1  # no se activa el evento si no se puede calcular

            equilibrium_event.terminal = True
            equilibrium_event.direction = -1
            events = [equilibrium_event]

        sol = solve_ivp(dX_dt, [0, 50000], [0.0], dense_output=True, max_step=1.0, events=events)

        t_final = sol.t_events[0][0] if (events and sol.t_events[0].size > 0) else sol.t[-1]
        t_eval = np.linspace(0, t_final, 100)
        X_A_eval = sol.sol(t_eval)[0]
        T_eval = [T0 + (-delta_H_rxn * x) / Cp_total for x in X_A_eval]
        k_final = calculate_rate_constant(A=A, E=E, T=T_eval[-1], T_ref=T_ref)
        concentrations = calculate_concentrations(C_A0, C_B0, C_C0, C_D0, X_A_eval, stoichiometry)
        Ta2 = None

        # Graficar si es reversible
        if reversible and K_eq_ref is not None:
            T_range = np.linspace(T_ref, max(T_eval) * 1.5, 100)
            X_eq_range = [
                equilibrium_conversion_calculate(
                    vant_hoff_keq_calculate(K_eq_ref, T_ref, T, delta_H_rxn),
                    stoichiometry, C_A0, C_B0, C_C0, C_D0
                )
                for T in T_range
            ]
            graph_equilibrium_vs_temperature(T_range, X_eq_range)
            graph_conversion_with_equilibrium(t_eval, X_A_eval, X_eq_range)

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
                C_A0=C_A0, C_B0=C_B0, C_C0=C_C0, C_D0=C_D0, C_I=C_I, order=order, stoichiometry=stoichiometry,
                excess_B=excess_B, C_p_dict=C_p_dict, delta_H_rxn=delta_H_rxn,
                T_ref=T_ref, E=E, K_eq_ref=K_eq_ref,
                U=U, A_ICQ=A_ICQ, T_cool=T_cool, m_c=m_c, Cp_ref=Cp_ref,
                reversible = reversible,
                sim_params = sim_params
        ),
            [0, 4000],
            [0.0, T0],  # X_A = 0, T = T0
            dense_output=True,
            events=evento_conversion_max,
            max_step=1.0
        )

        #PROCESAR RESULTADOS
        t_final = sol.t_events[0][0] if sol.t_events[0].size > 0 else sol.t[-1]
        t_eval = np.linspace(0, t_final, 100)
        X_A_eval = sol.sol(t_eval)[0]
        T_eval = sol.sol(t_eval)[1]
        concentrations = calculate_concentrations(C_A0, C_B0,C_C0, C_D0, X_A_eval, stoichiometry)
        T_final = T_eval[-1]
        k_final = calculate_rate_constant(A=A, E=E, T=T_final, T_ref=T_ref)
        Ta2 = T_eval - (T_eval - T_cool) * np.exp(-U * A_ICQ / (m_c * Cp_ref))

        if reversible:
            try:
                T_range = np.linspace(min(T_eval), max(T_eval) * 1.5, 100)
                X_eq_din_range = [
                    equilibrium_conversion_calculate(
                        calculate_keq_auto(sim_params, T=T),
                        stoichiometry,
                        C_A0, C_B0,
                        C_C0, C_D0
                    ) for T in T_eval
                ]
                graph_equilibrium_vs_temperature(T_range, X_eq_din_range)
                graph_conversion_with_equilibrium(t_eval, X_A_eval, X_eq_din_range)
            except Exception as e:
                print(f"❌ Error al graficar el equilibrio: {e}")



        return t_eval, X_A_eval, T_eval, concentrations, sol.t[-1], k_final, Ta2
