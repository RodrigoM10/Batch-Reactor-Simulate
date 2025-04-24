from Display import (
    graph_conversion,
    graph_concentrations,
    graph_inverse_rate,
    graph_temperature,
    graph_conversion_vs_temperature,
    concentration_time_table,
    graph_heat_rates
)
from Equilibrium import equilibrium_conversion_calculate, calculate_keq_auto
from IsothermalSimulate import isothermal_batch_reactor_simulate
from NonIsothermalSimulate import nonisothermal_batch_reactor_simulate
from VolumeCalculation import calculate_batch_reactor_volume
from load_json import load_json_params

sim_params = load_json_params()

# mode = input("¿Modo de operación? (isothermal / non-isothermal): ").strip().lower()
mode = sim_params["mode_op"]

if mode == "isothermal":
    C_A0 = sim_params["C_A0"]
    C_B0 = sim_params["C_B0"]
    order = 1
    stoichiometry = sim_params["stoichiometry"]
    excess_B = sim_params["excess_B"]

    print("\n--- Cálculo  de K_eq ---")

    K_eq = calculate_keq_auto(sim_params)
    print(f"✅ K_eq calculado automáticamente: {K_eq:.4f}")
    X_eq = equilibrium_conversion_calculate(K_eq, sim_params["stoichiometry"], sim_params["C_A0"], sim_params["C_B0"])
    print(f"✅ Conversión de equilibrio calculada: X_eq = {X_eq:.3f}")

    K_det = sim_params["K_det"]
    if K_det is not None:
        k = K_det
        A = E = T = None
    else:
        print("\n--- Cálculo de constante de velocidad usando Arrhenius ---")
        A = sim_params["A"]
        E = sim_params["E"]
        T = sim_params["T_iso"]
        k = None

    option = sim_params["option"].strip().upper()
    if option == "X":
        X_A_desired = sim_params["X_A_desired"]
        if X_A_desired > X_eq:
            print(f"⚠️ La conversión deseada ({X_A_desired:.4f}) supera la conversión de equilibrio ({X_eq:.4f}).")
            decide = input("¿Desea usar X_eq como nueva conversión? (s/n): ").strip().lower()
            if decide == "s":
                X_A_desired = X_eq
                sim_params["X_A_desired"] = X_eq
            else:
                nueva_X = float(input("Ingrese una nueva conversión deseada menor o igual a X_eq: "))
                X_A_desired = min(nueva_X, X_eq)
                sim_params["X_A_desired"] = min(nueva_X, X_eq)

        t_reaction_det = None
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
    if t_reaction_det is not None:
        print(f"\n🔍 Conversión alcanzada en {t_final:.2f} min es de X_A= {X_A_eval[-1]:.4f}")
    else:
        print(f"🕒 Tiempo necesario para alcanzar X_A = {X_A_desired} es {t_final:.2f} minutos")

    ans_volume = sim_params["ans_volume"]

    if ans_volume == "s":
        print("\n--- Cálculo del volumen del reactor ---")
        try:
            P_k = sim_params["P_k"]
            t_c_d = sim_params["t_c_d"]
            t_m = sim_params["t_m"]
            product_k = sim_params["product_k"].strip().upper()
            m_k = sim_params["m_k"]
            stoichiometry = sim_params["stoichiometry"]

            if product_k not in stoichiometry:
                raise ValueError(f"'{product_k}' no está definido en la estequiometría de la reacción.")

            alpha_k = stoichiometry[product_k]
            if alpha_k <= 0:
                raise ValueError(f"'{product_k}' no es un producto (coeficiente debe ser positivo).")

            alpha_X_list = [alpha_k * (X_A_desired if X_A_desired is not None else X_A_eval[-1])]
            V = calculate_batch_reactor_volume(P_k, m_k, alpha_X_list, t_final, t_c_d, t_m)

            print(f"\n✅ Volumen necesario del reactor: {V:.2f} L")
            graph_inverse_rate(X_A_eval, k, C_A0, C_B0, order, stoichiometry, excess_B)

        except ValueError as err:
            print(f"❌ Error en el cálculo del volumen: {err}")
    else:
        print("\nℹ️ Volumen del reactor no calculado.")

elif mode == "non-isothermal":
    C_A0 = sim_params["C_A0"]
    C_B0 = sim_params["C_B0"]
    C_I = sim_params["C_I"]
    order = sim_params["order"]
    stoichiometry = sim_params["stoichiometry"]
    excess_B = sim_params["excess_B"]
    k = None
    #----------
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

    t_eval, X_A_eval, T_eval, concentrations, t_final, k_final, Ta2 = nonisothermal_batch_reactor_simulate(
        k, C_A0, C_B0, C_I, order, stoichiometry, excess_B,
        A, E, T0, T_ref, delta_H_rxn, C_p_dict, K_eq_ref,
        mode_energy, U, A_ICQ, T_cool, m_c, Cp_ref
    )
    graph_temperature(t_eval, T_eval, Ta2)
    if mode_energy in ["adiabatic"]: graph_conversion_vs_temperature(X_A_eval, T_eval)
    if mode_energy in ["non-adiabatic", "ICQ"]: graph_heat_rates(t_eval, X_A_eval, T_eval, A, E, T_ref, delta_H_rxn, C_A0, C_B0, order, stoichiometry, excess_B,
                                                                 U, A_ICQ, T_cool, m_c, Cp_ref)
else:
    raise ValueError("Modo inválido")

# Mostrar resultados generales

graph_concentrations(t_eval, concentrations)
concentration_time_table(t_eval, concentrations, stoichiometry,t_final)
print(f"\n✅ Tiempo final de simulación: {t_final:.2f} min")
if mode == "non-isothermal":
    print(f"🌡️ Temperatura final: {T_eval[-1]:.2f} K")
    print(f"🌠 Constante de Velocidad K final: {k_final:.5f}")

print(f"🧪 Conversión final: {X_A_eval[-1]:.4f}")
