import json

sim_params = {
    "mode_op": "isothermal",
    "k_eq_method": "gibbs",
    "K_eq_direct": None,
    "K_det": None,
    "T_iso": 1000,
    "A": 1.2e4,
    "E": 10000,
    "option": "X",
    "X_A_desired": 0.7,
    "t_reaction_det": None,
    "C_A0": 0.061,
    "C_B0": 0.061,
    "C_I": 0,
    "order": 1,
    "stoichiometry": {"A": -1, "B": -1, "C": 1, "D": 1},
    "excess_B": False,
    "ans_volume": "s",
    "P_k": 100,
    "t_mcd": 1,
    "product_k": "C",
    "m_k": 45,

    "T_ref": 298,
    "T0": None,

    "K_eq_ref": 75000,
    "delta_H_rxn": -14000,
    "DG_dict": {"A": -47860, "B": -46040, "C": -94630, "D": 0},
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
