import numpy as np
from scipy.integrate import quad, solve_ivp

from ReactionUtils import balance_reactor, reaction_rate


def isothermal_reaction_time(k, C_A0, C_B0, X_A_desired, order, stoichiometry,excess_B):

    # Función interna para evaluar 1/r_A en función de X_A
    def integrand(X_A):
        r_A = reaction_rate(X_A, k, C_A0, C_B0, order, stoichiometry, excess_B)
        # Evita divisiones por cero retornando infinito si r_A = 0 o valores inconsistentes
        if r_A == 0:
            return np.inf
        return 1 / (r_A) if r_A < 0 else np.inf

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

def calculate_conversion_at_time(t_eval, k, C_A0, C_B0, order, stoichiometry, excess_B):

    y0 = [0.0]
    sol = solve_ivp( lambda t, y: balance_reactor(t, y, k, C_A0, C_B0, order, stoichiometry, excess_B),
                     [t_eval[0], t_eval[-1]], y0, t_eval=t_eval,dense_output=True)
    # Clip para mantener conversiones físicas válidas entre 0 y 1
    X_A_eval = np.clip(sol.y[0], 0.0, 1.0)

    return X_A_eval