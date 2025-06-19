import json
from SimulateBR.SimulateBatchReactor import simulate_batch_reactor

def main():
    # Ruta del archivo de parámetros
    input_path = "sim_params.json"

    # Cargar el JSON con los parámetros de simulación
    with open(input_path, "r") as f:
        sim_params = json.load(f)

    # Ejecutar simulación
    resultado = simulate_batch_reactor(sim_params)

    # Mostrar resultados
    if resultado["success"]:
        print("\n✅ Simulación completada exitosamente")
        print("Resumen:")
        for clave, valor in resultado["summary"].items():
            print(f"{clave}: {valor}")

    else:
        print("\n⚠️ Simulación no completada")
        print("Mensaje:", resultado["message"])
        if resultado.get("warning"):
            print("(Advertencia detectada durante la simulación)")

if __name__ == "__main__":
    main()
