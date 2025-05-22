def calculate_batch_reactor_volume(P_k, m_k, alpha_X_list, t_reaccion, t_carga_descarga, t_muerto):
    alpha_X_sum = sum(alpha_X_list)

    if alpha_X_sum <= 0:
        raise ValueError("La suma de α_ik * X_i debe ser mayor que cero.")

    T_op = t_carga_descarga + t_reaccion + t_muerto

    if T_op <= 0:
        raise ValueError("El tiempo total de operación debe ser mayor que cero.")

    P_k_mol = P_k / m_k

    V = (P_k_mol * T_op) / alpha_X_sum

    return V
