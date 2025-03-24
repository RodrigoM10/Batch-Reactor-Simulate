import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Importamos módulos
from ReactorBalance import balance_reactor
from Stoichiometry import calculate_concentrations
from Display import graph_conversion, graph_concentrations, graph_inverse_rate
from IsothermalReaction import isothermal_reaction_time
from RateConstant import calculate_rate_constant

# **Definir estequiometría de la reacción:
stoichiometry = {"A":-1, "B":-1, "C":1}
# **Parámetros iniciales**
type_reaction = "ia A + ib B -> ic C + id C"
C_A0 = 1 # Concentración inicial de A (mol/L)
C_B0 = 20.5  # Concentración inicial de B (mol/L)
C_I = 0.0  # Concentración de inertes (mol/L)
excess_B = True #Booleano que indica si B está en exceso
X_A_desired = 0.90 # Conversión deseada
mode = "isothermal"
order = 1 # Orden de la reacción

# Inicialización de variables
A = E = T = None
k = None # Constante de velocidad (1/min o s)

# Solo para modo isotérmico: pedir A, E, T
if mode == "isothermal":
    print("\n--- Cálculo de constante de velocidad usando Arrhenius ---")
    A = float(input("Ingrese el factor preexponencial A (1/min): "))
    E = float(input("Ingrese la energía de activación E (J/mol): "))
    T = float(input("Ingrese la temperatura de operación T (K): "))
else:
    A = E = T = None
    k = 0.311  # Valor de k fijo si no es isotérmico (1/min o s)

# Definimos una función para simular el reactor batch
def batch_reactor_simulate(k, C_A0, C_B0, C_I, X_A_desired, order, stoichiometry, mode, excess_B, A=None, E=None, T=None):
    """
     Simula la reacción en un reactor batch considerando los casos isotérmico y no isotérmico.

     Parámetros:
         k            -> Constante de velocidad (1/min, L/mol*min, etc.)
         C_A0         -> Concentración inicial de A (mol/L)
         C_B0         -> Concentración inicial de B (mol/L) (opcional)
         C_I          -> Concentración inicial de inertes (mol/L) (opcional)
         X_A_desired  -> Conversión deseada del reactivo limitante
         order        -> Orden de la reacción (1 o 2)
         stoichiometry -> Diccionario con coeficientes estequiométricos {"A": -1, "B": -1, "C": 1, "D": 1}
         mode         -> "isothermal" para calcular con integración, "non-isothermal" para solve_ivp.

     Retorna:
         t_eval, X_A_eval, concentrations, t_final -> Tiempos, conversión, concentraciones y tiempo final.
     """
    if X_A_desired >= 1 or X_A_desired < 0:
        raise ValueError("X_A_desired debe estar entre 0 y 1")

    if mode == "isothermal":
        # Si A, E y T están definidos, usamos la ecuación de Arrhenius
        if A is not None and E is not None and T is not None:
            k = calculate_rate_constant(A, E, T)
            print(f"🔹 Constante k calculada por Arrhenius: {k:.4f} 1/min")
        # **Usamos integración para calcular t*
        t_eval, X_A_eval = isothermal_reaction_time(k, C_A0, C_B0, X_A_desired, order, stoichiometry, excess_B)
        t_final = t_eval[-1]

        # Calculamos las concentraciones correspondientes
        concentrations = calculate_concentrations(C_A0, C_B0, X_A_eval, stoichiometry)

        # Retornamos los resultados calculados
        return t_eval, X_A_eval, concentrations, t_final, k

    else:
        # **We use solve_ivp para resolver dX_A/dt**
        def stop_event(t, y):
            return y[0] - X_A_desired

        stop_event.terminal = True
        stop_event.direction = 1

        y0 = [0.0]  # Conversión inicial
        sol = solve_ivp(lambda t, y: balance_reactor(t, y, k, C_A0, C_B0, order, stoichiometry, excess_B),
                        [0, 1000], y0, events=stop_event, dense_output=True)

        # Validación para asegurar que el evento fue detectado
        if len(sol.t_events[0]) == 0:
            raise ValueError(
                "El evento no fue detectado. Verifique las condiciones iniciales o reduzca el valor de X_A_desired.")

        t_final = sol.t_events[0][0]

        # Evaluamos en el rango de tiempo
        t_eval = np.linspace(0, t_final, 100)
        X_A_eval = sol.sol(t_eval)[0]

        # Calculamos la concentración de A
        concentrations = calculate_concentrations(C_A0, C_B0, X_A_eval, stoichiometry)

        return t_eval, X_A_eval, concentrations, t_final, k

# **Ejecutamos la simulación**
try:
    t_eval, X_A_eval, concentrations, t_final, k = batch_reactor_simulate(
        k, C_A0, C_B0, C_I, X_A_desired, order, stoichiometry, mode, excess_B,
        A=A, E=E, T=T
    )

    # **Graficamos los resultados**
    graph_conversion(t_eval, X_A_eval)
    graph_concentrations(t_eval, concentrations)

    # Graficamos 1/r_A vs X_A
    if mode == "isothermal":
        graph_inverse_rate(X_A_eval, k, C_A0, C_B0, order, stoichiometry, excess_B)

        # **Mostramos el tiempo necesario para alcanzar la conversión deseada**
        print(f"Tiempo necesario para alcanzar X_A = {X_A_desired} es {t_final:.2f} minutos ✅")

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

            # Calcular α_k * X_A (asumiendo una sola reacción)
            alpha_X_list = [alpha_k * X_A_desired]

            # Llamar a la función de cálculo del volumen
            from VolumeCalculation import calculate_batch_reactor_volume  # Asegurate de tener este módulo

            V = calculate_batch_reactor_volume(P_k, m_k, alpha_X_list, t_final, t_carga_descarga, t_muerto)

            print(f"\n✅ Volumen necesario del reactor: {V:.2f} L")
        except ValueError as err:
            print(f"❌ Error en el cálculo del volumen: {err}")

    # **Mostramos el tiempo necesario para alcanzar la conversión deseada**
    print(f"Tiempo necesario para alcanzar X_A = {X_A_desired} es {t_final:.2f} minutos")
except ValueError as e:
    print(f"Error: {e}")


