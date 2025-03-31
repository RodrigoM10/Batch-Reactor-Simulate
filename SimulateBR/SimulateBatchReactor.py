from Display import (
    graph_conversion,
    graph_concentrations,
    graph_inverse_rate,
    graph_temperature,
    graph_conversion_vs_temperature,
)
from IsothermalSimulate import isothermal_batch_reactor_simulate
from NonIsothermalSimulate import nonisothermal_batch_reactor_simulate
from VolumeCalculation import calculate_batch_reactor_volume

# Modo de operación
mode = input("¿Modo de operación? (isothermal / non-isothermal): ").strip().lower()

if mode == "isothermal":
    C_A0 = 1.0
    C_B0 = 55.5
    order = 1
    stoichiometry = {"A": -1, "B": -1, "C": 1}
    excess_B = True

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
        t_reaction_det = None
    elif opcion == "T":
        t_reaction_det = float(input("Ingrese tiempo de reacción (min): "))
        X_A_desired = None
    else:
        raise ValueError("Opción inválida")

    t_eval, X_A_eval, concentrations, t_final, k = isothermal_batch_reactor_simulate(
        k=k, C_A0=C_A0, C_B0=C_B0, order=order, stoichiometry=stoichiometry, excess_B=excess_B,
        A=A, E=E, T=T, X_A_desired=X_A_desired, t_reaction_det=t_reaction_det
    )

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
            producto_k = input("Ingrese el nombre del producto (por ejemplo, C o D): ").strip()
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
    C_A0 = 1.0
    C_B0 = 55.5
    C_I = 0.0
    order = 1
    X_A_desired = 0.8
    stoichiometry = {"A": -1, "B": -1, "C": 1}
    excess_B = True
    k = None
    #----------
    A = 4710000000
    E = 18000
    T_ref = 297
    T0 = 286
    delta_H_rxn = 20202
    mode_energy = "adiabatic"

    C_p_dict = {
        "A": 35,
        "B": 18,
        "C": 46,
        "I": 19.5,
    }
    #----------
    # A = float(input("Ingrese el factor preexponencial A (1/min): "))
    # E = float(input("Ingrese E (J/mol): "))
    # T_ref = float(input("Ingrese T_ref (K): "))
    # T0 = float(input("Ingrese temperatura inicial T0 (K): "))
    # delta_H_rxn = float(input("Ingrese ΔH_rxn (J/mol): "))
    # mode_energy = input("Modo energético (adiabatic / non-adiabatic / ICQ): ").strip()

    # C_p_dict = {
    #     "A": float(input("Cp A (J/mol·K): ")),
    #     "B": float(input("Cp B (J/mol·K): ")),
    #     "C": float(input("Cp C (J/mol·K): ")),
    #     "I": float(input("Cp I (J/mol·K): ")),
    # }

    U = A_ICQ = T_cool = None
    if mode_energy in ["non-adiabatic", "ICQ"]:
        U = float(input("Ingrese coeficiente global de transferencia U (J/min·m²·K): "))
        A_ICQ = float(input("Ingrese área de intercambio A (m²): "))
        T_cool = float(input("Ingrese temperatura del fluido de enfriamiento (K): "))

    t_eval, X_A_eval, T_eval, concentrations, t_final = nonisothermal_batch_reactor_simulate(
        k, C_A0, C_B0, C_I, order, stoichiometry, excess_B,
        A, E, T0, T_ref, delta_H_rxn, C_p_dict,
        mode_energy, U, A_ICQ, T_cool
    )
    graph_temperature(t_eval, T_eval)
    graph_conversion_vs_temperature(X_A_eval, T_eval)
else:
    raise ValueError("Modo inválido")

# Mostrar resultados generales
graph_conversion(t_eval, X_A_eval)
graph_concentrations(t_eval, concentrations)

print(f"\n✅ Tiempo final de simulación: {t_final:.2f} min")
if mode == "non-isothermal":
    print(f"🌡️ Temperatura final: {T_eval[-1]:.2f} K")
print(f"🧪 Conversión final: {X_A_eval[-1]:.4f}")
