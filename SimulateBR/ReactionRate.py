def reaction_rate(X_A, k, C_A0, C_B0, order, stoichiometry, excess_B):

    if not 0 <= X_A <= 1:
        raise ValueError("X_A fuera de rango válido (0 a 1)", X_A)

    # Concentraciones de los reactivos según estequiometría
    C_A = C_A0 * (1 - X_A) # Reactivo limitante
    C_B = C_B0 - (stoichiometry["B"] / stoichiometry["A"]) * C_A0 * X_A if "B" in stoichiometry else None

    # Ley de velocidad según orden de reacción
    if order == 1:
        r_A = k * C_A  # Primer orden
    elif order == 2:
        if C_B is not None and not excess_B:
            r_A = k * C_A * C_B  # Segundo orden con B presente
        elif excess_B and C_B0 is not None:
            r_A = k * C_B0 * C_A  # Pseudo-primer orden, ya que C_B ≈ C_B0 constante
        else:
            r_A = k * C_A ** 2  # Segundo orden solo en A
    else:
        raise ValueError("El orden de reacción debe ser 1 o 2")
    return -r_A
