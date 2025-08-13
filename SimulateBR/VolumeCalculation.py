def calculate_batch_reactor_volume(P_k, m_k, C_P, t_reaccion, t_mcd):
    if C_P <= 0 or m_k <= 0:
        raise ValueError("C_P y m_k deben ser mayores a cero.")

    T_op = t_reaccion + t_mcd
    if T_op <= 0:
        raise ValueError("Tiempo total inválido.")

    V = (P_k * T_op) / (C_P * m_k) 
    return V
