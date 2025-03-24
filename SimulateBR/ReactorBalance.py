#Funcion para operacion no Isotermica
from SimulateBR.ReactionRate import reaction_rate

def balance_reactor(t, y, k, C_A0, C_B0, order, stoichiometry, excess_B):
    """
    Generaliza el balance de moles en un reactor batch con cualquier estequiometría y orden de reacción.

    Parámetros:
        t             -> Tiempo (min)
        y             -> Vector de variables de estado [X_A]
        k             -> Constante de velocidad (1/min, L/mol*min, etc.)
        C_A0          -> Concentración inicial del reactivo A (mol/L)
        C_B0          -> Concentración inicial del reactivo B (mol/L) (opcional)
        C_I
        order         -> Orden de la reacción (1, 2)
        stoichiometry -> Diccionario con coeficientes estequiométricos {"A": -1, "B": -1, "C": 1, "D": 1}

    Retorna:
        dX_A_dt -> Tasa de cambio de conversión del reactivo A
    """
    # Conversión del reactivo limitante A
    X_A = y[0]

    #Calculo de la  velocidad de reaccion
    r_A = reaction_rate(X_A, k, C_A0, C_B0, order, stoichiometry, excess_B)

    dX_A_dt = -r_A / (C_A0)  # Se usa el volumen para normalizar

    return [dX_A_dt]

