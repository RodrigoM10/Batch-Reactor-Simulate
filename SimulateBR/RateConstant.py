import numpy as np

def calculate_rate_constant(A=None, E=None, T=None, T_ref=None):

    if E is None or T is None:
        raise ValueError("Se requieren E y T para calcular k")

    R = 1.987  # cal/mol·K

    k = None  # Inicializamos la variable k

    if A is not None:
        #Caso 1: Clásica (A,E,T)
        if T_ref is not None:
            #Usamos T_ref si está disponible
            k_ref = A * np.exp(-E / (R * T_ref))
            print("5 k_ref :", k_ref)
            k = k_ref * np.exp((E/R) * (1/T_ref - 1/T))
            print("6 k :", k)
        else:
            # Solo usamos A y T
            k = A * np.exp(-E / (R * T))
    else:
        raise ValueError("Falta el parametro A para calcular k")
    return k
