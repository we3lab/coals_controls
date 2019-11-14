def deterministic_annual_cfpp_coal_inputs(Plant_ID, Fuel_Data, Trace_Element_Data, State_Trace_Element_Data,Rank_Data):
    import pandas as pd
    import numpy as np
    from weighted_avg import weighted_avg

    # Pandas throws up a warning when writing onto a copy of a dataframe instead of the original dataframe.  That is
    # intentional and so I silence the pandas warning about this.  For more on this error, see this stackoverflow post.
    # https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    pd.options.mode.chained_assignment = None

    pd.set_option('display.max_rows', 10)
    pd.set_option('display.max_columns', 500)

    Fuel_Data_copy=Fuel_Data[Fuel_Data.Plant_ID == Plant_ID]
    Counties_Purchased_Coal =Fuel_Data_copy.groupby(['FIPS_Code_State', 'Rank']).describe()
    Counties_Purchased_Coal = Counties_Purchased_Coal['Quantity']

    Coal_Purchased = []
    i = 0
    while i<len(Counties_Purchased_Coal['count']):
        Coal_Purchased.append(Counties_Purchased_Coal['count'].iat[i] * Counties_Purchased_Coal['mean'].iat[i])
        i += 1

    Coal_Purchased = pd.Series(Coal_Purchased)
    Counties_Purchased_Coal['Coal_Quantity'] = Coal_Purchased.values
    Counties_Purchased_Coal['FIPS_Code_State_Rank'] = Counties_Purchased_Coal.index

    State_Purchased = []
    Rank_Purchased = []
    i = 0
    while i<len(Counties_Purchased_Coal['FIPS_Code_State_Rank']):
        State_Abbreviation = str(Counties_Purchased_Coal.FIPS_Code_State_Rank.iloc[i])[2:4]
        State_Purchased.append(State_Abbreviation)
        fips_code_state_rank_key = Counties_Purchased_Coal['FIPS_Code_State_Rank'][i]
        Rank = fips_code_state_rank_key[1]
        Rank_Purchased.append(Rank)
        i += 1

    State_Purchased = pd.Series(State_Purchased)
    Counties_Purchased_Coal['State_Purchased'] = State_Purchased.values
    Rank_Purchased = pd.Series(Rank_Purchased)
    Counties_Purchased_Coal['Rank_Purchased'] = Rank_Purchased.values

    i = 0
    State_Rank = []
    while i < len(Counties_Purchased_Coal['State_Purchased']):
        State_Rank.append((Counties_Purchased_Coal['State_Purchased'][i], Counties_Purchased_Coal['Rank_Purchased'][i]))
        i += 1
    State_Rank = pd.Series(State_Rank)
    Counties_Purchased_Coal['State_Rank'] = State_Rank.values

    i = 0
    FIPS_Code_State_Rank = []
    while i < len(Trace_Element_Data['FIPS_Code_State']):
        FIPS_Code_State_Rank.append((Trace_Element_Data['FIPS_Code_State'][i], Trace_Element_Data['Rank'][i]))
        i += 1
    FIPS_Code_State_Rank = pd.Series(FIPS_Code_State_Rank)
    Trace_Element_Data['FIPS_Code_State_Rank'] = FIPS_Code_State_Rank.values

    i = 0
    State_Rank = []
    while i < len(State_Trace_Element_Data['State']):
        State_Rank.append((str(State_Trace_Element_Data['State'][i]), str(State_Trace_Element_Data['Rank'][i])))
        i += 1
    State_Rank = pd.Series(State_Rank)
    State_Trace_Element_Data['State_Rank'] = State_Rank.values

    Counties_Purchased_Coal_Trace_Element_Concentration = pd.merge(Counties_Purchased_Coal, Trace_Element_Data,
                                                                   how='left', on='FIPS_Code_State_Rank')
    print(Counties_Purchased_Coal_Trace_Element_Concentration)
    print(Counties_Purchased_Coal)
    print(Trace_Element_Data)

    if Counties_Purchased_Coal_Trace_Element_Concentration.Arsenic.empty:
        Counties_Purchased_Coal_Trace_Element_Concentration = pd.merge(Counties_Purchased_Coal,
                                                                       State_Trace_Element_Data, how='left',
                                                                      on='State_Rank')
    i = 0
    while i < len(Counties_Purchased_Coal_Trace_Element_Concentration['Arsenic']):
        state_rank = Counties_Purchased_Coal_Trace_Element_Concentration['State_Rank'].iloc[i]
        state_rank_copy = State_Trace_Element_Data[State_Trace_Element_Data['State_Rank'] == state_rank]
        
        if not state_rank_copy.empty:
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Selenium'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Selenium'].iloc[i] = state_rank_copy['Selenium'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Arsenic'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Arsenic'].iloc[i] = state_rank_copy['Arsenic'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Lead'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Lead'].iloc[i] = state_rank_copy['Lead'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Mercury'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Mercury'].iloc[i] = state_rank_copy['Mercury'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Chloride'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Chloride'].iloc[i] = state_rank_copy['Chloride'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Boron'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Boron'].iloc[i] = state_rank_copy['Boron'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Bromine'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Bromine'].iloc[i] = state_rank_copy['Bromine'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Heat'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Heat'].iloc[i] = state_rank_copy['Heat'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Sulfur'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Sulfur'].iloc[i] = state_rank_copy['Sulfur'].iloc[0]
        else: 
            dic = {"SUBBITUMINOUS": "SUB", "BITUMINOUS":"BIT","LIGNITE":"LIG"}
            rank = dic[Counties_Purchased_Coal_Trace_Element_Concentration["Rank_Purchased"].iloc[i]] 
            rank_data_copy = Rank_Data[Rank_Data["Rank"] == rank]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Selenium'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Selenium'].iloc[i] = rank_data_copy['Selenium'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Arsenic'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Arsenic'].iloc[i] = rank_data_copy['Arsenic'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Lead'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Lead'].iloc[i] = rank_data_copy['Lead'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Mercury'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Mercury'].iloc[i] = rank_data_copy['Mercury'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Chloride'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Chloride'].iloc[i] = rank_data_copy['Chloride'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Boron'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Boron'].iloc[i] = rank_data_copy['Boron'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Bromine'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Bromine'].iloc[i] = rank_data_copy['Bromine'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Heat'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Heat'].iloc[i] = rank_data_copy['Heat'].iloc[0]
            if np.isnan(Counties_Purchased_Coal_Trace_Element_Concentration['Sulfur'].iloc[i]):
                Counties_Purchased_Coal_Trace_Element_Concentration['Sulfur'].iloc[i] = rank_data_copy['Sulfur'].iloc[0]
        i += 1

    selenium_inputs = weighted_avg(Counties_Purchased_Coal_Trace_Element_Concentration['Selenium'],
                                   Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
    arsenic_inputs = weighted_avg(Counties_Purchased_Coal_Trace_Element_Concentration['Arsenic'],
                                  Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
    lead_inputs = weighted_avg(Counties_Purchased_Coal_Trace_Element_Concentration['Lead'],
                               Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
    mercury_inputs = weighted_avg(Counties_Purchased_Coal_Trace_Element_Concentration['Mercury'],
                                  Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
    chloride_inputs = weighted_avg(Counties_Purchased_Coal_Trace_Element_Concentration['Chloride'],
                                   Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
    boron_inputs = weighted_avg(Counties_Purchased_Coal_Trace_Element_Concentration['Boron'],
                                Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
    bromine_inputs = weighted_avg(Counties_Purchased_Coal_Trace_Element_Concentration['Bromine'],
                                  Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
    heat_inputs = weighted_avg(Counties_Purchased_Coal_Trace_Element_Concentration['Heat'],
                               Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
    sulfur_inputs = weighted_avg(Counties_Purchased_Coal_Trace_Element_Concentration['Sulfur'],
                                 Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])

    return selenium_inputs, arsenic_inputs, lead_inputs, mercury_inputs, chloride_inputs, boron_inputs, bromine_inputs, \
           heat_inputs, sulfur_inputs


def stochastic_annual_cfpp_coal_inputs(dic, Plant_ID, Fuel_Data, Trace_Element_Data, State_Trace_Element_Data,Rank_Data,trials):
    import pandas as pd
    import numpy as np

    from statistical_functions import concentration_from_mle_normal_distribution, heat_from_mle_normal_distribution

    # Pandas throws up a warning when writing onto a copy of a dataframe instead of the original dataframe.  That is
    # intentional and so I silence the pandas warning about this.  For more on this error, see this stackoverflow post.
    # https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    pd.options.mode.chained_assignment = None

    pd.set_option('display.max_rows', 10)
    short_ton_to_kilograms = 907.185 # 1 short ton is equivalent to 907.185 kg.

    Fuel_Data_copy=Fuel_Data[Fuel_Data.Plant_ID == Plant_ID]
    Counties_Purchased_Coal = Fuel_Data_copy.groupby(['FIPS_Code_State', 'Rank']).describe()
    Counties_Purchased_Coal = Counties_Purchased_Coal['Quantity']

    Coal_Purchased = []
    i = 0
    while i<len(Counties_Purchased_Coal['count']):
        Coal_Purchased.append(Counties_Purchased_Coal['count'].iat[i] * Counties_Purchased_Coal['mean'].iat[i])
        i += 1

    Coal_Purchased = pd.Series(Coal_Purchased)
    Counties_Purchased_Coal['Coal_Quantity'] = Coal_Purchased.values
    Counties_Purchased_Coal['FIPS_Code_State_Rank'] = Counties_Purchased_Coal.index

    State_Purchased = []
    Rank_Purchased = []
    i = 0
    while i<len(Counties_Purchased_Coal['FIPS_Code_State_Rank']):
        State_Abbreviation = str(Counties_Purchased_Coal.FIPS_Code_State_Rank.iloc[i])[2:4]
        State_Purchased.append(State_Abbreviation)
        fips_code_state_rank_key = Counties_Purchased_Coal['FIPS_Code_State_Rank'][i]
        Rank = fips_code_state_rank_key[1]
        Rank_Purchased.append(Rank)
        i += 1

    State_Purchased = pd.Series(State_Purchased)
    Counties_Purchased_Coal['State_Purchased'] = State_Purchased.values
    Rank_Purchased = pd.Series(Rank_Purchased)
    Counties_Purchased_Coal['Rank_Purchased'] = Rank_Purchased.values

    i = 0
    State_Rank = []
    while i < len(Counties_Purchased_Coal['State_Purchased']):
        State_Rank.append((Counties_Purchased_Coal['State_Purchased'][i], Counties_Purchased_Coal['Rank_Purchased'][i]))
        i += 1
    State_Rank = pd.Series(State_Rank)
    Counties_Purchased_Coal['State_Rank'] = State_Rank.values

    i = 0
    FIPS_Code_State_Rank = []
    while i < len(Trace_Element_Data['FIPS_Code_State']):
        FIPS_Code_State_Rank.append((Trace_Element_Data['FIPS_Code_State'][i], Trace_Element_Data['Rank'][i]))
        i += 1
    FIPS_Code_State_Rank = pd.Series(FIPS_Code_State_Rank)
    Trace_Element_Data['FIPS_Code_State_Rank'] = FIPS_Code_State_Rank.values

    i = 0
    State_Rank = []
    while i < len(State_Trace_Element_Data['State']):
        State_Rank.append((str(State_Trace_Element_Data['State'][i]), str(State_Trace_Element_Data['Rank'][i])))
        i += 1
    State_Rank = pd.Series(State_Rank)
    State_Trace_Element_Data['State_Rank'] = State_Rank.values

    Counties_Purchased_Coal_Trace_Element_Concentration = pd.merge(Counties_Purchased_Coal, Trace_Element_Data,
                                                                   how='left', on='FIPS_Code_State_Rank')

    if Counties_Purchased_Coal_Trace_Element_Concentration.empty:
        Counties_Purchased_Coal_Trace_Element_Concentration = pd.merge(Counties_Purchased_Coal,
                                                                       State_Trace_Element_Data, how='left',
                                                                       on='State_Rank')
    
    #Counties_Purchased_Coal_Trace_Element_Concentration.dropna(axis=0, how='any')

    i = 0
    while i < len(Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity']):
        state_rank = Counties_Purchased_Coal_Trace_Element_Concentration['State_Rank'].iloc[i]
        state_rank_copy = State_Trace_Element_Data[State_Trace_Element_Data['State_Rank'] == state_rank]
        if not state_rank_copy.empty:
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_As'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_As'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_As'].iloc[i] = \
                    state_rank_copy['Mean_As'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_As'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_As'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_As'].iloc[i] = \
                    state_rank_copy['Sigma_As'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_B'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_B'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_B'].iloc[i] = \
                    state_rank_copy['Mean_B'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_B'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_B'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_B'].iloc[i] = \
                    state_rank_copy['Sigma_B'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Br'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Br'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Br'].iloc[i] = \
                    state_rank_copy['Mean_Br'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Br'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Br'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Br'].iloc[i] = \
                    state_rank_copy['Sigma_Br'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Cl'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Cl'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Cl'].iloc[i] = \
                    state_rank_copy['Mean_Cl'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Cl'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Cl'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Cl'].iloc[i] = \
                    state_rank_copy['Sigma_Cl'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Hg'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Hg'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Hg'].iloc[i] = \
                    state_rank_copy['Mean_Hg'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Hg'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Hg'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Hg'].iloc[i] = \
                    state_rank_copy['Sigma_Hg'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Pb'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Pb'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Pb'].iloc[i] = \
                    state_rank_copy['Mean_Pb'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Pb'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Pb'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Pb'].iloc[i] = \
                    state_rank_copy['Sigma_Pb'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Se'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Se'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Se'].iloc[i] = \
                    state_rank_copy['Mean_Se'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Se'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Se'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Se'].iloc[i] = \
                    state_rank_copy['Sigma_Se'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Heat'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Heat'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Heat'].iloc[i] = \
                    state_rank_copy['Mean_Heat'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Heat'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Heat'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Heat'].iloc[i] = \
                    state_rank_copy['Sigma_Heat'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_S'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_S'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_S'].iloc[i] = \
                    state_rank_copy['Mean_S'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_S'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_S'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_S'].iloc[i] = \
                    state_rank_copy['Sigma_S'].iloc[0]
        else:
            #dic = {"SUBBITUMINOUS": "SUB", "BITUMINOUS":"BIT","LIGNITE":"LIG"}
            rank = Counties_Purchased_Coal_Trace_Element_Concentration["Rank_Purchased"].iloc[i]
            Rank_Data_copy = Rank_Data[Rank_Data["Rank"] == rank]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_As'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_As'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_As'].iloc[i] = \
                    Rank_Data_copy['Mean_As'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_As'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_As'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_As'].iloc[i] = \
                    Rank_Data_copy['Sigma_As'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_B'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_B'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_B'].iloc[i] = \
                    Rank_Data_copy['Mean_B'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_B'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_B'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_B'].iloc[i] = \
                    Rank_Data_copy['Sigma_B'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Br'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Br'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Br'].iloc[i] = \
                    Rank_Data_copy['Mean_Br'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Br'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Br'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Br'].iloc[i] = \
                    Rank_Data_copy['Sigma_Br'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Cl'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Cl'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Cl'].iloc[i] = \
                    Rank_Data_copy['Mean_Cl'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Cl'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Cl'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Cl'].iloc[i] = \
                    Rank_Data_copy['Sigma_Cl'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Hg'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Hg'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Hg'].iloc[i] = \
                    Rank_Data_copy['Mean_Hg'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Hg'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Hg'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Hg'].iloc[i] = \
                    Rank_Data_copy['Sigma_Hg'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Pb'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Pb'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Pb'].iloc[i] = \
                    Rank_Data_copy['Mean_Pb'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Pb'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Pb'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Pb'].iloc[i] = \
                    Rank_Data_copy['Sigma_Pb'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Se'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Se'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Se'].iloc[i] = \
                    Rank_Data_copy['Mean_Se'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Se'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Se'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Se'].iloc[i] = \
                    Rank_Data_copy['Sigma_Se'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Heat'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Heat'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Heat'].iloc[i] = \
                    Rank_Data_copy['Mean_Heat'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Heat'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Heat'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Heat'].iloc[i] = \
                    Rank_Data_copy['Sigma_Heat'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_S'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Mean_S'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Mean_S'].iloc[i] = \
                    Rank_Data_copy['Mean_S'].iloc[0]
            if isinstance(Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_S'].iloc[i], float) or \
                    Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_S'].iloc[i] is None:
                Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_S'].iloc[i] = \
                    Rank_Data_copy['Sigma_S'].iloc[0]
        i += 1

    arsenic_total = np.zeros(trials)
    boron_total = np.zeros(trials)
    bromine_total = np.zeros(trials)
    chlorine_total = np.zeros(trials)
    mercury_total = np.zeros(trials)
    lead_total = np.zeros(trials)
    selenium_total = np.zeros(trials)
    heat_total = np.zeros(trials)
    sulfur_total = np.zeros(trials)

    i = 0
    while i < len(Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity']):
        CountyDataMissing = pd.isnull(Counties_Purchased_Coal_Trace_Element_Concentration['FIPS_Code_State_Rank'].iloc[i])
        key = Counties_Purchased_Coal_Trace_Element_Concentration['FIPS_Code_State_Rank'].iloc[i]
        if key not in dic or CountyDataMissing: 
        #if the county_rank has not occured before or the concentration depends on rank/state data 
        #draw from the distribution 
            arsenic_distribution = concentration_from_mle_normal_distribution(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_As'][i],
                                                                              Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_As'][i],
                                                                              trials)
            boron_distribution = concentration_from_mle_normal_distribution(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_B'][i],
                                                                              Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_B'][i],
                                                                              trials)
            bromine_distribution = concentration_from_mle_normal_distribution(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Br'][i],
                                                                              Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Br'][i],
                                                                              trials)
            chlorine_distribution = concentration_from_mle_normal_distribution(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Cl'][i],
                                                                              Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Cl'][i],
                                                                              trials)
            mercury_distribution = concentration_from_mle_normal_distribution(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Hg'][i],
                                                                              Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Hg'][i],
                                                                              trials)
            lead_distribution = concentration_from_mle_normal_distribution(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Pb'][i],
                                                                              Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Pb'][i],
                                                                              trials)
            selenium_distribution = concentration_from_mle_normal_distribution(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Se'][i],
                                                                              Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Se'][i],
                                                                              trials)
            heat_distribution = heat_from_mle_normal_distribution(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_Heat'][i],
                                                                              Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_Heat'][i],
                                                                              trials)
            sulfur_distribution = concentration_from_mle_normal_distribution(Counties_Purchased_Coal_Trace_Element_Concentration['Mean_S'][i],
                                                                              Counties_Purchased_Coal_Trace_Element_Concentration['Sigma_S'][i],
                                                                              trials)
            dic[key] = [arsenic_distribution, boron_distribution, bromine_distribution, 
                        chlorine_distribution, mercury_distribution, lead_distribution, 
                        selenium_distribution, heat_distribution, sulfur_distribution] 
        else:
        #if the county_rank has occurred before, use concentrations drawn before 
            [arsenic_distribution, boron_distribution, bromine_distribution, 
                chlorine_distribution, mercury_distribution, lead_distribution, 
                selenium_distribution, heat_distribution, sulfur_distribution] = dic[key]

        arsenic = np.multiply((Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'].iloc[i] *
                                   short_ton_to_kilograms), arsenic_distribution)
        boron = np.multiply((Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'].iloc[i] *
                               short_ton_to_kilograms), boron_distribution)
        bromine = np.multiply((Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'].iloc[i] *
                               short_ton_to_kilograms), bromine_distribution)
        chlorine = np.multiply((Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'].iloc[i] *
                               short_ton_to_kilograms),chlorine_distribution)
        mercury = np.multiply((Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'].iloc[i] *
                               short_ton_to_kilograms),mercury_distribution)
        lead = np.multiply((Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'].iloc[i] *
                               short_ton_to_kilograms),lead_distribution)
        selenium = np.multiply((Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'].iloc[i] *
                               short_ton_to_kilograms),selenium_distribution)
        heat = np.multiply((Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'].iloc[i] *
                               short_ton_to_kilograms),heat_distribution)
        sulfur = np.multiply((Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'].iloc[i] *
                               short_ton_to_kilograms),sulfur_distribution)
        
        arsenic_total = arsenic_total + arsenic
        boron_total = boron_total + boron
        bromine_total = bromine_total + bromine
        chlorine_total = chlorine_total + chlorine
        mercury_total = mercury_total + mercury
        lead_total = lead_total + lead
        selenium_total = selenium_total + selenium
        heat_total = heat_total + heat
        sulfur_total = sulfur_total + sulfur
        i += 1

    arsenic_inputs = arsenic_total/(sum(Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
                                     * short_ton_to_kilograms)
    boron_inputs = boron_total/(sum(Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
                                * short_ton_to_kilograms)
    bromine_inputs = bromine_total/(sum(Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
                                    * short_ton_to_kilograms)
    chloride_inputs = chlorine_total/(sum(Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
                                      * short_ton_to_kilograms)
    mercury_inputs = mercury_total/(sum(Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
                                    * short_ton_to_kilograms)
    lead_inputs = lead_total/(sum(Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
                              * short_ton_to_kilograms)
    selenium_inputs = selenium_total/(sum(Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
                                      * short_ton_to_kilograms)
    heat_inputs = heat_total/(sum(Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
                              * short_ton_to_kilograms)
    sulfur_inputs = sulfur_total/(sum(Counties_Purchased_Coal_Trace_Element_Concentration['Coal_Quantity'])
                              * short_ton_to_kilograms)

    return selenium_inputs, arsenic_inputs, lead_inputs, mercury_inputs, chloride_inputs, boron_inputs, bromine_inputs, \
           heat_inputs, sulfur_inputs, dic 

