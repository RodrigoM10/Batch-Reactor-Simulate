def calculate_concentrations(C_A0, C_B0, X_A, stoichiometry):
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
