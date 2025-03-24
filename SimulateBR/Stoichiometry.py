def calculate_concentrations(C_A0, C_B0, X_A, stoichiometry):
    """
    Calcula las concentraciones de todos los reactivos y productos en función de la conversión X_A.

    Parámetros:
        C_A0          -> Concentración inicial del reactivo A (mol/L)
        C_B0          -> Concentración inicial del reactivo B (mol/L)
        X_A           -> Lista de valores de conversión del reactivo limitante
        stoichiometry -> Diccionario con coeficientes estequiométricos {"A": -1, "B": -1, "C": 1, "D": 1}

    Retorna:
        Diccionario con listas de concentraciones de A, B, C y D en función del tiempo.
    """
    C_A = C_A0 * (1 - X_A)  # Reactivo limitante

    # Inicializamos concentraciones con None por si no existen en la estequiometría
    C_B = C_C = C_D = None

    if "B" in stoichiometry:
        C_B = C_B0 + (stoichiometry["B"] / abs(stoichiometry["A"])) * C_A0 * X_A
    if "C" in stoichiometry:
        C_C = abs(stoichiometry["C"] / stoichiometry["A"]) * C_A0 * X_A
    if "D" in stoichiometry:
        C_D = abs(stoichiometry["D"] / stoichiometry["A"]) * C_A0 * X_A

    return {
        "A": C_A,
        "B": C_B,
        "C": C_C,
        "D": C_D
    }
