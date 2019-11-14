import numpy as np


def interaction_term_variable_creation(X, variable_1, variable_2):
    i = 0
    width_variable_1 = np.shape(variable_1)
    if len(width_variable_1) == 1:
        width_variable_1 = width_variable_1 + (1,)
    width_variable_1 = width_variable_1[1]
    width_variable_2 = np.shape(variable_2)
    if len(width_variable_2) == 1:
        width_variable_2 = width_variable_2 + (1,)
    width_variable_2 = width_variable_2[1]
    while i < width_variable_1:
        j = 0
        while j < width_variable_2:
            if len(np.shape(variable_1)) == 1:
                a = variable_1
            else:
                a = variable_1[:, i]
            if len(np.shape(variable_2)) == 1:
                b = variable_2
            else:
                b = variable_2[:, j]
            indicator_row = (a.T * b).T
            X = np.column_stack([X, indicator_row])
            j += 1

        i += 1

    dependent_variables = X

    return dependent_variables
