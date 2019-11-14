import pandas as pd
import numpy as np
from state_name_to_abbreviation import state_name_to_abbreviation
from censored_data_mle import CensoredLikelihoodOLS

# In COALQUAL, states are reported by their full names.  In all other data sources, the states are reported using
# acronyms.  This function converts state names to abbreviations.

# This function takes one input:  a pandas array of state names.
# This function returns one output:  a pandas array of state abbreviations.

# This function is used in the following codes:  avg_county_coal_constitutents.py, appalachian_sulfur_analysis.py,
# coalqual_data_samples.py, weighted_ecdf_coalqual_data_samples.py


def state_abbreviations(state_names):
    state_abbreviation = []
    i = 0
    while i < len(state_names):
        state_abbreviation.append(state_name_to_abbreviation(state_names.iloc[i]))
        i += 1

    state_abbreviation = pd.Series(state_abbreviation)
    state_abbreviation = state_abbreviation.values

    return state_abbreviation

# In the coal data, the data key capitalization is both all caps and mixed caps.  This function converts everything to
# a lower capitalization case.

# This function takes one input:  a pandas array of names.
# This function returns one output:  a pandas array of the same names in lower case.

# This function is used in the following codes:  avg_county_coal_constituents.py, weighted_ecdf_coalqual_data_samples.py


def lower_case_data_keys(data_keys):
    lower_case = []
    i = 0
    while i < len(data_keys):
        lower_case.append(data_keys.iloc[i].lower())
        i += 1

    lower_case = pd.Series(lower_case)
    lower_case = lower_case.values

    return lower_case

# In the COALQUAL data, apparent rank is broken down into five bituminous classes, three subbituminous classes, and two
# lignite classes.  This function converts everything into a "BITUMINOUS", "SUBBITUMINOUS", and a "LIGNITE" class.

# This function takes one input:  a pandas array of apparent coal rank.
# This function returns one output:  a pandas array of coal rank.

# This function is used in the following codes:  avg_county_coal_constituents.py


def generic_coal_rank(coal_rank):
    rank = []
    i = 0
    while i < len(coal_rank):
        if coal_rank.iloc[i] == 'High volatile A bituminous' or \
                coal_rank.iloc[i] == 'High volatile B bituminous' or \
                coal_rank.iloc[i] == 'High volatile C bituminous' or \
                coal_rank.iloc[i] == 'Low volatile bituminous' or \
                coal_rank.iloc[i] == 'Medium volatile bituminous':
            rank.append('BITUMINOUS')
        elif coal_rank.iloc[i] == 'Subbituminous A' or coal_rank.iloc[i] == 'Subbituminous B' or \
                coal_rank.iloc[i] == 'Subbituminous C':
            rank.append('SUBBITUMINOUS')
        elif coal_rank.iloc[i] == 'Lignite A' or coal_rank.iloc[i] == 'Lignite B':
            rank.append('LIGNITE')
        else:
            rank.append('COAL')
        i += 1

    rank = pd.Series(rank)
    rank = rank.values

    return rank

# The COALQUAL county-level summary does not have a separate column for the state abbreviation.  This function creates
# that state abbreviation column.

# This function takes one input:  a Pandas array of the State FIPS_Code values
# This function returns one output:  a Pandas array of the State abbreviations.

# This function is used in the following codes:  avg_county_constituents.py


def pull_state_abbreviation(FIPS_code_state):
    state_abbreviation = []
    i = 0
    while i < len(FIPS_code_state):
        if isinstance(FIPS_code_state.iloc[i], float):
            state = last_state
        else:
            state = FIPS_code_state.iloc[i][:2]
        state_abbreviation.append(state)
        last_state = state
        i += 1

    state_abbreviation = pd.Series(state_abbreviation)
    state_abbreviation = state_abbreviation.values

    return state_abbreviation

# When using the .describe() function with multiple keys on a Pandas dataframe, the first key has several values that
# are left blank.  This fills in those blank values with the one preceding it.

# This function takes one input:  A Pandas array of the key's in a dataframe.
# This function returns one output:  A Pandas array of the key's.


def completing_missing_keys_in_a_describe_dataframe(dataframe_keys):
    keys = []
    i = 0
    while i < len(dataframe_keys):
        if pd.isnull(dataframe_keys.iloc[i]):
            key = (last_key)
        else:
            key = dataframe_keys.iloc[i]
            last_key = key
        keys.append(key)
        i += 1

    keys = pd.Series(keys)
    keys = keys.values

    return keys

# This creates a list of the COALQUAL county and rank data for individual keys.

# This function takes two inputs: A pandas array of the county, state and a pandas array of the rank.
# This function returns one output:  A list of the county/rank combinations.


def geography_rank_list_compilation(geography, ranks):
    list_of_geography_ranks = []
    i = 0
    while i < len(geography):
        if pd.isnull(geography.iloc[i]):
            i += 1
        else:
            list_of_geography_ranks.append([geography.iloc[i], ranks.iloc[i]])
            i += 1
    unique_geography_ranks = []
    unique_geography_ranks.append(list_of_geography_ranks[0])
    i = 1
    while i < len(list_of_geography_ranks):
        j = 0
        index = 0
        while j < len(unique_geography_ranks):
            if list_of_geography_ranks[i] == unique_geography_ranks[j]:
                index = 1
            j += 1
        if index == 0:
            unique_geography_ranks.append(list_of_geography_ranks[i])
        i += 1

    return unique_geography_ranks

# This function processes the qualifiers used in USGS COALQUAL data to determine if a value is below the lower detection
# limit.  If it is, it corrects the reported value (USGS assumed actual value was 0.7 times the LDL).

# This function takes two inputs:  The USGS reported value and the USGS data qualifier.
# This function reports one outputs:  A pandas dataframe containing trace element concentrations and a 0 or 1 indicating
# if the data was observed (1) or censored (0).


def qualifier_interpreter(reported_values, data_qualifiers):
    trace_element_concentration_data = np.zeros([len(data_qualifiers), 2], dtype=np.object)
    i = 0
    while i < len(reported_values):
        if not isinstance(data_qualifiers.iloc[i], float):
            if "L" in data_qualifiers.iloc[i]:
                trace_element_concentration_data[i, 0] = np.log10(reported_values.iloc[i]/0.7)
                trace_element_concentration_data[i, 1] = int(0)
            else:
                trace_element_concentration_data[i, 0] = np.log10(reported_values.iloc[i])
                trace_element_concentration_data[i, 1] = int(1)
        else:
            trace_element_concentration_data[i, 0] = np.log10(reported_values.iloc[i])
            trace_element_concentration_data[i, 1] = int(1)
        i += 1
    return trace_element_concentration_data

# This function takes the output of the qualifier interpreter function to calculate two parameters for the maximum
# likelihood estimation model.

# This function takes one input:  A two-column matrix containing the observed/LDL data (column 1) and a boolean value
# on whether the sample is observed or censored (column 2).
# This function returns two ouptuts:  the mean and standard deviation of a normal distribution fitted to the data.


def maximum_likelihood_estimation(exog):
    endog = np.ones(len(exog))
    model = CensoredLikelihoodOLS(exog, endog).fit()
    results = model.params
    mu = results[0]
    sigma = results[1]
    return mu, sigma
