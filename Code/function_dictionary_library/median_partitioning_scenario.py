import numpy as np

def partitioning_scenario(te_fate, p1, p2, odd=True):
    '''This function will display the partitioning of TE by APCD for either odd or even
    number of Monte Carlo runs'''
    te_total_input = te_fate[:, 0] + te_fate[:, 1] + te_fate[:, 2]
    te_median_input = np.median(te_total_input)
    te_p1_input = np.percentile(te_total_input, p1)
    te_p2_input = np.percentile(te_total_input, p2)

    sorted_list = sorted(te_total_input)
    if odd:
        # if the number of runs is odd, we can directly find the index of the value
        te_median_index = np.nonzero(te_total_input == te_median_input)[0][0]
        te_median_solid = te_fate[te_median_index, 0]
        te_median_liquid = te_fate[te_median_index, 1]
        te_median_gas = te_fate[te_median_index, 2]

        te_p1_index = np.nonzero(te_total_input == te_p1_input)[0][0]
        te_p1_solid = te_fate[te_p1_index, 0]
        te_p1_liquid = te_fate[te_p1_index, 1]
        te_p1_gas = te_fate[te_p1_index, 2]

        te_p2_index = np.nonzero(te_total_input == te_p2_input)[0][0]
        te_p2_solid = te_fate[te_p2_index, 0]
        te_p2_liquid = te_fate[te_p2_index, 1]
        te_p2_gas = te_fate[te_p2_index, 2]
    else:
        # if the number
        median_index = np.where(te_total_input == sorted_list[len(te_fate) // 2])[0][0]
        median_second_index = np.where(te_total_input == sorted_list[len(te_fate) // 2 + 1])[0][0]
        te_median_solid = (te_fate[median_index, 0] + te_fate[median_second_index, 0]) / 2
        te_median_liquid = (te_fate[median_index, 1] + te_fate[median_second_index, 1]) / 2
        te_median_gas = (te_fate[median_index, 2] + te_fate[median_second_index, 2]) / 2

        p1_index = np.where(te_total_input == sorted_list[int(len(te_fate) // (100 / p1))])[0][0]
        p1_second_index = np.where(te_total_input == sorted_list[int(len(te_fate) // (100 / p1) + 1)])[0][0]

        p2_index = np.where(te_total_input == sorted_list[int(len(te_fate) // (100 / p2))])[0][0]
        p2_second_index = np.where(te_total_input == sorted_list[int(len(te_fate) // (100 / p2) + 1)])[0][0]

        te_p1_solid = (te_fate[p1_index, 0] + te_fate[p1_second_index, 0]) / 2
        te_p1_liquid = (te_fate[p1_index, 1] + te_fate[p1_second_index, 1]) / 2
        te_p1_gas = (te_fate[p1_index, 2] + te_fate[p1_second_index, 2]) / 2

        te_p2_solid = (te_fate[p2_index, 0] + te_fate[p2_second_index, 0]) / 2
        te_p2_liquid = (te_fate[p2_index, 1] + te_fate[p2_second_index, 1]) / 2
        te_p2_gas = (te_fate[p2_index, 2] + te_fate[p2_second_index, 2]) / 2

    te_median_summary = [te_median_input, te_median_solid, te_median_liquid, te_median_gas]
    te_p1_summary = [te_p1_input, te_p1_solid, te_p1_liquid, te_p1_gas]
    te_p2_summary = [te_p2_input, te_p2_solid, te_p2_liquid, te_p2_gas]

    return te_median_summary, te_p1_summary, te_p2_summary


# This one is used for the non-GUI model, which does not allow the user to determine the number of
# Monte Carlo runs, and therefore does not need to worry about potential even number of runs which
# will not work using the code below
def median_partitioning_scenario(te_fate):
    te_total_input = te_fate[:, 0] + te_fate[:, 1] + te_fate[:, 2]
    te_median_input = np.median(te_total_input)
    te_median_index = np.nonzero(te_total_input == te_median_input)[0][0]
    te_median_solid = te_fate[te_median_index, 0]
    te_median_liquid = te_fate[te_median_index, 1]
    te_median_gas = te_fate[te_median_index, 2]

    te_median_summary = [te_median_input, te_median_solid, te_median_liquid, te_median_gas]

    return te_median_summary