import matplotlib.pyplot as plt
import numpy as np

from SimulateBR.ReactionUtils import reaction_rate
from SimulateBR.RateConstant import calculate_rate_constant

def graph_equilibrium_temperature_plot(T_range, X_eq_values):
    """
    Gráfico de conversión de equilibrio en función de la temperatura.

    Parámetros:
        T_eval       -> Lista de temperaturas evaluadas.
        X_eq_values   -> Lista de conversiones de equilibrio correspondientes.
    """

    plt.figure()
    plt.plot(T_range, X_eq_values, label="X_eq vs T", color="green")
    plt.xlabel("Temperatura (K)")
    plt.ylabel("Conversión de equilibrio X_eq")
    plt.title("Conversión de equilibrio en función de la temperatura")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def graph_equilibrium_line(X_eq, T_op):
    """
    Dibuja una línea horizontal mostrando X_eq en función de T constante.

    Parámetros:
        X_eq         -> Valor de conversión de equilibrio (constante).
        T_op  -> Temperatura de operación (solo para mostrar en el título).
    """
    plt.figure()
    plt.axhline(y=X_eq, color='green', linestyle='--', label=f"X_eq = {X_eq:.3f}")
    plt.xlabel("Tiempo o Variable independiente")
    plt.ylabel("Conversión X_A")
    plt.title(f"Conversión de Equilibrio a T = {T_op} K")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def graph_equilibrium_vs_temperature(T_range, X_eq_range):
    """
    Gráfico de conversión de equilibrio X_eq en función de la temperatura.
    """
    plt.figure()
    plt.plot(T_range, X_eq_range, label="X_eq vs T", color="green")
    plt.xlabel("Temperatura (K)")
    plt.ylabel("Conversión de equilibrio X_eq")
    plt.title("Conversión de equilibrio en función de la temperatura")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def graph_conversion(t_eval, X_A_eval, X_eq=None):
    """
    Grafica la conversión del reactivo limitante en función del tiempo.

    Parámetros:
        t_eval    -> Lista de tiempos evaluados.
        X_A_eval  -> Lista de valores de conversión del reactivo limitante.
    """
    plt.figure()
    plt.plot(t_eval, X_A_eval, label=f'Conversión de A = {X_A_eval[-1]:.2f}', color='b')

    if X_eq is not None:
        plt.axhline(y=X_eq, color='r', linestyle='--', label=f'Conversion de Equilibrio = {X_eq:.2f}')

    plt.xlabel('Tiempo (min)')
    plt.ylabel('Conversión X_A')
    plt.legend()
    plt.grid()
    plt.title("Conversión de A vs. Tiempo")
    plt.show()

def graph_conversion_with_equilibrium(t_eval, X_A_eval, X_eq_range):
    """
    Gráfica la conversión de A y la conversión de equilibrio (en función del tiempo).
    """
    plt.figure()
    plt.plot(t_eval, X_A_eval, label="Conversión de A", color="blue")
    plt.plot(t_eval, X_eq_range[:len(t_eval)], '--', label="Conversión de equilibrio", color="red")
    plt.xlabel("Tiempo (min)")
    plt.ylabel("Conversión X_A")
    plt.title("Conversión vs. Tiempo con equilibrio")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def graph_concentrations(t_eval, concentrations):

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
def graph_inverse_rate(X_A, k, C_A0, C_B0, C_C0, C_D0, order, stoichiometry, excess_B, reversible=False, Keq=None):
    inverse_rate = []
    for x in X_A:
        try:
            r = reaction_rate(x, k, C_A0, C_B0, C_C0, C_D0, order, stoichiometry, excess_B, reversible, Keq)
            inverse_rate.append(1 / r if r > 0 else float('inf'))
        except Exception:
            inverse_rate.append(float('inf'))

    plt.figure()
    plt.plot(X_A, inverse_rate, label="1/r_A vs X_A", color='purple')
    plt.xlabel('Conversión X_A')
    plt.ylabel('1 / r_A (min/mol/L)')
    plt.legend()
    plt.grid()
    plt.title("Gráfico de 1/r_A vs X_A")
    plt.show()


# Graficas para modo no isotermico
def graph_temperature(t_eval, T_eval, Ta2=None):
    import matplotlib.pyplot as plt
    import numpy as np

    plt.figure()
    plt.plot(t_eval, T_eval, label='T (K)', color='r')

    if Ta2 is not None:
        plt.plot(t_eval, Ta2, label='Ta2 (K)', linestyle='--')

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Temperatura (K)")
    plt.title("Evolución de la Temperatura" + (" y del refrigerante" if Ta2 is not None else ""))
    plt.legend()
    plt.grid(True)

    # Distribución de ticks más estética
    max_t = max(t_eval)
    salto = max_t / 10  # dividir en 10 partes iguales
    ticks_x = np.arange(0, max_t + salto, salto)
    plt.xticks(ticks_x)

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


def graph_heat_rates(t_eval, Qgb_eval, Qrb_eval):

    plt.figure(figsize=(8, 5))
    plt.plot(np.array(t_eval) / 60, Qgb_eval, label='Qg (cal/s)', color='gray')
    plt.plot(np.array(t_eval) / 60, Qrb_eval, label='Qr (cal/s)', color='black')
    plt.xlabel("Tiempo (min)")
    plt.ylabel("Tasa de calor (cal/s)")
    plt.title("Tasas de generación y remoción de calor (Qg y Qr)")
    plt.legend()
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
