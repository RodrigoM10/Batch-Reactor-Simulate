import matplotlib.pyplot as plt
from ReactionRate import reaction_rate

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
