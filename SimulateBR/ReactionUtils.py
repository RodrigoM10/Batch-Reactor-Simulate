def balance_reactor(t, y, k, C_A0, C_B0, C_C0, C_D0, order,
                    stoichiometry, excess_B, reversible, Keq):
    X_A = y[0]

    # Garantizar que X_A no exceda sus límites físicos
    X_A = min(max(X_A, 0.0), 1.0)

    r_A = reaction_rate(X_A, k, C_A0, C_B0, C_C0, C_D0, order, stoichiometry,excess_B, reversible , Keq)
    dX_A_dt = r_A / C_A0
    return [dX_A_dt]

def reaction_rate(X_A, k, C_A0, C_B0, C_C0, C_D0, order, stoichiometry, excess_B, reversible=False, Keq=None):
    if not 0 <= X_A <= 1:
        raise ValueError("X_A fuera de rango válido (0 a 1)", X_A)

    # Concentraciones de los reactivos según estequiometría
    C_A = C_A0 * (1 - X_A)  # Reactivo limitante
    C_B = C_B0 - (stoichiometry["B"] / stoichiometry["A"]) * C_A0 * X_A if "B" in stoichiometry else None
    C_C = C_C0 + (stoichiometry.get("C", 0) / stoichiometry.get("A", 1)) * C_A0 * X_A if "C" in stoichiometry else 0.0
    C_D = C_D0 + (stoichiometry.get("D", 0) / stoichiometry.get("A", 1)) * C_A0 * X_A if "D" in stoichiometry else 0.0

    # Ley de velocidad según orden de reacción
    if order == 1:
        r_direct = k * C_A  # Primer orden
    elif order == 2:
        if C_B is not None and not excess_B:
            r_direct = k * C_A * C_B  # Segundo orden con B presente
        elif excess_B and C_B0 is not None:
            r_direct = k * C_B0 * C_A  # Pseudo-primer orden, ya que C_B ≈ C_B0 constante
        else:
            r_direct = k * C_A ** 2  # Segundo orden solo en A
    else:
        raise ValueError("El orden de reacción debe ser 1 o 2")

    if reversible and Keq is not None:
         if order == 1:
            r_A = r_direct - k * (C_C * C_D) / Keq
         elif order == 2:
            r_A = r_direct - k * (C_C * C_D) / Keq
    else:
        r_A = r_direct

    return r_A



