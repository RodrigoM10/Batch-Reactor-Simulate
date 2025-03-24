def calculate_batch_reactor_volume(P_k, m_k, alpha_X_list, t_reaccion, t_carga_descarga, t_muerto):
    """
    Calcula el volumen necesario de un reactor batch para cumplir una producción deseada.

    Parámetros:
        P_k               -> Producción deseada del producto k (g/min o kg/min)
        m_k               -> Masa molar del producto k (g/mol o kg/mol)
        alpha_X_list      -> Lista de α_ik * X_i (asumida una sola reacción si hay una sola entrada)
        t_reaccion        -> Tiempo de reacción obtenido de la simulación (min)
        t_carga_descarga  -> Tiempo de carga y descarga (min)
        t_muerto          -> Tiempo muerto (min)

    Retorna:
        V -> Volumen del reactor (L o m³, según unidad de entrada)
    """
    alpha_X_sum = sum(alpha_X_list)

    if alpha_X_sum <= 0:
        raise ValueError("La suma de α_ik * X_i debe ser mayor que cero.")

    T_op = t_carga_descarga + t_reaccion + t_muerto

    if T_op <= 0:
        raise ValueError("El tiempo total de operación debe ser mayor que cero.")

    P_k_mol = P_k / m_k

    V = (P_k_mol * T_op) / alpha_X_sum

    return V
