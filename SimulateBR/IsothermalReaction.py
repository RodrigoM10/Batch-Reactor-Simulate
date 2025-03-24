import numpy as np
from scipy.integrate import quad
from ReactionRate import reaction_rate

def isothermal_reaction_time(k, C_A0, C_B0, X_A_desired, order, stoichiometry,excess_B):
    """
    Calcula el tiempo de reacción isotérmico resolviendo la integral t_r = ∫ (1/r_A) dX_A.

    Parámetros:
        k            -> Constante de velocidad (1/min, L/mol*min, etc.)
        C_A0         -> Concentración inicial de A (mol/L)
        C_B0         -> Concentración inicial de B (mol/L) (opcional)
        X_A_desired  -> Conversión deseada del reactivo limitante
        order        -> Orden de la reacción (1 o 2)
        stoichiometry -> Diccionario con coeficientes estequiométricos {"A": -1, "B": -1, "C": 1, "D": 1}


    Retorna:
        t_r_values -> Lista de tiempos acumulados evaluados.
        X_A_values -> Lista de conversiones correspondientes.
    """

    # Función interna para evaluar 1/r_A en función de X_A
    def integrand(X_A):
        r_A = reaction_rate(X_A, k, C_A0, C_B0, order, stoichiometry, excess_B)
        # Evita divisiones por cero retornando infinito si r_A = 0 o valores inconsistentes
        if r_A == 0:
            return np.inf
        return 1 / (-r_A) if r_A < 0 else np.inf

    # Generar valores de conversión de 0 a X_A_desired distribuidos uniformemente
    X_A_values = np.linspace(0, X_A_desired, 100)

    # Calcular el tiempo acumulado resolviendo la integral para cada X_A
    t_r_values = []
    for x in X_A_values:
        try:
            # Resolver la integral desde 0 hasta x
            integral_result, _ = quad(integrand, 0, x)
            t_r_values.append(integral_result)
        except Exception as e:
            # En caso de falla, manejar valores no integrables
            t_r_values.append(np.inf)

    return t_r_values, X_A_values  # Devolvemos tiempos y conversiones correctas
