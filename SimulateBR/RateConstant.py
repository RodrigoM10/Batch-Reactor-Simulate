import numpy as np


def calculate_rate_constant(A=None, E=None, T=None, T_ref=None):
    """
    Calcula la constante de velocidad k usando la ecuación de Arrhenius.

    Puede usarse en dos formas:
    1. Clásica: A, E, T
    2. Relativa: k_ref, E, T_ref, T

    Retorna:
        k -> Constante de velocidad (1/min)
    """
    if E is None or T is None:
        raise ValueError("Se requieren E y T para calcular k")

    R = 1.987207  # cal/mol·K
    # R= 8.3144626  # J/mol·K

    k = None  # Inicializamos la variable k

    if A is not None:
        #Caso 1: Clásica (A,E,T)
        if T_ref is not None:
            #Usamos T_ref si está disponible
            k_ref = A * np.exp(-E / (R * T_ref))
            k = k_ref * np.exp((E/R) * (1/T_ref - 1/T))
        else:
            # Solo usamos A y T
            k = A * np.exp(-E / (R * T))
    else:
        raise ValueError("Falta el parametro A para calcular k")
    return k
