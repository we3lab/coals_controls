def chemical_precipitation_costs(wastewater_flowrate_m3_per_hour, n, i):
    wastewater_flowrate_gpd = wastewater_flowrate_m3_per_hour * 264.1721 * 24 # [gpd] There are 264 gallons per cubic meter and 24 hours per day

    capital_costs = 7040000 + (35.0 * wastewater_flowrate_gpd) # [$]
    o_and_m_costs = 230000 + (4.05 * wastewater_flowrate_gpd) # [$/yr]

    pv_of_o_and_m_costs = o_and_m_costs * (((1 + i) ** n) -1)/(i * ((1 + i) ** n))
    net_present_costs = capital_costs + pv_of_o_and_m_costs

    return capital_costs, o_and_m_costs, pv_of_o_and_m_costs, net_present_costs


def biological_treatment_costs(wastewater_flowrate_m3_per_hour, n, i):
    wastewater_flowrate_gpd = wastewater_flowrate_m3_per_hour * 264.1721 * 24  # [gpd] There are 264 gallons per cubic meter and 24 hours per day

    capital_costs = 3180000 + (9.74 * wastewater_flowrate_gpd)  # [$]
    o_and_m_costs = 329000 + (0.803 * wastewater_flowrate_gpd)  # [$/yr]

    pv_of_o_and_m_costs = o_and_m_costs * (((1 + i) ** n) -1)/(i * ((1 + i) ** n))
    net_present_costs = capital_costs + pv_of_o_and_m_costs

    return capital_costs, o_and_m_costs, pv_of_o_and_m_costs, net_present_costs


def thermal_evaporation_costs(wastewater_flowrate_m3_per_hour, n, i):
    wastewater_flowrate_gpd = wastewater_flowrate_m3_per_hour * 264.1721 * 24  # [gpd] There are 264 gallons per cubic meter and 24 hours per day

    capital_costs = 14400000 + (36.7 * wastewater_flowrate_gpd)  # [$]
    o_and_m_costs = 1020000 + (5.81 * wastewater_flowrate_gpd)  # [$/yr]

    pv_of_o_and_m_costs = o_and_m_costs * (((1 + i) ** n) -1)/(i * ((1 + i) ** n))
    net_present_costs = capital_costs + pv_of_o_and_m_costs

    return capital_costs, o_and_m_costs, pv_of_o_and_m_costs, net_present_costs


def pretreated_membrane_filtration_costs(wastewater_flowrate_m3_per_hour, n, i):
    wastewater_flowrate_gpd = wastewater_flowrate_m3_per_hour * 264.1721 * 24  # [gpd] There are 264 gallons per cubic meter and 24 hours per day

    capital_costs = 1650000 + (45.5 * wastewater_flowrate_gpd)  # [$]
    o_and_m_costs = 451000 + (6.95 * wastewater_flowrate_gpd)  # [$/yr]

    pv_of_o_and_m_costs = o_and_m_costs * (((1 + i) ** n) -1)/(i * ((1 + i) ** n))
    net_present_costs = capital_costs + pv_of_o_and_m_costs

    return capital_costs, o_and_m_costs, pv_of_o_and_m_costs, net_present_costs


def non_pretreated_membrane_filtration_costs(wastewater_flowrate_m3_per_hour, n, i):
    wastewater_flowrate_gpd = wastewater_flowrate_m3_per_hour * 264.1721 * 24  # [gpd] There are 264 gallons per cubic meter and 24 hours per day

    capital_costs = 1620000 + (39.9 * wastewater_flowrate_gpd)  # [$]
    o_and_m_costs = 467000 + (6.00 * wastewater_flowrate_gpd)  # [$/yr]

    pv_of_o_and_m_costs = o_and_m_costs * (((1 + i) ** n) -1)/(i * ((1 + i) ** n))
    net_present_costs = capital_costs + pv_of_o_and_m_costs

    return capital_costs, o_and_m_costs, pv_of_o_and_m_costs, net_present_costs

def zero_valent_iron_costs(wastewater_flowrate_m3_per_hour, n, i):
    """This process cost model is based on the process published in Huang, Y. H., Peddi, P. K., Tang, C., Zeng, H., &
    Teng, X. (2013). Hybrid zero-valent iron processes for removing heavy metals and nitrate from
    flue-gas-desulfurization wastewater. Separation and Purification Technology, 118, 690-698. Their process is a series
     of chemical reactors, so we assume that capital costs follow the chemical precipitation process.  Huang et al. also
      estimate O&M costs of ~$0.5/m^3 of water treated so we include this as the O&M cost estiamtes.
"""

    wastewater_flowrate_gpd = wastewater_flowrate_m3_per_hour * 264.1721 * 24  # [gpd] There are 264 gallons per cubic meter and 24 hours per day

    capital_costs = 7040000 + (35.0 * wastewater_flowrate_gpd) # [$]

    o_and_m_chem_costs = 0.5 * wastewater_flowrate_m3_per_hour * 24 * 365  # [$/yr]
    pv_of_o_and_m_chem_costs = o_and_m_chem_costs * (((1 + i) ** n) -1)/(i * ((1 + i) ** n))

    o_and_m_elec_costs = ((4 * 0.015) + 0.009 + 0.01 + 0.0095) * 0.05 * wastewater_flowrate_m3_per_hour * 24 * 365 # [$/yr]
    pv_of_o_and_m_elec_costs = o_and_m_elec_costs * (((1 + i) ** n) -1)/(i * ((1 + i) ** n))

    net_present_costs = capital_costs + pv_of_o_and_m_chem_costs + pv_of_o_and_m_elec_costs

    return capital_costs, o_and_m_chem_costs, pv_of_o_and_m_chem_costs, o_and_m_elec_costs, pv_of_o_and_m_elec_costs, \
           net_present_costs