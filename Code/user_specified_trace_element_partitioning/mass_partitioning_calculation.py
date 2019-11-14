import numpy as np
def apcd_mass_partitioning(runs, Cl_mass, Cl_partitioning, Se_mass, Se_partitioning, B_mass, B_partitioning, Br_mass,
                           Br_partitioning, Pb_mass, Pb_partitioning, As_mass, As_partitioning, Hg_mass, Hg_partitioning,
                           S_mass, S_partitioning):
    Cl_exiting=np.zeros(shape=[runs,3])
    Cl_exiting[:, 0] = Cl_mass * Cl_partitioning[:, 0]
    Cl_exiting[:, 1] = Cl_mass * Cl_partitioning[:, 1]
    Cl_exiting[:, 2] = Cl_mass * Cl_partitioning[:, 2]

    Se_exiting = np.zeros(shape=[runs, 3])
    Se_exiting[:, 0] = Se_mass * Se_partitioning[:, 0]
    Se_exiting[:, 1] = Se_mass * Se_partitioning[:, 1]
    Se_exiting[:, 2] = Se_mass * Se_partitioning[:, 2]

    B_exiting=np.zeros(shape=[runs,3])
    B_exiting[:, 0] = B_mass * B_partitioning[:, 0]
    B_exiting[:, 1] = B_mass * B_partitioning[:, 1]
    B_exiting[:, 2] = B_mass * B_partitioning[:, 2]

    Br_exiting = np.zeros(shape=[runs, 3])
    Br_exiting[:, 0] = Br_mass * Br_partitioning[:, 0]
    Br_exiting[:, 1] = Br_mass * Br_partitioning[:, 1]
    Br_exiting[:, 2] = Br_mass * Br_partitioning[:, 2]

    Pb_exiting=np.zeros(shape=[runs,3])
    Pb_exiting[:, 0] = Pb_mass * Pb_partitioning[:, 0]
    Pb_exiting[:, 1] = Pb_mass * Pb_partitioning[:, 1]
    Pb_exiting[:, 2] = Pb_mass * Pb_partitioning[:, 2]

    As_exiting = np.zeros(shape=[runs, 3])
    As_exiting[:, 0] = As_mass * As_partitioning[:, 0]
    As_exiting[:, 1] = As_mass * As_partitioning[:, 1]
    As_exiting[:, 2] = As_mass * As_partitioning[:, 2]

    Hg_exiting = np.zeros(shape=[runs, 3])
    Hg_exiting[:, 0] = Hg_mass * Hg_partitioning[:, 0]
    Hg_exiting[:, 1] = Hg_mass * Hg_partitioning[:, 1]
    Hg_exiting[:, 2] = Hg_mass * Hg_partitioning[:, 2]

    S_exiting = np.zeros(shape=[runs, 3])
    S_exiting[:, 0] = S_mass * S_partitioning[:, 0]
    S_exiting[:, 1] = S_mass * S_partitioning[:, 1]
    S_exiting[:, 2] = S_mass * S_partitioning[:, 2]

    return Cl_exiting, Se_exiting, B_exiting, Br_exiting, Pb_exiting, As_exiting, Hg_exiting, S_exiting

def wpcd_mass_partitioning(runs, as_mass, as_partitioning, cl_mass, cl_partitioning, pb_mass, pb_partitioning, hg_mass,
                           hg_partitioning, se_mass, se_partitioning):
    as_exiting = np.zeros(shape=[runs, 2])
    as_exiting[:, 0] = as_mass * as_partitioning[:, 0]
    as_exiting[:, 1] = as_mass * as_partitioning[:, 1]

    cl_exiting = np.zeros(shape=[runs, 2])
    cl_exiting[:, 0] = cl_mass * cl_partitioning[:, 0]
    cl_exiting[:, 1] = cl_mass * cl_partitioning[:, 1]

    pb_exiting = np.zeros(shape=[runs, 2])
    pb_exiting[:, 0] = pb_mass * pb_partitioning[:, 0]
    pb_exiting[:, 1] = pb_mass * pb_partitioning[:, 1]

    hg_exiting = np.zeros(shape=[runs, 2])
    hg_exiting[:, 0] = hg_mass * hg_partitioning[:, 0]
    hg_exiting[:, 1] = hg_mass * hg_partitioning[:, 1]

    se_exiting = np.zeros(shape=[runs, 2])
    se_exiting[:, 0] = se_mass * se_partitioning[:, 0]
    se_exiting[:, 1] = se_mass * se_partitioning[:, 1]

    return as_exiting, cl_exiting, pb_exiting, hg_exiting, se_exiting

def mc_wpcd_mass_partitioning(as_mass, as_partitioning, cl_mass, cl_partitioning, pb_mass, pb_partitioning, hg_mass,
                           hg_partitioning, se_mass, se_partitioning):
    as_exiting = np.multiply(as_mass, as_partitioning)
    cl_exiting = np.multiply(cl_mass, cl_partitioning)
    pb_exiting = np.multiply(pb_mass, pb_partitioning)
    hg_exiting = np.multiply(hg_mass, hg_partitioning)
    se_exiting = np.multiply(se_mass, se_partitioning)

    return as_exiting, cl_exiting, pb_exiting, hg_exiting, se_exiting

