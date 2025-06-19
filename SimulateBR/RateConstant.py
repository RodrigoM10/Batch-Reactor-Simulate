import numpy as np

def calculate_rate_constant(A=None, E=None, T=None, T_ref=None):

    if E is None or T is None:
        raise ValueError("Se requieren E y T para calcular k")

    R = 1.987  # cal/mol·K

    k = None  # Inicializamos la variable k

    if A is not None:
        if T_ref is not None:
            k_ref = A * np.exp(-E / (R * T_ref))
            k = k_ref * np.exp((E/R) * (1/T_ref - 1/T))
        else:
            k = A * np.exp(-E / (R * T))
    else:
        raise ValueError("Falta el parametro A para calcular k")
    return k
