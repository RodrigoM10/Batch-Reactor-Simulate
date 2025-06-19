import json

sim_params = {
    "mode_op": "isothermal",
    "k_eq_method": "direct",
    "K_eq_direct": 2.93,
    "K_det": 0.0004758,
    "T_iso": 373,
    "A": None,
    "E": None,
    #"option": "X",
    "option": "T",
    #"X_A_desired": 0.35,
    "X_A_desired": None,
    "t_reaction_det": 120,
    "C_A0": 3.91,
    "C_B0": 10.18,
    "C_C0": 0,
    "C_D0": 17.56,
    "C_I": 0,
    "order": 2,
    "reversible": True,
    "stoichiometry": {"A": -1, "B": -1, "C": 1, "D": 1},
    "excess_B": False,
    "ans_volume": "s",
    "P_k": 37.72,
    "t_mcd": 30,
    "product_k": "C",
    "m_k": 88,

    "T_ref": None,
    "T0": None,

    "K_eq_ref": None,
    "delta_H_rxn": None,
    "DG_dict": {"A": None, "B": None, "C": None, "D": None},
    "C_p_dict": None,

    "mode_energy": None,

    "U": None,
    "A_ICQ": None,
    "T_cool": None,
    "m_c": None,
    "Cp_ref": None
}

# Guardar en un archivo JSON (por ejemplo en tu carpeta local de config o inputs)
output_path = "sim_params.json"
with open(output_path, "w") as f:
    json.dump(sim_params, f, indent=4)

print(f"✅ Parámetros guardados en: {output_path}")
