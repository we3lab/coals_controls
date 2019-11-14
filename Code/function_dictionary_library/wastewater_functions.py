import numpy as np

def wastewater_generation(electricity_generated, FGD_water_treatment):
    FGD_makeup_water = electricity_generated * FGD_water_treatment
    FGD_wastewater = FGD_makeup_water #Based on the NETL model plants ~50% of water is evaporated and 50% is treated and reused.

    return FGD_wastewater

def fgd_wastewater_concentration(mass, wastewater_proudction):
    concentration = (mass/1000)/wastewater_proudction

    return concentration

def fgd_wastewater_generation_for_cl_limits(cl_mass):
    min_wastewater_production = cl_mass/16
    max_wastewater_production = cl_mass/9.6
    med_wastewater_production = cl_mass/7.3

    return min_wastewater_production, max_wastewater_production, med_wastewater_production

def fgd_wastewater_generation_for_corrosion_limits(cl_mass):
    # FGD systems typically operate at chloride concenetrations of 8000 to 20000 mg/L in order to avoid corrosion,
    # with an additional factor of safety of 80%.  Additionally, we use a conversion factor of a 1000 to go from L to
    # cubic meters.
    min_concentration = 8000 * 0.8 * 1000
    max_concentration = 20000 * 0.8 * 1000
    concentration_limit = (max_concentration - min_concentration) * np.random.random(len(cl_mass),) + min_concentration
    fgd_wastewater = cl_mass/concentration_limit  # The units are in [m^3/hr]

    return fgd_wastewater

def fgd_wastewater_generation_for_low_corrosion_limits(cl_mass):
    # FGD systems typically operate at chloride concenetrations of 8000 to 20000 mg/L in order to avoid corrosion,
    # with an additional factor of safety of 80%.  Additionally, we use a conversion factor of a 1000 to go from L to
    # cubic meters.  This code focuses though on the low end of the spectrum, potentially better reflecting current
    # operating conditions where water constraints are less of an issue.
    min_concentration = 8000 * 0.8 * 1000
    max_concentration = 8000 * 1.0 * 1000
    concentration_limit = (max_concentration - min_concentration) * np.random.random(len(cl_mass),) + min_concentration
    fgd_wastewater = cl_mass/concentration_limit  # The units are in [m^3/hr]

    return fgd_wastewater

def fgd_wastewater_generation_for_high_corrosion_limits(cl_mass):
    # FGD systems typically operate at chloride concenetrations of 8000 to 20000 mg/L in order to avoid corrosion,
    # with an additional factor of safety of 80%.  Additionally, we use a conversion factor of a 1000 to go from L to
    # cubic meters.  This code focuses though on the high end of the spectrum, potentially better reflecting current
    # operating conditions where water constraints are less of an issue.
    min_concentration = 20000 * 0.8 * 1000
    max_concentration = 20000 * 1.0 * 1000
    concentration_limit = (max_concentration - min_concentration) * np.random.random(len(cl_mass),) + min_concentration
    fgd_wastewater = cl_mass/concentration_limit  # The units are in [m^3/hr]

    return fgd_wastewater

def wastewater_treatment_electricity_consumption(wastewater_volume, cp, mbr, bt, mvc, iex, alox, feox, zvi, crys):
    unit_process_electricity_consumption_dic = {'cp': [0.0085, 0.023],
                                                'mbr': [0.10, 1.5],
                                                'bt': [0.18, 0.42],
                                                'iex': [0.029, 0.029],
                                                'alox': [0.029, 0.029],
                                                'feox': [0.029, 0.029],
                                                'zvi': [0.029, 0.029],
                                                'mvc': [18, 26],
                                                'crys': [52, 66],
                                                'solids': [0.01, 0.02],
                                                'clar': [0.01, 0.01]}

    if cp == 1:
        cp_unit_consumption = np.random.uniform(unit_process_electricity_consumption_dic['cp'][0],
                                                unit_process_electricity_consumption_dic['cp'][1],
                                                len(wastewater_volume))
        solids_unit_consumption = np.random.uniform(unit_process_electricity_consumption_dic['solids'][0],
                                                unit_process_electricity_consumption_dic['solids'][1],
                                                len(wastewater_volume))
        clar_unit_consumption = np.random.uniform(unit_process_electricity_consumption_dic['clar'][0],
                                                unit_process_electricity_consumption_dic['clar'][1],
                                                len(wastewater_volume))
    else:
        cp_unit_consumption = np.zeros(len(wastewater_volume))
        solids_unit_consumption = np.zeros(len(wastewater_volume))
        clar_unit_consumption = np.zeros(len(wastewater_volume))

    if mbr == 1:
        mbr_unit_consumption = np.random.uniform(unit_process_electricity_consumption_dic['mbr'][0],
                                                unit_process_electricity_consumption_dic['mbr'][1],
                                                len(wastewater_volume))
    else:
        mbr_unit_consumption = np.zeros(len(wastewater_volume))

    if bt == 1:
        bt_unit_consumption = np.random.uniform(unit_process_electricity_consumption_dic['bt'][0],
                                                unit_process_electricity_consumption_dic['bt'][1],
                                                len(wastewater_volume))
    else:
        bt_unit_consumption = np.zeros(len(wastewater_volume))

    if iex == 1:
        iex_unit_consumption = np.random.uniform(unit_process_electricity_consumption_dic['iex'][0],
                                                 unit_process_electricity_consumption_dic['iex'][1],
                                                 len(wastewater_volume))
    else:
        iex_unit_consumption = np.zeros(len(wastewater_volume))

    if iex == 1:
        iex_unit_consumption = np.random.uniform(unit_process_electricity_consumption_dic['iex'][0],
                                                unit_process_electricity_consumption_dic['iex'][1],
                                                len(wastewater_volume))
    else:
        iex_unit_consumption = np.zeros(len(wastewater_volume))

    if alox == 1:
        alox_unit_consumption = np.random.uniform(unit_process_electricity_consumption_dic['alox'][0],
                                                unit_process_electricity_consumption_dic['alox'][1],
                                                len(wastewater_volume))
    else:
        alox_unit_consumption = np.zeros(len(wastewater_volume))

    if feox == 1:
        feox_unit_consumption = np.random.uniform(unit_process_electricity_consumption_dic['feox'][0],
                                                unit_process_electricity_consumption_dic['feox'][1],
                                                len(wastewater_volume))
    else:
        feox_unit_consumption = np.zeros(len(wastewater_volume))

    if zvi == 1:
        zvi_unit_consumption = np.random.uniform(unit_process_electricity_consumption_dic['zvi'][0],
                                                 unit_process_electricity_consumption_dic['zvi'][1],
                                                 len(wastewater_volume))
    else:
        zvi_unit_consumption = np.zeros(len(wastewater_volume))

    if mvc == 1:
        mvc_unit_consumption = np.random.uniform(unit_process_electricity_consumption_dic['mvc'][0],
                                                unit_process_electricity_consumption_dic['mvc'][1],
                                                len(wastewater_volume))
    else:
        mvc_unit_consumption = np.zeros(len(wastewater_volume))

    if crys == 1:
        crys_unit_consumption = np.random.uniform(unit_process_electricity_consumption_dic['crys'][0],
                                                unit_process_electricity_consumption_dic['crys'][1],
                                                len(wastewater_volume))
    else:
        crys_unit_consumption = np.zeros(len(wastewater_volume))

    total_unit_consumption = (3 * 1.25 * (cp_unit_consumption + clar_unit_consumption)) + \
                             (3 * 0.27 * solids_unit_consumption) + mbr_unit_consumption + bt_unit_consumption + \
                             iex_unit_consumption + alox_unit_consumption + feox_unit_consumption + \
                             zvi_unit_consumption + mvc_unit_consumption + (0.33 * crys_unit_consumption)

    electricity_consumption = np.multiply(total_unit_consumption, wastewater_volume)
    cost_electricity_consumption = electricity_consumption * (82.1/1000) # Cost of Electricity from Bit Baseline is $82.1/MWh

    return electricity_consumption, cost_electricity_consumption

def wastewater_chemical_consumption(wastewater_volume, cp, mbr, bt, mvc, iex, alox, feox, zvi, ro, crys):

    # For chemical precipitation dosages.
    lime_dosage = 0.58  # kg/m^3 of lime used for FGD wastewater treatment
    organosulfide_dosage = 0.0019 # kg/m^3 of organosulfide used for FGD wastewater treatment
    iron_chloride_dosage = 0.0253  # kg/m^3 of iron chloride used for FGD wastewater treatment
    cp_acid_dosage = 0.0886  # kg/m^3 of hydrochloric acid used for FGD wastewater treatment
    cp_polymer_dosage = 0.0049 # kg/m^3 of polymer used for FGD wastewater treatment

    # For biological treatment dosages.
    nutrient_min = 1.4 * 1.3  # kg/m^3 of nutrient used for biological treatment
    nutrient_max = 7.1 * 1.3  # kg/m^3 of nutrient used for biological treatment

    # For mechanical vapor compression dosages.
    coagulant_dosage = 0.1287  # kg/m^3 of coagulant used for MVC
    mvc_polymer_dosage = 0.0149  # kg/m^3 of polymer used for MVC
    mvc_antiscalant_dosage = 0.0022  # kg/m^3 of antiscalant used for MVC
    mvc_acid_dosage = 0.0146  # kg/m^3 of acid used for MVC
    soda_ash_dosage = 0.1159  #kg/m^3 of soda ash used for FGD wastewater treatment

    # For reverse osmosis dosages.
    ro_antiscalant_dosage = 0.010 # kg/m^3 of antiscalant used for RO

    lime_consumption = np.zeros(len(wastewater_volume))
    organosulfide_consumption = np.zeros(len(wastewater_volume))
    iron_chloride_consumption = np.zeros(len(wastewater_volume))
    cp_acid_consumption = np.zeros(len(wastewater_volume))
    cp_polymer_consumption = np.zeros(len(wastewater_volume))
    nutrient_consumption = np.zeros(len(wastewater_volume))
    coagulant_consumption = np.zeros(len(wastewater_volume))
    mvc_polymer_consumption = np.zeros(len(wastewater_volume))
    antiscalant_consumption = np.zeros(len(wastewater_volume))
    mvc_acid_consumption = np.zeros(len(wastewater_volume))
    soda_ash_consumption = np.zeros(len(wastewater_volume))

    if cp == 1:
        lime_consumption = lime_dosage * wastewater_volume
        organosulfide_consumption = organosulfide_dosage * wastewater_volume
        iron_chloride_consumption = iron_chloride_dosage * wastewater_volume
        cp_acid_consumption = cp_acid_dosage * wastewater_volume
        cp_polymer_consumption = cp_polymer_dosage * wastewater_volume

    if bt == 1:
        nutrient_dosage = np.random.uniform(nutrient_min, nutrient_max, len(wastewater_volume))
        nutrient_consumption = np.multiply(nutrient_dosage, wastewater_volume)

    if mvc == 1:
        coagulant_consumption = coagulant_dosage * wastewater_volume
        mvc_polymer_consumption = mvc_polymer_dosage * wastewater_volume
        mvc_antiscalant_consumption = mvc_antiscalant_dosage * wastewater_volume
        mvc_acid_consumption = mvc_acid_dosage * wastewater_volume
        soda_ash_consumption = soda_ash_dosage * wastewater_volume

    if ro == 1:
        ro_antiscalant_consumption = ro_antiscalant_dosage * wastewater_volume

    acid_consumption = cp_acid_consumption + mvc_acid_consumption
    polymer_consumption = cp_polymer_consumption + mvc_polymer_consumption

    return lime_consumption, organosulfide_consumption, iron_chloride_consumption, nutrient_consumption, \
           coagulant_consumption, antiscalant_consumption, soda_ash_consumption, acid_consumption, polymer_consumption
