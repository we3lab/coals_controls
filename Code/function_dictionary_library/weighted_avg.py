import numpy as np
import math

# Weighted average and standard deviation calculated using NumPy.  Code is based on this StackOverflow page.
# https://stackoverflow.com/questions/2413522/weighted-standard-deviation-in-numpy

def weighted_avg(values, weights):
    # Return the weighted average and standard deviation.
    # values, weights -- numpy ndarrays with the same shape.

    average = np.average(values, weights=weights)
    return (average)
