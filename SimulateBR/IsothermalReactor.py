import numpy as np
from scipy.integrate import quad, solve_ivp

from SimulateBR.ReactionUtils import balance_reactor, reaction_rate


def isothermal_reaction_time(k, C_A0, C_B0, C_C0, C_D0, X_A_desired,
                             order, stoichiometry, excess_B,
                             reversible=False, Keq=None):
    def integrand(X_A):
        try:
            r_A = reaction_rate(X_A, k, C_A0, C_B0, C_C0, C_D0, order,
                                stoichiometry, excess_B,
                                reversible=reversible, Keq=Keq)
            if r_A <= 0 or np.isnan(r_A):
                return np.inf
            return C_A0 / r_A
        except Exception:
            return np.inf

    # Evitamos pasar X_A_desired > 1 o < 0
    X_A_desired = np.clip(X_A_desired, 0.0, 1.0)

    X_A_values = np.linspace(0, X_A_desired, 100)
    t_r_values = []

    for x in X_A_values:
        try:
            integral_result, _ = quad(integrand, 0, x)
            t_r_values.append(integral_result)
        except Exception:
            t_r_values.append(np.inf)

    return t_r_values, X_A_values

def calculate_conversion_at_time(t_eval, k, C_A0, C_B0, C_C0, C_D0, order,
                                  stoichiometry, excess_B, X_eq,
                                  reversible=False, Keq=None):
    y0 = [0.0] # X_A inicial

    sol = solve_ivp( lambda t, y: balance_reactor(t, y, k, C_A0, C_B0, C_C0, C_D0, order,
                                                  stoichiometry, excess_B, reversible, Keq),
                     [t_eval[0], t_eval[-1]], y0, t_eval=t_eval,dense_output=True)

    if reversible:
        # Clip físico con el límite de equilibrio
        X_A_eval = np.clip(sol.y[0], 0.0, X_eq)
    else:
        # Clip físico sin límite artificial entre 0 y 1
        X_A_eval = np.clip(sol.y[0], 0.0, 1.0)

    return X_A_eval