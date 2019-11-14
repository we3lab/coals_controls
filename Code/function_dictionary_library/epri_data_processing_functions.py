import pandas as pd
import numpy as np

def merge_observation_data_on_date(datasets):
    i = 0
    while i < len(datasets):
        if i == 0:
            merged_data = pd.merge(datasets[0], datasets[1], how='inner',on='Collection_Date')
            i += 2
        else:
            merged_data = pd.merge(merged_data, datasets[i], how='inner', on='Collection_Date')
            i += 1

    return merged_data


def data_in_time_interval(dataset, start_date, end_date):
    dataset = dataset.set_index(['Collection_Date'])
    processed_data = dataset[start_date: end_date]

    return processed_data


def wastewater_removal_efficiencies(initial_concentration, effluent_concentration):
    removal = []
    i = 0
    while i <len(initial_concentration):
        if ~np.isnan(initial_concentration[i]) and ~np.isnan(effluent_concentration[i]):
            removal.append((initial_concentration[i] - effluent_concentration[i])/initial_concentration[i])
        i += 1
    avg_removal = sum(removal)/len(removal)

    return avg_removal
