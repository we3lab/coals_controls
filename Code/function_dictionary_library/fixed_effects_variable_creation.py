import numpy as np


def fixed_effects_variable_creation(X, variable_array):

    unique = variable_array.unique()
    unique = [x for x in unique if str(x) != 'nan']
    i = 1
    while i < len(unique):
        fe_variable = unique[i]
        fe_array = np.zeros((len(variable_array), 1))
        j = 0
        while j < len(variable_array):
            if variable_array.iloc[j] == fe_variable:
                fe_array[j] = 1
            else:
                fe_array[j] = 0
            j += 1

        fe_array = np.asarray(fe_array)
        X = np.hstack((X, fe_array))

        i += 1

    dependent_variables = X

    return dependent_variables


