def energy_balance(t, T, Q, C_p, rho, V, delta_H, r_A):
    """
    Calcula el balance de energía en un reactor batch.

    Parámetros:
        t        -> Tiempo (min)
        T        -> Temperatura actual (K)
        Q        -> Calor agregado o removido (J/min)
        C_p      -> Capacidad calorífica (J/mol*K)
        rho      -> Densidad del fluido (mol/L)
        V        -> Volumen del reactor (L)
        delta_H  -> Entalpía de reacción (J/mol)
        r_A      -> Velocidad de reacción (mol/L*min)

    Retorna:
        dT/dt -> Derivada de la temperatura con respecto al tiempo.
    """
    return (Q - delta_H * r_A * V) / (rho * C_p * V)

