import matplotlib.pyplot as plt
import numpy as np
from ReactionUtils import reaction_rate


def graph_conversion(t_eval, X_A_eval):
    """
    Grafica la conversión del reactivo limitante en función del tiempo.

    Parámetros:
        t_eval    -> Lista de tiempos evaluados.
        X_A_eval  -> Lista de valores de conversión del reactivo limitante.
    """
    plt.figure()
    plt.plot(t_eval, X_A_eval, label='Conversión de A', color='b')
    plt.xlabel('Tiempo (min)')
    plt.ylabel('Conversión X_A')
    plt.legend()
    plt.grid()
    plt.title("Conversión de A vs. Tiempo")
    plt.show()

def graph_concentrations(t_eval, concentrations):
    """
    Grafica las concentraciones de todos los componentes en función del tiempo.

    Parámetros:
        t_eval       -> Lista de tiempos evaluados.
        concentrations -> Diccionario con listas de concentraciones de A, B, C y D.
    """
    plt.figure()

    if concentrations["A"] is not None:
        plt.plot(t_eval, concentrations["A"], label='[A] (Reactivo)', color='r')
    if concentrations["B"] is not None:
        plt.plot(t_eval, concentrations["B"], label='[B] (Reactivo)', color='b')
    if concentrations["C"] is not None:
        plt.plot(t_eval, concentrations["C"], label='[C] (Producto)', color='g')
    if concentrations["D"] is not None:
        plt.plot(t_eval, concentrations["D"], label='[D] (Producto)', color='m')

    plt.xlabel('Tiempo (min)')
    plt.ylabel('Concentración (mol/L)')
    plt.legend()
    plt.grid()
    plt.title("Concentraciones de Reactivos y Productos vs. Tiempo")
    plt.show()


# Grafica exclusiva para modo isotermico
def graph_inverse_rate(X_A, k, C_A0, C_B0, order, stoichiometry,excess_B):
    """
    Grafica 1/r_A en función de X_A.

    Parámetros:
        X_A          -> Lista de conversiones
        k            -> Constante de velocidad
        C_A0, C_B0   -> Concentraciones iniciales
        order        -> Orden de la reacción
        stoichiometry -> Estequiometría del sistema
    """
    inverse_rate = [1 / -reaction_rate(x, k, C_A0, C_B0, order, stoichiometry,excess_B) for x in X_A]

    plt.figure()
    plt.plot(X_A, inverse_rate, label="1/r_A vs X_A", color='purple')
    plt.xlabel('Conversión X_A')
    plt.ylabel('1 / r_A (min/mol/L)')
    plt.legend()
    plt.grid()
    plt.title("Gráfico de 1/r_A vs X_A")
    plt.show()


# Graficas para modo no isotermico
def graph_temperature(t_eval, T_eval):
    plt.figure()
    plt.plot(t_eval, T_eval)
    plt.xlabel("Tiempo (min)")
    plt.ylabel("Temperatura (K)")
    plt.title("Evolución de la Temperatura")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def graph_conversion_vs_temperature(X_A_eval, T_eval):
    plt.figure()
    plt.plot(T_eval, X_A_eval)
    plt.xlabel("Temperatura (K)")
    plt.ylabel("Conversión de A")
    plt.title("Conversión vs Temperatura")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def concentration_time_table(t_eval, concentrations, stoichiometry, t_final):
    # ⚙️ Paso 1: generar hasta 10 tiempos uniformemente espaciados y redondearlos
    num_puntos = 10
    tiempos_objetivo = np.linspace(0, t_final, num=num_puntos)
    tiempos_objetivo = [round(t, 2) for t in tiempos_objetivo]

    # 🧪 Paso 2: definir especies y columnas
    especies = list(stoichiometry.keys())
    columnas = ["Tiempo (min)"] + [f"[{e}] (mol/L)" for e in especies]

    # 🧩 Paso 3: construir las filas de la tabla
    data = []
    for t_obj in tiempos_objetivo:
        idx = np.abs(np.array(t_eval) - t_obj).argmin()  # buscar el tiempo más cercano
        fila = [f"{t_obj:.2f}"]
        for e in especies:
            conc = concentrations.get(e)
            fila.append(round(conc[idx], 4) if conc is not None else "N/A")
        data.append(fila)

    # 🎨 Paso 4: mostrar como tabla gráfica con altura ajustada
    fig, ax = plt.subplots(figsize=(10, len(data) * 0.5))
    ax.axis('off')
    tabla = plt.table(cellText=data, colLabels=columnas, cellLoc='center', loc='center')
    tabla.scale(1.2, 1.5)
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    plt.title("Concentraciones en el tiempo (Vista Tabla)", fontweight='bold')
    plt.subplots_adjust(top=0.85)  # espacio para título
    plt.show()