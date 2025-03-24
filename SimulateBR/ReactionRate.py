def reaction_rate(X_A, k, C_A0, C_B0, order, stoichiometry, excess_B):
    """
    Calcula la veloidad de reacción en función de la conversión X_A.

    Parámetros:
        X_A          -> Conversión del reactivo A
        k            -> Constante de velocidad (1/min, L/mol*min, etc.)
        C_A0         -> Concentración inicial del reactivo A (mol/L)
        C_B0    -> Concentración inicial de B (mol/l), usada en pseudo-primer orden (opcional)
        excess_B -> Booleano que indica si B está en exceso
        order        -> Orden de la reacción (1 o 2)
        stoichiometry -> Diccionario con coeficientes estequiométricos {"A": -1, "B": -1, "C": 1}

    Retorna:
        r_A -> Velocidad de reacción (-mol/L*min)
    """
    # Concentraciones de los reactivos según estequiometría
    C_A = C_A0 * (1 - X_A) # Reactivo limitante
    C_B = C_B0 - (stoichiometry["B"] / stoichiometry["A"]) * C_A0 * X_A if "B" in stoichiometry else None

    # Ley de velocidad según orden de reacción
    if order == 1:
        r_A = -k * C_A  # Primer orden
    elif order == 2:
        if C_B is not None and not excess_B:
            r_A = k * C_A * C_B  # Segundo orden con B presente
        elif excess_B and C_B0 is not None:
            r_A = k * C_B0 * C_A  # Pseudo-primer orden, ya que C_B ≈ C_B0 constante
        else:
            r_A = -k * C_A ** 2  # Segundo orden solo en A
    else:
        raise ValueError("El orden de reacción debe ser 1 o 2")

    return r_A
