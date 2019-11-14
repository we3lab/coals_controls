def deterministic_trace_elements_in_boiler(boiler_fuel, trace_elements, rank_summary, less_than_1_list):
    import pandas as pd
    import numpy as np

    # Pandas throws up a warning when writing onto a copy of a dataframe instead of the original dataframe.  That is
    # intentional and so I silence the pandas warning about this.  For more on this error, see this stackoverflow post.
    # https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    pd.options.mode.chained_assignment = None

    unique_plants = boiler_fuel.Plant_ID.unique()

    i = 0
    boiler_fuel_share = pd.DataFrame()
    while i < len(unique_plants):
        boiler_fuel_copy = boiler_fuel[boiler_fuel.Plant_ID == unique_plants[i]]
        trace_elements_copy = trace_elements[trace_elements.Plant_ID == unique_plants[i]]
        total_coals = boiler_fuel_copy['Coal_Consumption'].sum()
        share_coal = []
        if unique_plants[i] in less_than_1_list:
            #the plant is not qualified plant (capacity < 1MW) list 
            i += 1
        else: 
            if len(trace_elements_copy.Plant_ID) == 1:
                #Use te concentration for this plant 
                selenium_concentration = trace_elements_copy.Selenium.iloc[0]
                arsenic_concentration = trace_elements_copy.Arsenic.iloc[0]
                lead_concentration = trace_elements_copy.Lead.iloc[0]
                mercury_concentration= trace_elements_copy.Mercury.iloc[0]
                chloride_concentration = trace_elements_copy.Chloride.iloc[0]
                boron_concentration = trace_elements_copy.Boron.iloc[0]
                bromide_concentration = trace_elements_copy.Bromide.iloc[0]
                heat_concentration = trace_elements_copy.Heat.iloc[0]
                sulfur_concentration = trace_elements_copy.Sulfur.iloc[0]
            else:
                #if the plant is burning IMP coal, use rank summary data to estimate
                rank_summary_copy = rank_summary[boiler_fuel_copy.Fuel.iloc[0] == rank_summary.Rank]
                selenium_concentration = rank_summary_copy.Selenium.iloc[0]
                arsenic_concentration = rank_summary_copy.Arsenic.iloc[0]
                lead_concentration = rank_summary_copy.Lead.iloc[0]
                mercury_concentration = rank_summary_copy.Mercury.iloc[0]
                chloride_concentration = rank_summary_copy.Chloride.iloc[0]
                boron_concentration = rank_summary_copy.Boron.iloc[0]
                bromide_concentration = rank_summary_copy.Bromine.iloc[0]
                heat_concentration = rank_summary_copy.Heat.iloc[0]
                sulfur_concentration = rank_summary_copy.Sulfur.iloc[0]
            selenium = []
            arsenic = []
            lead = []
            mercury = []
            chloride = []
            boron = []
            bromide = []
            heat = []
            sulfur = []
            j = 0
            while j < len(boiler_fuel_copy.Coal_Consumption):
                if total_coals > 0:
                    coal_burned = boiler_fuel_copy.Coal_Consumption.iloc[j]
                    selenium_boiler = np.multiply(selenium_concentration, (coal_burned * 9.07185e-4)) #in kg/yr
                    arsenic_boiler = np.multiply(arsenic_concentration, (coal_burned * 9.07185e-4)) #in kg/yr
                    lead_boiler = np.multiply(lead_concentration, (coal_burned * 9.07185e-4)) #in kg/yr
                    mercury_boiler = np.multiply(mercury_concentration, (coal_burned * 9.07185e-4)) #in kg/yr
                    chloride_boiler = np.multiply(chloride_concentration, (coal_burned * 9.07185e-4)) #in kg/yr
                    boron_boiler = np.multiply(boron_concentration, (coal_burned * 9.07185e-4)) #in kg/yr
                    bromide_boiler = np.multiply(bromide_concentration, (coal_burned * 9.07185e-4)) #in kg/yr
                    heat_boiler = np.multiply(heat_concentration, (coal_burned * 2)) #in MBtu/yr
                    sulfur_boiler = np.multiply(sulfur_concentration, (coal_burned * 9.07185e2))  # in kg/yr
                    coal_burned = pd.Series(coal_burned)
                    selenium_boiler = pd.Series(selenium_boiler)
                    arsenic_boiler = pd.Series(arsenic_boiler)
                    lead_boiler = pd.Series(lead_boiler)
                    mercury_boiler = pd.Series(mercury_boiler)
                    chloride_boiler = pd.Series(chloride_boiler)
                    boron_boiler = pd.Series(boron_boiler)
                    bromide_boiler = pd.Series(bromide_boiler)
                    heat_boiler = pd.Series(heat_boiler)
                    sulfur_boiler = pd.Series(sulfur_boiler)
                    if j == 0:
                        coal = coal_burned
                        selenium = selenium_boiler
                        arsenic = arsenic_boiler
                        lead = lead_boiler
                        mercury = mercury_boiler
                        chloride = chloride_boiler
                        boron = boron_boiler
                        bromide = bromide_boiler
                        heat = heat_boiler
                        sulfur = sulfur_boiler
                    else:
                        coal = coal.append(coal_burned)
                        selenium = selenium.append(selenium_boiler)
                        arsenic = arsenic.append(arsenic_boiler)
                        lead = lead.append(lead_boiler)
                        mercury = mercury.append(mercury_boiler)
                        chloride = chloride.append(chloride_boiler)
                        boron = boron.append(boron_boiler)
                        bromide = bromide.append(bromide_boiler)
                        heat = heat.append(heat_boiler)
                        sulfur = sulfur.append(sulfur_boiler)
                else:
                    coal_burned = 0
                    selenium_boiler = 0
                    arsenic_boiler = 0
                    lead_boiler = 0
                    mercury_boiler = 0
                    chloride_boiler = 0
                    boron_boiler = 0
                    bromide_boiler = 0
                    heat_boiler = 0
                    sulfur_boiler = 0
                    coal_burned = pd.Series(coal_burned)
                    selenium_boiler = pd.Series(selenium_boiler)
                    arsenic_boiler = pd.Series(arsenic_boiler)
                    lead_boiler = pd.Series(lead_boiler)
                    mercury_boiler = pd.Series(mercury_boiler)
                    chloride_boiler = pd.Series(chloride_boiler)
                    boron_boiler = pd.Series(boron_boiler)
                    bromide_boiler = pd.Series(bromide_boiler)
                    heat_boiler = pd.Series(heat_boiler)
                    sulfur_boiler = pd.Series(sulfur_boiler)
                    if j == 0:
                        coal = coal_burned
                        selenium = selenium_boiler
                        arsenic = arsenic_boiler
                        lead = lead_boiler
                        mercury = mercury_boiler
                        chloride = chloride_boiler
                        boron = boron_boiler
                        bromide = bromide_boiler
                        heat = heat_boiler
                        sulfur = sulfur_boiler
                    else:
                        coal = coal.append(coal_burned)
                        selenium = selenium.append(selenium_boiler)
                        arsenic = arsenic.append(arsenic_boiler)
                        lead = lead.append(lead_boiler)
                        mercury = mercury.append(mercury_boiler)
                        chloride = chloride.append(chloride_boiler)
                        boron = boron.append(boron_boiler)
                        bromide = bromide.append(bromide_boiler)
                        heat = heat.append(heat_boiler)
                        sulfur = sulfur.append(sulfur_boiler)
                coal = pd.Series(coal)
                selenium = pd.Series(selenium)
                arsenic = pd.Series(arsenic)
                lead = pd.Series(lead)
                mercury = pd.Series(mercury)
                chloride = pd.Series(chloride)
                boron = pd.Series(boron)
                bromide = pd.Series(bromide)
                heat = pd.Series(heat)
                sulfur = pd.Series(sulfur)
                j += 1
            boiler_fuel_copy['Coal'] = coal.values
            boiler_fuel_copy['Share_Selenium'] = selenium.values
            boiler_fuel_copy['Share_Arsenic'] = arsenic.values
            boiler_fuel_copy['Share_Lead'] = lead.values
            boiler_fuel_copy['Share_Mercury'] = mercury.values
            boiler_fuel_copy['Share_Chloride'] = chloride.values
            boiler_fuel_copy['Share_Boron'] = boron.values
            boiler_fuel_copy['Share_Bromide'] = bromide.values
            boiler_fuel_copy['Share_Heat'] = heat.values
            boiler_fuel_copy['Share_Sulfur'] = sulfur.values

            if boiler_fuel_share.empty:
                boiler_fuel_share = boiler_fuel_copy
            else:
                boiler_fuel_share = boiler_fuel_share.append(boiler_fuel_copy)
            i += 1

    return boiler_fuel_share

def stochastic_trace_elements_in_boiler(boiler_fuel, trace_elements, rank_summary, trials):
    import numpy as np
    import pandas as pd
    from statistical_functions import concentration_from_mle_normal_distribution, heat_from_mle_normal_distribution

    # Pandas throws up a warning when writing onto a copy of a dataframe instead of the original dataframe.  That is
    # intentional and so I silence the pandas warning about this.  For more on this error, see this stackoverflow post.
    # https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    pd.options.mode.chained_assignment = None

    unique_plants = boiler_fuel.Plant_ID.unique()

    print(unique_plants)

    i = 0
    while i < len(unique_plants):
        boiler_fuel_copy = boiler_fuel[boiler_fuel.Plant_ID == unique_plants[i]]
        trace_elements_copy = trace_elements[trace_elements.Plant_ID == unique_plants[i]]
        print(type(boiler_fuel_copy['Coal_Consumption']))
        if type(boiler_fuel_copy['Coal_Consumption']) == str:
            total_coals = 0
        else:
            total_coals = boiler_fuel_copy['Coal_Consumption'].sum()
        if len(trace_elements_copy.Plant_ID) == 1:
            selenium_concentration = trace_elements_copy.iloc[0][0:int(trials)]
            arsenic_concentration = trace_elements_copy.iloc[0][int(trials):2 * int(trials)]
            lead_concentration = trace_elements_copy.iloc[0][2 * int(trials):3 * int(trials)]
            mercury_concentration= trace_elements_copy.iloc[0][3 * int(trials):4 * int(trials)]
            chloride_concentration = trace_elements_copy.iloc[0][4 * int(trials):5 * int(trials)]
            boron_concentration = trace_elements_copy.iloc[0][5 * int(trials):6 * int(trials)]
            bromide_concentration = trace_elements_copy.iloc[0][6 * int(trials):7 * int(trials)]
            heat_concentration = trace_elements_copy.iloc[0][7 * int(trials):8 * int(trials)]
            sulfur_concentration = trace_elements_copy.iloc[0][8*int(trials):9 * int(trials)]
        else:
            if boiler_fuel_copy.Fuel.iloc[0] == 'BIT':
                rank_summary_copy = rank_summary[rank_summary.Rank == 'BITUMINOUS']
            elif boiler_fuel_copy.Fuel.iloc[0] == 'SUB':
                rank_summary_copy = rank_summary[rank_summary.Rank == 'SUBBITUMINOUS']
            elif boiler_fuel_copy.Fuel.iloc[0] == 'LIG':
                rank_summary_copy = rank_summary[rank_summary.Rank == 'LIGNITE']
            elif boiler_fuel_copy.Fuel.iloc[0] == 'RC':
                rank_summary_copy = rank_summary[rank_summary.Rank == 'BITUMINOUS']
            else:
                rank_summary_copy = rank_summary[rank_summary.Rank == boiler_fuel_copy.Fuel.iloc[0]]
            selenium_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_Se.iloc[0]),
                                                                                float(rank_summary_copy.Sigma_Se.iloc[0]),
                                                                                trials)
            arsenic_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_As.iloc[0]),
                                                                               float(rank_summary_copy.Sigma_As.iloc[0]),
                                                                               trials)
            lead_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_Pb.iloc[0]),
                                                                            float(rank_summary_copy.Sigma_Pb.iloc[0]),
                                                                            trials)
            mercury_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_Hg.iloc[0]),
                                                                               float(rank_summary_copy.Sigma_Hg.iloc[0]),
                                                                               trials)
            chloride_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_Cl.iloc[0]),
                                                                                float(rank_summary_copy.Sigma_Cl.iloc[0]),
                                                                                trials)
            boron_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_B.iloc[0]),
                                                                             float(rank_summary_copy.Sigma_B.iloc[0]),
                                                                             trials)
            bromide_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_Br.iloc[0]),
                                                                               float(rank_summary_copy.Sigma_Br.iloc[0]),
                                                                               trials)
            heat_concentration = heat_from_mle_normal_distribution(float(rank_summary_copy.Mean_Heat.iloc[0]),
                                                                   float(rank_summary_copy.Sigma_Heat.iloc[0]),
                                                                   trials)
            sulfur_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_S.iloc[0]),
                                                                   float(rank_summary_copy.Sigma_S.iloc[0]),
                                                                   trials)
        coal = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        selenium = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        arsenic = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        lead = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        mercury = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        chloride = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        boron = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        bromide = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        heat = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        sulfur = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))

        j = 0
        while j < len(boiler_fuel_copy.Coal_Consumption):
            if total_coals > 0:
                coal_burned = boiler_fuel_copy.Coal_Consumption.iloc[j]
                selenium_boiler = np.multiply((coal_burned * 9.07185e-4), selenium_concentration) #in kg/yr
                arsenic_boiler = np.multiply((coal_burned * 9.07185e-4), arsenic_concentration) #in kg/yr
                lead_boiler = np.multiply((coal_burned * 9.07185e-4), lead_concentration) #in kg/yr
                mercury_boiler = np.multiply((coal_burned * 9.07185e-4), mercury_concentration) #in kg/yr
                chloride_boiler = np.multiply((coal_burned * 9.07185e-4), chloride_concentration) #in kg/yr
                boron_boiler = np.multiply((coal_burned * 9.07185e-4), boron_concentration) #in kg/yr
                if type(bromide_concentration) == list:
                    if bromide_concentration == []: bromide_boiler = list(np.zeros(trials))
                    else: bromide_boiler = np.multiply((coal_burned * 9.07185e-4), bromide_concentration) #in kg/yr
                else:
                    if bromide_concentration.hasnans:
                        bromide_boiler = list(np.zeros(trials))
                    else: bromide_boiler = np.multiply((coal_burned * 9.07185e-4), bromide_concentration) #in kg/yr
                bromide_boiler = np.multiply((coal_burned * 9.07185e-4), bromide_concentration) #in kg/yr
                heat_boiler = np.multiply((coal_burned * 2), heat_concentration) #in MBtu/yr
                sulfur_boiler = np.multiply((coal_burned * 9.07185e2), sulfur_concentration) #in kg/yr
            else:
                coal_burned = 0
                selenium_boiler = list(np.zeros(trials))
                arsenic_boiler = list(np.zeros(trials))
                lead_boiler = list(np.zeros(trials))
                mercury_boiler = list(np.zeros(trials))
                chloride_boiler = list(np.zeros(trials))
                boron_boiler = list(np.zeros(trials))
                bromide_boiler = list(np.zeros(trials))
                heat_boiler = list(np.zeros(trials))
                sulfur_boiler = list(np.zeros(trials))
            coal[j] = coal_burned
            selenium[j] = selenium_boiler
            arsenic[j] = arsenic_boiler
            lead[j] = lead_boiler
            mercury[j] = mercury_boiler
            chloride[j] = chloride_boiler
            boron[j] = boron_boiler
            bromide[j] = bromide_boiler
            heat[j] = heat_boiler
            sulfur[j] = sulfur_boiler
            j += 1

        boiler_fuel_copy['Coal'] = coal.values
        boiler_fuel_copy['Selenium_Inputs'] = selenium.values
        boiler_fuel_copy['Arsenic_Inputs'] = arsenic.values
        boiler_fuel_copy['Lead_Inputs'] = lead.values
        boiler_fuel_copy['Mercury_Inputs'] = mercury.values
        boiler_fuel_copy['Chloride_Inputs'] = chloride.values
        boiler_fuel_copy['Boron_Inputs'] = boron.values
        boiler_fuel_copy['Bromide_Inputs'] = bromide.values
        boiler_fuel_copy['Heat_Inputs'] = heat.values
        boiler_fuel_copy['Sulfur_Inputs'] = sulfur.values

        if i == 0:
            boiler_fuel_share = boiler_fuel_copy
        else:
            boiler_fuel_share = boiler_fuel_share.append(boiler_fuel_copy)
        i += 1

    return boiler_fuel_share


def stochastic_trace_elements_in_boiler_refined_coal(boiler_fuel, trace_elements, rank_summary, trials):
    import numpy as np
    import pandas as pd
    from statistical_functions import concentration_from_mle_normal_distribution, heat_from_mle_normal_distribution

    # Pandas throws up a warning when writing onto a copy of a dataframe instead of the original dataframe.  That is
    # intentional and so I silence the pandas warning about this.  For more on this error, see this stackoverflow post.
    # https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    pd.options.mode.chained_assignment = None

    unique_plants = boiler_fuel.Plant_ID.unique()

    i = 0
    while i < len(unique_plants):
        boiler_fuel_copy = boiler_fuel[boiler_fuel.Plant_ID == unique_plants[i]]
        trace_elements_copy = trace_elements[trace_elements.Plant_ID == unique_plants[i]]
        total_coals = boiler_fuel_copy['Coal_Consumption'].sum()
        if len(trace_elements_copy.Plant_ID) == 1:
            selenium_concentration = trace_elements_copy.iloc[0][0:int(trials)]
            arsenic_concentration = trace_elements_copy.iloc[0][int(trials):2 * int(trials)]
            lead_concentration = trace_elements_copy.iloc[0][2 * int(trials):3 * int(trials)]
            mercury_concentration= trace_elements_copy.iloc[0][3 * int(trials):4 * int(trials)]
            chloride_concentration = trace_elements_copy.iloc[0][4 * int(trials):5 * int(trials)]
            boron_concentration = trace_elements_copy.iloc[0][5 * int(trials):6 * int(trials)]
            if boiler_fuel_copy.Fuel.iloc[0] == 'RC':
                bromide_concentration = trace_elements_copy.iloc[0][6 * int(trials):7 * int(trials)] + 100
            else:
                bromide_concentration = trace_elements_copy.iloc[0][6 * int(trials):7 * int(trials)]
            heat_concentration = trace_elements_copy.iloc[0][7 * int(trials):8 * int(trials)]
            sulfur_concentration = trace_elements_copy.iloc[0][8*int(trials):9 * int(trials)]
        else:
            if boiler_fuel_copy.Fuel.iloc[0] == 'BIT':
                rank_summary_copy = rank_summary[rank_summary.Rank == 'BITUMINOUS']
            elif boiler_fuel_copy.Fuel.iloc[0] == 'SUB':
                rank_summary_copy = rank_summary[rank_summary.Rank == 'SUBBITUMINOUS']
            elif boiler_fuel_copy.Fuel.iloc[0] == 'LIG':
                rank_summary_copy = rank_summary[rank_summary.Rank == 'LIGNITE']
            else:
                rank_summary_copy = rank_summary[rank_summary.Rank == boiler_fuel_copy.Fuel.iloc[0]]
            selenium_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_Se.iloc[0]),
                                                                                float(rank_summary_copy.Sigma_Se.iloc[0]),
                                                                                trials)
            arsenic_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_As.iloc[0]),
                                                                               float(rank_summary_copy.Sigma_As.iloc[0]),
                                                                               trials)
            lead_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_Pb.iloc[0]),
                                                                            float(rank_summary_copy.Sigma_Pb.iloc[0]),
                                                                            trials)
            mercury_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_Hg.iloc[0]),
                                                                               float(rank_summary_copy.Sigma_Hg.iloc[0]),
                                                                               trials)
            chloride_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_Cl.iloc[0]),
                                                                                float(rank_summary_copy.Sigma_Cl.iloc[0]),
                                                                                trials)
            boron_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_B.iloc[0]),
                                                                             float(rank_summary_copy.Sigma_B.iloc[0]),
                                                                             trials)
            if boiler_fuel_copy.Fuel.iloc[0] == 'RC':
                bromide_concentration = 100 + concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_Br.iloc[0]),
                                                                                         float(rank_summary_copy.Sigma_Br.iloc[0]),
                                                                                         trials)
            else:
                bromide_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_Br.iloc[0]),
                                                                                         float(rank_summary_copy.Sigma_Br.iloc[0]),
                                                                                         trials)
            heat_concentration = heat_from_mle_normal_distribution(float(rank_summary_copy.Mean_Heat.iloc[0]),
                                                                   float(rank_summary_copy.Sigma_Heat.iloc[0]),
                                                                   trials)
            sulfur_concentration = concentration_from_mle_normal_distribution(float(rank_summary_copy.Mean_S.iloc[0]),
                                                                   float(rank_summary_copy.Sigma_S.iloc[0]),
                                                                   trials)
        coal = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        selenium = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        arsenic = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        lead = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        mercury = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        chloride = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        boron = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        bromide = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        heat = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))
        sulfur = pd.Series(np.zeros(len(boiler_fuel_copy.Coal_Consumption), dtype=object))

        j = 0
        while j < len(boiler_fuel_copy.Coal_Consumption):
            if total_coals > 0:
                coal_burned = boiler_fuel_copy.Coal_Consumption.iloc[j]
                selenium_boiler = np.multiply((coal_burned * 9.07185e-4), selenium_concentration) #in kg/yr
                arsenic_boiler = np.multiply((coal_burned * 9.07185e-4), arsenic_concentration) #in kg/yr
                lead_boiler = np.multiply((coal_burned * 9.07185e-4), lead_concentration) #in kg/yr
                mercury_boiler = np.multiply((coal_burned * 9.07185e-4), mercury_concentration) #in kg/yr
                chloride_boiler = np.multiply((coal_burned * 9.07185e-4), chloride_concentration) #in kg/yr
                boron_boiler = np.multiply((coal_burned * 9.07185e-4), boron_concentration) #in kg/yr
                if type(bromide_concentration) == list:
                    if bromide_concentration == []: bromide_boiler = list(np.zeros(trials))
                    else: bromide_boiler = np.multiply((coal_burned * 9.07185e-4), bromide_concentration) #in kg/yr
                else:
                    if bromide_concentration.hasnans:
                        bromide_boiler = list(np.zeros(trials))
                    else: bromide_boiler = np.multiply((coal_burned * 9.07185e-4), bromide_concentration) #in kg/yr
                bromide_boiler = np.multiply((coal_burned * 9.07185e-4), bromide_concentration) #in kg/yr
                heat_boiler = np.multiply((coal_burned * 2), heat_concentration) #in MBtu/yr
                sulfur_boiler = np.multiply((coal_burned * 9.07185e2), sulfur_concentration) #in kg/yr
            else:
                coal_burned = 0
                selenium_boiler = list(np.zeros(trials))
                arsenic_boiler = list(np.zeros(trials))
                lead_boiler = list(np.zeros(trials))
                mercury_boiler = list(np.zeros(trials))
                chloride_boiler = list(np.zeros(trials))
                boron_boiler = list(np.zeros(trials))
                bromide_boiler = list(np.zeros(trials))
                heat_boiler = list(np.zeros(trials))
                sulfur_boiler = list(np.zeros(trials))
            coal[j] = coal_burned
            selenium[j] = selenium_boiler
            arsenic[j] = arsenic_boiler
            lead[j] = lead_boiler
            mercury[j] = mercury_boiler
            chloride[j] = chloride_boiler
            boron[j] = boron_boiler
            bromide[j] = bromide_boiler
            heat[j] = heat_boiler
            sulfur[j] = sulfur_boiler
            j += 1

        boiler_fuel_copy['Coal'] = coal.values
        boiler_fuel_copy['Selenium_Inputs'] = selenium.values
        boiler_fuel_copy['Arsenic_Inputs'] = arsenic.values
        boiler_fuel_copy['Lead_Inputs'] = lead.values
        boiler_fuel_copy['Mercury_Inputs'] = mercury.values
        boiler_fuel_copy['Chloride_Inputs'] = chloride.values
        boiler_fuel_copy['Boron_Inputs'] = boron.values
        boiler_fuel_copy['Bromide_Inputs'] = bromide.values
        boiler_fuel_copy['Heat_Inputs'] = heat.values
        boiler_fuel_copy['Sulfur_Inputs'] = sulfur.values

        if i == 0:
            boiler_fuel_share = boiler_fuel_copy
        else:
            boiler_fuel_share = boiler_fuel_share.append(boiler_fuel_copy)
        i += 1

    return boiler_fuel_share
