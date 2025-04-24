import json

sim_params = {
    "mode_op": "non-isothermal",
    "k_eq_method": "vant_hoff",
    "K_eq_direct": None,
    "K_det": None,
    "T_iso": None,
    "A": 756.07,
    "E": 10000,
    "option": None,
    "X_A_desired": None,
    "t_reaction_det": None,
    "C_A0": 1,
    "C_B0": None,
    "C_I": 1,
    "order": 1,
    "stoichiometry": {"A": -1, "C": 1},
    "excess_B": False,
    "ans_volume": None,
    "P_k": None,
    "t_c_d": None,
    "t_m": None,
    "product_k": None,
    "m_k": None,

    "T_ref": 298,
    "T0": 480,
    "K_eq_ref": 75000,
    "delta_H_rxn": -14000,
    "DG_dict": None,

    "C_p_dict": {"A": 25, "C": 25, "I": 50},

    "mode_energy": "adiabatic",

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
