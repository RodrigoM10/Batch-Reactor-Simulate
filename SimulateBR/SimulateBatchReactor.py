import numpy as np

from SimulateBR.Display import (
    graph_conversion,
    graph_concentrations,
    graph_inverse_rate,
    graph_temperature,
    graph_conversion_vs_temperature,
    concentration_time_table,
    graph_heat_rates
)
from SimulateBR.Equilibrium import calculate_keq_auto, equilibrium_conversion_calculate
from SimulateBR.HeatRatesCalculate import heat_rates_calculate
from SimulateBR.IsothermalSimulate import isothermal_batch_reactor_simulate
from SimulateBR.NonIsothermalSimulate import nonisothermal_batch_reactor_simulate
from SimulateBR.VolumeCalculation import calculate_batch_reactor_volume


def simulate_batch_reactor(sim_params: dict):

    mode = sim_params["mode_op"]
    resultado = {
        "success": False,
        "summary": {},
        "data": {},
        "message": ""
    }

    if mode == "isothermal":
        C_A0 = sim_params["C_A0"]
        C_B0 = sim_params["C_B0"]
        order = sim_params["order"]
        stoichiometry = sim_params["stoichiometry"]
        excess_B = sim_params["excess_B"]

        print("\n--- Cálculo de K_eq ---")
        K_eq = calculate_keq_auto(sim_params)
        print(f"✅ K_eq calculado automáticamente: {K_eq:.4f}")
        X_eq = equilibrium_conversion_calculate(K_eq, stoichiometry, C_A0, C_B0)
        print(f"✅ Conversión de equilibrio calculada: X_eq = {X_eq:.3f}")

        K_det = sim_params["K_det"]
        if K_det is not None:
            k = K_det
            A = E = T = None
        else:
            A = sim_params["A"]
            E = sim_params["E"]
            T = sim_params["T_iso"]
            k = None

        option = sim_params["option"].strip().upper()
        if option == "X":
            X_A_desired = sim_params["X_A_desired"]
            t_reaction_det = None
            if X_eq is not None and X_A_desired > X_eq:
                resultado["message"] = (
                    f"⚠️ La conversión deseada ({X_A_desired:.3f}) excede la conversión de equilibrio ({X_eq:.3f}). "
                    f"Por favor, ingrese un valor menor o igual a X_eq."
                )
                resultado["success"] = False
                resultado["warning"] = True  # Campo personalizado para que el front muestre un aviso
                resultado["summary"] = {
                    "X_A_desired": X_A_desired,
                    "X_eq": X_eq
                }
                return resultado
        elif option == "T":
            t_reaction_det = sim_params["t_reaction_det"]
            X_A_desired = None
        else:
            raise ValueError("Opción inválida")

        t_eval, X_A_eval, concentrations, t_final, k = isothermal_batch_reactor_simulate(
            k=k, C_A0=C_A0, C_B0=C_B0, order=order,
            stoichiometry=stoichiometry, excess_B=excess_B, X_eq=X_eq,
            A=A, E=E, T=T, X_A_desired=X_A_desired, t_reaction_det=t_reaction_det
        )

        graph_conversion(t_eval, X_A_eval, X_eq)

        ans_volume = sim_params.get("ans_volume", "n").strip().lower()
        V = None
        if ans_volume == "s":
            try:
                P_k = sim_params["P_k"]
                t_c_d = sim_params["t_c_d"]
                t_m = sim_params["t_m"]
                product_k = sim_params["product_k"].strip().upper()
                m_k = sim_params["m_k"]

                if product_k not in stoichiometry:
                    raise ValueError(f"'{product_k}' no está definido en la estequiometría de la reacción.")

                alpha_k = stoichiometry[product_k]
                if alpha_k <= 0:
                    raise ValueError(f"'{product_k}' no es un producto válido (coeficiente debe ser positivo).")

                alpha_X_list = [alpha_k * (X_A_desired if X_A_desired is not None else X_A_eval[-1])]

                V = calculate_batch_reactor_volume(P_k, m_k, alpha_X_list, t_final, t_c_d, t_m)
                print(f"✅ Volumen necesario del reactor: {V:.2f} L")

                graph_inverse_rate(X_A_eval, k, C_A0, C_B0, order, stoichiometry, excess_B)

            except Exception as e:
                print(f"❌ Error calculando volumen: {e}")

        graph_concentrations(t_eval, concentrations)
        concentration_time_table(t_eval, concentrations, stoichiometry, t_final)

        resultado["success"] = True
        resultado["summary"] = {
            "t_final": t_final,
            "X_A_final": X_A_eval[-1],
            "k_final": k,
            "T_final": None,
            "volume": V
        }
        resultado["data"] = {
            "t_eval": t_eval,
            "X_A_eval": X_A_eval,
            "concentrations": concentrations,
            "X_eq": X_eq
        }
        resultado["message"] = "Simulación isotérmica completada."

    elif mode == "non-isothermal":
        C_A0 = sim_params["C_A0"]
        C_B0 = sim_params["C_B0"]
        C_I = sim_params["C_I"]
        order = sim_params["order"]
        stoichiometry = sim_params["stoichiometry"]
        excess_B = sim_params["excess_B"]
        k = None

        A = sim_params["A"]
        E = sim_params["E"]
        T_ref = sim_params["T_ref"]
        K_eq_ref = sim_params["K_eq_ref"]
        T0 = sim_params["T0"]
        delta_H_rxn = sim_params["delta_H_rxn"]
        C_p_dict = sim_params["C_p_dict"]
        mode_energy = sim_params["mode_energy"]
        U = sim_params["U"]
        A_ICQ = sim_params["A_ICQ"]
        T_cool = sim_params["T_cool"]
        m_c = sim_params["m_c"]
        Cp_ref = sim_params["Cp_ref"]
        Qgb_eval = None
        Qrb_eval = None

        t_eval, X_A_eval, T_eval, concentrations, t_final, k_final, Ta2 = nonisothermal_batch_reactor_simulate(
            k, C_A0, C_B0, C_I, order, stoichiometry, excess_B,
            A, E, T0, T_ref, delta_H_rxn, C_p_dict, K_eq_ref,
            mode_energy, U, A_ICQ, T_cool, m_c, Cp_ref
        )

        graph_temperature(t_eval, T_eval, Ta2)

        if mode_energy == "adiabatic":
            graph_conversion_vs_temperature(X_A_eval, T_eval)
        elif mode_energy == "icq":
            try:
                Qgb_eval, Qrb_eval = heat_rates_calculate(
                     X_A_eval, T_eval, A, E, T_ref, delta_H_rxn,
                    C_A0, C_B0, order, stoichiometry, excess_B,
                    U, A_ICQ, T_cool, m_c, Cp_ref
                )
                graph_heat_rates(t_eval, Qgb_eval, Qrb_eval)
            except Exception as e:
                print(f"❌ Error Calculo de Calor Generado: {e}")

        graph_concentrations(t_eval, concentrations)
        concentration_time_table(t_eval, concentrations, stoichiometry, t_final)

        resultado["success"] = True
        resultado["summary"] = {
            "t_final": t_final,
            "X_A_final": X_A_eval[-1],
            "k_final": k_final,
            "T_final": T_eval[-1],
            "volume": None,
            "Qgb_eval":Qgb_eval,
            "Qrb_eval":Qrb_eval
        }
        resultado["data"] = {
            "t_eval": t_eval,
            "X_A_eval": X_A_eval,
            "T_eval": T_eval,
            "Ta2": Ta2,
            "concentrations": concentrations,
            "Qgb_eval": Qgb_eval,
            "Qrb_eval": Qrb_eval
        }
        resultado["message"] = "Simulación no isotérmica completada."

    else:
        raise ValueError("Modo de operación inválido.")


    # Convertir todos los arrays numpy a listas para que sean serializables por JSON
    def safe_convert(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: safe_convert(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [safe_convert(i) for i in obj]
        else:
            return obj

    resultado["summary"] = safe_convert(resultado["summary"])
    resultado["data"] = safe_convert(resultado["data"])

    return resultado
