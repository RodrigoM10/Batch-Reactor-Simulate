import numpy as np
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
        try:
            # Conversión segura de parámetros numéricos
            C_A0 = float(sim_params.get("C_A0", 0))
            C_B0 = float(sim_params.get("C_B0", 0))
            C_C0 = float(sim_params.get("C_C0", 0))
            C_D0 = float(sim_params.get("C_D0", 0))

        except (TypeError, ValueError) as e:
            resultado["message"] = f"Error en parámetros iniciales de concentración: {e}"
            return resultado

        order = sim_params["order"]
        stoichiometry = sim_params["stoichiometry"]
        excess_B = sim_params["excess_B"]
        reversible = sim_params["reversible"]

        K_det = sim_params["K_det"]
        if K_det is not None:
            k = K_det
            A = E = None
            T = sim_params["T_iso"]
        else:
            A = sim_params["A"]
            E = sim_params["E"]
            T = sim_params["T_iso"]
            k = None

        K_eq = None
        X_eq = None

        if reversible:
            print("\n--- Cálculo de K_eq ---")
            K_eq = calculate_keq_auto(sim_params)
            print(f"✅ K_eq calculado automáticamente: {K_eq:.4f}")
            X_eq = equilibrium_conversion_calculate(K_eq, stoichiometry, C_A0, C_B0, C_C0, C_D0)
            print(f"✅ Conversión de equilibrio calculada: X_eq = {X_eq:.3f}")

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
            k=k, C_A0=C_A0, C_B0=C_B0, C_C0=C_C0, C_D0=C_D0, order=order,
            stoichiometry=stoichiometry, excess_B=excess_B, X_eq=X_eq,
            A=A, E=E, T=T, X_A_desired=X_A_desired, t_reaction_det=t_reaction_det,
            reversible=reversible, Keq=K_eq
        )
        ans_volume = sim_params.get("ans_volume", "n").strip().lower()
        V = None
        if ans_volume == "s":
            try:
                P_k = sim_params["P_k"]
                t_mcd = sim_params["t_mcd"]
                product_k = sim_params["product_k"].strip().upper()
                m_k = sim_params["m_k"]/1000
                C_k_final = concentrations[product_k][-1]  # Última concentración simulada del producto
                if C_k_final <= 0:
                    raise ValueError(f"La concentración final del producto '{product_k}' no puede ser cero o negativa.")
                V = calculate_batch_reactor_volume(
                    P_k,
                    m_k,
                    C_k_final,
                    t_final,
                    t_mcd
                )
                print(f"✅ Volumen necesario del reactor: {V:.2f} L")
            except Exception as e:
                print(f"❌ Error calculando volumen: {e}")

        resultado["success"] = True
        resultado["summary"] = {
            "t_final": round(t_final, 2),
            "X_A_final": round(float(X_A_eval[-1]), 2),
            "k_final": k,
            "T_final": round(T, 2) if T is not None else None,
            "volume": round(V, 2) if V is not None else None,
            "X_eq": round(X_eq, 2) if X_eq is not None else None
        }
        resultado["data"] = {
            "t_eval": t_eval,
            "X_A_eval": X_A_eval,
            "concentrations": concentrations,
            "X_eq": X_eq
        }
        resultado["message"] = "Simulación isotérmica completada."

    elif mode == "non-isothermal":
        try:
            # Conversión segura de parámetros numéricos
            C_A0 = float(sim_params.get("C_A0", 0))
            C_B0 = float(sim_params.get("C_B0", 0))
            C_C0 = float(sim_params.get("C_C0", 0))
            C_D0 = float(sim_params.get("C_D0", 0))
            C_I = float(sim_params.get("C_I", 0))
        except (TypeError, ValueError) as e:
            resultado["message"] = f"Error en parámetros iniciales de concentración: {e}"
            return resultado

        order = sim_params["order"]
        reversible = sim_params["reversible"]
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
        mode_energy = sim_params["mode_energy"].strip().lower()
        U = sim_params["U"]
        A_ICQ = sim_params["A_ICQ"]
        T_cool = sim_params["T_cool"]
        m_c = sim_params["m_c"]
        Cp_ref = sim_params["Cp_ref"]
        Qgb_eval = None
        Qrb_eval = None

        t_eval, X_A_eval, T_eval, concentrations, t_final, k_final, Ta2 = nonisothermal_batch_reactor_simulate(
            k, C_A0, C_B0, C_C0, C_D0, C_I, order, reversible, stoichiometry, excess_B,
            A, E, T0, T_ref, delta_H_rxn, C_p_dict, K_eq_ref,
            mode_energy, U, A_ICQ, T_cool, m_c, Cp_ref, sim_params=sim_params
        )

        if mode_energy == "icq":
            try:
                Qgb_eval, Qrb_eval = heat_rates_calculate(
                    X_A_eval, T_eval, A, E, T_ref, delta_H_rxn,
                    C_A0, C_B0, C_C0, C_D0, order, stoichiometry, excess_B, reversible,
                    sim_params,
                    U, A_ICQ, T_cool, m_c, Cp_ref
                )
            except Exception as e:
                print(f"❌ Error Calculo de Calor Generado: {e}")

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
