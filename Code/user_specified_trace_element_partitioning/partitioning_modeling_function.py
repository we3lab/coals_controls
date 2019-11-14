# Import standard python libraries.
import pathlib
import numpy as np
import sys
import pandas as pd

# Import the functions used throughout this project from the function dictionary library file
fileDir = pathlib.Path(__file__).parents[2]
code_library_folder = fileDir / 'Code' / 'function_dictionary_library'
sys.path.append(str(code_library_folder))
from statistical_functions import ecdf, random_value_from_ecdf
from coal_ecdf import coal_ecdf
from fuel_and_energy_modeling import coal_combustion
from wastewater_functions import wastewater_generation, fgd_wastewater_concentration
from APCD_partition_modeling import bottom_modeling, csESP_modeling, hsESP_modeling, FF_modeling, SCR_modeling, \
    ACI_modeling, wetFGD_modeling, dryFGD_modeling, wetFGD_wastewater_Se_modeling
#from WPCD_partition_modeling import cp_modeling, mbr_modeling, bt_modeling, mvc_modeling, iex_modeling, alox_modeling, feox_modeling, zvi_modeling, crys_modeling
from mc_WPCD_partition_modeling import cp_modeling, mbr_modeling, bt_modeling, mvc_modeling, iex_modeling, alox_modeling, feox_modeling, zvi_modeling, crys_modeling
from mass_partitioning_calculation import apcd_mass_partitioning, wpcd_mass_partitioning, mc_wpcd_mass_partitioning
from elg_compliance_check import elg_compliance_check_simulation, elg_compliance_check_simulation_no_as


def treatment_train_violation_checks(coal_input, csesp_input, hsesp_input, ff_input, scr_input, aci_input, wetfgd_input,
                                     wetfgdtype_input, dryfgd_input, elg_input, zld_input, cp_input, mbr_input,
                                     bt_input, mvc_input, iex_input, alox_input, feox_input, zvi_input, crys_input,
                                     electricity_generated_input):

    # Select a coal and import the CDFs of Chlorine, Selenium, Boron, Bromine, and Arsenic concentrations in the coal.
    coal = coal_input
    qe_Cl, pe_Cl, qe_Se, pe_Se, qe_B, pe_B, qe_Br, pe_Br, qe_Pb, pe_Pb, qe_As, pe_As, qe_Hg, pe_Hg, qe_Heat, pe_Heat, \
        gross_heat_rate, FGD_water_treatment = coal_ecdf(coal)

    # Define the flue gas treatment train based on user inputs.
    csESP = csesp_input
    hsESP = hsesp_input
    FF = ff_input
    SCR = scr_input
    ACI = aci_input
    wetFGD = wetfgd_input
    dryFGD = dryfgd_input
    wetFGD_type = wetfgdtype_input

    # Define the flue gas desulfurization wastewater treatment train based on user inputs.
    elg = elg_input
    zld = zld_input
    cp = cp_input
    mbr = mbr_input
    bt = bt_input
    mvc = mvc_input
    iex = iex_input
    alox = alox_input
    feox = feox_input
    zvi = zvi_input
    crys = crys_input

    # Initialize Monte Carlo Analysis by developing array of concentrations.
    runs = 500
    mc_Cl_concentration = random_value_from_ecdf(qe_Cl, pe_Cl, runs)
    mc_Se_concentration = random_value_from_ecdf(qe_Se, pe_Se, runs)
    mc_B_concentration = random_value_from_ecdf(qe_B, pe_B, runs)
    mc_Br_concentration = random_value_from_ecdf(qe_Br, pe_Br, runs)
    mc_Pb_concentration = random_value_from_ecdf(qe_Pb, pe_Pb, runs)
    mc_As_concentration = random_value_from_ecdf(qe_As, pe_As, runs)
    mc_Hg_concentration = random_value_from_ecdf(qe_Hg, pe_Hg, runs)
    mc_Heat_concentration = random_value_from_ecdf(qe_Heat, pe_Heat, runs)

    # Calculate the amount of trace elements entering in the coal.  Assume 1 metric tons (1000 kg) of coal is combusted.
    electricity_generated = electricity_generated_input
    coal_combusted = coal_combustion(electricity_generated, mc_Heat_concentration, gross_heat_rate) # kg of coal combusted
    if wetFGD == 1:
        wastewater_production = wastewater_generation(electricity_generated, FGD_water_treatment) #[m^3/hr] of FGD wastewater produced
    else:
        wastewater_production = 0
    Cl_mass_entering = mc_Cl_concentration * coal_combusted
    Se_mass_entering = mc_Se_concentration * coal_combusted
    B_mass_entering = mc_B_concentration * coal_combusted
    Br_mass_entering = mc_Br_concentration * coal_combusted
    Pb_mass_entering = mc_Pb_concentration * coal_combusted
    As_mass_entering = mc_As_concentration * coal_combusted
    Hg_mass_entering = mc_Hg_concentration * coal_combusted

    #Create partitioning coefficient simulations.
    Cl_bottom, Se_bottom, B_bottom, Br_bottom, Pb_bottom, As_bottom, Hg_bottom = bottom_modeling(runs)
    Cl_csESP, Se_csESP, B_csESP, Br_csESP, Pb_csESP, As_csESP, Hg_csESP = csESP_modeling(csESP, runs)
    Cl_hsESP, Se_hsESP, B_hsESP, Br_hsESP, Pb_hsESP, As_hsESP, Hg_hsESP = hsESP_modeling(hsESP, runs)
    Cl_FF, Se_FF, B_FF, Br_FF, Pb_FF, As_FF, Hg_FF = FF_modeling(FF, runs)
    Cl_SCR, Se_SCR, B_SCR, Br_SCR, Pb_SCR, As_SCR, Hg_SCR = SCR_modeling(SCR, runs)
    Cl_ACI, Se_ACI, B_ACI, Br_ACI, Pb_ACI, As_ACI, Hg_ACI = ACI_modeling(ACI, runs)
    Cl_wetFGD, Se_wetFGD, B_wetFGD, Br_wetFGD, Pb_wetFGD, As_wetFGD, Hg_wetFGD, Se_wetFGD_ww = wetFGD_modeling(wetFGD, wetFGD_type, runs)
    Cl_dryFGD, Se_dryFGD, B_dryFGD, Br_dryFGD, Pb_dryFGD, As_dryFGD, Hg_dryFGD = dryFGD_modeling(dryFGD, runs)


    #Calculate partitioning
    Cl_mass_bottom, Se_mass_bottom, B_mass_bottom, Br_mass_bottom, Pb_mass_bottom, As_mass_bottom, Hg_mass_bottom = apcd_mass_partitioning(runs,
        Cl_mass_entering, Cl_bottom, Se_mass_entering, Se_bottom, B_mass_entering, B_bottom, Br_mass_entering, Br_bottom,
        Pb_mass_entering, Pb_bottom, As_mass_entering, As_bottom, Hg_mass_entering, Hg_bottom)

    Cl_mass_dryFGD, Se_mass_dryFGD, B_mass_dryFGD, Br_mass_dryFGD, Pb_mass_dryFGD, As_mass_dryFGD, Hg_mass_dryFGD = apcd_mass_partitioning(runs,
        Cl_mass_bottom[:,2], Cl_dryFGD, Se_mass_bottom[:,2], Se_dryFGD, B_mass_bottom[:,2], B_dryFGD, Br_mass_bottom[:,2],
        Br_dryFGD, Pb_mass_bottom[:,2], Pb_dryFGD, As_mass_bottom[:,2], As_dryFGD, Hg_mass_bottom[:,2], Hg_dryFGD)

    Cl_mass_csESP, Se_mass_csESP, B_mass_csESP, Br_mass_csESP, Pb_mass_csESP, As_mass_csESP, Hg_mass_csESP = apcd_mass_partitioning(runs,
        Cl_mass_dryFGD[:,2], Cl_csESP, Se_mass_dryFGD[:,2], Se_csESP, B_mass_dryFGD[:,2], B_csESP, Br_mass_dryFGD[:,2],
        Br_csESP, Pb_mass_dryFGD[:,2], Pb_csESP, As_mass_dryFGD[:,2], As_csESP, Hg_mass_dryFGD[:,2], Hg_csESP)

    Cl_mass_hsESP, Se_mass_hsESP, B_mass_hsESP, Br_mass_hsESP, Pb_mass_hsESP, As_mass_hsESP, Hg_mass_hsESP = apcd_mass_partitioning(runs,
        Cl_mass_csESP[:,2], Cl_hsESP, Se_mass_csESP[:,2], Se_hsESP, B_mass_csESP[:,2], B_hsESP, Br_mass_csESP[:,2],
        Br_hsESP, Pb_mass_csESP[:,2], Pb_hsESP, As_mass_csESP[:,2], As_hsESP, Hg_mass_csESP[:,2], Hg_hsESP)

    Cl_mass_FF, Se_mass_FF, B_mass_FF, Br_mass_FF, Pb_mass_FF, As_mass_FF, Hg_mass_FF = apcd_mass_partitioning(runs,
        Cl_mass_hsESP[:,2], Cl_FF, Se_mass_hsESP[:,2], Se_FF, B_mass_hsESP[:,2], B_FF, Br_mass_hsESP[:,2], Br_FF,
        Pb_mass_hsESP[:,2], Pb_FF, As_mass_hsESP[:,2], As_FF, Hg_mass_hsESP[:,2], Hg_FF)

    Cl_mass_SCR, Se_mass_SCR, B_mass_SCR, Br_mass_SCR, Pb_mass_SCR, As_mass_SCR, Hg_mass_SCR = apcd_mass_partitioning(runs,
        Cl_mass_FF[:,2], Cl_SCR, Se_mass_FF[:,2], Se_SCR, B_mass_FF[:,2], B_SCR, Br_mass_FF[:,2], Br_SCR, Pb_mass_FF[:,2],
        Pb_SCR, As_mass_FF[:,2], As_SCR, Hg_mass_FF[:,2], Hg_SCR)

    Cl_mass_ACI, Se_mass_ACI, B_mass_ACI, Br_mass_ACI, Pb_mass_ACI, As_mass_ACI, Hg_mass_ACI = apcd_mass_partitioning(runs,
        Cl_mass_SCR[:,2], Cl_ACI, Se_mass_SCR[:,2], Se_ACI, B_mass_SCR[:,2], B_ACI, Br_mass_SCR[:,2],
        Br_ACI, Pb_mass_SCR[:,2], Pb_ACI, As_mass_SCR[:,2], As_ACI, Hg_mass_SCR[:,2], Hg_ACI)

    Cl_mass_wetFGD, Se_mass_wetFGD, B_mass_wetFGD, Br_mass_wetFGD, Pb_mass_wetFGD, As_mass_wetFGD, Hg_mass_wetFGD = apcd_mass_partitioning(runs,
        Cl_mass_ACI[:,2], Cl_wetFGD, Se_mass_ACI[:,2], Se_wetFGD, B_mass_ACI[:,2], B_wetFGD, Br_mass_ACI[:,2],
        Br_wetFGD, Pb_mass_ACI[:,2], Pb_wetFGD, As_mass_ACI[:,2], As_wetFGD, Hg_mass_ACI[:,2], Hg_wetFGD)

    Cl_mass_dryFGD, Se_mass_dryFGD, B_mass_dryFGD, Br_mass_dryFGD, Pb_mass_dryFGD, As_mass_dryFGD, Hg_mass_dryFGD = apcd_mass_partitioning(runs,
        Cl_mass_wetFGD[:,2], Cl_dryFGD, Se_mass_wetFGD[:,2], Se_dryFGD, B_mass_wetFGD[:,2], B_dryFGD, Br_mass_wetFGD[:,2],
        Br_dryFGD, Pb_mass_wetFGD[:,2], Pb_dryFGD, As_mass_wetFGD[:,2], As_dryFGD, Hg_mass_wetFGD[:,2], Hg_dryFGD)

    #Calculate total mass splits
    Cl_fate=Cl_mass_bottom+Cl_mass_csESP+Cl_mass_hsESP+Cl_mass_FF+Cl_mass_SCR+Cl_mass_ACI+Cl_mass_wetFGD+Cl_mass_dryFGD
    Cl_fate[:,2]=Cl_mass_dryFGD[:,2]

    Se_fate=Se_mass_bottom+Se_mass_csESP+Se_mass_hsESP+Se_mass_FF+Se_mass_SCR+Se_mass_ACI+Se_mass_wetFGD+Se_mass_dryFGD
    Se_fate[:,2]=Se_mass_dryFGD[:,2]

    B_fate=B_mass_bottom+B_mass_csESP+B_mass_hsESP+B_mass_FF+B_mass_SCR+B_mass_ACI+B_mass_wetFGD+B_mass_dryFGD
    B_fate[:,2]=B_mass_dryFGD[:,2]

    Br_fate=Br_mass_bottom+Br_mass_csESP+Br_mass_hsESP+Br_mass_FF+Br_mass_SCR+Br_mass_ACI+Br_mass_wetFGD+Br_mass_dryFGD
    Br_fate[:,2]=Br_mass_dryFGD[:,2]

    Pb_fate=Pb_mass_bottom+Pb_mass_csESP+Pb_mass_hsESP+Pb_mass_FF+Pb_mass_SCR+Pb_mass_ACI+Pb_mass_wetFGD+Pb_mass_dryFGD
    Pb_fate[:,2]=Pb_mass_dryFGD[:,2]

    As_fate=As_mass_bottom+As_mass_csESP+As_mass_hsESP+As_mass_FF+As_mass_SCR+As_mass_ACI+As_mass_wetFGD+As_mass_dryFGD
    As_fate[:,2]=As_mass_dryFGD[:,2]

    Hg_fate=Hg_mass_bottom+Hg_mass_csESP+Hg_mass_hsESP+Hg_mass_FF+Hg_mass_SCR+Hg_mass_ACI+Hg_mass_wetFGD+Hg_mass_dryFGD
    Hg_fate[:,2]=Hg_mass_dryFGD[:,2]

    if wetFGD == 1:
        # Calculate trace element concentration in the FGD wastewater influent

        Cl_concentration = fgd_wastewater_concentration(Cl_fate[:, 1], wastewater_production)  # [g/m^3]
        Se_concentration = fgd_wastewater_concentration(Se_fate[:, 1], wastewater_production)  # [g/m^3]
        B_concentration = fgd_wastewater_concentration(B_fate[:, 1], wastewater_production)  # [g/m^3]
        Br_concentration = fgd_wastewater_concentration(Br_fate[:, 1], wastewater_production)  # [g/m^3]
        Pb_concentration = fgd_wastewater_concentration(Pb_fate[:, 1], wastewater_production)  # [g/m^3]
        As_concentration = fgd_wastewater_concentration(As_fate[:, 1], wastewater_production)  # [g/m^3]
        Hg_concentration = fgd_wastewater_concentration(Hg_fate[:, 1], wastewater_production)  # [g/m^3]

        if type(Se_wetFGD_ww) != int:
            # calculate the Se speciation in wetFGD waste water
            Se_speciation = np.zeros(shape=[runs, 4])
            for i in range(0, 4):
                Se_speciation[:, i] = Se_concentration * Se_wetFGD_ww[:, i]  # [g/m^3]

        cl_conc_distribution = [np.percentile(Cl_concentration, 5), np.percentile(Cl_concentration, 25),
                                np.percentile(Cl_concentration, 50), np.percentile(Cl_concentration, 75),
                                np.percentile(Cl_concentration, 95)]

        se_conc_distribution = [np.percentile(Se_concentration, 5), np.percentile(Se_concentration, 25),
                                np.percentile(Se_concentration, 50), np.percentile(Se_concentration, 75),
                                np.percentile(Se_concentration, 95)]

        as_conc_distribution = [np.percentile(As_concentration, 5), np.percentile(As_concentration, 25),
                                np.percentile(As_concentration, 50), np.percentile(As_concentration, 75),
                                np.percentile(As_concentration, 95)]

        hg_conc_distribution = [np.percentile(Hg_concentration, 5), np.percentile(Hg_concentration, 25),
                                np.percentile(Hg_concentration, 50), np.percentile(Hg_concentration, 75),
                                np.percentile(Hg_concentration, 95)]

        b_conc_distribution = [np.percentile(B_concentration, 5), np.percentile(B_concentration, 25),
                                np.percentile(B_concentration, 50), np.percentile(B_concentration, 75),
                                np.percentile(B_concentration, 95)]


        br_conc_distribution = [np.percentile(Br_concentration, 5), np.percentile(Br_concentration, 25),
                                np.percentile(Br_concentration, 50), np.percentile(Br_concentration, 75),
                                np.percentile(Br_concentration, 95)]

        pb_conc_distribution = [np.percentile(Pb_concentration, 5), np.percentile(Pb_concentration, 25),
                                np.percentile(Pb_concentration, 50), np.percentile(Pb_concentration, 75),
                                np.percentile(Pb_concentration, 95)]


        # Create FGD Wastewater concentration data frame.
        concentration_summary = np.array([as_conc_distribution, b_conc_distribution, br_conc_distribution, cl_conc_distribution,
                                          hg_conc_distribution, pb_conc_distribution, se_conc_distribution])
        concentration_summary = pd.DataFrame(concentration_summary, index=['As', 'B', 'Br', 'Cl', 'Hg', 'Pb', 'Se'],
                                             columns=['5th_Percentile', '25th_Percentile', 'Median', '75th_Percentile',
                                                      '95th_Percentile'])

        # Calculate the removal of trace elements that takes place in the FGD wastewater treatment process.  Note that we do
        # not model nitrogen removal performance.

        # Start with chemical precipitation.

        as_cp, cl_cp, pb_cp, hg_cp, se_cp = cp_modeling(cp, runs)
        as_mass_cp, cl_mass_cp, pb_mass_cp, hg_mass_cp, se_mass_cp = wpcd_mass_partitioning(runs, As_fate[:, 1], as_cp,
                                                                                            Cl_fate[:, 1], cl_cp,
                                                                                            Pb_fate[:, 1], pb_cp,
                                                                                            Hg_fate[:, 1], hg_cp,
                                                                                            Se_fate[:, 1], se_cp)

        # And then model the treatment of FGD wastewater to comply with the ELGs.
        if elg == 1:
            as_mbr, cl_mbr, pb_mbr, hg_mbr, se_mbr = mbr_modeling(mbr, runs)
            as_bt, cl_bt, pb_bt, hg_bt, se_bt = bt_modeling(bt, runs)
            as_iex, cl_iex, pb_iex, hg_iex, se_iex = iex_modeling(iex, runs)
            as_alox, cl_alox, pb_alox, hg_alox, se_alox = alox_modeling(alox, runs)
            as_feox, cl_feox, pb_feox, hg_feox, se_feox = feox_modeling(feox, runs)
            as_zvi, cl_zvi, pb_zvi, hg_zvi, se_zvi = zvi_modeling(zvi, runs)

            as_mass_mbr, cl_mass_mbr, pb_mass_mbr, hg_mass_mbr, se_mass_mbr = wpcd_mass_partitioning(runs, as_mass_cp[:, 1],
                                                                                                     as_mbr, cl_mass_cp[:, 1],
                                                                                                     cl_mbr, pb_mass_cp[:, 1],
                                                                                                     pb_mbr, hg_mass_cp[:, 1],
                                                                                                     hg_mbr, se_mass_cp[:, 1],
                                                                                                     se_mbr)

            as_mass_bt, cl_mass_bt, pb_mass_bt, hg_mass_bt, se_mass_bt = wpcd_mass_partitioning(runs, as_mass_mbr[:, 1], as_bt,
                                                                                                cl_mass_mbr[:, 1], cl_bt,
                                                                                                pb_mass_mbr[:, 1], pb_bt,
                                                                                                hg_mass_mbr[:, 1], hg_bt,
                                                                                                se_mass_mbr[:, 1], se_bt)

            as_mass_iex, cl_mass_iex, pb_mass_iex, hg_mass_iex, se_mass_iex = wpcd_mass_partitioning(runs, as_mass_bt[:, 1],
                                                                                                     as_iex, cl_mass_bt[:, 1],
                                                                                                     cl_iex, pb_mass_bt[:, 1],
                                                                                                     pb_iex, hg_mass_bt[:, 1],
                                                                                                     hg_iex, se_mass_bt[:, 1],
                                                                                                     se_iex)

            as_mass_alox, cl_mass_alox, pb_mass_alox, hg_mass_alox, se_mass_alox = wpcd_mass_partitioning(runs,
                                                                                                          as_mass_iex[:, 1],
                                                                                                          as_alox,
                                                                                                          cl_mass_iex[:, 1],
                                                                                                          cl_alox,
                                                                                                          pb_mass_iex[:, 1],
                                                                                                          pb_alox,
                                                                                                          hg_mass_iex[:, 1],
                                                                                                          hg_alox,
                                                                                                          se_mass_iex[:, 1],
                                                                                                          se_alox)

            as_mass_feox, cl_mass_feox, pb_mass_feox, hg_mass_feox, se_mass_feox = wpcd_mass_partitioning(runs, as_mass_alox[:, 1],
                                                                                                          as_feox,
                                                                                                          cl_mass_alox[:, 1],
                                                                                                          cl_feox,
                                                                                                          pb_mass_alox[:, 1],
                                                                                                          pb_feox,
                                                                                                          hg_mass_alox[:, 1],
                                                                                                          hg_feox,
                                                                                                          se_mass_alox[:, 1],
                                                                                                          se_feox)

            as_mass_zvi, cl_mass_zvi, pb_mass_zvi, hg_mass_zvi, se_mass_zvi = wpcd_mass_partitioning(runs, as_mass_feox[:, 1],
                                                                                                     as_zvi, cl_mass_feox[:, 1],
                                                                                                     cl_zvi, pb_mass_feox[:, 1],
                                                                                                     pb_zvi, hg_mass_feox[:, 1],
                                                                                                     hg_zvi, se_mass_feox[:, 1],
                                                                                                     se_zvi)

            as_fgd_effluent_concentration = fgd_wastewater_concentration(as_mass_zvi[:, 1], wastewater_production)
            cl_fgd_effluent_concentration = fgd_wastewater_concentration(cl_mass_zvi[:, 1], wastewater_production)
            pb_fgd_effluent_concentration = fgd_wastewater_concentration(pb_mass_zvi[:, 1], wastewater_production)
            hg_fgd_effluent_concentration = fgd_wastewater_concentration(hg_mass_zvi[:, 1], wastewater_production)
            se_fgd_effluent_concentration = fgd_wastewater_concentration(se_mass_zvi[:, 1], wastewater_production)

        if zld == 1:
            as_mvc, cl_mvc, pb_mvc, hg_mvc, se_mvc = mvc_modeling(mvc, runs)
            as_crys, cl_crys, pb_crys, hg_crys, se_crys = crys_modeling(crys, runs)

            as_mass_mvc, cl_mass_mvc, pb_mass_mvc, hg_mass_mvc, se_mass_mvc = wpcd_mass_partitioning(runs, as_mass_cp[:, 1], as_mvc,
                                                                                                     cl_mass_cp[:, 1], cl_mvc,
                                                                                                     pb_mass_cp[:, 1], pb_mvc,
                                                                                                     hg_mass_cp[:, 1], hg_mvc,
                                                                                                     se_mass_cp[:, 1], se_mvc)

            as_mass_crys, cl_mass_crys, pb_mass_crys, hg_mass_crys, se_mass_crys = wpcd_mass_partitioning(runs, as_mass_mvc[:, 1], as_crys,
                                                                                                cl_mass_mvc[:, 1], cl_crys,
                                                                                                pb_mass_mvc[:, 1], pb_crys,
                                                                                                hg_mass_mvc[:, 1], hg_crys,
                                                                                                se_mass_mvc[:, 1], se_crys)

            as_fgd_effluent_concentration = fgd_wastewater_concentration(as_mass_crys[:, 1], wastewater_production)
            cl_fgd_effluent_concentration = fgd_wastewater_concentration(cl_mass_crys[:, 1], wastewater_production)
            pb_fgd_effluent_concentration = fgd_wastewater_concentration(pb_mass_crys[:, 1], wastewater_production)
            hg_fgd_effluent_concentration = fgd_wastewater_concentration(hg_mass_crys[:, 1], wastewater_production)
            se_fgd_effluent_concentration = fgd_wastewater_concentration(se_mass_crys[:, 1], wastewater_production)

        if alox == 0 and iex == 0:
            total_violations, as_violations, hg_violations, se_violations = elg_compliance_check_simulation(elg, zld,
                                                                                                            as_fgd_effluent_concentration,
                                                                                                            cl_fgd_effluent_concentration,
                                                                                                            hg_fgd_effluent_concentration,
                                                                                                            se_fgd_effluent_concentration)
        elif alox == 1 or iex == 1:
            total_violations, as_violations, hg_violations, se_violations = elg_compliance_check_simulation_no_as(elg,
                                                                                                            zld,
                                                                                                            as_fgd_effluent_concentration,
                                                                                                            cl_fgd_effluent_concentration,
                                                                                                            hg_fgd_effluent_concentration,
                                                                                                            se_fgd_effluent_concentration)

        return total_violations, np.median(as_fgd_effluent_concentration), as_violations, \
               np.median(hg_fgd_effluent_concentration), hg_violations, np.median(se_fgd_effluent_concentration), \
               se_violations, np.median(cl_fgd_effluent_concentration), np.median(pb_fgd_effluent_concentration)


def mc_treatment_train_violation_checks(coal_input, csesp_input, hsesp_input, ff_input, scr_input, aci_input, wetfgd_input,
                                     wetfgdtype_input, dryfgd_input, elg_input, zld_input, cp_input, mbr_input,
                                     bt_input, mvc_input, iex_input, alox_input, feox_input, zvi_input, crys_input,
                                     electricity_generated_input):

    # Select a coal and import the CDFs of Chlorine, Selenium, Boron, Bromine, and Arsenic concentrations in the coal.
    coal = coal_input
    qe_Cl, pe_Cl, qe_Se, pe_Se, qe_B, pe_B, qe_Br, pe_Br, qe_Pb, pe_Pb, qe_As, pe_As, qe_Hg, pe_Hg, qe_Heat, pe_Heat, \
        gross_heat_rate, FGD_water_treatment = coal_ecdf(coal)

    # Define the flue gas treatment train based on user inputs.
    csESP = csesp_input
    hsESP = hsesp_input
    FF = ff_input
    SCR = scr_input
    ACI = aci_input
    wetFGD = wetfgd_input
    dryFGD = dryfgd_input
    wetFGD_type = wetfgdtype_input

    # Define the flue gas desulfurization wastewater treatment train based on user inputs.
    elg = elg_input
    zld = zld_input
    cp = cp_input
    mbr = mbr_input
    bt = bt_input
    mvc = mvc_input
    iex = iex_input
    alox = alox_input
    feox = feox_input
    zvi = zvi_input
    crys = crys_input

    # Initialize Monte Carlo Analysis by developing array of concentrations.
    runs = 500
    mc_Cl_concentration = random_value_from_ecdf(qe_Cl, pe_Cl, runs)
    mc_Se_concentration = random_value_from_ecdf(qe_Se, pe_Se, runs)
    mc_B_concentration = random_value_from_ecdf(qe_B, pe_B, runs)
    mc_Br_concentration = random_value_from_ecdf(qe_Br, pe_Br, runs)
    mc_Pb_concentration = random_value_from_ecdf(qe_Pb, pe_Pb, runs)
    mc_As_concentration = random_value_from_ecdf(qe_As, pe_As, runs)
    mc_Hg_concentration = random_value_from_ecdf(qe_Hg, pe_Hg, runs)
    mc_Heat_concentration = random_value_from_ecdf(qe_Heat, pe_Heat, runs)

    # Calculate the amount of trace elements entering in the coal.  Assume 1 metric tons (1000 kg) of coal is combusted.
    electricity_generated = electricity_generated_input
    coal_combusted = coal_combustion(electricity_generated, mc_Heat_concentration, gross_heat_rate) # kg of coal combusted
    if wetFGD == 1:
        wastewater_production = wastewater_generation(electricity_generated, FGD_water_treatment) #[m^3/hr] of FGD wastewater produced
    else:
        wastewater_production = 0
    Cl_mass_entering = mc_Cl_concentration * coal_combusted
    Se_mass_entering = mc_Se_concentration * coal_combusted
    B_mass_entering = mc_B_concentration * coal_combusted
    Br_mass_entering = mc_Br_concentration * coal_combusted
    Pb_mass_entering = mc_Pb_concentration * coal_combusted
    As_mass_entering = mc_As_concentration * coal_combusted
    Hg_mass_entering = mc_Hg_concentration * coal_combusted

    #Create partitioning coefficient simulations.
    Cl_bottom, Se_bottom, B_bottom, Br_bottom, Pb_bottom, As_bottom, Hg_bottom = bottom_modeling(runs)
    Cl_csESP, Se_csESP, B_csESP, Br_csESP, Pb_csESP, As_csESP, Hg_csESP = csESP_modeling(csESP, runs)
    Cl_hsESP, Se_hsESP, B_hsESP, Br_hsESP, Pb_hsESP, As_hsESP, Hg_hsESP = hsESP_modeling(hsESP, runs)
    Cl_FF, Se_FF, B_FF, Br_FF, Pb_FF, As_FF, Hg_FF = FF_modeling(FF, runs)
    Cl_SCR, Se_SCR, B_SCR, Br_SCR, Pb_SCR, As_SCR, Hg_SCR = SCR_modeling(SCR, runs)
    Cl_ACI, Se_ACI, B_ACI, Br_ACI, Pb_ACI, As_ACI, Hg_ACI = ACI_modeling(ACI, runs)
    Cl_wetFGD, Se_wetFGD, B_wetFGD, Br_wetFGD, Pb_wetFGD, As_wetFGD, Hg_wetFGD, Se_wetFGD_ww = wetFGD_modeling(wetFGD, wetFGD_type, runs)
    Cl_dryFGD, Se_dryFGD, B_dryFGD, Br_dryFGD, Pb_dryFGD, As_dryFGD, Hg_dryFGD = dryFGD_modeling(dryFGD, runs)


    #Calculate partitioning
    Cl_mass_bottom, Se_mass_bottom, B_mass_bottom, Br_mass_bottom, Pb_mass_bottom, As_mass_bottom, Hg_mass_bottom = apcd_mass_partitioning(runs,
        Cl_mass_entering, Cl_bottom, Se_mass_entering, Se_bottom, B_mass_entering, B_bottom, Br_mass_entering, Br_bottom,
        Pb_mass_entering, Pb_bottom, As_mass_entering, As_bottom, Hg_mass_entering, Hg_bottom)

    Cl_mass_dryFGD, Se_mass_dryFGD, B_mass_dryFGD, Br_mass_dryFGD, Pb_mass_dryFGD, As_mass_dryFGD, Hg_mass_dryFGD = apcd_mass_partitioning(runs,
        Cl_mass_bottom[:,2], Cl_dryFGD, Se_mass_bottom[:,2], Se_dryFGD, B_mass_bottom[:,2], B_dryFGD, Br_mass_bottom[:,2],
        Br_dryFGD, Pb_mass_bottom[:,2], Pb_dryFGD, As_mass_bottom[:,2], As_dryFGD, Hg_mass_bottom[:,2], Hg_dryFGD)

    Cl_mass_csESP, Se_mass_csESP, B_mass_csESP, Br_mass_csESP, Pb_mass_csESP, As_mass_csESP, Hg_mass_csESP = apcd_mass_partitioning(runs,
        Cl_mass_dryFGD[:,2], Cl_csESP, Se_mass_dryFGD[:,2], Se_csESP, B_mass_dryFGD[:,2], B_csESP, Br_mass_dryFGD[:,2],
        Br_csESP, Pb_mass_dryFGD[:,2], Pb_csESP, As_mass_dryFGD[:,2], As_csESP, Hg_mass_dryFGD[:,2], Hg_csESP)

    Cl_mass_hsESP, Se_mass_hsESP, B_mass_hsESP, Br_mass_hsESP, Pb_mass_hsESP, As_mass_hsESP, Hg_mass_hsESP = apcd_mass_partitioning(runs,
        Cl_mass_csESP[:,2], Cl_hsESP, Se_mass_csESP[:,2], Se_hsESP, B_mass_csESP[:,2], B_hsESP, Br_mass_csESP[:,2],
        Br_hsESP, Pb_mass_csESP[:,2], Pb_hsESP, As_mass_csESP[:,2], As_hsESP, Hg_mass_csESP[:,2], Hg_hsESP)

    Cl_mass_FF, Se_mass_FF, B_mass_FF, Br_mass_FF, Pb_mass_FF, As_mass_FF, Hg_mass_FF = apcd_mass_partitioning(runs,
        Cl_mass_hsESP[:,2], Cl_FF, Se_mass_hsESP[:,2], Se_FF, B_mass_hsESP[:,2], B_FF, Br_mass_hsESP[:,2], Br_FF,
        Pb_mass_hsESP[:,2], Pb_FF, As_mass_hsESP[:,2], As_FF, Hg_mass_hsESP[:,2], Hg_FF)

    Cl_mass_SCR, Se_mass_SCR, B_mass_SCR, Br_mass_SCR, Pb_mass_SCR, As_mass_SCR, Hg_mass_SCR = apcd_mass_partitioning(runs,
        Cl_mass_FF[:,2], Cl_SCR, Se_mass_FF[:,2], Se_SCR, B_mass_FF[:,2], B_SCR, Br_mass_FF[:,2], Br_SCR, Pb_mass_FF[:,2],
        Pb_SCR, As_mass_FF[:,2], As_SCR, Hg_mass_FF[:,2], Hg_SCR)

    Cl_mass_ACI, Se_mass_ACI, B_mass_ACI, Br_mass_ACI, Pb_mass_ACI, As_mass_ACI, Hg_mass_ACI = apcd_mass_partitioning(runs,
        Cl_mass_SCR[:,2], Cl_ACI, Se_mass_SCR[:,2], Se_ACI, B_mass_SCR[:,2], B_ACI, Br_mass_SCR[:,2],
        Br_ACI, Pb_mass_SCR[:,2], Pb_ACI, As_mass_SCR[:,2], As_ACI, Hg_mass_SCR[:,2], Hg_ACI)

    Cl_mass_wetFGD, Se_mass_wetFGD, B_mass_wetFGD, Br_mass_wetFGD, Pb_mass_wetFGD, As_mass_wetFGD, Hg_mass_wetFGD = apcd_mass_partitioning(runs,
        Cl_mass_ACI[:,2], Cl_wetFGD, Se_mass_ACI[:,2], Se_wetFGD, B_mass_ACI[:,2], B_wetFGD, Br_mass_ACI[:,2],
        Br_wetFGD, Pb_mass_ACI[:,2], Pb_wetFGD, As_mass_ACI[:,2], As_wetFGD, Hg_mass_ACI[:,2], Hg_wetFGD)

    Cl_mass_dryFGD, Se_mass_dryFGD, B_mass_dryFGD, Br_mass_dryFGD, Pb_mass_dryFGD, As_mass_dryFGD, Hg_mass_dryFGD = apcd_mass_partitioning(runs,
        Cl_mass_wetFGD[:,2], Cl_dryFGD, Se_mass_wetFGD[:,2], Se_dryFGD, B_mass_wetFGD[:,2], B_dryFGD, Br_mass_wetFGD[:,2],
        Br_dryFGD, Pb_mass_wetFGD[:,2], Pb_dryFGD, As_mass_wetFGD[:,2], As_dryFGD, Hg_mass_wetFGD[:,2], Hg_dryFGD)

    #Calculate total mass splits
    Cl_fate=Cl_mass_bottom+Cl_mass_csESP+Cl_mass_hsESP+Cl_mass_FF+Cl_mass_SCR+Cl_mass_ACI+Cl_mass_wetFGD+Cl_mass_dryFGD
    Cl_fate[:,2]=Cl_mass_dryFGD[:,2]

    Se_fate=Se_mass_bottom+Se_mass_csESP+Se_mass_hsESP+Se_mass_FF+Se_mass_SCR+Se_mass_ACI+Se_mass_wetFGD+Se_mass_dryFGD
    Se_fate[:,2]=Se_mass_dryFGD[:,2]

    B_fate=B_mass_bottom+B_mass_csESP+B_mass_hsESP+B_mass_FF+B_mass_SCR+B_mass_ACI+B_mass_wetFGD+B_mass_dryFGD
    B_fate[:,2]=B_mass_dryFGD[:,2]

    Br_fate=Br_mass_bottom+Br_mass_csESP+Br_mass_hsESP+Br_mass_FF+Br_mass_SCR+Br_mass_ACI+Br_mass_wetFGD+Br_mass_dryFGD
    Br_fate[:,2]=Br_mass_dryFGD[:,2]

    Pb_fate=Pb_mass_bottom+Pb_mass_csESP+Pb_mass_hsESP+Pb_mass_FF+Pb_mass_SCR+Pb_mass_ACI+Pb_mass_wetFGD+Pb_mass_dryFGD
    Pb_fate[:,2]=Pb_mass_dryFGD[:,2]

    As_fate=As_mass_bottom+As_mass_csESP+As_mass_hsESP+As_mass_FF+As_mass_SCR+As_mass_ACI+As_mass_wetFGD+As_mass_dryFGD
    As_fate[:,2]=As_mass_dryFGD[:,2]

    Hg_fate=Hg_mass_bottom+Hg_mass_csESP+Hg_mass_hsESP+Hg_mass_FF+Hg_mass_SCR+Hg_mass_ACI+Hg_mass_wetFGD+Hg_mass_dryFGD
    Hg_fate[:,2]=Hg_mass_dryFGD[:,2]

    if wetFGD == 1:
        # Calculate trace element concentration in the FGD wastewater influent

        Cl_concentration = fgd_wastewater_concentration(Cl_fate[:, 1], wastewater_production)  # [g/m^3]
        Se_concentration = fgd_wastewater_concentration(Se_fate[:, 1], wastewater_production)  # [g/m^3]
        B_concentration = fgd_wastewater_concentration(B_fate[:, 1], wastewater_production)  # [g/m^3]
        Br_concentration = fgd_wastewater_concentration(Br_fate[:, 1], wastewater_production)  # [g/m^3]
        Pb_concentration = fgd_wastewater_concentration(Pb_fate[:, 1], wastewater_production)  # [g/m^3]
        As_concentration = fgd_wastewater_concentration(As_fate[:, 1], wastewater_production)  # [g/m^3]
        Hg_concentration = fgd_wastewater_concentration(Hg_fate[:, 1], wastewater_production)  # [g/m^3]

        if type(Se_wetFGD_ww) != int:
            # calculate the Se speciation in wetFGD waste water
            Se_speciation = np.zeros(shape=[runs, 4])
            for i in range(0, 4):
                Se_speciation[:, i] = Se_concentration * Se_wetFGD_ww[:, i]  # [g/m^3]

        cl_conc_distribution = [np.percentile(Cl_concentration, 5), np.percentile(Cl_concentration, 25),
                                np.percentile(Cl_concentration, 50), np.percentile(Cl_concentration, 75),
                                np.percentile(Cl_concentration, 95)]

        se_conc_distribution = [np.percentile(Se_concentration, 5), np.percentile(Se_concentration, 25),
                                np.percentile(Se_concentration, 50), np.percentile(Se_concentration, 75),
                                np.percentile(Se_concentration, 95)]

        as_conc_distribution = [np.percentile(As_concentration, 5), np.percentile(As_concentration, 25),
                                np.percentile(As_concentration, 50), np.percentile(As_concentration, 75),
                                np.percentile(As_concentration, 95)]

        hg_conc_distribution = [np.percentile(Hg_concentration, 5), np.percentile(Hg_concentration, 25),
                                np.percentile(Hg_concentration, 50), np.percentile(Hg_concentration, 75),
                                np.percentile(Hg_concentration, 95)]

        b_conc_distribution = [np.percentile(B_concentration, 5), np.percentile(B_concentration, 25),
                                np.percentile(B_concentration, 50), np.percentile(B_concentration, 75),
                                np.percentile(B_concentration, 95)]


        br_conc_distribution = [np.percentile(Br_concentration, 5), np.percentile(Br_concentration, 25),
                                np.percentile(Br_concentration, 50), np.percentile(Br_concentration, 75),
                                np.percentile(Br_concentration, 95)]

        pb_conc_distribution = [np.percentile(Pb_concentration, 5), np.percentile(Pb_concentration, 25),
                                np.percentile(Pb_concentration, 50), np.percentile(Pb_concentration, 75),
                                np.percentile(Pb_concentration, 95)]


        # Create FGD Wastewater concentration data frame.
        concentration_summary = np.array([as_conc_distribution, b_conc_distribution, br_conc_distribution, cl_conc_distribution,
                                          hg_conc_distribution, pb_conc_distribution, se_conc_distribution])
        concentration_summary = pd.DataFrame(concentration_summary, index=['As', 'B', 'Br', 'Cl', 'Hg', 'Pb', 'Se'],
                                             columns=['5th_Percentile', '25th_Percentile', 'Median', '75th_Percentile',
                                                      '95th_Percentile'])

        # Calculate the removal of trace elements that takes place in the FGD wastewater treatment process.  Note that we do
        # not model nitrogen removal performance.

        # Start with chemical precipitation.

        as_cp, cl_cp, pb_cp, hg_cp, se_cp = cp_modeling(cp, runs)
        as_mass_cp, cl_mass_cp, pb_mass_cp, hg_mass_cp, se_mass_cp = mc_wpcd_mass_partitioning(As_fate[:, 1], as_cp,
                                                                                            Cl_fate[:, 1], cl_cp,
                                                                                            Pb_fate[:, 1], pb_cp,
                                                                                            Hg_fate[:, 1], hg_cp,
                                                                                            Se_fate[:, 1], se_cp)

        # And then model the treatment of FGD wastewater to comply with the ELGs.
        if elg == 1:
            as_mbr, cl_mbr, pb_mbr, hg_mbr, se_mbr = mbr_modeling(mbr, runs)
            as_bt, cl_bt, pb_bt, hg_bt, se_bt = bt_modeling(bt, runs)
            as_iex, cl_iex, pb_iex, hg_iex, se_iex = iex_modeling(iex, runs)
            as_alox, cl_alox, pb_alox, hg_alox, se_alox = alox_modeling(alox, runs)
            as_feox, cl_feox, pb_feox, hg_feox, se_feox = feox_modeling(feox, runs)
            as_zvi, cl_zvi, pb_zvi, hg_zvi, se_zvi = zvi_modeling(zvi, runs)
            #as_mass_mbr, cl_mass_mbr, pb_mass_mbr, hg_mass_mbr, se_mass_mbr = mc_wpcd_mass_partitioning(as_mass_cp,
            #                                                                                         as_mbr[:], cl_mass_cp,
            #                                                                                         cl_mbr[:], pb_mass_cp,
            #                                                                                         pb_mbr[:], hg_mass_cp,
            #                                                                                         hg_mbr[:], se_mass_cp,
            #                                                                                         se_mbr[:])

            as_mass_bt, cl_mass_bt, pb_mass_bt, hg_mass_bt, se_mass_bt = mc_wpcd_mass_partitioning(as_mass_cp, as_bt[:],
                                                                                                cl_mass_cp, cl_bt[:],
                                                                                                pb_mass_cp, pb_bt[:],
                                                                                                hg_mass_cp, hg_bt[:],
                                                                                                se_mass_cp, se_bt[:])

            #as_mass_iex, cl_mass_iex, pb_mass_iex, hg_mass_iex, se_mass_iex = mc_wpcd_mass_partitioning(as_mass_bt,
            #                                                                                         as_iex[:], cl_mass_bt,
            #                                                                                         cl_iex[:], pb_mass_bt,
            #                                                                                         pb_iex[:], hg_mass_bt,
            #                                                                                         hg_iex[:], se_mass_bt,
            #                                                                                         se_iex[:])

            #as_mass_alox, cl_mass_alox, pb_mass_alox, hg_mass_alox, se_mass_alox = mc_wpcd_mass_partitioning(as_mass_iex,
            #                                                                                              as_alox[:],
            #                                                                                              cl_mass_iex,
            #                                                                                              cl_alox[:],
            #                                                                                              pb_mass_iex,
            #                                                                                              pb_alox[:],
            #                                                                                              hg_mass_iex,
            #                                                                                              hg_alox[:],
            #                                                                                              se_mass_iex,
            #                                                                                              se_alox[:])

            #as_mass_feox, cl_mass_feox, pb_mass_feox, hg_mass_feox, se_mass_feox = mc_wpcd_mass_partitioning(as_mass_alox,
            #                                                                                              as_feox[:],
            #                                                                                              cl_mass_alox,
            #                                                                                              cl_feox[:],
            #                                                                                              pb_mass_alox,
            #                                                                                              pb_feox[:],
            #                                                                                              hg_mass_alox,
            #                                                                                              hg_feox[:],
            #                                                                                              se_mass_alox,
            #                                                                                              se_feox[:])

            as_mass_zvi, cl_mass_zvi, pb_mass_zvi, hg_mass_zvi, se_mass_zvi = mc_wpcd_mass_partitioning(as_mass_bt,
                                                                                                     as_zvi[:], cl_mass_bt,
                                                                                                     cl_zvi[:], pb_mass_bt,
                                                                                                     pb_zvi[:], hg_mass_bt,
                                                                                                     hg_zvi[:], se_mass_bt,
                                                                                                     se_zvi[:])
            as_fgd_effluent_concentration = fgd_wastewater_concentration(as_mass_zvi, wastewater_production)
            cl_fgd_effluent_concentration = fgd_wastewater_concentration(cl_mass_zvi, wastewater_production)
            pb_fgd_effluent_concentration = fgd_wastewater_concentration(pb_mass_zvi, wastewater_production)
            hg_fgd_effluent_concentration = fgd_wastewater_concentration(hg_mass_zvi, wastewater_production)
            se_fgd_effluent_concentration = fgd_wastewater_concentration(se_mass_zvi, wastewater_production)

        if zld == 1:
            as_mvc, cl_mvc, pb_mvc, hg_mvc, se_mvc = mvc_modeling(mvc, runs)
            as_crys, cl_crys, pb_crys, hg_crys, se_crys = crys_modeling(crys, runs)

            as_mass_mvc, cl_mass_mvc, pb_mass_mvc, hg_mass_mvc, se_mass_mvc = mc_wpcd_mass_partitioning(as_mass_cp, as_mvc[:],
                                                                                                     cl_mass_cp, cl_mvc[:],
                                                                                                     pb_mass_cp, pb_mvc[:],
                                                                                                     hg_mass_cp, hg_mvc[:],
                                                                                                     se_mass_cp, se_mvc[:])

            as_mass_crys, cl_mass_crys, pb_mass_crys, hg_mass_crys, se_mass_crys = wpcd_mass_partitioning(as_mass_mvc, as_crys[:],
                                                                                                cl_mass_mvc, cl_crys[:],
                                                                                                pb_mass_mvc, pb_crys[:],
                                                                                                hg_mass_mvc, hg_crys[:],
                                                                                                se_mass_mvc, se_crys[:])

            as_fgd_effluent_concentration = fgd_wastewater_concentration(as_mass_crys, wastewater_production)
            cl_fgd_effluent_concentration = fgd_wastewater_concentration(cl_mass_crys, wastewater_production)
            pb_fgd_effluent_concentration = fgd_wastewater_concentration(pb_mass_crys, wastewater_production)
            hg_fgd_effluent_concentration = fgd_wastewater_concentration(hg_mass_crys, wastewater_production)
            se_fgd_effluent_concentration = fgd_wastewater_concentration(se_mass_crys, wastewater_production)

        if alox == 0 and iex == 0:
            total_violations, as_violations, hg_violations, se_violations = elg_compliance_check_simulation(elg, zld,
                                                                                                            as_fgd_effluent_concentration,
                                                                                                            cl_fgd_effluent_concentration,
                                                                                                            hg_fgd_effluent_concentration,
                                                                                                            se_fgd_effluent_concentration)
        elif alox == 1 or iex == 1:
            total_violations, as_violations, hg_violations, se_violations = elg_compliance_check_simulation_no_as(elg,
                                                                                                            zld,
                                                                                                            as_fgd_effluent_concentration,
                                                                                                            cl_fgd_effluent_concentration,
                                                                                                            hg_fgd_effluent_concentration,
                                                                                                            se_fgd_effluent_concentration)

        return total_violations, np.median(as_fgd_effluent_concentration), as_violations, \
               np.median(hg_fgd_effluent_concentration), hg_violations, np.median(se_fgd_effluent_concentration), \
               se_violations, np.median(cl_fgd_effluent_concentration), np.median(pb_fgd_effluent_concentration)
