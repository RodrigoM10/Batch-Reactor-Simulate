def calculate_batch_reactor_volume(P_k, m_k, C_P, t_reaccion, t_mcd):
    """
    Calcula el volumen del reactor (en litros) usando concentración final del producto:
    V = (P_k * (t_reaccion + t_mcd)) / (C_P * m_k)

    - P_k: producción deseada del producto [kg]
    - m_k: masa molar del producto [kg/mol]
    - C_P: concentración final del producto [mol/L]
    - t_reaccion: tiempo de reacción [min]
    - t_mcd: tiempo de carga/descarga/muerto [min]
    """
    if C_P <= 0 or m_k <= 0:
        raise ValueError("C_P y m_k deben ser mayores a cero.")

    T_op = t_reaccion + t_mcd
    if T_op <= 0:
        raise ValueError("Tiempo total inválido.")

    V = (P_k * T_op) / (C_P * m_k)  # (kg/min * min) / (mol/l * kg/mol) resultado en Litros
    return V
