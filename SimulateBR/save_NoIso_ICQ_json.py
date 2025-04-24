import json

sim_params = {
    "mode_op": "non-isothermal",
    "k_eq_method": "vant_hoff",
    "K_eq_direct": 1.4,
    "K_det": 0.311,
    "T_iso": None,
    "A": 4710000000,
    "E": 18000,
    "option": None,
    "X_A_desired": None,
    "t_reaction_det": None,
    "C_A0": 54.8,
    "C_B0": 555,
    "C_I": 98.8,
    "order": 1,
    "stoichiometry": {"A": -1, "B": -1, "C": 1},
    "excess_B": False,
    "ans_volume": None,
    "P_k": None,
    "t_c_d": None,
    "t_m": None,
    "product_k": None,
    "m_k": None,

    "T_ref": 298,
    "T0": 286,
    "K_eq_ref": 1.2,
    "delta_H_rxn": -20202,
    "DG_dict": None,

    "C_p_dict": {"A": 35,
                 "B": 18,
                 "C": 46,
                 "I": 19.5,
                 },

    "mode_energy": "ICQ",

    "U": 10,
    "A_ICQ": 1,
    "T_cool": 290,
    "m_c": 10,
    "Cp_ref": 4.16
}

# Guardar en un archivo JSON (por ejemplo en tu carpeta local de config o inputs)
output_path = "sim_params.json"
with open(output_path, "w") as f:
    json.dump(sim_params, f, indent=4)

print(f"✅ Parámetros guardados en: {output_path}")
