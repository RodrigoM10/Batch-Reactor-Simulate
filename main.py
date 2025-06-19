from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
from fastapi.responses import JSONResponse

from SimulateBR.SimulateBatchReactor import simulate_batch_reactor

# Inicializamos la app
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O podés restringir a tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo que representa los parámetros que envías desde el front
class SimParams(BaseModel):
    mode_op: str
    k_eq_method: str
    K_eq_direct: Optional[float] = None
    K_det: Optional[float] = None
    T_iso: Optional[float] = None
    A: Optional[float] = None
    E: Optional[float] = None
    option: Optional[str] = None
    X_A_desired: Optional[float] = None
    t_reaction_det: Optional[float] = None
    C_A0: Optional[float] = None
    C_B0: Optional[float] = None
    C_C0: Optional[float] = None
    C_D0: Optional[float] = None
    C_I: Optional[float] = None
    order: int
    reversible: bool
    stoichiometry: Dict[str, int]
    excess_B: Optional[bool] = None
    ans_volume: Optional[str] = None
    P_k: Optional[float] = None
    t_mcd: Optional[float] = None
    product_k: Optional[str] = None
    m_k: Optional[float] = None
    T_ref: Optional[float] = None
    T0: Optional[float] = None
    K_eq_ref: Optional[float] = None
    delta_H_rxn: Optional[float] = None
    DG_dict: Optional[Dict[str, float]] = None
    C_p_dict: Optional[Dict[str, float]] = None
    mode_energy: Optional[str] = None
    U: Optional[float] = None
    A_ICQ: Optional[float] = None
    T_cool: Optional[float] = None
    m_c: Optional[float] = None
    Cp_ref: Optional[float] = None

# Ruta que recibe los datos

@app.post("/simulate")
async def recibir_parametros(sim_params: SimParams):
    sim_params_dict = sim_params.dict()
    print("✅ Parámetros recibidos:", sim_params_dict)

    try:
        resultado = simulate_batch_reactor(sim_params_dict)
        return JSONResponse(content=resultado)

    except Exception as e:
        print(f"❌ Error en simulación: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Error en la simulación: {str(e)}",
                "summary": {},
                "data": {}
            }
        )

