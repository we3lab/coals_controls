# Import standard python libraries.
import pandas as pd
import numpy as np
import pathlib
import warnings
import sys

# Import the functions used throughout this project from the function dictionary library file
fileDir = pathlib.Path(__file__).parents[2]
code_library_folder = fileDir / 'Code' / 'function_dictionary_library'
sys.path.append(str(code_library_folder))
from coal_data_processing_functions import state_abbreviations, generic_coal_rank, lower_case_data_keys
from statistical_functions import ecdf, weighted_ecdf
from statistics import mean

def weighted_coal_ecdf(coal):

    warnings

    # Read in (1) COALQUAL Data (2) and the amount of coal mining done in each county.  We use skipfooter to not read in the
    # search criteria rows.
    coalqual_filename = fileDir / 'Data' / 'COALQUAL Data' / 'CQ_upper_level.csv'
    COALQUAL = pd.read_csv(coalqual_filename, header=0,
                           names=['Sample_ID', 'State', 'County', 'Province', 'Region', 'Field', 'Formation', 'Bed',
                                  'Apparent_Rank', 'Sulfur', 'Heat', 'Arsenic', 'Boron', 'Bromine', 'Chlorides',
                                  'Mercury',
                                  'Lead', 'Selenium'], usecols=[0, 1, 2, 5, 6, 7, 9, 11, 28, 84, 87, 147, 151, 159, 165,
                                                                191, 219, 239])
    mining_volume_filename = fileDir / 'Intermediate' / 'Coal Mining By Counties.csv'
    Mining_Volume = pd.read_csv(mining_volume_filename, header=0, names=['Coal_Sales', 'FIPS_Code_State',
                                                                         'County_Name_State_Normal_Capitalization'],
                                usecols=[1, 2, 8])

    # Drop COALQUAL anthracite and samples with blank apparent rank.
    COALQUAL = COALQUAL[COALQUAL.Apparent_Rank != 'Anthracite']
    COALQUAL = COALQUAL[COALQUAL.Apparent_Rank != 'Semianthracite']
    COALQUAL = COALQUAL[COALQUAL.Apparent_Rank != 'Rock']
    COALQUAL = COALQUAL.dropna(subset=['Apparent_Rank'])

    # Classify apparent ranks into broad categories.
    COALQUAL['Rank'] = generic_coal_rank(COALQUAL.Apparent_Rank)

    # Process the columns that will serve as keys for the data merging.
    COALQUAL['State_Abbreviation'] = state_abbreviations(COALQUAL.State)
    County_Name_State_Normal_Capitalization = COALQUAL['County'] + ' County, ' + COALQUAL['State_Abbreviation']
    COALQUAL['County_Name_State'] = lower_case_data_keys(County_Name_State_Normal_Capitalization)
    Mining_Volume['County_Name_State'] = lower_case_data_keys(Mining_Volume['County_Name_State_Normal_Capitalization'])

    # mask = pd.Series(np.isfinite(COALQUAL['Chlorides']))
    COALQUAL_all_samples_Cl = COALQUAL.loc[pd.Series(np.isfinite(COALQUAL['Chlorides']))]
    COALQUAL_all_samples_Br = COALQUAL.loc[pd.Series(np.isfinite(COALQUAL['Bromine']))]

    COALQUAL_all_samples_Cl = COALQUAL_all_samples_Cl.groupby(['County_Name_State']).mean()
    COALQUAL_all_samples_Cl['County_Name_State'] = COALQUAL_all_samples_Cl.index
    COALQUAL_all_samples_Cl = pd.merge(COALQUAL_all_samples_Cl, Mining_Volume, on='County_Name_State')

    COALQUAL_all_samples_Br = COALQUAL_all_samples_Br.groupby(['County_Name_State']).mean()
    COALQUAL_all_samples_Br['County_Name_State'] = COALQUAL_all_samples_Br.index
    COALQUAL_all_samples_Br = pd.merge(COALQUAL_all_samples_Br, Mining_Volume, on='County_Name_State')

    qe_Cl_All, pe_Cl_All = weighted_ecdf(COALQUAL_all_samples_Cl['Chlorides'], COALQUAL_all_samples_Cl['Coal_Sales'])
    qe_Br_All, pe_Br_All = weighted_ecdf(COALQUAL_all_samples_Br['Bromine'], COALQUAL_all_samples_Br['Coal_Sales'])

    # For Appalachian Low Sulfur Coal
    if coal == 'Appalachian Low Sulfur':
        COALQUAL = COALQUAL[
            (COALQUAL['Region'] == 'SOUTHERN APPALACHIAN') | (COALQUAL['Region'] == 'CENTRAL APPALACHIAN')
            | (COALQUAL['Region'] == 'NORTHERN APPALACHIAN')]
        # USGS Circular 891 defines "low sulfur coal" as less than 1% total sulfur (https://pubs.usgs.gov/circ/c891/glossary.htm).
        # This is identical to the standard used by the EIA.
        COALQUAL = COALQUAL[COALQUAL['Sulfur'] < 1]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        #Chlorides = [x for x in COALQUAL['Chlorides'] if x != '']
        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        bromine = COALQUAL[np.isfinite(COALQUAL['Bromine'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Cl, pe_Cl = weighted_ecdf(chlorine['Chlorides'], chlorine['Coal_Sales'])
        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Br, pe_Br = weighted_ecdf(bromine['Bromine'], bromine['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        gross_heat_rate = 8188  # Btu/kWh
        FGD_water_treatment = 2.14e-4  # m^3/kWh

    # For Appalachian Medium Sulfur Coal
    elif coal == 'Appalachian Med Sulfur':
        COALQUAL = COALQUAL[
            (COALQUAL['Region'] == 'SOUTHERN APPALACHIAN') | (COALQUAL['Region'] == 'CENTRAL APPALACHIAN') | (
                        COALQUAL['Region'] == 'NORTHERN APPALACHIAN')]
        COALQUAL = COALQUAL[(COALQUAL['Sulfur'] > 1) & (COALQUAL['Sulfur'] < 3)]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        bromine = COALQUAL[np.isfinite(COALQUAL['Bromine'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Cl, pe_Cl = weighted_ecdf(chlorine['Chlorides'], chlorine['Coal_Sales'])
        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Br, pe_Br = weighted_ecdf(bromine['Bromine'], bromine['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        gross_heat_rate = 8210  # Btu/kWh
        FGD_water_treatment = 2.20e-4  # m^3/kWh

    # For Beulah-Zap Bed Coal
    elif coal == 'Beulah-Zap':
        COALQUAL = COALQUAL[(COALQUAL['Bed'] == 'BEULAH-ZAP')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Cl, pe_Cl = weighted_ecdf(chlorine['Chlorides'], chlorine['Coal_Sales'])
        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        qe_Br = qe_Br_All
        pe_Br = pe_Br_All
        gross_heat_rate = 8680  # Btu/kWh
        FGD_water_treatment = 2.36e-4  # m^3/kWh

    # For Illinois #6 Coal
    elif coal == 'Illinois #6':
        COALQUAL = COALQUAL[(COALQUAL['Bed'] == 'HERRIN NO 6')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        bromine = COALQUAL[np.isfinite(COALQUAL['Bromine'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Br, pe_Br = weighted_ecdf(bromine['Bromine'], bromine['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        qe_Cl = qe_Cl_All
        pe_Cl = pe_Cl_All
        gross_heat_rate = (8279 + 8319) / 2  # Btu/kWh
        FGD_water_treatment = 2.22e-4  # m^3/kWh

    # For ND Lignite Coal
    elif coal == 'ND Lignite':
        COALQUAL = COALQUAL[(COALQUAL['State'] == 'North Dakota') & (COALQUAL['Rank'] == 'LIGNITE')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        bromine = COALQUAL[np.isfinite(COALQUAL['Bromine'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Cl, pe_Cl = weighted_ecdf(chlorine['Chlorides'], chlorine['Coal_Sales'])
        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        qe_Br = qe_Br_All
        pe_Br = pe_Br_All
        gross_heat_rate = 8865  # Btu/kWh
        FGD_water_treatment = 2.39e-4  # m^3/kWh

    # For Pocahontas #3 Seam Coal
    elif coal == "Pocahontas #3":
        COALQUAL = COALQUAL[(COALQUAL['Bed'] == 'POCAHONTAS NO 3')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        bromine = COALQUAL[np.isfinite(COALQUAL['Bromine'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Cl, pe_Cl = weighted_ecdf(chlorine['Chlorides'], chlorine['Coal_Sales'])
        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Br, pe_Br = weighted_ecdf(bromine['Bromine'], bromine['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        gross_heat_rate = 8099  # Btu/kWh
        FGD_water_treatment = 2.19e-4  # m^3/kWh

    # For Upper Freeport Coal
    elif coal == 'Upper Freeport':
        COALQUAL = COALQUAL[(COALQUAL['Bed'] == 'UPPER FREEPORT')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        bromine = COALQUAL[np.isfinite(COALQUAL['Bromine'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Cl, pe_Cl = weighted_ecdf(chlorine['Chlorides'], chlorine['Coal_Sales'])
        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Br, pe_Br = weighted_ecdf(bromine['Bromine'], bromine['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        gross_heat_rate = 8104  # Btu/kWh
        FGD_water_treatment = 2.11e-4  # m^3/kWh

    # For WPC Utah Coal
    elif coal == 'WPC Utah':
        COALQUAL = COALQUAL[(COALQUAL['Region'] == 'SOUTHWESTERN UTAH')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Cl, pe_Cl = weighted_ecdf(chlorine['Chlorides'], chlorine['Coal_Sales'])
        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        qe_Br = qe_Br_All
        pe_Br = pe_Br_All
        gross_heat_rate = 8347  # Btu/kWh
        FGD_water_treatment = 2.42e-4  # m^3/kWh

    # For Wyodak Coal
    elif coal == 'Wyodak':
        COALQUAL = COALQUAL[(COALQUAL['Bed'] == 'WYODAK')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Cl, pe_Cl = weighted_ecdf(chlorine['Chlorides'], chlorine['Coal_Sales'])
        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        qe_Br = qe_Br_All
        pe_Br = pe_Br_All
        gross_heat_rate = 8192  # Btu/kWh
        FGD_water_treatment = 1.66e-4  # m^3/kWh

    # For Wyodak-Anderson Coal
    elif coal == 'Wyodak Anderson':
        COALQUAL = COALQUAL[(COALQUAL['Bed'] == 'WYODAK-ANDERSON')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Cl, pe_Cl = weighted_ecdf(chlorine['Chlorides'], chlorine['Coal_Sales'])
        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        qe_Br = qe_Br_All
        pe_Br = pe_Br_All
        gross_heat_rate = 8585  # Btu/kWh
        FGD_water_treatment = 2.32e-4  # m^3/kWh

    # For Wyoming PRB Coal
    elif coal == 'Wyoming PRB':
        COALQUAL = COALQUAL[(COALQUAL['Region'] == 'POWDER RIVER') & (COALQUAL['State'] == 'Wyoming')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        bromine = COALQUAL[np.isfinite(COALQUAL['Bromine'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Cl, pe_Cl = weighted_ecdf(chlorine['Chlorides'], chlorine['Coal_Sales'])
        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Br, pe_Br = weighted_ecdf(bromine['Bromine'], bromine['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        gross_heat_rate = 8588  # Btu/kWh
        FGD_water_treatment = 2.28e-4  # m^3/kWh

    # For Bituminous Coal
    elif coal == 'Bituminous':
        COALQUAL = COALQUAL[(COALQUAL['Rank'] == 'BITUMINOUS')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        bromine = COALQUAL[np.isfinite(COALQUAL['Bromine'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Cl, pe_Cl = weighted_ecdf(chlorine['Chlorides'], chlorine['Coal_Sales'])
        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Br, pe_Br = weighted_ecdf(bromine['Bromine'], bromine['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        gross_heat_rate = 8188  # Btu/kWh
        FGD_water_treatment = 2.14e-4  # m^3/kWh

    # For Subbituminous Coal
    elif coal == 'Subbituminous':
        COALQUAL = COALQUAL[(COALQUAL['Rank'] == 'SUBBITUMINOUS')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        bromine = COALQUAL[np.isfinite(COALQUAL['Bromine'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Cl, pe_Cl = weighted_ecdf(chlorine['Chlorides'], chlorine['Coal_Sales'])
        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Br, pe_Br = weighted_ecdf(bromine['Bromine'], bromine['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        gross_heat_rate = 8588  # Btu/kWh
        FGD_water_treatment = 2.28e-4  # m^3/kWh

    # For Lignite Coal
    elif coal == 'Lignite':
        COALQUAL = COALQUAL[(COALQUAL['Rank'] == 'LIGNITE')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        selenium = COALQUAL[np.isfinite(COALQUAL['Selenium'])]
        boron = COALQUAL[np.isfinite(COALQUAL['Boron'])]
        lead = COALQUAL[np.isfinite(COALQUAL['Lead'])]
        arsenic = COALQUAL[np.isfinite(COALQUAL['Arsenic'])]
        mercury = COALQUAL[np.isfinite(COALQUAL['Mercury'])]
        heat = COALQUAL[np.isfinite(COALQUAL['Heat'])]
        sulfur = COALQUAL[np.isfinite(COALQUAL['Sulfur'])]

        qe_Cl, pe_Cl = weighted_ecdf(chlorine['Chlorides'], chlorine['Coal_Sales'])
        qe_Se, pe_Se = weighted_ecdf(selenium['Selenium'], selenium['Coal_Sales'])
        qe_B, pe_B = weighted_ecdf(boron['Boron'], boron['Coal_Sales'])
        qe_Pb, pe_Pb = weighted_ecdf(lead['Lead'], lead['Coal_Sales'])
        qe_As, pe_As = weighted_ecdf(arsenic['Arsenic'], arsenic['Coal_Sales'])
        qe_Hg, pe_Hg = weighted_ecdf(mercury['Mercury'], mercury['Coal_Sales'])
        qe_Heat, pe_Heat = weighted_ecdf(heat['Heat'], heat['Coal_Sales'])
        qe_Sulfur, pe_Sulfur = weighted_ecdf(sulfur['Sulfur'], sulfur['Coal_Sales'])
        qe_Br = qe_Br_All
        pe_Br = pe_Br_All
        gross_heat_rate = 8865  # Btu/kWh
        FGD_water_treatment = 2.39e-4  # m^3/kWh

    # For Quality Guidelines for Energy System Studies - Illinois #6 coal (The bituminous coal used for the 550 MW
    # Bituminous Baseline)
    elif coal == 'QGESS Bituminous':
        COALQUAL = COALQUAL[(COALQUAL['Bed'] == 'HERRIN NO 6')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        bromine = COALQUAL[np.isfinite(COALQUAL['Bromine'])]

        qe_Cl = [1671, 1671]
        pe_Cl = [0, 1]
        qe_Se = [1.9, 1.9]
        pe_Se = [0, 1]
        qe_B = [90, 90]
        pe_B = [0, 1]
        qe_Br = [np.average(bromine['Bromine'], weights=bromine['Coal_Sales']),
                 np.average(bromine['Bromine'], weights=bromine['Coal_Sales'])]
        pe_Br = [0, 1]
        qe_Pb = [24, 24]
        pe_Pb = [0, 1]
        qe_As = [7.5, 7.5]
        pe_As = [0, 1]
        qe_Hg = [0.09, 0.09]
        pe_Hg = [0, 1]
        qe_Heat = [11666, 11666]
        pe_Heat = [0, 1]
        qe_Sulfur = [2.51, 2.51]
        pe_Sulfur = [0, 1]
        gross_heat_rate = (8279+8319)/2 #Btu/kWh
        FGD_water_treatment = 2.22e-4 #m^3/kWh

    # For Quality Guidelines for Energy System Studies - Illinois #6 coal (The bituminous coal used for the 550 MW
    # Bituminous Baseline)
    elif coal == 'QGESS Subbituminous':
        COALQUAL = COALQUAL[(COALQUAL['Region'] == 'POWDER RIVER') & (COALQUAL['State'] == 'Wyoming')]

        COALQUAL = COALQUAL.groupby(['County_Name_State']).mean()
        COALQUAL['County_Name_State'] = COALQUAL.index
        COALQUAL = pd.merge(COALQUAL, Mining_Volume, on='County_Name_State')

        chlorine = COALQUAL[np.isfinite(COALQUAL['Chlorides'])]
        bromine = COALQUAL[np.isfinite(COALQUAL['Bromine'])]

        qe_Cl = [np.average(chlorine['Chlorides'], weights=chlorine['Coal_Sales']),
                 np.average(chlorine['Chlorides'], weights=chlorine['Coal_Sales'])]
        pe_Cl = [0, 1]
        qe_Se = [0.3, 0.3]
        pe_Se = [0, 1]
        qe_B = [43, 43]
        pe_B = [0, 1]
        qe_Br = [np.average(bromine['Bromine'], weights=bromine['Coal_Sales']),
                 np.average(bromine['Bromine'], weights=bromine['Coal_Sales'])]
        pe_Br = [0, 1]
        qe_Pb = [5, 5]
        pe_Pb = [0, 1]
        qe_As = [1.5, 1.5]
        pe_As = [0, 1]
        qe_Hg = [0.1, 0.1]
        pe_Hg = [0, 1]
        qe_Heat = [8800, 8800]
        pe_Heat = [0, 1]
        qe_Sulfur = [0.22, 0.22]
        pe_Sulfur = [0, 1]
        gross_heat_rate = (8279+8319)/2 #Btu/kWh
        FGD_water_treatment = 2.22e-4 #m^3/kWh

    return qe_Cl, pe_Cl, qe_Se, pe_Se, qe_B, pe_B, qe_Br, pe_Br, qe_Pb, pe_Pb, qe_As, pe_As, qe_Hg, pe_Hg, qe_Heat, \
           pe_Heat, qe_Sulfur, pe_Sulfur, gross_heat_rate, FGD_water_treatment


def coal_ecdf(coal):

    # Read in Coal Qual Data on the Samples.

    # For frozen code:
    fileDir = pathlib.Path(__file__).parents[1]
    samples_filename = fileDir / 'newData' / 'COALQUAL Data' / 'Coal Qual Sample Data.csv'
    trace_element_filename = fileDir / 'newData' / 'COALQUAL Data' / 'Coal Qual Trace Element Data.csv'
    ultimate_analysis_filename = fileDir / 'newData' / 'COALQUAL Data' / 'Coal Qual Ultimate Analysis Data.csv'

    # For original python code
    # fileDir = pathlib.Path(__file__).parents[2]
    # code_library_folder = fileDir / 'Code' / 'function_dictionary_library'
    # sys.path.append(str(code_library_folder))
    #
    # fileDir = pathlib.Path(__file__).parents[2]
    # samples_filename = fileDir / 'Data' / 'COALQUAL Data' / 'Coal Qual Sample Data.csv'
    # trace_element_filename = fileDir / 'Data' / 'COALQUAL Data' / 'Coal Qual Trace Element Data.csv'
    # ultimate_analysis_filename = fileDir / 'Data' / 'COALQUAL Data' / 'Coal Qual Ultimate Analysis Data.csv'



    warnings



    # Note that we use skipfooter to not read in the search criteria column.
    Samples = pd.read_csv(samples_filename, header=1,
                          names=['Sample_ID', 'State', 'County', 'Region', 'Field', 'Formation', 'Bed', 'Rank'],
                          usecols=[0, 1, 2, 6, 7, 9, 11, 27], engine='python', skipfooter=2)
    Trace_Element = pd.read_csv(trace_element_filename, header=1, names=['Sample_ID', 'Arsenic', 'Boron', 'Bromine',
                                                                         'Chlorides', 'Mercury', 'Lead', 'Selenium'],
                                usecols=[0, 23, 27, 35, 41, 67, 95, 115], engine='python', skipfooter=2)
    Ultimate_Analysis = pd.read_csv(ultimate_analysis_filename, header=1, names=['Sample_ID', 'Sulfur', 'Heat'],
                                    usecols=[0, 18, 21], engine='python', skipfooter=2)
    # Merge data together
    COALQUAL = pd.merge(Samples, Trace_Element, on='Sample_ID')
    COALQUAL = pd.merge(COALQUAL, Ultimate_Analysis, on='Sample_ID')

    qe_Cl_All, pe_Cl_All = ecdf(COALQUAL['Chlorides'])
    qe_Br_All, pe_Br_All = ecdf(COALQUAL['Bromine'])

    #For Appalachian Low Sulfur Coal
    if coal == 'Appalachian Low Sulfur':
        COALQUAL = COALQUAL[(COALQUAL['Region'] == 'SOUTHERN APPALACHIAN') | (COALQUAL['Region'] == 'CENTRAL APPALACHIAN')
                            | (COALQUAL['Region'] == 'NORTHERN APPALACHIAN')]
        # USGS Circular 891 defines "low sulfur coal" as less than 1% total sulfur (https://pubs.usgs.gov/circ/c891/glossary.htm).
        # This is identical to the standard used by the EIA.
        COALQUAL = COALQUAL[COALQUAL['Sulfur'] < 1]
        Chlorides = [x for x in COALQUAL['Chlorides'] if x != '']
        qe_Cl, pe_Cl = ecdf(COALQUAL['Chlorides'])
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br, pe_Br = ecdf(COALQUAL['Bromine'])
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = 8188 #Btu/kWh
        FGD_water_treatment = 2.14e-4 #m^3/kWh

    # For Appalachian Medium Sulfur Coal
    elif coal == 'Appalachian Med Sulfur':
        COALQUAL = COALQUAL[(COALQUAL['Region'] == 'SOUTHERN APPALACHIAN') | (COALQUAL['Region'] == 'CENTRAL APPALACHIAN') | (COALQUAL['Region'] == 'NORTHERN APPALACHIAN')]
        COALQUAL = COALQUAL[(COALQUAL['Sulfur'] > 1) & (COALQUAL['Sulfur'] < 3)]
        qe_Cl, pe_Cl = ecdf(COALQUAL['Chlorides'])
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br, pe_Br = ecdf(COALQUAL['Bromine'])
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = 8210 #Btu/kWh
        FGD_water_treatment = 2.20e-4 #m^3/kWh

    # For Beulah-Zap Bed Coal
    elif coal == 'Beulah-Zap':
        COALQUAL = COALQUAL[(COALQUAL['Bed'] == 'BEULAH-ZAP')]
        qe_Cl, pe_Cl = ecdf(COALQUAL['Chlorides'])
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br = qe_Br_All
        pe_Br = pe_Br_All
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = 8680 #Btu/kWh
        FGD_water_treatment = 2.36e-4 #m^3/kWh

    # For Illinois #6 Coal
    elif coal == 'Illinois #6':
        COALQUAL = COALQUAL[(COALQUAL['Bed'] == 'HERRIN NO 6')]
        qe_Cl = qe_Cl_All
        pe_Cl = pe_Cl_All
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br, pe_Br = ecdf(COALQUAL['Bromine'])
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = (8279+8319)/2 #Btu/kWh
        FGD_water_treatment = 2.22e-4 #m^3/kWh

    # For ND Lignite Coal
    elif coal == 'ND Lignite':
        COALQUAL = COALQUAL[(COALQUAL['State'] == 'North Dakota') & (COALQUAL['Rank'] == 'LIGNITE')]
        qe_Cl, pe_Cl = ecdf(COALQUAL['Chlorides'])
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br = qe_Br_All
        pe_Br = pe_Br_All
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = 8865 #Btu/kWh
        FGD_water_treatment = 2.39e-4 #m^3/kWh

    # For Pocahontas #3 Seam Coal
    elif coal == "Pocahontas #3":
        COALQUAL = COALQUAL[(COALQUAL['Bed'] == 'POCAHONTAS NO 3')]
        qe_Cl, pe_Cl = ecdf(COALQUAL['Chlorides'])
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br, pe_Br = ecdf(COALQUAL['Bromine'])
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = 8099 #Btu/kWh
        FGD_water_treatment = 2.19e-4 #m^3/kWh

    # For Upper Freeport Coal
    elif coal == 'Upper Freeport':
        COALQUAL = COALQUAL[(COALQUAL['Bed'] == 'UPPER FREEPORT')]
        qe_Cl, pe_Cl = ecdf(COALQUAL['Chlorides'])
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br, pe_Br = ecdf(COALQUAL['Bromine'])
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = 8104 #Btu/kWh
        FGD_water_treatment = 2.11e-4 #m^3/kWh

    # For WPC Utah Coal
    elif coal == 'WPC Utah':
        COALQUAL = COALQUAL[(COALQUAL['Region'] == 'SOUTHWESTERN UTAH')]
        qe_Cl, pe_Cl = ecdf(COALQUAL['Chlorides'])
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br = qe_Br_All
        pe_Br = pe_Br_All
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = 8347 #Btu/kWh
        FGD_water_treatment = 2.42e-4 #m^3/kWh

    # For Wyodak Coal
    elif coal == 'Wyodak':
        COALQUAL = COALQUAL[(COALQUAL['Bed'] == 'WYODAK')]
        qe_Cl, pe_Cl = ecdf(COALQUAL['Chlorides'])
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br = qe_Br_All
        pe_Br = pe_Br_All
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = 8192 #Btu/kWh
        FGD_water_treatment = 1.66e-4 #m^3/kWh

    # For Wyodak-Anderson Coal
    elif coal == 'Wyodak Anderson':
        COALQUAL = COALQUAL[(COALQUAL['Bed'] == 'WYODAK-ANDERSON')]
        qe_Cl, pe_Cl = ecdf(COALQUAL['Chlorides'])
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br, pe_Br = ecdf(COALQUAL['Bromine'])
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = 8585 #Btu/kWh
        FGD_water_treatment = 2.32e-4 #m^3/kWh

    # For Wyoming PRB Coal
    elif coal == 'Wyoming PRB':
        COALQUAL = COALQUAL[(COALQUAL['Region'] == 'POWDER RIVER') & (COALQUAL['State'] == 'Wyoming')]
        qe_Cl, pe_Cl = ecdf(COALQUAL['Chlorides'])
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br, pe_Br = ecdf(COALQUAL['Bromine'])
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = 8588 #Btu/kWh
        FGD_water_treatment = 2.28e-4 #m^3/kWh

    # For Bituminous Coal
    elif coal == 'Bituminous':
        COALQUAL = COALQUAL[(COALQUAL['Rank'] == 'BITUMINOUS')]
        qe_Cl, pe_Cl = ecdf(COALQUAL['Chlorides'])
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br, pe_Br = ecdf(COALQUAL['Bromine'])
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = 8188 #Btu/kWh
        FGD_water_treatment = 2.14e-4 #m^3/kWh

    # For Subbituminous Coal
    elif coal == 'Subbituminous':
        COALQUAL = COALQUAL[(COALQUAL['Rank'] == 'SUBBITUMINOUS')]
        qe_Cl, pe_Cl = ecdf(COALQUAL['Chlorides'])
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br, pe_Br = ecdf(COALQUAL['Bromine'])
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = 8588 #Btu/kWh
        FGD_water_treatment = 2.28e-4 #m^3/kWh

    # For Lignite Coal
    elif coal == 'Lignite':
        COALQUAL = COALQUAL[(COALQUAL['Rank'] == 'LIGNITE')]
        qe_Cl, pe_Cl = ecdf(COALQUAL['Chlorides'])
        qe_Se, pe_Se = ecdf(COALQUAL['Selenium'])
        qe_B, pe_B = ecdf(COALQUAL['Boron'])
        qe_Br = qe_Br_All
        pe_Br = pe_Br_All
        qe_Pb, pe_Pb = ecdf(COALQUAL['Lead'])
        qe_As, pe_As = ecdf(COALQUAL['Arsenic'])
        qe_Hg, pe_Hg = ecdf(COALQUAL['Mercury'])
        qe_Heat, pe_Heat = ecdf(COALQUAL['Heat'])
        qe_Sulfur, pe_Sulfur = ecdf(COALQUAL['Sulfur'])
        gross_heat_rate = 8865 #Btu/kWh
        FGD_water_treatment = 2.39e-4 #m^3/kWh


    return qe_Cl, pe_Cl, qe_Se, pe_Se, qe_B, pe_B, qe_Br, pe_Br, qe_Pb, pe_Pb, qe_As, pe_As, qe_Hg, pe_Hg, qe_Heat, \
           pe_Heat, qe_Sulfur, pe_Sulfur, gross_heat_rate, FGD_water_treatment
