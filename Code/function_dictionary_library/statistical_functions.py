import numpy as np
import math
from scipy import stats
import pandas as pd

# Create parameters for an empirical cdf function.  From this Stack Overflow post ->
# https://stackoverflow.com/questions/33345780/empirical-cdf-in-python-similiar-to-matlabs-one

# This function takes one input:  A numpy array
# This function returns two outputs:  The values of an array ordered from least to greatest and an array of cumulative
# probabilities for the values array.

# This function is used in the following codes:  Appalachian_Sulfur_Analysis.py, coalqual_data_samples.py

def ecdf(sample):

    # convert sample to a numpy array, if it isn't already
    sample = np.atleast_1d(sample)


    # drop samples that do not have reported scores
    sample = sample[~np.isnan(sample)]

    if sample.size == 0:
        quantiles = []
        cumprob = []
    elif len(sample) == 1:
        quantiles = [sample, sample]
        cumprob = [0, 1]
    else:
        # find the unique values and their corresponding counts
        quantiles, counts = np.unique(sample, return_counts=True)
        quantiles = np.insert(quantiles, 0, min(quantiles))

        # take the cumulative sum of hte counts and divide by the sample size to get the cumulative probabilities between
        # 0 and 1.
        cumprob = np.cumsum(counts).astype(np.double) / sample.size
        cumprob = np.insert(cumprob, 0, 0)
    return quantiles, cumprob

# This function will pull a random value from an empirical cumulative distribution function (ecdf).  This is used in
# Monte Carlo analyses from COALQUAL data.

# This function takes three inputs:  an array of quartiles form the ECDF, an array of percentiles for the ECDF, and the
# number of trials.
# This function generates one output:  an array of random values taken from the ECDF.

# This function is used in the following codes:


def random_value_from_ecdf(q, p, n):

    percentiles = np.random.random(n)
    values = np.zeros(shape=n)
    j = 0
    for x in percentiles:
        i = 0
        while i < len(p):
            if x > p[i]:
                i = i + 1
            else:
                p_index_floor = i - 1
                p_floor = p[i - 1]
                p_index_ceil = i
                p_ceil = p[i]
                break
        q_floor = q[p_index_floor]
        q_ceil = q[p_index_ceil]
        concentration = q_floor+((x-p_floor)*((q_ceil-q_floor)/(p_ceil-p_floor)))
        if x < p[0]:
            concentration = q[0]
        values[j] = concentration
        j = j+1

    return values

# This function will calculate the probability value from an empiricial cumulative distribution function (ecdf).  This
# is used in plotting observed values on a ecdf.

# This function takes three inputs:  an array of quartiles from the ECDF, an array of percentiles for the ECDF, and the
# observed value.
# This function generates one output:  a percentile value.

# This function is ued in the following codes:


def percentile_value_from_ecdf(q, p, observed_value):

    if observed_value > max(q):
        percentile_value = 1
    elif observed_value < min(q):
        percentile_value = 0
    # elif observed_value > max(q):
    #     print('Maximum Value')
    #     print(observed_value)
    #     print(max(q))
    #     percentile_value = 1
    elif min(q) < observed_value < max(q):
        i = 0
        while i < len(p) - 1:
            if q[i] <= observed_value <= q[i + 1]:
                percentile_value = p[i]
                break
            i += 1

    return percentile_value

# Calculate the mean squared error of a dataset.

# This function takes two inputs:  two arrays of values to be compared.
# This function returns one output:  the mean squared error.

# This function is used in the following codes generation_volume_regression.py

def mse(values_1, values_2):

    sum = 0
    i = 0
    while i < len(values_1):
        squared_error = (values_1[i] - values_2[i])**2
        sum += squared_error
        i += 1

    mean_squared_error = sum/(len(values_1) + 1)
    residual_squared_error = math.sqrt(sum)

    return mean_squared_error, residual_squared_error


# Create parameters for an empirical cdf function.  From this Stack Overflow post ->
# https://stackoverflow.com/questions/33345780/empirical-cdf-in-python-similiar-to-matlabs-one

# This function takes two inputs:  an array of values to be converted into ECDFs and an array of weights for those
# samples.
# This function returns two outputs:  the quantile and percentile values of a weighted ECDF.

# This function is used in the following codes:  weighted_ecdf_coalqual_data_samples.py


def weighted_ecdf(sample, weight):

    # Convert sample to a numpy array, if it isn't already
    sample = np.atleast_1d(sample)

    # Drop samples that do not have reported scores
    weight = weight[~np.isnan(sample)]
    sample = sample[~np.isnan(sample)]

    # Convert weight to a numpy array as well if it isn't already
    weight = np.atleast_1d(weight)

    # Find the unique values and their corresponding counts
    quantiles_raw, counts = np.unique(sample, return_counts=True)
    quantiles = np.insert(quantiles_raw, 0, min(quantiles_raw))

    # Take the cumulative sum of hte counts and divide by the sample size to get the cumulative probabilities between
    # 0 and 1.

    if len(weight) == len(counts):
        cumprob = np.cumsum(weight*counts).astype(np.double) / np.sum(weight)
        cumprob = np.insert(cumprob, 0, 0)

    else:
        weights = []
        i = 0
        while i < len(quantiles_raw):
            weight_subset = weight[sample == quantiles_raw[i]]
            weights.append(sum(weight_subset))
            i += 1

        cumprob = np.cumsum(weights*counts).astype(np.double) / np.sum(weight)
        cumprob = np.insert(cumprob, 0, 0)
        cumprob = cumprob/max(cumprob)

    return quantiles, cumprob



# Weighted average and standard deviation calculated using NumPy.  Code is based on this StackOverflow page.
# https://stackoverflow.com/questions/2413522/weighted-standard-deviation-in-numpy

# This function takes two inputs:  an array of values to be analyzed and an array of weights for those values.
# This function returns two outputs:  the weighted average and the weighted standard deviation (i.e. the square root of
# the variance).

# This function is used in the following codes:  weighted_ecdf_coalqual_data_samples.py


def weighted_avg_and_std(values, weights):
    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)

    return average, math.sqrt(variance)

# This function calculates the p-values for a correlation matrix.  It is based on this stack overflow post.
# https://stackoverflow.com/questions/25571882/pandas-columns-correlation-with-statistical-significance.

# This function takes one input:  A pandas dataframe.
# This function returns one output:  A matrix containing the p-values of the correlations.

# This function is used in the following codes:  coalqual_te_concentration_correlation.py

def calculate_pvalues(df):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(stats.pearsonr(df[r], df[c])[1], 4)
    return pvalues

# This function calculates distribution summary statistics (i.e. 5th percentile, 25th percentile, median, 75th
# percentile, 95th percentile, mean, and standard deviation).

# This function takes one input:  an array of numbers to calculate these statistics for
# This function returns one output:  an array of summary statistics.

# This function is used in the following codes:  stochastic_CFPP_trace_element_partitioning.py


def distribution_summary_statistics(distribution):
    percentile_5th = np.percentile(distribution, 5)
    percentile_25th = np.percentile(distribution, 25)
    median = np.median(distribution)
    percentile_75th = np.percentile(distribution, 75)
    percentile_95th = np.percentile(distribution, 95)
    mean = np.mean(distribution)
    std_dev = np.std(distribution)
    summary_statistics = [percentile_5th, percentile_25th, median, percentile_75th, percentile_95th, mean, std_dev]

    return summary_statistics

# This function calculates a list of random variables based on a normal distribution.

# This function takes three inputs, the mu for a normal distribution, the sigma for a normal distribution, and a number
# of trials.
# This function returns one output, the vector of coal concentrations.

# This function is used in the following codes:  annual_CFPP_coal_inputs.


def concentration_from_mle_normal_distribution(mu, sigma, n):

    random_values = np.random.random(n)
    concentration = []
    sigma = float(sigma)
    for x in random_values:
        exponent = stats.norm.ppf(x, loc=mu, scale=sigma)
        concentration.append(10**exponent)

    return concentration

def heat_from_mle_normal_distribution(mu, sigma, n):

    random_values = np.random.random(n)
    concentration = []
    for x in random_values:
        concentration.append(stats.norm.ppf(x, loc=mu, scale=sigma))

    return concentration

def mann_whitney_u_three_way(sample_1, sample_2, sample_3):

    test_1 = stats.mannwhitneyu(sample_1, sample_2, alternative='two-sided')
    result_1 = test_1[1]

    test_2 = stats.mannwhitneyu(sample_1, sample_3, alternative='two-sided')
    result_2 = test_2[1]

    test_3 = stats.mannwhitneyu(sample_2, sample_3, alternative='two-sided')
    result_3 = test_3[1]

    result_matrix = np.matrix([[0, result_1, result_2], [result_1, 0, result_3], [result_2, result_3, 0]])

    return result_matrix

def mann_whitney_u_four_way(sample_1, sample_2, sample_3, sample_4):

    test_1 = stats.mannwhitneyu(sample_1, sample_2, alternative='two-sided')
    result_1 = test_1[1]

    test_2 = stats.mannwhitneyu(sample_1, sample_3, alternative='two-sided')
    result_2 = test_2[1]

    test_3 = stats.mannwhitneyu(sample_1, sample_4, alternative='two-sided')
    result_3 = test_3[1]

    test_4 = stats.mannwhitneyu(sample_2, sample_3, alternative='two-sided')
    result_4 = test_4[1]

    test_5 = stats.mannwhitneyu(sample_2, sample_4, alternative='two-sided')
    result_5 = test_5[1]

    test_6 = stats.mannwhitneyu(sample_3, sample_4, alternative='two-sided')
    result_6 = test_6[1]

    result_matrix = np.matrix([[0, result_1, result_2, result_3], [result_1, 0, result_4, result_5],
                               [result_2, result_4, 0, result_6], [result_3, result_5, result_6, 0]])

    return result_matrix

