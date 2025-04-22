from Display import (
    graph_conversion,
    graph_concentrations,
    graph_inverse_rate,
    graph_temperature,
    graph_conversion_vs_temperature,
    concentration_time_table,
    graph_heat_rates
)
from IsothermalEquilibriumConstant import equilibrium_conversion_calculate
from IsothermalSimulate import isothermal_batch_reactor_simulate
from NonIsothermalSimulate import nonisothermal_batch_reactor_simulate
from VolumeCalculation import calculate_batch_reactor_volume

# Modo de operación
mode = input("¿Modo de operación? (isothermal / non-isothermal): ").strip().lower()

if mode == "isothermal":
    C_A0 = 0.061
    C_B0 = 0.061
    order = 1
    stoichiometry = {"A": -1, "B": -1, "C": 1, "D": 1}
    excess_B = True

    X_eq = equilibrium_conversion_calculate(stoichiometry, C_A0, C_B0)

    k_det = (
        input("¿Desea ingresar directamente la constante de velocidad k? (s/n): ")
        .strip()
        .lower()
    )
    if k_det == "s":
        k = float(input("Ingrese la constante de velocidad k (1/min): "))
        A = E = T = None
    else:
        print("\n--- Cálculo de constante de velocidad usando Arrhenius ---")
        A = float(input("Ingrese el factor preexponencial A (1/min): "))
        E = float(input("Ingrese la energía de activación E (J/mol): "))
        T = float(input("Ingrese la temperatura de operación T (K): "))
        k = None

    opcion = input("¿Desea ingresar conversión deseada (X) o tiempo (T)? ").strip().upper()
    if opcion == "X":
        X_A_desired = float(input("Ingrese conversión deseada (0–1): "))
        if X_A_desired > X_eq:
            print(f"⚠️ La conversión deseada ({X_A_desired:.4f}) supera la conversión de equilibrio ({X_eq:.4f}).")
            decide = input("¿Desea usar X_eq como nueva conversión? (s/n): ").strip().lower()
            if decide == "s":
                X_A_desired = X_eq
            else:
                nueva_X = float(input("Ingrese una nueva conversión deseada menor o igual a X_eq: "))
                X_A_desired = min(nueva_X, X_eq)
        t_reaction_det = None
    elif opcion == "T":
        t_reaction_det = float(input("Ingrese tiempo de reacción (min): "))
        X_A_desired = None
    else:
        raise ValueError("Opción inválida")

    t_eval, X_A_eval, concentrations, t_final, k = isothermal_batch_reactor_simulate(
        k=k, C_A0=C_A0, C_B0=C_B0, order=order, stoichiometry=stoichiometry, excess_B=excess_B, X_eq=X_eq,
        A=A, E=E, T=T, X_A_desired=X_A_desired, t_reaction_det=t_reaction_det
    )
    graph_conversion(t_eval, X_A_eval, X_eq)
    if t_reaction_det is not None:
        print(f"\n🔍 Conversión alcanzada en {t_final:.2f} min es de X_A= {X_A_eval[-1]:.4f}")
    else:
        print(f"🕒 Tiempo necesario para alcanzar X_A = {X_A_desired} es {t_final:.2f} minutos")

    ans_volume = input("¿Desea calcular el volumen del reactor? (s / n): ").strip().lower()

    if ans_volume == "s":
        print("\n--- Cálculo del volumen del reactor ---")
        try:
            P_k = float(input("Ingrese la producción deseada del producto k (en g/min): "))
            t_carga_descarga = float(input("Ingrese el tiempo de carga y descarga (min): "))
            t_muerto = float(input("Ingrese el tiempo muerto del ciclo (min): "))
            producto_k = input("Ingrese el nombre del producto (por ejemplo, C o D): ").strip().upper()
            m_k = float(input(f"Ingrese la masa molar de {producto_k} (g/mol): "))

            if producto_k not in stoichiometry:
                raise ValueError(f"'{producto_k}' no está definido en la estequiometría de la reacción.")

            alpha_k = stoichiometry[producto_k]
            if alpha_k <= 0:
                raise ValueError(f"'{producto_k}' no es un producto (coeficiente debe ser positivo).")

            alpha_X_list = [alpha_k * (X_A_desired if X_A_desired is not None else X_A_eval[-1])]
            V = calculate_batch_reactor_volume(P_k, m_k, alpha_X_list, t_final, t_carga_descarga, t_muerto)

            print(f"\n✅ Volumen necesario del reactor: {V:.2f} L")
            graph_inverse_rate(X_A_eval, k, C_A0, C_B0, order, stoichiometry, excess_B)


        except ValueError as err:
            print(f"❌ Error en el cálculo del volumen: {err}")
    else:
        print("\nℹ️ Volumen del reactor no calculado.")

elif mode == "non-isothermal":
    C_A0 = 1
    C_B0 = None
    C_I = 1
    order = 1
    stoichiometry = {"A": -1, "C": 1}
    excess_B = False
    k = None
    #----------
    A = 756.07
    E = 10000
    T_ref = 298
    T0 = 480
    delta_H_rxn = -14000
    C_p_dict = {
        "A": 25,
        "C": 25,
        "I": 50,
    }
    K_eq_ref = 75000
    # C_A0 = 54.8
    # C_B0 = 555
    # C_I = 98.8
    # order = 1
    # stoichiometry = {"A": -1, "B": -1, "C": 1}
    # excess_B = False
    # k = None
    # # ----------
    # A = 4710000000
    # E = 18000
    # T_ref = 298
    # T0 = 286
    # delta_H_rxn = -20202
    # C_p_dict = {
    #     "A": 35,
    #     "B": 18,
    #     "C": 46,
    #     "I": 19.5,
    # }
    # K_eq_ref = 1.2

    mode_energy = "adiabatic"

    U = A_ICQ = T_cool = m_c = Cp_ref = None
    if mode_energy in ["non-adiabatic", "ICQ"]:

        U = 10
        A_ICQ = 1
        T_cool = 290
        m_c = 10
        Cp_ref = 4.16

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
