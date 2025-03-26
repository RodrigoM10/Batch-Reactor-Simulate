import numpy as np

def calculate_rate_constant(A, E, T):
    """
    Calcula la constante de velocidad k usando la ecuación de Arrhenius.

    Parámetros:
        A -> Factor preexponencial (1/min)
        E -> Energía de activación (J/mol)
        T -> Temperatura absoluta (K)

    Retorna:
        k -> Constante de velocidad (1/min)
    """
    R = 1.987207  # J/mol·K (constante de los gases)
    #R = 8.31447  # J/mol·K (constante de los gases)
    k = A * np.exp(-E / (R * T))
    return k
