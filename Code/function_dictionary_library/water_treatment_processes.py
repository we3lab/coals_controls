def FOC_Model(Cl_Conc, Flowrate):
    Cost = 1.132 + (2.416e-4 * Cl_Conc)
    Thermal_Energy = -0.6199 + (11.275e-4 * Cl_Conc ** 2) + (-1.377e-2 * Flowrate ** 2) + (4.043e2 * Flowrate) + (1.675e-1 * Cl_Conc)
    Electrical_Energy = -1954.418 + (25.031 * Flowrate) + (1.906 * Cl_Conc)

    return Cost, Thermal_Energy, Electrical_Energy
