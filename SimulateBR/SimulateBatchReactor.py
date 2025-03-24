import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Importamos módulos
from ReactorBalance import balance_reactor
from SimulateBR.IsothermalReaction import calculate_conversion_at_time
from SimulateBR.VolumeCalculation import calculate_batch_reactor_volume
from Stoichiometry import calculate_concentrations
from Display import graph_conversion, graph_concentrations, graph_inverse_rate
from IsothermalReaction import isothermal_reaction_time
from RateConstant import calculate_rate_constant


def batch_reactor_simulate(k, C_A0, C_B0, C_I, X_A_desired, order, stoichiometry, mode, excess_B,
                           A=None, E=None, T=None, t_reaction_det=None):

    #if X_A_desired >= 1 or X_A_desired <= 0:
      #  raise ValueError("X_A_desired debe estar entre 0 y 1")

    if mode == "isothermal":
        # Si se proporciona A, E y T, se calcula k por Arrhenius
        if A is not None and E is not None and T is not None:
            k = calculate_rate_constant(A, E, T)
            print(f"\n🔹 Constante k calculada por Arrhenius: {k:.4f} 1/min")

        if t_reaction_det is not None:
            # Nuevo camino: calcular conversión a tiempo dado
            t_eval = np.linspace(0, t_reaction_det, 100)
            X_A_eval = calculate_conversion_at_time(t_eval, k, C_A0, C_B0, order, stoichiometry, excess_B)
            t_final = t_reaction_det
        else:
            # Camino clásico: conversión deseada
            t_eval, X_A_eval = isothermal_reaction_time(k, C_A0, C_B0, X_A_desired, order, stoichiometry, excess_B)
            t_final = t_eval[-1]

        concentrations = calculate_concentrations(C_A0, C_B0, X_A_eval, stoichiometry)
        return t_eval, X_A_eval, concentrations, t_final, k

    else:
        def stop_event(t, y):
            return y[0] - X_A_desired

        stop_event.terminal = True
        stop_event.direction = 1

        y0 = [0.0]  # Conversión inicial
        sol = solve_ivp(lambda t, y: balance_reactor(t, y, k, C_A0, C_B0, order, stoichiometry, excess_B),
                        [0, 1000], y0, events=stop_event, dense_output=True)


        if len(sol.t_events[0]) == 0:
            raise ValueError( "El evento no fue detectado. Verifique las condiciones iniciales o reduzca el valor de X_A_desired.")

        t_final = sol.t_events[0][0]
        t_eval = np.linspace(0, t_final, 100)
        X_A_eval = sol.sol(t_eval)[0]

        concentrations = calculate_concentrations(C_A0, C_B0, X_A_eval, stoichiometry)

        return t_eval, X_A_eval, concentrations, t_final, k

# =================== FIN BLOQUE PRINCIPAL ===================

# **Parámetros iniciales**
mode = "isothermal"
stoichiometry = {"A":-1, "B":-1, "C":1}
type_reaction = "ia A + ib B -> ic C + id C"
order = 1 # Orden de la reacción
C_A0 = 1 # Concentración inicial de A (mol/L)
C_B0 = 2.5  # Concentración inicial de B (mol/L)
C_I = 0.0  # Concentración de inertes (mol/L)
excess_B = False #Booleano que indica si B está en exceso

# Inicialización de variables
A = E = T  = None
k = 0.0254 # Constante de velocidad (1/min o s)
t_reaction_det = None
X_A_desired = None

# Ingreso de Datos según el modo de operacion:
if mode == "isothermal":
    print("\n--- Parámetros para modo isotérmico ---")

    k_det = input("¿Desea ingresar directamente la constante de velocidad k? (s/n): ").strip().lower()
    if k_det == "s":
        k = float(input("Ingrese la constante de velocidad k (1/min): "))
    else:
     print("\n--- Cálculo de constante de velocidad usando Arrhenius ---")
     A = float(input("Ingrese el factor preexponencial A (1/min): "))
     E = float(input("Ingrese la energía de activación E (J/mol): "))
     T = float(input("Ingrese la temperatura de operación T (K): "))

    print("\n¿Desea calcular a partir de la conversión deseada o del tiempo de reacción?")
    opcion = input("Escriba 'X' para conversión deseada o 'T' para tiempo de reacción: ").strip().upper()

    if opcion == "X":
        X_A_desired = float(input("Ingrese la conversión deseada de A (entre 0 y 1): "))
        t_reaction_det = None
    elif opcion == "T":
        t_reaction_det = float(input("Ingrese el tiempo de reacción (min): "))
        X_A_desired = None
    else:
        raise ValueError("Opción inválida. Debe ingresar 'X' o 'T'.")
else:
    A = E = T = t_reaction_det = None
    X_A_desired = 0.90
    k = 0.311

# Ejecutamos la simulación
try:
    t_eval, X_A_eval, concentrations, t_final, k = batch_reactor_simulate(
        k, C_A0, C_B0, C_I, X_A_desired, order, stoichiometry, mode, excess_B,
        A=A, E=E, T=T, t_reaction_det = t_reaction_det
    )

    # **Graficamos los resultados**
    graph_conversion(t_eval, X_A_eval)
    graph_concentrations(t_eval, concentrations)

    if mode == "isothermal":
        graph_inverse_rate(X_A_eval, k, C_A0, C_B0, order, stoichiometry, excess_B)

        # Mostrar conversión alcanzada si se ingresó tiempo
        if t_reaction_det is not None:
            print(f"\n🔍 Conversión alcanzada en {t_final:.2f} min: {X_A_eval[-1]:.4f}")
        else:
            # **Mostramos el tiempo necesario para alcanzar la conversión deseada**
            print(f"Tiempo necesario para alcanzar X_A = {X_A_desired} es {t_final:.2f} minutos ✅")

        # Cálculo de volumen
        print("\n--- Cálculo del volumen del reactor ---")
        try:
            # Solicitar al usuario los datos necesarios
            P_k = float(input("Ingrese la producción deseada del producto k (en g/min): "))
            t_carga_descarga = float(input("Ingrese el tiempo de carga y descarga (min): "))
            t_muerto = float(input("Ingrese el tiempo muerto del ciclo (min): "))
            producto_k = input("Ingrese el nombre del producto (por ejemplo, C o D): ").strip()
            m_k = float(input(f"Ingrese la masa molar de {producto_k} (g/mol): "))

            # Obtener coeficiente estequiométrico del producto desde el diccionario
            if producto_k not in stoichiometry:
                raise ValueError(f"'{producto_k}' no está definido en la estequiometría de la reacción.")

            alpha_k = stoichiometry[producto_k]
            if alpha_k <= 0:
                raise ValueError(f"'{producto_k}' no es un producto (coeficiente debe ser positivo).")

            alpha_X_list = [alpha_k * (X_A_desired if X_A_desired is not None else X_A_eval[-1])]
            V = calculate_batch_reactor_volume(P_k, m_k, alpha_X_list, t_final, t_carga_descarga, t_muerto)
            print(f"\n✅ Volumen necesario del reactor: {V:.2f} L")

        except ValueError as err:
            print(f"❌ Error en el cálculo del volumen: {err}")

    # **Mostramos el tiempo necesario para alcanzar la conversión deseada**
    #print(f"Tiempo necesario para alcanzar X_A = {X_A_desired} es {t_final:.2f} minutos")

except ValueError as e:
    print(f"Error: {e}")


