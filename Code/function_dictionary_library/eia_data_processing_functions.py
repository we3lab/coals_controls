# Import standard python packages
import numbers
import copy
import pandas as pd
import pathlib
import numpy as np
import sys


# EIA reports coal counties using the FIPS Codes for the county.  The county can be a one, two, or three digit number.
# For standardization sake, we convert them all to a three digit number.

# This function takes one input:  an array of FIPS county codes.
# This function returns one output:  an array of three-digit FIPS county codes

# This function is used in the following codes:  eia_coal_consumption_data.py


def convert_fips_county_three_digits(fips_codes):
    fips_three = []
    fips_codes = int(fips_codes)
    for county_fips in fips_codes:
        if len(str(int(county_fips))) == 1:
            fips_three.append('00' + str(int(county_fips)))
        elif len(str(int(county_fips))) == 2:
            fips_three.append('0' + str(int(county_fips)))
        elif len(str(int(county_fips))) == 3:
            fips_three.append(str(int(county_fips)))

    fips_three = pd.Series(fips_three)
    fips_three = fips_three.values

    return fips_three

def convert_fips_state_two_digits(fips_codes):
    fips_two = []
    for state_fips in fips_codes:
        if len(str(int(state_fips))) == 1:
            fips_two.append('0' + str(int(state_fips)))
        elif len(str(int(state_fips))) == 2:
            fips_two.append(str(int(state_fips)))

    fips_two = pd.Series(fips_two)
    fips_two = fips_two.values

    return fips_two


# FIPS county codes can be one to three digits.  The standard way of reporting them is to report them with three digits
# with preceding zeros.  This function converts adds the preceding zeros to the county codes in an array if necessary.
# It then combines the fips code with the state abbreviation.

# This function takes two inputs:  a pandas array of FIPS county codes and a pandas array of state abbreviations.
# This function returns one output:  a pandas array of State Abbreviation and FIPS county codes.

# This function is used in the following codes:  CFPP_fuel_data_processing_2015.py, CFPP_fuel_data_processing.py


def fips_codes_state_county_codes(fips_county_codes, state_abbreviations):
    i = 0
    t = 0
    temp = []
    state_county_codes = []
    while i < len(fips_county_codes):
        if isinstance(fips_county_codes.iloc[i], numbers.Number):
            code = int(fips_county_codes.iloc[i])
            if fips_county_codes.iloc[i] / 100 >= 1:
                state_county_codes.append(state_abbreviations.iloc[i] + ', ' + str(code))
            elif fips_county_codes.iloc[i] / 10 >= 1:
                state_county_codes.append(state_abbreviations.iloc[i] + ', 0' + str(code))
            elif fips_county_codes.iloc[i] / 1 >= 0:
                state_county_codes.append(state_abbreviations.iloc[i] + ', 00' + str(code))
        else:
            state_county_codes.append(state_abbreviations.iloc[i] + ', ' + str(fips_county_codes.iloc[i]))
        i += 1

    state_county_codes = pd.Series(state_county_codes)
    state_county_codes = state_county_codes.values

    return state_county_codes

# EIA reports coal rank using a three letter abbreviations.  COALQUAL reports everything using the full rank name.
# This function converts those three letter abbreviations to the full rank name (in all caps).

# This function takes one inputs:  a pandas array of coal rank abbreviations.
# This function returns one output:  a pandas array of coal ranks.

# This function is used in the following codes:  CFPP_fuel_data_processing_2015.py, CFPP_fuel_data_processing.py


def rank_abbreviation_to_full_name(coal_rank_abbreviations):
    i = 0
    fuel_abbreviation = []
    while i < len(coal_rank_abbreviations):
        if coal_rank_abbreviations.iloc[i] == 'BIT':
            fuel_abbreviation.append('BITUMINOUS')
        elif coal_rank_abbreviations.iloc[i] == 'SUB':
            fuel_abbreviation.append('SUBBITUMINOUS')
        elif coal_rank_abbreviations.iloc[i] == 'LIG':
            fuel_abbreviation.append('LIGNITE')
        i += 1

    fuel_abbreviation = pd.Series(fuel_abbreviation)
    fuel_abbreviation = fuel_abbreviation.values

    return fuel_abbreviation

# EIA and coal mine data includes both county names and county codes, but we need to create a merge key that has both
# these county identifiers and the relevant state.  This code concatenates these functions.

# This function takes two inputs:  two arrays to concatenate with a comma between them.
# This function returns one input:  an array of the concatenated strings.

# This function is used in the following codes:  eia_coal_consumption_data.py


def fips_code_county_name_state_concatenation(identifiers_1, identifiers_2):
    concatenated_strings = []
    i = 0
    while i < len(identifiers_1):
        if ~isinstance(identifiers_1.iloc[i], str):
            identifier_1 = str(identifiers_1.iloc[i])
        else:
            identifier_1 = identifiers_1.iloc[i]
        if ~isinstance(identifiers_2.iloc[i], str):
            identifier_2 = str(identifiers_2.iloc[i])
        else:
            identifier_2 = identifiers_2.iloc[i]
        concatenated_strings.append(identifier_1 + ", " + identifier_2)
        i += 1

    concatenated_strings = pd.Series(concatenated_strings)
    concatenated_strings = concatenated_strings.values

    return concatenated_strings

def state_county_fips_code_concatenation(identifiers_1, identifiers_2):
    concatenated_strings = []
    i = 0
    while i < len(identifiers_1):
        if ~isinstance(identifiers_1.iloc[i], str):
            identifier_1 = str(identifiers_1.iloc[i])
        else:
            identifier_1 = identifiers_1.iloc[i]
        if ~isinstance(identifiers_2.iloc[i], str):
            identifier_2 = str(identifiers_2.iloc[i])
        else:
            identifier_2 = identifiers_2.iloc[i]
        concatenated_strings.append(identifier_1 + identifier_2)
        i += 1

    concatenated_strings = pd.Series(concatenated_strings)
    concatenated_strings = concatenated_strings.values

    return concatenated_strings


def state_code_to_abbreviation(series):
    state_dic = {1:"AL", 2: 'AK', 3: 'IM', 4: 'AZ', 5: 'AR', 6: 'CA', 8: 'CO', 9: 'CT', 10: 'DE', 11: 'DC', 12: 'FL', 13: 'GA', 15: 'HI', 16: 'ID', 17: 'IL', 18: 'IN', 19: 'IA', 20: 'KS', 21: 'KY', 22: 'LA', 23: 'ME', 24: 'MD', 25: 'MA', 26: 'MI', 27: 'MN', 28: 'MS', 29: 'MO', 30: 'MT', 31: 'NE', 32: 'NV', 33: 'NH', 34: 'NJ', 35: 'NM', 36: 'NY', 37: 'NC', 38: 'ND', 39: 'OH', 40: 'OK', 41: 'OR', 42: 'PA', 44: 'RI', 45: 'SC', 46: 'SD', 47: 'TN', 48: 'TX', 49: 'UT', 50: 'VT', 51: 'VA', 53: 'WA', 54: 'WV', 55: 'WI', 56: 'WY'}
    i = 0 
    temp = []
    while i < len(series):
        state = state_dic[series.iloc[i]]
        temp.append(state)
        i = i + 1 
    return pd.Series(temp)


def data_filtering(dataframe, capacity, outputfile):

    # Filter plants that (1) don't use coal and (2) use either imported coal (IMP) or waste coal (WC).
    if type(dataframe.Fuel_Group.iloc[2]) != str:
        dataframe = dataframe[dataframe.Fuel_Group == 1]
        temp = ['Coal'] * len(dataframe.Fuel_Group)
        fuel = pd.Series(temp)
        dataframe.Fuel_Group = fuel
    else:
        dataframe = dataframe[dataframe.Fuel_Group == 'Coal']
    #dataframe = dataframe[dataframe.Mine_County != 'IMP']
    dataframe = dataframe[dataframe.Rank != 'WC']
    dataframe = dataframe[(dataframe.Rank == 'BIT') | (dataframe.Rank == 'LIG') |(dataframe.Rank == 'SUB')]
    #dataframe = dataframe[dataframe.Mine_County != 'IMP']

    # Filter out plants that do not report a county or state that there coal is sourced from.

    dataframe = dataframe[dataframe.Mine_County.notnull()]
    dataframe = dataframe[dataframe.Mine_State.notnull()]

    if type(dataframe.Mine_State.iloc[2]) != str:
        dataframe.Mine_State = state_code_to_abbreviation(dataframe.Mine_State)
    dataframe = dataframe[dataframe.Mine_State.notnull()]
    
    #Filter out plants with capacity lower than 1MW
    PlantsLessThanOne = []
    Plants = dataframe.Plant_ID.unique().tolist()
    PlantsLargerThanOne = copy.deepcopy(Plants)
    for p in Plants:
        temp = capacity[capacity.Plant_ID == p]
        tempCapacity = temp.Capacity.tolist()
        for c in tempCapacity: 
            if c < 1:
                PlantsLessThanOne.append(p)
                PlantsLargerThanOne.remove(p)
                break

    # #Do not filter out plants with boiler connecting to multiple generators 
    #Boilers connecting to multiple generators will be filtered out at boiler level 
    # PlantsLeft = []
    # for p in PlantsLargerThanOne:
    #     temp = generator[generator.Plant_ID == p]
    #     tempBoiler = temp.Boiler_ID.unique().tolist()
    #     tempGenerator = temp.Generator_ID.unique().tolist()
    #     if len(tempBoiler) >= len(tempGenerator):
    #         PlantsLeft.append(p)

    Qualifed = {'Plant_ID':PlantsLargerThanOne}
    Qualifed = pd.DataFrame(Qualifed)
    dataframe = Qualifed.merge(dataframe, how='left', on='Plant_ID')
    dataframe = dataframe.sort_values(by = ["Month",'Plant_ID'])
    dataframe = dataframe[['Month','Plant_ID', 'Rank', 'Fuel_Group', 'Mine_State', 'Mine_County',
        'Quantity', 'Heat_Content']]

    filteredOut = [x for x in Plants if x not in PlantsLargerThanOne]
    for b in filteredOut:
        dataframe = dataframe[dataframe.Plant_ID != b]

    # Qualifed = {'Plant_ID':PlantsLargerThanOne}
    # Qualifed = pd.DataFrame(Qualifed)
    # print(Qualifed)
    # print(dataframe)
    # dataframe = Qualifed.merge(dataframe, how='left', on='Plant_ID')
    # dataframe = dataframe.sort_values(by = ["Month",'Plant_ID'])
    # dataframe = dataframe[['Month','Plant_ID', 'Rank', 'Fuel_Group', 'Mine_State', 'Mine_County',
    #     'Quantity', 'Heat_Content']]
       

    # The FIPS code can be anywhere from one digit to three digits, this function converts it to a uniform three digits and
    # adds the state abbreviation to create a string uniquely identifying each county as it .
    dataframe['FIPS_Code_State'] = fips_codes_state_county_codes(dataframe.Mine_County,
                                                                    dataframe.Mine_State)


    # EIA reports the fuel consumed using a three letter abbreviation (i.e. "BIT", "SUB", and "LIG").  COALQUAL uses the
    # full name in all capital letters.  This function converts the EIA code to the COALQUAL rank name.
    dataframe['Rank'] = rank_abbreviation_to_full_name(dataframe.Rank)

    PlantsLessThanOne = PlantsLessThanOne + [0]*(len(dataframe['Rank'])-len(PlantsLessThanOne))

    dataframe["Capacity_LessThan1"] = pd.Series(PlantsLessThanOne)
    print(dataframe)
    dataframe.to_csv(outputfile)

def merge_generator_boiler_data(boiler_data, boiler_fuel_data, generator_generation_data, generator_capacity_data, go_between_table):

    # Start by creating the plant_boiler column for the boiler data table
    i = 0
    plant_boiler_combination = []
    while i < len(boiler_data['Plant_ID']):
        plant_boiler_combination.append(str(int(boiler_data['Plant_ID'].iloc[i])) + '_' +
                                        str(boiler_data['Boiler_ID'].iloc[i]))
        i += 1

    plant_boiler_combination = pd.Series(plant_boiler_combination)
    boiler_data['Plant_Boiler'] = plant_boiler_combination.values

    # Start by creating the plant_boiler column for the boiler data table
    i = 0
    plant_boiler_combination = []
    while i < len(boiler_fuel_data['Plant_ID']):
        plant_boiler_combination.append(str(int(boiler_fuel_data['Plant_ID'].iloc[i])) + '_' +
                                        str(boiler_fuel_data['Boiler_ID'].iloc[i]))
        i += 1

    plant_boiler_combination = pd.Series(plant_boiler_combination)
    boiler_fuel_data['Plant_Boiler'] = plant_boiler_combination.values

    # Then create the plant_generator column for the generation data table
    i = 0
    plant_generator_combination = []
    while i < len(generator_generation_data['Plant_ID']):
        plant_generator_combination.append(str(int(generator_generation_data['Plant_ID'].iloc[i])) + '_' +
                                           str(generator_generation_data['Generator_ID'].iloc[i]))
        i += 1

    plant_generator_combination = pd.Series(plant_generator_combination)
    generator_generation_data['Plant_Generator'] = plant_generator_combination.values

    # Create the plant_generator column for the capacity data table
    i = 0
    plant_generator_combination = []
    while i < len(generator_capacity_data['Plant_ID']):
        plant_generator_combination.append(str(int(generator_capacity_data['Plant_ID'].iloc[i])) + '_' +
                                           str(generator_capacity_data['Generator_ID'].iloc[i]))
        i += 1

    plant_generator_combination = pd.Series(plant_generator_combination)
    generator_capacity_data['Plant_Generator'] = plant_generator_combination.values

    # Finally create the columns that will allow to go between boilers and generators
    i = 0
    plant_generator_combination = []
    plant_boiler_combination = []
    while i < len(go_between_table['Plant_ID']):
        plant_generator_combination.append(str(int(go_between_table['Plant_ID'].iloc[i])) + '_' +
                                           str(go_between_table['Generator_ID'].iloc[i]))
        plant_boiler_combination.append(str(int(go_between_table['Plant_ID'].iloc[i])) + '_' +
                                        str(go_between_table['Boiler_ID'].iloc[i]))
        i += 1

    plant_generator_combination = pd.Series(plant_generator_combination)
    go_between_table['Plant_Generator'] = plant_generator_combination.values
    plant_boiler_combination = pd.Series(plant_boiler_combination)
    go_between_table['Plant_Boiler'] = plant_boiler_combination.values

    boiler_generator_data = pd.merge(boiler_data, boiler_fuel_data, on='Plant_Boiler')
    boiler_generator_data = pd.merge(boiler_generator_data, go_between_table, on='Plant_Boiler')
    boiler_generator_data = pd.merge(boiler_generator_data, generator_capacity_data, on='Plant_Generator')
    boiler_generator_data = pd.merge(boiler_generator_data, generator_generation_data, on='Plant_Generator')

    return boiler_generator_data


def drop_noncoal_fuels(boiler_generator_data):
    coal_types = ['BIT', 'SUB', 'LIG', 'COL']
    boiler_generator_data = boiler_generator_data[boiler_generator_data['Fuel_Type'].isin(coal_types)]

    return boiler_generator_data


def so2_compliance_strategy_approaches(boiler_generator_data):
    fgd_use_generation = 0
    fgd_use_capacity = 0
    design_changes_generation = 0
    design_changes_capacity = 0
    low_sulfur_fuel_generation = 0
    low_sulfur_fuel_capacity = 0
    allocation_generation = 0
    allocation_capacity = 0
    sulfur_requirements_transfer_generation = 0
    sulfur_requirements_transfer_capacity = 0
    utilization_changes_generation = 0
    utilization_changes_capacity = 0
    no_change_generation = 0
    no_change_capacity = 0
    no_reported_strategy_generation = 0
    no_reported_strategy_capacity = 0
    i = 0
    while i < len(boiler_generator_data.SO2_Strat_1):
        so2_compliance_strategy = boiler_generator_data['SO2_Strat_1'].iloc[i]
        # if so2_compliance_strategy == 'NC':
        #     so2_compliance_strategy = boiler_generator_data['SO2_Strat_2'].iloc[i]
        if isinstance(so2_compliance_strategy, float):
            so2_compliance_strategy = boiler_generator_data['SO2_Strat_2'].iloc[i]
        if so2_compliance_strategy == 'BO':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'CF':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'CU':
            sulfur_requirements_transfer_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            sulfur_requirements_transfer_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'FR':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'IF':
            fgd_use_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            fgd_use_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'LA':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'LN':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'NC':
            no_change_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            no_change_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'RP':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'OV':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'SS':
            low_sulfur_fuel_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            low_sulfur_fuel_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'SU':
            sulfur_requirements_transfer_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            sulfur_requirements_transfer_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'TU':
            sulfur_requirements_transfer_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            sulfur_requirements_transfer_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'UC':
            sulfur_requirements_transfer_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            sulfur_requirements_transfer_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'UE':
            utilization_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            utilization_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'US':
            utilization_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            utilization_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'UP':
            utilization_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            utilization_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'WA':
            allocation_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            allocation_generation += boiler_generator_data['Generation'].iloc[i]
        elif isinstance(so2_compliance_strategy, float):
            no_reported_strategy_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            no_reported_strategy_generation += boiler_generator_data['Generation'].iloc[i]
        i += 1

    capacity = sum(boiler_generator_data['Nameplate_Capacity'])
    generation = sum(boiler_generator_data['Generation'])

    return fgd_use_generation, fgd_use_capacity, low_sulfur_fuel_generation, low_sulfur_fuel_capacity, \
           design_changes_generation, design_changes_capacity, allocation_generation, allocation_capacity, \
           sulfur_requirements_transfer_generation, sulfur_requirements_transfer_capacity, \
           utilization_changes_generation, utilization_changes_capacity, no_change_generation, no_change_capacity, \
           no_reported_strategy_generation, no_reported_strategy_capacity, capacity, generation

def backcasted_so2_compliance_strategy_approaches(boiler_generator_data, next_year_boiler_generator_data):
    fgd_use_generation = 0
    fgd_use_capacity = 0
    design_changes_generation = 0
    design_changes_capacity = 0
    low_sulfur_fuel_generation = 0
    low_sulfur_fuel_capacity = 0
    allocation_generation = 0
    allocation_capacity = 0
    sulfur_requirements_transfer_generation = 0
    sulfur_requirements_transfer_capacity = 0
    utilization_changes_generation = 0
    utilization_changes_capacity = 0
    no_change_generation = 0
    no_change_capacity = 0
    no_reported_strategy_generation = 0
    no_reported_strategy_capacity = 0
    i = 0
    while i < len(boiler_generator_data.SO2_Strat_1):
        so2_compliance_strategy = boiler_generator_data['SO2_Strat_1'].iloc[i]
        if so2_compliance_strategy == 'NC':
            matching_last_year_boiler_data = next_year_boiler_generator_data[next_year_boiler_generator_data.Plant_Boiler == boiler_generator_data.Plant_Boiler.iloc[i]]
            if len(matching_last_year_boiler_data['SO2_Strat_1']) > 0:
                so2_compliance_strategy = matching_last_year_boiler_data['SO2_Strat_1'].iloc[0]
                boiler_generator_data['SO2_Strat_1'].iloc[i] = so2_compliance_strategy
        if isinstance(so2_compliance_strategy, float):
            so2_compliance_strategy = boiler_generator_data['SO2_Strat_2'].iloc[i]
        if so2_compliance_strategy == 'BO':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'CF':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'CU':
            sulfur_requirements_transfer_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            sulfur_requirements_transfer_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'FR':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'IF':
            fgd_use_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            fgd_use_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'LA':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'LN':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'NC':
            no_change_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            no_change_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'RP':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'OV':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'SS':
            low_sulfur_fuel_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            low_sulfur_fuel_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'SU':
            sulfur_requirements_transfer_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            sulfur_requirements_transfer_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'TU':
            sulfur_requirements_transfer_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            sulfur_requirements_transfer_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'UC':
            sulfur_requirements_transfer_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            sulfur_requirements_transfer_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'UE':
            utilization_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            utilization_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'US':
            utilization_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            utilization_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'UP':
            utilization_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            utilization_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'WA':
            allocation_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            allocation_generation += boiler_generator_data['Generation'].iloc[i]
        elif isinstance(so2_compliance_strategy, float):
            no_reported_strategy_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            no_reported_strategy_generation += boiler_generator_data['Generation'].iloc[i]
        i += 1

    capacity = sum(boiler_generator_data['Nameplate_Capacity'])
    generation = sum(boiler_generator_data['Generation'])

    return fgd_use_generation, fgd_use_capacity, low_sulfur_fuel_generation, low_sulfur_fuel_capacity, \
           design_changes_generation, design_changes_capacity, allocation_generation, allocation_capacity, \
           sulfur_requirements_transfer_generation, sulfur_requirements_transfer_capacity, \
           utilization_changes_generation, utilization_changes_capacity, no_change_generation, no_change_capacity, \
           no_reported_strategy_generation, no_reported_strategy_capacity, capacity, generation, boiler_generator_data

def forecasted_so2_compliance_strategy_approaches(boiler_generator_data, previous_year_boiler_generator_data):
    fgd_use_generation = 0
    fgd_use_capacity = 0
    design_changes_generation = 0
    design_changes_capacity = 0
    low_sulfur_fuel_generation = 0
    low_sulfur_fuel_capacity = 0
    allocation_generation = 0
    allocation_capacity = 0
    sulfur_requirements_transfer_generation = 0
    sulfur_requirements_transfer_capacity = 0
    utilization_changes_generation = 0
    utilization_changes_capacity = 0
    no_change_generation = 0
    no_change_capacity = 0
    no_reported_strategy_generation = 0
    no_reported_strategy_capacity = 0
    i = 0
    while i < len(boiler_generator_data.SO2_Strat_1):
        so2_compliance_strategy = boiler_generator_data['SO2_Strat_1'].iloc[i]
        if so2_compliance_strategy == 'NC':
            matching_last_year_boiler_data = previous_year_boiler_generator_data[previous_year_boiler_generator_data.Plant_Boiler == boiler_generator_data.Plant_Boiler.iloc[i]]
            if len(matching_last_year_boiler_data['SO2_Strat_1']) > 0:
                so2_compliance_strategy = matching_last_year_boiler_data['SO2_Strat_1'].iloc[0]
                boiler_generator_data['SO2_Strat_1'].iloc[i] = so2_compliance_strategy
        if isinstance(so2_compliance_strategy, float):
            so2_compliance_strategy = boiler_generator_data['SO2_Strat_2'].iloc[i]
        if so2_compliance_strategy == 'BO':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'CF':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'CU':
            sulfur_requirements_transfer_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            sulfur_requirements_transfer_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'FR':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'IF':
            fgd_use_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            fgd_use_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'LA':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'LN':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'NC':
            no_change_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            no_change_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'RP':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'OV':
            design_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            design_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'SS':
            low_sulfur_fuel_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            low_sulfur_fuel_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'SU':
            sulfur_requirements_transfer_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            sulfur_requirements_transfer_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'TU':
            sulfur_requirements_transfer_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            sulfur_requirements_transfer_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'UC':
            sulfur_requirements_transfer_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            sulfur_requirements_transfer_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'UE':
            utilization_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            utilization_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'US':
            utilization_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            utilization_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'UP':
            utilization_changes_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            utilization_changes_generation += boiler_generator_data['Generation'].iloc[i]
        elif so2_compliance_strategy == 'WA':
            allocation_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            allocation_generation += boiler_generator_data['Generation'].iloc[i]
        elif isinstance(so2_compliance_strategy, float):
            no_reported_strategy_capacity += boiler_generator_data['Nameplate_Capacity'].iloc[i]
            no_reported_strategy_generation += boiler_generator_data['Generation'].iloc[i]
        i += 1

    capacity = sum(boiler_generator_data['Nameplate_Capacity'])
    generation = sum(boiler_generator_data['Generation'])

    return fgd_use_generation, fgd_use_capacity, low_sulfur_fuel_generation, low_sulfur_fuel_capacity, \
           design_changes_generation, design_changes_capacity, allocation_generation, allocation_capacity, \
           sulfur_requirements_transfer_generation, sulfur_requirements_transfer_capacity, \
           utilization_changes_generation, utilization_changes_capacity, no_change_generation, no_change_capacity, \
           no_reported_strategy_generation, no_reported_strategy_capacity, capacity, generation, boiler_generator_data

def sulfur_switching_boilers(boiler_generator_data):
    boiler_generator_data_sulfur_switched = boiler_generator_data[boiler_generator_data.SO2_Strat_1 == 'SS']
    boiler_generators_sulfur_switched = boiler_generator_data_sulfur_switched['Plant_ID']
    boiler_generators_sulfur_switched = list(set(boiler_generators_sulfur_switched))

    return boiler_generators_sulfur_switched
