def energy_balance(t, T, Q, C_p, rho, V, delta_H, r_A):

    return (Q - delta_H * r_A * V) / (rho * C_p * V)

