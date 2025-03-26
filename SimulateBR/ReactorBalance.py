from SimulateBR.ReactionRate import reaction_rate

def balance_reactor(t, y, k, C_A0, C_B0, order, stoichiometry, excess_B):

    # Conversión del reactivo limitante A
    X_A = y[0]
    #Calculo de la  velocidad de reaccion
    r_A = reaction_rate(X_A, k, C_A0, C_B0, order, stoichiometry, excess_B)
    dX_A_dt = -r_A / (C_A0)

    return [dX_A_dt]

