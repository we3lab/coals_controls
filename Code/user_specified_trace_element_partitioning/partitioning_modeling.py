# Import standard python libraries.
import pathlib
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import sys
import pandas as pd
import seaborn as sns


# Import the functions used throughout this project from the function dictionary library file
from statistical_functions import ecdf, random_value_from_ecdf
from valid_coal_test import valid_coal_test
from coal_ecdf import coal_ecdf, weighted_coal_ecdf
from fuel_and_energy_modeling import coal_combustion
from apcd_user_inputs import apcd_user_inputs
from wpcd_user_inputs import wpcd_user_inputs
from wastewater_functions import wastewater_generation, fgd_wastewater_concentration, \
    fgd_wastewater_generation_for_corrosion_limits, wastewater_treatment_electricity_consumption, wastewater_chemical_consumption
from APCD_partition_modeling import bottom_modeling, csESP_modeling, hsESP_modeling, FF_modeling, SCR_modeling, \
    ACI_modeling, DSI_modeling, wetFGD_modeling, dryFGD_modeling, wetFGD_wastewater_Se_modeling
from median_partitioning_scenario import median_partitioning_scenario
from WPCD_partition_modeling import cp_modeling, mbr_modeling, bt_modeling, mvc_modeling, iex_modeling, alox_modeling, \
    feox_modeling, zvi_modeling, crys_modeling, gac_modeling, ro_modeling
from mass_partitioning_calculation import apcd_mass_partitioning, wpcd_mass_partitioning
from elg_compliance_check import elg_compliance_check
from median_partitioning_scenario import partitioning_scenario


fileDir = pathlib.Path(__file__).parents[2]
code_library_folder = fileDir / 'Code' / 'function_dictionary_library'
sys.path.append(str(code_library_folder))


summary_output_filepath = fileDir / 'Results' / 'FGD Wastewater Composition Distributions' / '8 Lig csESP wetFGD Summary.xlsx'
raw_value_output_filepath = fileDir / 'Results' / 'FGD Wastewater Composition Distributions' / '8 Lig csESP wetFGD Raw Values.xlsx'
figure_filepath = fileDir / 'Results' / 'FGD Wastewater Composition Distributions' / '8 Lig csESP wetFGD wetFGD.pdf'

# Select a coal and import the CDFs of Chlorine, Selenium, Boron, Bromine, and Arsenic concentrations in the coal.
coal = input("What coal is the plant burning? The options are 'Appalachian Low Sulfur', 'Appalachian Med Sulfur', "
             "'Beulah-Zap', 'Illinois #6', 'ND Lignite', 'Pocahontas #3', 'Upper Freeport', 'WPC Utah', 'Wyodak', "
             "'Wyodak Anderson', 'Wyoming PRB', 'Bituminous', 'QGESS Bituminous', 'Subbituminous', "
             "'QGESS Subbituminous', or 'Lignite'.")
valid_coal_test(coal)
qe_Cl, pe_Cl, qe_Se, pe_Se, qe_B, pe_B, qe_Br, pe_Br, qe_Pb, pe_Pb, qe_As, pe_As, qe_Hg, pe_Hg, qe_Heat, pe_Heat, \
    qe_S, pe_S, gross_heat_rate, FGD_water_treatment = coal_ecdf(coal)

# Ask the user for the air pollution control systems installed
csESP, hsESP, FF, SCR, ACI, wetFGD, dryFGD, DSI, wetFGD_type = apcd_user_inputs()
if wetFGD == 1:
    elg, zld, cp, mbr, bt, mvc, iex, alox, feox, zvi, crys, gac, ro = wpcd_user_inputs()

# Initialize Monte Carlo Analysis by developing array of concentrations.
runs = 501
mc_Cl_concentration = random_value_from_ecdf(qe_Cl, pe_Cl, runs)  # Concentration is in [mg/kg]
mc_Se_concentration = random_value_from_ecdf(qe_Se, pe_Se, runs)  # Concentration is in [mg/kg]
mc_B_concentration = random_value_from_ecdf(qe_B, pe_B, runs)  # Concentration is in [mg/kg]
mc_Br_concentration = random_value_from_ecdf(qe_Br, pe_Br, runs)  # Concentration is in [mg/kg]
mc_Pb_concentration = random_value_from_ecdf(qe_Pb, pe_Pb, runs)  # Concentration is in [mg/kg]
mc_As_concentration = random_value_from_ecdf(qe_As, pe_As, runs)  # Concentration is in [mg/kg]
mc_Hg_concentration = random_value_from_ecdf(qe_Hg, pe_Hg, runs)  # Concentration is in [mg/kg]
mc_S_concentration = random_value_from_ecdf(qe_S, pe_S, runs)  # Concentration is in [%]
mc_Heat_concentration = random_value_from_ecdf(qe_Heat, pe_Heat, runs)    # Concentration is in [Btu/lb]

print([np.median(mc_Cl_concentration), np.median(mc_Se_concentration), np.median(mc_As_concentration), np.median(mc_Hg_concentration)])

# Calculate the amount of trace elements entering in the coal.  Assume 1 metric tons (1000 kg) of coal is combusted.
electricity_generated = float(input('How much electricity is generated hourly (in MWh)?'))  #MWh of capacity for the plant
coal_combusted = coal_combustion(electricity_generated, mc_Heat_concentration, gross_heat_rate)  # [kg/hr] of coal combusted

Cl_mass_entering = mc_Cl_concentration * coal_combusted  #[mg/hr] of chlorine entering the plant
Se_mass_entering = mc_Se_concentration * coal_combusted  #[mg/hr] of selenium entering the plant
B_mass_entering = mc_B_concentration * coal_combusted    #[mg/hr] of boron entering the plant
Br_mass_entering = mc_Br_concentration * coal_combusted  #[mg/hr] of bromine entering the plant
Pb_mass_entering = mc_Pb_concentration * coal_combusted  #[mg/hr] of lead entering the plant
As_mass_entering = mc_As_concentration * coal_combusted  #[mg/hr] of arsenic entering the plant
Hg_mass_entering = mc_Hg_concentration * coal_combusted  #[mg/hr] of mercury entering the plant
# Note that sulfur concentrations are reported in terms of %.  To maintain consistency with the other units, we convert to mg
S_mass_entering = mc_S_concentration * coal_combusted * 10000  #[mg/hr] of sulfur entering the plant

print([np.median(Cl_mass_entering), np.median(Se_mass_entering), np.median(As_mass_entering), np.median(Hg_mass_entering)])


#Plot a ecdf of the amount of coal combusted.
# qe_coal_combusted, pe_coal_combusted = ecdf(coal_combusted)
# fig, ax = plt.subplots(1,1)
# fig.figsize=(2.8,2.8)
# #ax.hold(True)
# ax.plot(qe_coal_combusted/1000, pe_coal_combusted, '-k', lw=2, label = 'Coal Combusted')
# ax.set_xlabel('Coal Combusted [metric tonnes/hr]')
# ax.set_ylabel('Cumulative Probability')
# ax.set_ylim([0,1])
# plt.show()
# #ax.hold(False)
# ax.clear()
# plt.close()

#Plot a ecdf of the heat rate
# fig, ax = plt.subplots(1,1)
# fig.figsize=(2.8,2.8)
# #ax.hold(True)
# ax.plot(qe_Heat, pe_Heat, '-k', lw=2, label = 'Coal Combusted')
# ax.set_xlabel('Coal Heat Content [Btu/lb]')
# ax.set_ylabel('Cumulative Probability')
# ax.set_ylim([0,1])
# plt.show()
# ax.clear()
# plt.close()

#Create partitioning coefficient simulations.
Cl_bottom, Se_bottom, B_bottom, Br_bottom, Pb_bottom, As_bottom, Hg_bottom, S_bottom = bottom_modeling(runs)
Cl_csESP, Se_csESP, B_csESP, Br_csESP, Pb_csESP, As_csESP, Hg_csESP, S_csESP = csESP_modeling(csESP, runs)
Cl_hsESP, Se_hsESP, B_hsESP, Br_hsESP, Pb_hsESP, As_hsESP, Hg_hsESP, S_hsESP = hsESP_modeling(hsESP, runs)
Cl_FF, Se_FF, B_FF, Br_FF, Pb_FF, As_FF, Hg_FF, S_FF = FF_modeling(FF, runs)
Cl_SCR, Se_SCR, B_SCR, Br_SCR, Pb_SCR, As_SCR, Hg_SCR, S_SCR = SCR_modeling(SCR, runs)
Cl_ACI, Se_ACI, B_ACI, Br_ACI, Pb_ACI, As_ACI, Hg_ACI, S_ACI = ACI_modeling(ACI, runs)
Cl_DSI, Se_DSI, B_DSI, Br_DSI, Pb_DSI, As_DSI, Hg_DSI, S_DSI = DSI_modeling(DSI, runs)
Cl_wetFGD, Se_wetFGD, B_wetFGD, Br_wetFGD, Pb_wetFGD, As_wetFGD, Hg_wetFGD, Se_wetFGD_ww, S_wetFGD = wetFGD_modeling(wetFGD, wetFGD_type, runs)
Cl_dryFGD, Se_dryFGD, B_dryFGD, Br_dryFGD, Pb_dryFGD, As_dryFGD, Hg_dryFGD, S_dryFGD = dryFGD_modeling(dryFGD, runs)

#Calculate partitioning
Cl_mass_bottom, Se_mass_bottom, B_mass_bottom, Br_mass_bottom, Pb_mass_bottom, As_mass_bottom, Hg_mass_bottom, \
S_mass_bottom = apcd_mass_partitioning(runs, Cl_mass_entering, Cl_bottom, Se_mass_entering, Se_bottom, B_mass_entering,
                                       B_bottom, Br_mass_entering, Br_bottom, Pb_mass_entering, Pb_bottom,
                                       As_mass_entering, As_bottom, Hg_mass_entering, Hg_bottom, S_mass_entering,
                                       S_bottom)

Cl_mass_dryFGD, Se_mass_dryFGD, B_mass_dryFGD, Br_mass_dryFGD, Pb_mass_dryFGD, As_mass_dryFGD, Hg_mass_dryFGD, \
S_mass_dryFGD = apcd_mass_partitioning(runs, Cl_mass_bottom[:,2], Cl_dryFGD, Se_mass_bottom[:,2], Se_dryFGD,
                                       B_mass_bottom[:,2], B_dryFGD, Br_mass_bottom[:,2], Br_dryFGD,
                                       Pb_mass_bottom[:,2], Pb_dryFGD, As_mass_bottom[:,2], As_dryFGD,
                                       Hg_mass_bottom[:,2], Hg_dryFGD, S_mass_bottom[:,2], S_dryFGD)

Cl_mass_csESP, Se_mass_csESP, B_mass_csESP, Br_mass_csESP, Pb_mass_csESP, As_mass_csESP, Hg_mass_csESP, S_mass_csESP = apcd_mass_partitioning(runs,
    Cl_mass_dryFGD[:,2], Cl_csESP, Se_mass_dryFGD[:,2], Se_csESP, B_mass_dryFGD[:,2], B_csESP, Br_mass_dryFGD[:,2],
    Br_csESP, Pb_mass_dryFGD[:,2], Pb_csESP, As_mass_dryFGD[:,2], As_csESP, Hg_mass_dryFGD[:,2], Hg_csESP,
    S_mass_dryFGD[:,2], S_csESP)

Cl_mass_hsESP, Se_mass_hsESP, B_mass_hsESP, Br_mass_hsESP, Pb_mass_hsESP, As_mass_hsESP, Hg_mass_hsESP, S_mass_hsESP = apcd_mass_partitioning(runs,
    Cl_mass_csESP[:,2], Cl_hsESP, Se_mass_csESP[:,2], Se_hsESP, B_mass_csESP[:,2], B_hsESP, Br_mass_csESP[:,2],
    Br_hsESP, Pb_mass_csESP[:,2], Pb_hsESP, As_mass_csESP[:,2], As_hsESP, Hg_mass_csESP[:,2], Hg_hsESP,
    S_mass_csESP[:,2], S_hsESP)

Cl_mass_FF, Se_mass_FF, B_mass_FF, Br_mass_FF, Pb_mass_FF, As_mass_FF, Hg_mass_FF, S_mass_FF = apcd_mass_partitioning(runs,
    Cl_mass_hsESP[:,2], Cl_FF, Se_mass_hsESP[:,2], Se_FF, B_mass_hsESP[:,2], B_FF, Br_mass_hsESP[:,2], Br_FF,
    Pb_mass_hsESP[:,2], Pb_FF, As_mass_hsESP[:,2], As_FF, Hg_mass_hsESP[:,2], Hg_FF, S_mass_hsESP[:,2], S_FF)

Cl_mass_SCR, Se_mass_SCR, B_mass_SCR, Br_mass_SCR, Pb_mass_SCR, As_mass_SCR, Hg_mass_SCR, S_mass_SCR = apcd_mass_partitioning(runs,
    Cl_mass_FF[:,2], Cl_SCR, Se_mass_FF[:,2], Se_SCR, B_mass_FF[:,2], B_SCR, Br_mass_FF[:,2], Br_SCR, Pb_mass_FF[:,2],
    Pb_SCR, As_mass_FF[:,2], As_SCR, Hg_mass_FF[:,2], Hg_SCR, S_mass_FF[:,2], S_SCR)

Cl_mass_ACI, Se_mass_ACI, B_mass_ACI, Br_mass_ACI, Pb_mass_ACI, As_mass_ACI, Hg_mass_ACI, S_mass_ACI = apcd_mass_partitioning(runs,
    Cl_mass_SCR[:,2], Cl_ACI, Se_mass_SCR[:,2], Se_ACI, B_mass_SCR[:,2], B_ACI, Br_mass_SCR[:,2],
    Br_ACI, Pb_mass_SCR[:,2], Pb_ACI, As_mass_SCR[:,2], As_ACI, Hg_mass_SCR[:,2], Hg_ACI, S_mass_SCR[:,2], S_ACI)

Cl_mass_DSI, Se_mass_DSI, B_mass_DSI, Br_mass_DSI, Pb_mass_DSI, As_mass_DSI, Hg_mass_DSI, S_mass_DSI = apcd_mass_partitioning(runs,
    Cl_mass_ACI[:,2], Cl_DSI, Se_mass_ACI[:,2], Se_DSI, B_mass_ACI[:,2], B_DSI, Br_mass_ACI[:,2],
    Br_DSI, Pb_mass_ACI[:,2], Pb_DSI, As_mass_ACI[:,2], As_DSI, Hg_mass_ACI[:,2], Hg_DSI, S_mass_ACI[:,2], S_DSI)

Cl_mass_wetFGD, Se_mass_wetFGD, B_mass_wetFGD, Br_mass_wetFGD, Pb_mass_wetFGD, As_mass_wetFGD, Hg_mass_wetFGD, S_mass_wetFGD = apcd_mass_partitioning(runs,
    Cl_mass_ACI[:,2], Cl_wetFGD, Se_mass_ACI[:,2], Se_wetFGD, B_mass_ACI[:,2], B_wetFGD, Br_mass_ACI[:,2],
    Br_wetFGD, Pb_mass_ACI[:,2], Pb_wetFGD, As_mass_ACI[:,2], As_wetFGD, Hg_mass_ACI[:,2], Hg_wetFGD, S_mass_ACI[:,2],
    S_wetFGD)

Cl_mass_dryFGD, Se_mass_dryFGD, B_mass_dryFGD, Br_mass_dryFGD, Pb_mass_dryFGD, As_mass_dryFGD, Hg_mass_dryFGD, S_mass_dryFGD = apcd_mass_partitioning(runs,
    Cl_mass_wetFGD[:,2], Cl_dryFGD, Se_mass_wetFGD[:,2], Se_dryFGD, B_mass_wetFGD[:,2], B_dryFGD, Br_mass_wetFGD[:,2],
    Br_dryFGD, Pb_mass_wetFGD[:,2], Pb_dryFGD, As_mass_wetFGD[:,2], As_dryFGD, Hg_mass_wetFGD[:,2], Hg_dryFGD,
    S_mass_wetFGD[:,2], S_dryFGD)

# Calculate total mass splits.  All units are in [mg/hr]
Cl_fate=Cl_mass_bottom+Cl_mass_csESP+Cl_mass_hsESP+Cl_mass_FF+Cl_mass_SCR+Cl_mass_ACI+Cl_mass_DSI+Cl_mass_wetFGD+Cl_mass_dryFGD
Cl_fate[:,2]=Cl_mass_dryFGD[:,2]

Se_fate=Se_mass_bottom+Se_mass_csESP+Se_mass_hsESP+Se_mass_FF+Se_mass_SCR+Se_mass_ACI+Se_mass_DSI+Se_mass_wetFGD+Se_mass_dryFGD
Se_fate[:,2]=Se_mass_dryFGD[:,2]

B_fate=B_mass_bottom+B_mass_csESP+B_mass_hsESP+B_mass_FF+B_mass_SCR+B_mass_ACI+B_mass_DSI+B_mass_wetFGD+B_mass_dryFGD
B_fate[:,2]=B_mass_dryFGD[:,2]

Br_fate=Br_mass_bottom+Br_mass_csESP+Br_mass_hsESP+Br_mass_FF+Br_mass_SCR+Br_mass_ACI+Br_mass_DSI+Br_mass_wetFGD+Br_mass_dryFGD
Br_fate[:,2]=Br_mass_dryFGD[:,2]

Pb_fate=Pb_mass_bottom+Pb_mass_csESP+Pb_mass_hsESP+Pb_mass_FF+Pb_mass_SCR+Pb_mass_ACI+Pb_mass_DSI+Pb_mass_wetFGD+Pb_mass_dryFGD
Pb_fate[:,2]=Pb_mass_dryFGD[:,2]

As_fate=As_mass_bottom+As_mass_csESP+As_mass_hsESP+As_mass_FF+As_mass_SCR+As_mass_ACI+As_mass_DSI+As_mass_wetFGD+As_mass_dryFGD
As_fate[:,2]=As_mass_dryFGD[:,2]

Hg_fate=Hg_mass_bottom+Hg_mass_csESP+Hg_mass_hsESP+Hg_mass_FF+Hg_mass_SCR+Hg_mass_ACI+Hg_mass_ACI+Hg_mass_wetFGD+Hg_mass_dryFGD
Hg_fate[:,2]=Hg_mass_dryFGD[:,2]

S_fate=S_mass_bottom+S_mass_csESP+S_mass_hsESP+S_mass_FF+S_mass_SCR+S_mass_ACI+S_mass_DSI+S_mass_wetFGD+S_mass_dryFGD
S_fate[:,2]=S_mass_dryFGD[:,2]

if wetFGD == 1:
    wastewater_production = fgd_wastewater_generation_for_corrosion_limits(Cl_fate[:, 1]) #[m^3/hr] of FGD wastewater produced
else:
    wastewater_production = 0

# Plot Wastewater Flow Rate ECDFs
qe_wastewater, pe_wastewater = ecdf(wastewater_production)
fig, ax = plt.subplots(1,1)
fig.figsize=(2.8,2.8)
#ax.hold(True)
ax.plot(qe_wastewater, pe_wastewater, '-k', lw=2, label = 'Solid')
ax.set_xlabel('Wastewater Flow Rate [m^3/hr]')
ax.set_ylabel('Cumulative Probability')
ax.set_ylim([0,1])
#ax.set_adjustable(box = )
plt.show()
Wastewater_CDF = fileDir / 'Results' / 'Mass Balance' / 'Wastewater Flowrate.pdf'
fig.savefig(str(Wastewater_CDF), bbox_inches='tight')
#ax.hold(False)
ax.clear()
plt.close()

# Plot Chlorine Fate ECDFs
qe_Cl_fate_solid, pe_Cl_fate_solid = ecdf(Cl_fate[:,0])
qe_Cl_fate_liquid, pe_Cl_fate_liquid = ecdf(Cl_fate[:,1])
qe_Cl_fate_gas, pe_Cl_fate_gas = ecdf(Cl_fate[:,2])
fig, ax = plt.subplots(1,1)
fig.figsize=(2.8,2.8)
#ax.hold(True)
ax.plot(qe_Cl_fate_solid, pe_Cl_fate_solid, '-k', lw=2, label = 'Solid')
ax.plot(qe_Cl_fate_liquid, pe_Cl_fate_liquid, '-b', lw=2, label = 'Liquid')
ax.plot(qe_Cl_fate_gas, pe_Cl_fate_gas, '-r', lw=2, label = 'Gas')
ax.set_xlabel('Chlorine Mass [mg]')
ax.set_ylabel('Cumulative Probability')
ax.set_ylim([0,1])
#ax.set_adjustable(box = )
plt.show()
Chloride_CDF = fileDir / 'Results' / 'Mass Balance' / 'Chloride CDF.pdf'
fig.savefig(str(Chloride_CDF), bbox_inches='tight')
#ax.hold(False)
ax.clear()
plt.close()


#Calculate summary statistics for Chlorine
cl_summary_statistics = median_partitioning_scenario(Cl_fate)


#Plot Selenium Fate ECDFs
qe_Se_fate_solid, pe_Se_fate_solid = ecdf(Se_fate[:,0])
qe_Se_fate_liquid, pe_Se_fate_liquid = ecdf(Se_fate[:,1])
qe_Se_fate_gas, pe_Se_fate_gas = ecdf(Se_fate[:,2])
fig, ax = plt.subplots(1,1)
fig.figsize=(2.8,2.8)
#ax.hold(True)
ax.plot(qe_Se_fate_solid, pe_Se_fate_solid, '-k', lw=2, label = 'Solid')
ax.plot(qe_Se_fate_liquid, pe_Se_fate_liquid, '-b', lw=2, label = 'Liquid')
ax.plot(qe_Se_fate_gas, pe_Se_fate_gas, '-r', lw=2, label = 'Gas')
ax.set_xlabel('Selenium Mass [mg]')
ax.set_ylabel('Cumulative Probability')
ax.set_ylim([0,1])
#ax.set_adjustable(box = )
plt.show()
Selenium_CDF = fileDir / 'Results' / 'Mass Balance' / 'Selenium CDF.pdf'
fig.savefig(str(Selenium_CDF), bbox_inches='tight')
#ax.hold(False)
ax.clear()
plt.close()

#Calculate summary statitics for Selenium
se_summary_statistics = median_partitioning_scenario(Se_fate)


#Plot Arsenic Fate ECDFs
qe_As_fate_solid, pe_As_fate_solid = ecdf(As_fate[:,0])
qe_As_fate_liquid, pe_As_fate_liquid = ecdf(As_fate[:,1])
qe_As_fate_gas, pe_As_fate_gas = ecdf(As_fate[:,2])
fig, ax = plt.subplots(1,1)
fig.figsize=(2.8,2.8)
#ax.hold(True)
ax.plot(qe_As_fate_solid, pe_As_fate_solid, '-k', lw=2, label = 'Solid')
ax.plot(qe_As_fate_liquid, pe_As_fate_liquid, '-b', lw=2, label = 'Liquid')
ax.plot(qe_As_fate_gas, pe_As_fate_gas, '-r', lw=2, label = 'Gas')
ax.set_xlabel('Arsenic Mass [mg]')
ax.set_ylabel('Cumulative Probability')
ax.set_ylim([0,1])
#ax.set_adjustable(box = )
plt.show()
Arsenic_CDF = fileDir / 'Results' / 'Mass Balance' / 'Arsenic CDF.pdf'
fig.savefig(str(Arsenic_CDF), bbox_inches='tight')
#ax.hold(False)
ax.clear()
plt.close()
#Calculate summary statitics for Arsenic
as_summary_statistics = median_partitioning_scenario(As_fate)

#Plot Mercury Fate ECDFs
qe_Hg_fate_solid, pe_Hg_fate_solid = ecdf(Hg_fate[:,0])
qe_Hg_fate_liquid, pe_Hg_fate_liquid = ecdf(Hg_fate[:,1])
qe_Hg_fate_gas, pe_Hg_fate_gas = ecdf(Hg_fate[:,2])
fig, ax = plt.subplots(1,1)
fig.figsize=(2.8,2.8)
#ax.hold(True)
ax.plot(qe_Hg_fate_solid, pe_Hg_fate_solid, '-k', lw=2, label = 'Solid')
ax.plot(qe_Hg_fate_liquid, pe_Hg_fate_liquid, '-b', lw=2, label = 'Liquid')
ax.plot(qe_Hg_fate_gas, pe_Hg_fate_gas, '-r', lw=2, label = 'Gas')
ax.set_xlabel('Mercury Mass [mg]')
ax.set_ylabel('Cumulative Probability')
ax.set_ylim([0,1])
#ax.set_adjustable(box = )
plt.show()
Mercury_CDF = fileDir / 'Results' / 'Mass Balance' / 'Mercury CDF.pdf'
fig.savefig(str(Mercury_CDF), bbox_inches='tight')
#ax.hold(False)
ax.clear()
plt.close()

#Calculate summary statitics for Mercury
hg_summary_statistics = median_partitioning_scenario(Hg_fate)


#Plot Boron Fate ECDFs
qe_B_fate_solid, pe_B_fate_solid = ecdf(B_fate[:,0])
qe_B_fate_liquid, pe_B_fate_liquid = ecdf(B_fate[:,1])
qe_B_fate_gas, pe_B_fate_gas = ecdf(B_fate[:,2])
fig, ax = plt.subplots(1,1)
fig.figsize=(2.8,2.8)
#ax.hold(True)
ax.plot(qe_B_fate_solid, pe_B_fate_solid, '-k', lw=2, label = 'Solid')
ax.plot(qe_B_fate_liquid, pe_B_fate_liquid, '-b', lw=2, label = 'Liquid')
ax.plot(qe_B_fate_gas, pe_B_fate_gas, '-r', lw=2, label = 'Gas')
ax.set_xlabel('Boron Mass [mg]')
ax.set_ylabel('Cumulative Probability')
ax.set_ylim([0,1])
#ax.set_adjustable(box = )
plt.show()
Boron_CDF = fileDir / 'Results' / 'Mass Balance' / 'Boron CDF.pdf'
fig.savefig(str(Boron_CDF), bbox_inches='tight')
#ax.hold(False)
ax.clear()
plt.close()

#Calculate summary statitics for Boron
b_summary_statistics = median_partitioning_scenario(B_fate)

#Plot Bromide Fate ECDFs
qe_Br_fate_solid, pe_Br_fate_solid = ecdf(Br_fate[:,0])
qe_Br_fate_liquid, pe_Br_fate_liquid = ecdf(Br_fate[:,1])
qe_Br_fate_gas, pe_Br_fate_gas = ecdf(Br_fate[:,2])
fig, ax = plt.subplots(1,1)
fig.figsize=(2.8,2.8)
#ax.hold(True)
ax.plot(qe_Br_fate_solid, pe_Br_fate_solid, '-k', lw=2, label = 'Solid')
ax.plot(qe_Br_fate_liquid, pe_Br_fate_liquid, '-b', lw=2, label = 'Liquid')
ax.plot(qe_Br_fate_gas, pe_Br_fate_gas, '-r', lw=2, label = 'Gas')
ax.set_xlabel('Bromide Mass [mg]')
ax.set_ylabel('Cumulative Probability')
ax.set_ylim([0,1])
#ax.set_adjustable(box = )
plt.show()
Bromide_CDF = fileDir / 'Results' / 'Mass Balance' / 'Bromide CDF.pdf'
fig.savefig(str(Bromide_CDF), bbox_inches='tight')
#ax.hold(False)
ax.clear()
plt.close()

#Calculate summary statitics for Bromide
br_summary_statistics = median_partitioning_scenario(Br_fate)

#Plot Lead Fate ECDFs
qe_Pb_fate_solid, pe_Pb_fate_solid = ecdf(Pb_fate[:,0])
qe_Pb_fate_liquid, pe_Pb_fate_liquid = ecdf(Pb_fate[:,1])
qe_Pb_fate_gas, pe_Pb_fate_gas = ecdf(Pb_fate[:,2])
fig, ax = plt.subplots(1,1)
fig.figsize=(2.8,2.8)
#ax.hold(True)
ax.plot(qe_Pb_fate_solid, pe_Pb_fate_solid, '-k', lw=2, label = 'Solid')
ax.plot(qe_Pb_fate_liquid, pe_Pb_fate_liquid, '-b', lw=2, label = 'Liquid')
ax.plot(qe_Pb_fate_gas, pe_Pb_fate_gas, '-r', lw=2, label = 'Gas')
ax.set_xlabel('Lead Mass [mg]')
ax.set_ylabel('Cumulative Probability')
ax.set_ylim([0,1])
#ax.set_adjustable(box = )
plt.show()
Lead_CDF = fileDir / 'Results' / 'Mass Balance' / 'Lead CDF.pdf'
fig.savefig(str(Lead_CDF), bbox_inches='tight')
#ax.hold(False)
ax.clear()
plt.close()

#Calculate summary statitics for Lead
Pb_summary_statistics = median_partitioning_scenario(Pb_fate)


#Plot Sulfur Fate ECDFs
qe_S_fate_solid, pe_S_fate_solid = ecdf(S_fate[:,0])
qe_S_fate_liquid, pe_S_fate_liquid = ecdf(S_fate[:,1])
qe_S_fate_gas, pe_S_fate_gas = ecdf(S_fate[:,2])
fig, ax = plt.subplots(1,1)
fig.figsize=(2.8,2.8)
#ax.hold(True)
ax.plot(qe_S_fate_solid, pe_S_fate_solid, '-k', lw=2, label = 'Solid')
ax.plot(qe_S_fate_liquid, pe_S_fate_liquid, '-b', lw=2, label = 'Liquid')
ax.plot(qe_S_fate_gas, pe_S_fate_gas, '-r', lw=2, label = 'Gas')
ax.set_xlabel('Sulfur Mass [mg]')
ax.set_ylabel('Cumulative Probability')
ax.set_ylim([0,1])
#ax.set_adjustable(box = )
plt.show()
Sulfur_CDF = fileDir / 'Results' / 'Mass Balance' / 'Sulfur CDF.pdf'
fig.savefig(str(Sulfur_CDF), bbox_inches='tight')
#ax.hold(False)
ax.clear()
plt.close()

#Calculate summary statitics for Sulfur
s_summary_statistics = median_partitioning_scenario(S_fate)


if wetFGD == 1:
    # Calculate trace element concentration in the FGD wastewater influent

    Cl_concentration = fgd_wastewater_concentration(Cl_fate[:, 1], wastewater_production)  # [g/m^3]
    Se_concentration = fgd_wastewater_concentration(Se_fate[:, 1], wastewater_production)  # [g/m^3]
    B_concentration = fgd_wastewater_concentration(B_fate[:, 1], wastewater_production)  # [g/m^3]
    Br_concentration = fgd_wastewater_concentration(Br_fate[:, 1], wastewater_production)  # [g/m^3]
    Pb_concentration = fgd_wastewater_concentration(Pb_fate[:, 1], wastewater_production)  # [g/m^3]
    As_concentration = fgd_wastewater_concentration(As_fate[:, 1], wastewater_production)  # [g/m^3]
    As_concentration = As_concentration[As_concentration != 0]
    Hg_concentration = fgd_wastewater_concentration(Hg_fate[:, 1], wastewater_production)  # [g/m^3]
    print(Hg_concentration)

    if type(Se_wetFGD_ww) != int:
        # calculate the Se speciation in wetFGD waste water
        Se_speciation = np.zeros(shape=[runs, 4])
        for i in range(0, 4):
            Se_speciation[:, i] = Se_concentration * Se_wetFGD_ww[:, i]  # [g/m^3]

    #Plot Chlorine Concentration ECDF
    # qe_Cl_concentration, pe_Cl_concentration = ecdf(Cl_concentration)
    # fig, ax = plt.subplots(1,1)
    # fig.figsize=(2.8,2.8)
    # #ax.hold(True)
    # ax.plot(qe_Cl_concentration, pe_Cl_concentration, '-k', lw=2)
    # ax.set_xlabel('Chlorine concentration [g/m^3]')
    # ax.set_ylabel('Cumulative Probability')
    # ax.set_ylim([0,1])
    # #ax.set_adjustable(box = )
    # plt.show()
    # Chloride_CDF = fileDir / 'Results' / 'Mass Balance' / 'Chloride Concentration CDF.pdf'
    # fig.savefig(str(Chloride_CDF), bbox_inches='tight')
    # #ax.hold(False)
    # ax.clear()
    # plt.close()

    cl_conc_distribution = [np.percentile(Cl_concentration, 5), np.percentile(Cl_concentration, 25),
                            np.percentile(Cl_concentration, 50), np.percentile(Cl_concentration, 75),
                            np.percentile(Cl_concentration, 95)]

    #Plot Selenium Concentration ECDF
    qe_Se_concentration, pe_Se_concentration = ecdf(Se_concentration)
    fig, ax = plt.subplots(1,1)
    fig.figsize=(2.8,2.8)
    #ax.hold(True)
    ax.plot(qe_Se_concentration, pe_Se_concentration, '-k', lw=2)
    ax.set_xlabel('Selenium concentration [g/m^3]')
    ax.set_ylabel('Cumulative Probability')
    ax.set_ylim([0,1])
    #ax.set_adjustable(box = )
    plt.show()
    Selenium_CDF = fileDir / 'Results' / 'Mass Balance' / 'Selenium Concentration CDF.pdf'
    fig.savefig(str(Selenium_CDF), bbox_inches='tight')
    #ax.hold(False)
    ax.clear()
    plt.close()

    se_conc_distribution = [np.percentile(Se_concentration, 5), np.percentile(Se_concentration, 25),
                            np.percentile(Se_concentration, 50), np.percentile(Se_concentration, 75),
                            np.percentile(Se_concentration, 95)]

##################################
    if type(Se_wetFGD_ww) != int:
        # Plot Selenium Speciation ECDFs
        qe_Se4, pe_Se4 = ecdf(Se_speciation[:,0])
        qe_Se6, pe_Se6 = ecdf(Se_speciation[:,1])
        qe_SeSO3, pe_SeSO3 = ecdf(Se_speciation[:,2])
        qe_Others, pe_Others = ecdf(Se_speciation[:,3])
        qe_se_Total, pe_se_Total = ecdf(Se_speciation[:,0]+Se_speciation[:,1]+Se_speciation[:,2]+Se_speciation[:,3])
        fig, ax = plt.subplots(1,1)
        fig.figsize=(2.8,2.8)
#        ax.hold(True)
        ax.plot(qe_Se4, pe_Se4, '-m', lw=2, label = 'Se4')
        ax.plot(qe_Se6, pe_Se6, '-b', lw=2, label = 'Se6')
        ax.plot(qe_SeSO3, pe_SeSO3, '-r', lw=2, label = 'SeSO3')
        ax.plot(qe_Others, pe_Others, '-g', lw=2, label = 'Others')
        ax.plot(qe_se_Total, pe_se_Total, '-k', lw=2, label = "Total")
        ax.set_xlabel('Selenium Speciation Concentration [g/m^3]')
        ax.set_ylabel('Cumulative Probability')
        ax.legend()
        ax.set_ylim([0,1])
        # #ax.set_adjustable(box = )
        plt.show()
        Selenium_CDF = fileDir / 'Results' / 'Mass Balance' / 'Selenium Speciation CDF.pdf'
        fig.savefig(str(Selenium_CDF), bbox_inches='tight')
#        ax.hold(False)
        ax.clear()
        plt.close()
##########################
    #TODO Put effluent in micro g..
    #Plot Arsenic Concentration ECDF
    # qe_As_concentration, pe_As_concentration = ecdf(As_concentration)
    # fig, ax = plt.subplots(1,1)
    # fig.figsize=(2.8,2.8)
    # #ax.hold(True)
    # ax.plot(qe_As_concentration, pe_As_concentration, '-k', lw=2)
    # ax.set_xlabel('Arsenic concentration [g/m^3]')
    # ax.set_ylabel('Cumulative Probability')
    # ax.set_ylim([0,1])
    # #ax.set_adjustable(box = )
    # plt.show()
    # Arsenic_CDF = fileDir / 'Results' / 'Mass Balance' / 'Arsenic Concentration CDF.pdf'
    # fig.savefig(str(Arsenic_CDF), bbox_inches='tight')
    # #ax.hold(False)
    # ax.clear()
    # plt.close()

    as_conc_distribution = [np.percentile(As_concentration, 5), np.percentile(As_concentration, 25),
                            np.percentile(As_concentration, 50), np.percentile(As_concentration, 75),
                            np.percentile(As_concentration, 95)]

    #Plot Mercury Concentration ECDF
    # qe_Hg_concentration, pe_Hg_concentration = ecdf( Hg_concentration)
    # fig, ax = plt.subplots(1,1)
    # fig.figsize=(2.8,2.8)
    # #ax.hold(True)
    # ax.plot(qe_Hg_concentration, pe_Hg_concentration, '-k', lw=2)
    # ax.set_xlabel('Mercury concentration [g/m^3]')
    # ax.set_ylabel('Cumulative Probability')
    # ax.set_ylim([0,1])
    # #ax.set_adjustable(box = )
    # plt.show()
    # Mercury_CDF = fileDir / 'Results' / 'Mass Balance' / 'Mercury Concentration CDF.pdf'
    # fig.savefig(str(Mercury_CDF), bbox_inches='tight')
    # #ax.hold(False)
    # ax.clear()
    # plt.close()

    hg_conc_distribution = [np.percentile(Hg_concentration, 5), np.percentile(Hg_concentration, 25),
                            np.percentile(Hg_concentration, 50), np.percentile(Hg_concentration, 75),
                            np.percentile(Hg_concentration, 95)]

    #Plot Boron Concentration ECDF
    # qe_B_concentration, pe_B_concentration = ecdf(B_concentration)
    # fig, ax = plt.subplots(1,1)
    # fig.figsize=(2.8,2.8)
    # #ax.hold(True)
    # ax.plot(qe_B_concentration, pe_B_concentration, '-k', lw=2)
    # ax.set_xlabel('Boron concentration [g/m^3]')
    # ax.set_ylabel('Cumulative Probability')
    # ax.set_ylim([0,1])
    # #ax.set_adjustable(box = )
    # plt.show()
    # Boron_CDF = fileDir / 'Results' / 'Mass Balance' / 'Boron Concentration CDF.pdf'
    # fig.savefig(str(Boron_CDF), bbox_inches='tight')
    # #ax.hold(False)
    # ax.clear()
    # plt.close()

    b_conc_distribution = [np.percentile(B_concentration, 5), np.percentile(B_concentration, 25),
                            np.percentile(B_concentration, 50), np.percentile(B_concentration, 75),
                            np.percentile(B_concentration, 95)]

    #Plot Bromine Concentration ECDF
    # qe_Br_concentration, pe_Br_concentration = ecdf(Br_concentration)
    # fig, ax = plt.subplots(1,1)
    # fig.figsize=(2.8,2.8)
    # #ax.hold(True)
    # ax.plot(qe_Br_concentration, pe_Br_concentration, '-k', lw=2)
    # ax.set_xlabel('Bromine concentration [g/m^3]')
    # ax.set_ylabel('Cumulative Probability')
    # ax.set_ylim([0,1])
    # #ax.set_adjustable(box = )
    # plt.show()
    # Bromine_CDF = fileDir / 'Results' / 'Mass Balance' / 'Bromine Concentration CDF.pdf'
    # fig.savefig(str(Bromine_CDF), bbox_inches='tight')
    # #ax.hold(False)
    # ax.clear()
    # plt.close()

    br_conc_distribution = [np.percentile(Br_concentration, 5), np.percentile(Br_concentration, 25),
                            np.percentile(Br_concentration, 50), np.percentile(Br_concentration, 75),
                            np.percentile(Br_concentration, 95)]

    #Plot Lead Concentration ECDF
    # qe_Pb_concentration, pe_Pb_concentration = ecdf(Pb_concentration)
    # fig, ax = plt.subplots(1,1)
    # fig.figsize=(2.8,2.8)
    # #ax.hold(True)
    # ax.plot(qe_Pb_concentration, pe_Pb_concentration, '-k', lw=2)
    # ax.set_xlabel('Lead concentration [g/m^3]')
    # ax.set_ylabel('Cumulative Probability')
    # ax.set_ylim([0,1])
    # #ax.set_adjustable(box = )
    # plt.show()
    # Lead_CDF = fileDir / 'Results' / 'Mass Balance' / 'Lead Concentration CDF.pdf'
    # fig.savefig(str(Lead_CDF), bbox_inches='tight')
    # #ax.hold(False)
    # ax.clear()
    # plt.close()

    pb_conc_distribution = [np.percentile(Pb_concentration, 5), np.percentile(Pb_concentration, 25),
                            np.percentile(Pb_concentration, 50), np.percentile(Pb_concentration, 75),
                            np.percentile(Pb_concentration, 95)]


    # Create FGD Wastewater summary concentration data frame.
    concentration_summary = np.array([as_conc_distribution, b_conc_distribution, br_conc_distribution, cl_conc_distribution,
                                      hg_conc_distribution, pb_conc_distribution, se_conc_distribution])
    concentration_summary = pd.DataFrame(concentration_summary, index=['As', 'B', 'Br', 'Cl', 'Hg', 'Pb', 'Se'],
                                         columns=['5th_Percentile', '25th_Percentile', 'Median', '75th_Percentile',
                                                  '95th_Percentile'])
    concentration_summary.to_excel(summary_output_filepath)

    empty_array = np.empty([len(B_concentration) - len(As_concentration), 1])
    empty_array[:] = np.nan
    As_concentration_empty = np.append(As_concentration, empty_array)

    # Create FGD Wastewater raw concentration data frame.
    concentration_raw = np.column_stack([As_concentration_empty, B_concentration, Br_concentration, Cl_concentration,
                                         Hg_concentration, Pb_concentration, Se_concentration])
    concentration_raw = pd.DataFrame(concentration_raw, columns=['As', 'B', 'Br', 'Cl', 'Hg', 'Pb', 'Se'])
    concentration_raw.to_excel(raw_value_output_filepath)


    # Create FGD concentration boxplot
    fig, ax = plt.subplots(1, 1)
    fig.figsize = (2.8, 2.8)
    medianprops = dict(color='k')
    boxprops = dict(color='k')
    flierprops = dict(color='k')
    capprops = dict(color='k')
    whiskerprops = dict(color='k')

    ax.boxplot([np.log10(As_concentration), np.log10(Hg_concentration), np.log10(Pb_concentration),
                np.log10(Se_concentration), np.log10(B_concentration), np.log10(Br_concentration),
                np.log10(Cl_concentration)], whis=[5, 95], labels=['As', 'Hg', 'Pb', 'Se', 'B', 'Br', 'Cl'],
               medianprops=medianprops, boxprops=boxprops, flierprops=flierprops, capprops=capprops,
               whiskerprops=whiskerprops)
    ax.set_ylabel('Concentration [mg/L]')
    #fig.savefig(figure_filepath, bbox_inches='tight')
    plt.show()
    plt.close()

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
        as_gac, cl_gac, pb_gac, hg_gac, se_gac = gac_modeling(gac, runs)
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

        as_mass_gac, cl_mass_gac, pb_mass_gac, hg_mass_gac, se_mass_gac = wpcd_mass_partitioning(runs, as_mass_zvi[:, 1],
                                                                                                 as_gac, cl_mass_zvi[:, 1],
                                                                                                 cl_gac, pb_mass_zvi[:, 1],
                                                                                                 pb_gac, hg_mass_zvi[:, 1],
                                                                                                 hg_gac, se_mass_zvi[:, 1],
                                                                                                 se_gac)

        as_fgd_effluent_concentration = fgd_wastewater_concentration(as_mass_gac[:, 1], wastewater_production)
        cl_fgd_effluent_concentration = fgd_wastewater_concentration(cl_mass_gac[:, 1], wastewater_production)
        pb_fgd_effluent_concentration = fgd_wastewater_concentration(pb_mass_gac[:, 1], wastewater_production)
        hg_fgd_effluent_concentration = fgd_wastewater_concentration(hg_mass_gac[:, 1], wastewater_production)
        se_fgd_effluent_concentration = fgd_wastewater_concentration(se_mass_gac[:, 1], wastewater_production)

    if zld == 1:
        as_mvc, cl_mvc, pb_mvc, hg_mvc, se_mvc = mvc_modeling(mvc, runs)
        as_ro, cl_ro, pb_ro, hg_ro, se_ro = ro_modeling(ro, runs)
        as_crys, cl_crys, pb_crys, hg_crys, se_crys = crys_modeling(crys, runs)

        as_mass_mvc, cl_mass_mvc, pb_mass_mvc, hg_mass_mvc, se_mass_mvc = wpcd_mass_partitioning(runs, as_mass_cp[:, 1], as_mvc,
                                                                                                 cl_mass_cp[:, 1], cl_mvc,
                                                                                                 pb_mass_cp[:, 1], pb_mvc,
                                                                                                 hg_mass_cp[:, 1], hg_mvc,
                                                                                                 se_mass_cp[:, 1], se_mvc)

        as_mass_ro, cl_mass_ro, pb_mass_ro, hg_mass_ro, se_mass_ro = wpcd_mass_partitioning(runs, as_mass_mvc[:, 1], as_ro,
                                                                                            cl_mass_mvc[:, 1], cl_ro,
                                                                                            pb_mass_mvc[:, 1], pb_ro,
                                                                                            hg_mass_mvc[:, 1], hg_ro,
                                                                                            se_mass_mvc[:, 1], se_ro)

        as_mass_crys, cl_mass_crys, pb_mass_crys, hg_mass_crys, se_mass_crys = wpcd_mass_partitioning(runs, as_mass_ro[:, 1], as_crys,
                                                                                            cl_mass_ro[:, 1], cl_crys,
                                                                                            pb_mass_ro[:, 1], pb_crys,
                                                                                            hg_mass_ro[:, 1], hg_crys,
                                                                                            se_mass_ro[:, 1], se_crys)
        as_mass_distillate = as_mass_mvc[:, 0] + as_mass_ro[:, 0] + as_mass_crys[:, 1]
        cl_mass_distillate = cl_mass_mvc[:, 0] + cl_mass_ro[:, 0] + cl_mass_crys[:, 1]
        pb_mass_distillate = pb_mass_mvc[:, 0] + pb_mass_ro[:, 0] + pb_mass_crys[:, 1]
        hg_mass_distillate = hg_mass_mvc[:, 0] + hg_mass_ro[:, 0] + hg_mass_crys[:, 1]
        se_mass_distillate = se_mass_mvc[:, 0] + se_mass_ro[:, 0] + se_mass_crys[:, 1]

        as_fgd_effluent_concentration = fgd_wastewater_concentration(as_mass_distillate, wastewater_production)
        cl_fgd_effluent_concentration = fgd_wastewater_concentration(cl_mass_distillate, wastewater_production)
        pb_fgd_effluent_concentration = fgd_wastewater_concentration(pb_mass_distillate, wastewater_production)
        hg_fgd_effluent_concentration = fgd_wastewater_concentration(hg_mass_distillate, wastewater_production)
        se_fgd_effluent_concentration = fgd_wastewater_concentration(se_mass_distillate, wastewater_production)
    original_length = len(hg_fgd_effluent_concentration)
    hg_fgd_effluent_concentration = hg_fgd_effluent_concentration[hg_fgd_effluent_concentration != 0]
    no_zero_length = len(hg_fgd_effluent_concentration)
    print(original_length, no_zero_length, no_zero_length / original_length)
    # Plot Arsenic Concentration PDFs
    # fig = figure(num=None, figsize=(3.3, 3.3), dpi=80, facecolor="w", edgecolor='k')
    # log_effluent = np.log10(as_fgd_effluent_concentration)
    # log_effluent = log_effluent[~np.isinf(log_effluent)]
    # ax = sns.distplot(np.log10(log_effluent), color=[153/255, 153/255, 153/255], hist=False, kde=True, kde_kws={'linewidth': 2})
    # kde_x, kde_y = ax.lines[0].get_data()
    # ax.fill_between(kde_x, kde_y, where=(kde_x > np.log10(0.008)), interpolate=True, color=[153/255, 153/255, 153/255])
    # sns.distplot(np.log10(As_concentration), color=[228/255, 26/255, 28/255], hist=False, kde=True,
    #              kde_kws={'linewidth': 2}, label='Influent')
    # if cp == 1 and (mbr + bt + iex + alox + feox + zvi != 0):
    #     sns.distplot(np.log10(fgd_wastewater_concentration(as_mass_cp[:,1], wastewater_production)),
    #                  color=[55/255, 126/255, 184/255], hist=False, kde=True, kde_kws={'linewidth': 2},
    #                  label='CP')
    # if mbr == 1 and (bt + iex + alox + feox + zvi != 0):
    #     sns.distplot(np.log10(fgd_wastewater_concentration(as_mass_mbr[:,1], wastewater_production)),
    #                  color=[77/ 255, 175/ 255, 74/ 255], hist=False, kde=True, kde_kws={'linewidth': 2},
    #                  label='MBR')
    # if bt == 1 and (iex + alox + feox + zvi + gac != 0):
    #     sns.distplot(np.log10(fgd_wastewater_concentration(as_mass_bt[:,1], wastewater_production)),
    #                  color=[152/ 255, 78/ 255, 163/ 255], hist=False, kde=True, kde_kws={'linewidth': 2},
    #                  label='Bio')
    # if iex == 1 and (alox + feox + zvi + gac != 0):
    #     sns.distplot(np.log10(fgd_wastewater_concentration(as_mass_iex[:,1], wastewater_production)),
    #                  color=[255/255, 127/ 255, 0/ 255], hist=False, kde=True, kde_kws={'linewidth': 2},
    #                  label='IEx')
    # if alox == 1 and (feox + zvi + gac != 0):
    #     sns.distplot(np.log10(fgd_wastewater_concentration(as_mass_alox[:,1], wastewater_production)),
    #                  color=[255/ 255, 255/ 255, 51/ 255], hist=False, kde=True, kde_kws={'linewidth': 2},
    #                  label='AlOx')
    # if feox == 1 and (zvi + gac != 0):
    #     sns.distplot(np.log10(fgd_wastewater_concentration(as_mass_feox[:,1], wastewater_production)),
    #                  color=[166/255, 86/255, 40/255], hist=False, kde=True, kde_kws={'linewidth': 2},
    #                  label='FeOx')
    # if zvi == 1 and gac != 0:
    #     sns.distplot(np.log10(fgd_wastewater_concentration(as_mass_alox[:,1], wastewater_production)),
    #                  color=[247/255, 129/255, 191/255], hist=False, kde=True, kde_kws={'linewidth': 2},
    #                  label='ZVI')
    # ax = sns.distplot(np.log10(as_fgd_effluent_concentration), color=[153/255, 153/255, 153/255], hist=False, kde=True,
    #              kde_kws={'linewidth': 2}, label='Effluent')
    # plt.axvline(np.log10(0.008), color='black')
    # ax.set_xlabel('Arsenic Concentration [mg/L]', fontsize=12, fontname='Arial')
    # ax.set_ylabel('Probability Density', fontsize=12, fontname='Arial')
    # ax.set_ylim([0, 0.4])
    # ax.set_xlim([-12, 6])
    # plt.yticks([0, 0.1, 0.2, 0.3, 0.4], fontsize=10, fontname='Arial')
    # plt.xticks([-12, -9, -6, -3, 0, 3, 6])
    # plt.legend(prop={'family': 'Arial', 'size': 10}, loc='upper left', frameon=False)
    # ax.set_position([0.2, 0.15, 0.75, 0.75])
    # plt.show()

    # Plot Selenium Concentration PDFs
    fig = figure(num=None, figsize=(3.3, 3.3), dpi=80, facecolor="w", edgecolor='k')
    ax = sns.distplot(np.log10(se_fgd_effluent_concentration), color=[153/255, 153/255, 153/255], hist=False, kde=True,
                 kde_kws={'linewidth': 2})
    kde_x, kde_y = ax.lines[0].get_data()
    ax.fill_between(kde_x, kde_y, where=(kde_x > np.log10(0.012)), interpolate=True, color=[153/255, 153/255, 153/255])
    sns.distplot(np.log10(Se_concentration), color=[228 / 255, 26 / 255, 28 / 255], hist=False, kde=True,
                 kde_kws={'linewidth': 2}, label='Influent')
    if cp == 1 and (mbr + bt + iex + alox + feox + zvi != 0):
        sns.distplot(np.log10(fgd_wastewater_concentration(se_mass_cp[:, 1], wastewater_production)),
                     color=[55 / 255, 126 / 255, 184 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                     label='Chemical Precipitation')
    if mbr == 1 and (bt + iex + alox + feox + zvi != 0):
        sns.distplot(np.log10(fgd_wastewater_concentration(se_mass_mbr[:, 1], wastewater_production)),
                     color=[77 / 255, 175 / 255, 74 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                     label='Membrane Bioreactor')
    if bt == 1 and (iex + alox + feox + zvi + gac != 0):
        sns.distplot(np.log10(fgd_wastewater_concentration(se_mass_bt[:, 1], wastewater_production)),
                     color=[152 / 255, 78 / 255, 163 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                     label='Biological Treatment')
    if iex == 1 and (alox + feox + zvi + gac != 0):
        sns.distplot(np.log10(fgd_wastewater_concentration(se_mass_iex[:, 1], wastewater_production)),
                     color=[255 / 255, 127 / 255, 0 / 255], hist=False, kde=True, kde_kws={'linewidth': 2})
    if alox == 1 and (feox + zvi + gac != 0):
        sns.distplot(np.log10(fgd_wastewater_concentration(se_mass_alox[:, 1], wastewater_production)),
                     color=[255 / 255, 255 / 255, 51 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                     label='Aluminum Oxide')
    if feox == 1 and (zvi + gac != 0):
        sns.distplot(np.log10(fgd_wastewater_concentration(se_mass_feox[:, 1], wastewater_production)),
                     color=[166 / 255, 86 / 255, 40 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                     label='Iron Oxide')
    if zvi == 1 and gac != 0:
        sns.distplot(np.log10(fgd_wastewater_concentration(se_mass_alox[:, 1], wastewater_production)),
                     color=[247 / 255, 129 / 255, 191 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                     label='Zero-Valent Iron')
    ax = sns.distplot(np.log10(se_fgd_effluent_concentration), color=[153/255, 153/255, 153/255], hist=False, kde=True,
                 kde_kws={'linewidth': 2}, label='Effluent')
    plt.axvline(np.log10(0.012), color='black')
    ax.set_xlabel('Selenium Concentration [mg/L]', fontsize=12, fontname='Arial')
    ax.set_ylabel('Probability Density', fontsize=12, fontname='Arial')
    ax.set_ylim([0, 0.4])
    plt.yticks([0, 0.1, 0.2, 0.3, 0.4], fontsize=10, fontname='Arial')
    plt.legend(prop={'family': 'Arial', 'size': 10}, frameon=False)
    plt.show()

    # Plot Mercury Concentrations PDFs
    fig = figure(num=None, figsize=(3.3, 3.3), dpi=80, facecolor="w", edgecolor='k')
    ax = sns.distplot(np.log10(hg_fgd_effluent_concentration), color=[153 / 255, 153 / 255, 153 / 255], hist=False,
                      kde=True,
                      kde_kws={'linewidth': 2})
    kde_x, kde_y = ax.lines[0].get_data()
    ax.fill_between(kde_x, kde_y, where=(kde_x > np.log10(0.000356)), interpolate=True,
                    color=[153 / 255, 153 / 255, 153 / 255])
    sns.distplot(np.log10(Hg_concentration), color=[228 / 255, 26 / 255, 28 / 255], hist=False, kde=True,
                 kde_kws={'linewidth': 2}, label='Influent')
    if cp == 1 and (mbr + bt + iex + alox + feox + zvi != 0):
        sns.distplot(np.log10(fgd_wastewater_concentration(hg_mass_cp[:, 1], wastewater_production)),
                     color=[55 / 255, 126 / 255, 184 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                     label='Chemical Precipitation')
    if mbr == 1 and (bt + iex + alox + feox + zvi != 0):
        sns.distplot(np.log10(fgd_wastewater_concentration(hg_mass_mbr[:, 1], wastewater_production)),
                     color=[77 / 255, 175 / 255, 74 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                     label='Membrane Bioreactor')
    if bt == 1 and (iex + alox + feox + zvi + gac != 0):
        sns.distplot(np.log10(fgd_wastewater_concentration(hg_mass_bt[:, 1], wastewater_production)),
                     color=[152 / 255, 78 / 255, 163 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                     label='Biological Treatment')
    if iex == 1 and (alox + feox + zvi + gac != 0):
        sns.distplot(np.log10(fgd_wastewater_concentration(hg_mass_iex[:, 1], wastewater_production)),
                     color=[255 / 255, 127 / 255, 0 / 255], hist=False, kde=True, kde_kws={'linewidth': 2})
    if alox == 1 and (feox + zvi + gac != 0):
        sns.distplot(np.log10(fgd_wastewater_concentration(hg_mass_alox[:, 1], wastewater_production)),
                     color=[255 / 255, 255 / 255, 51 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                     label='Aluminum Oxide')
    if feox == 1 and (zvi + gac != 0):
        sns.distplot(np.log10(fgd_wastewater_concentration(hg_mass_feox[:, 1], wastewater_production)),
                     color=[166 / 255, 86 / 255, 40 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                     label='Iron Oxide')
    if zvi == 1 and gac != 0:
        sns.distplot(np.log10(fgd_wastewater_concentration(hg_mass_alox[:, 1], wastewater_production)),
                     color=[247 / 255, 129 / 255, 191 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                     label='Zero-Valent Iron')
    ax = sns.distplot(np.log10(hg_fgd_effluent_concentration), color=[153 / 255, 153 / 255, 153 / 255], hist=False,
                      kde=True,
                      kde_kws={'linewidth': 2}, label='Effluent')
    plt.axvline(np.log10(0.000356), color='black')
    ax.set_xlabel('Mercury Concentration [mg/L]', fontsize=12, fontname='Arial')
    ax.set_ylabel('Probability Density', fontsize=12, fontname='Arial')
    ax.set_ylim([0, 0.4])
    plt.yticks([0, 0.1, 0.2, 0.3, 0.4], fontsize=10, fontname='Arial')
    plt.legend(prop={'family': 'Arial', 'size': 10}, frameon=False)
    plt.show()

    #Plot Arsenic Concentration ECDF
    qe_As_concentration, pe_As_concentration = ecdf(as_fgd_effluent_concentration)
    fig, ax = plt.subplots(1,1)
    fig.figsize=(2.8,2.8)
    #ax.hold(True)
    ax.plot(qe_As_concentration, pe_As_concentration, '-k', lw=2)
    ax.set_xlabel('Arsenic Concentration [mg/L]')
    ax.set_ylabel('Cumulative Probability')
    ax.set_ylim([0,1])
    #ax.set_adjustable(box = )
    plt.show()
    Arsenic_CDF = fileDir / 'Results' / 'FGD Wastewater Effluent' / 'Arsenic Concentration CDF.pdf'
    fig.savefig(str(Arsenic_CDF), bbox_inches='tight')
    #ax.hold(False)
    ax.clear()
    plt.close()

    #Plot Chloride Concentration ECDF
    qe_Cl_concentration, pe_Cl_concentration = ecdf(cl_fgd_effluent_concentration)
    fig, ax = plt.subplots(1,1)
    fig.figsize=(2.8,2.8)
    #ax.hold(True)
    ax.plot(qe_Cl_concentration, pe_Cl_concentration, '-k', lw=2)
    ax.set_xlabel('Chloride Concentration [mg/L]')
    ax.set_ylabel('Cumulative Probability')
    ax.set_ylim([0,1])
    #ax.set_adjustable(box = )
    plt.show()
    Chlorine_CDF = fileDir / 'Results' / 'FGD Wastewater Effluent' / 'Chloride Concentration CDF.pdf'
    fig.savefig(str(Chlorine_CDF), bbox_inches='tight')
    #ax.hold(False)
    ax.clear()
    plt.close()

    #Plot Mercury Concentration ECDF
    qe_Hg_concentration, pe_Hg_concentration = ecdf(hg_fgd_effluent_concentration)
    fig, ax = plt.subplots(1,1)
    fig.figsize=(2.8,2.8)
    #ax.hold(True)
    ax.plot(qe_Hg_concentration, pe_Hg_concentration, '-k', lw=2)
    ax.set_xlabel('Mercury concentration [mg/L]')
    ax.set_ylabel('Cumulative Probability')
    ax.set_ylim([0,1])
    #ax.set_adjustable(box = )
    plt.show()
    Mercury_CDF = fileDir / 'Results' / 'FGD Wastewater Effluent' / 'Mercury Concentration CDF.pdf'
    fig.savefig(str(Mercury_CDF), bbox_inches='tight')
    #ax.hold(False)
    ax.clear()
    plt.close()

    #Plot Selenium Concentration ECDF
    qe_Se_concentration, pe_Se_concentration = ecdf(se_fgd_effluent_concentration)
    fig, ax = plt.subplots(1,1)
    fig.figsize=(2.8,2.8)
    #ax.hold(True)
    ax.plot(qe_Se_concentration, pe_Se_concentration, '-k', lw=2)
    ax.set_xlabel('Selenium concentration [mg/L]')
    ax.set_ylabel('Cumulative Probability')
    ax.set_ylim([0,1])
    #ax.set_adjustable(box = )
    plt.show()
    Selenium_CDF = fileDir / 'Results' / 'FGD Wastewater Effluent' / 'Selenium Concentration CDF.pdf'
    fig.savefig(str(Selenium_CDF), bbox_inches='tight')
    #ax.hold(False)
    ax.clear()
    plt.close()

    elg_compliance_check(elg, zld, as_fgd_effluent_concentration, cl_fgd_effluent_concentration,
                         hg_fgd_effluent_concentration, se_fgd_effluent_concentration)

    # Model electricity consumption
    electricity_used_for_wastewater_treatment, cost_of_electricity = \
        wastewater_treatment_electricity_consumption(wastewater_production, cp, mbr, bt, mvc, iex, alox, feox, zvi,
                                                     crys)
    # Plot CDF of electricity consumption
    qe_electricity_consumption, pe_electricity_consumption = ecdf(electricity_used_for_wastewater_treatment)
    fig, ax = plt.subplots(1,1)
    fig.figsize=(2.8,2.8)
    #ax.hold(True)
    ax.plot(qe_electricity_consumption, pe_electricity_consumption, '-k', lw=2)
    ax.set_xlabel('Electricity Consumed [kWh/hr]')
    ax.set_ylabel('Cumulative Probability')
    ax.set_ylim([0,1])
    #ax.set_adjustable(box = )
    plt.show()
    Selenium_CDF = fileDir / 'Results' / 'Electricity Consumed for Wastewater Treatment CDF.pdf'
    fig.savefig(str(Selenium_CDF), bbox_inches='tight')
    #ax.hold(False)
    ax.clear()
    plt.close()

    # Plot CDF of electricity cost
    qe_electricity_cost, pe_electricity_cost = ecdf(cost_of_electricity)
    fig, ax = plt.subplots(1,1)
    fig.figsize=(2.8,2.8)
    #ax.hold(True)
    ax.plot(qe_electricity_cost, pe_electricity_cost, '-k', lw=2)
    ax.set_xlabel('Electricity Cost [$/hr]')
    ax.set_ylabel('Cumulative Probability')
    ax.set_ylim([0,1])
    #ax.set_adjustable(box = )
    plt.show()
    Selenium_CDF = fileDir / 'Results' / 'Electricity Consumed for Wastewater Treatment CDF.pdf'
    fig.savefig(str(Selenium_CDF), bbox_inches='tight')
    #ax.hold(False)
    ax.clear()
    plt.close()

    # Model chemical consumption
    lime_consumption, organosulfide_consumption, iron_chloride_consumption, nutrient_consumption, coagulant_consumption, \
    antiscalant_consumption, soda_ash_consumption, acid_consumption, polymer_consumption = \
        wastewater_chemical_consumption(wastewater_production, cp, mbr, bt, mvc, iex, alox, feox, zvi, ro, crys)

    # Plot CDFs of chemical consumption
    qe_lime_consumption, pe_lime_consumption = ecdf(lime_consumption)
    qe_organosulfide_consumption, pe_organosulfide_consumption = ecdf(organosulfide_consumption)
    qe_iron_chloride_consumption, pe_iron_chloride_consumption = ecdf(iron_chloride_consumption)
    qe_nutrient_consumption, pe_nutrient_consumption = ecdf(nutrient_consumption)
    qe_coagulant_consumption, pe_coagulant_consumption = ecdf(coagulant_consumption)
    qe_antiscalant_consumption, pe_antiscalant_consumption = ecdf(antiscalant_consumption)
    qe_soda_ash_consumption, pe_soda_ash_consumption = ecdf(soda_ash_consumption)
    qe_acid_consumption, pe_acid_consumption = ecdf(acid_consumption)
    qe_polymer_consumption, pe_polymer_consumption = ecdf(polymer_consumption)

    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(nrows=3, ncols=3)
    fig.set_size_inches(8.5, 8.5)
    ax1.plot(qe_lime_consumption, pe_lime_consumption, color=(228/255, 26/255, 28/255), lw=2)
    ax1.set_xlabel(' ')
    ax1.set_ylabel('Cumulative Probability')
    ax1.set_ylim([0, 1])
    ax2.plot(qe_organosulfide_consumption, pe_organosulfide_consumption, color=(55/255, 126/255, 184/255), lw=2)
    ax2.set_xlabel(' ')
    ax2.set_ylabel(' ')
    ax2.set_yticks([])
    ax3.plot(qe_iron_chloride_consumption, pe_iron_chloride_consumption, color=(77/255, 175/255, 74/255), lw=2)
    ax3.set_xlabel(' ')
    ax3.set_ylabel(' ')
    ax3.set_yticks([])
    ax4.plot(qe_nutrient_consumption, pe_nutrient_consumption, color=(152/255, 78/255, 163/255), lw=2)
    ax4.set_xlabel('')
    ax4.set_ylabel('Cumulative Probability')
    ax4.set_ylim([0, 1])
    ax5.plot(qe_coagulant_consumption, pe_coagulant_consumption, color=(255/255, 127/255, 0/255), lw=2)
    ax5.set_xlabel(' ')
    ax5.set_ylabel(' ')
    ax5.set_yticks([])
    ax6.plot(qe_antiscalant_consumption, pe_antiscalant_consumption, color=(255/255, 255/255, 51/255), lw=2)
    ax6.set_xlabel(' ')
    ax6.set_ylabel(' ')
    ax6.set_yticks([])
    ax7.plot(qe_soda_ash_consumption, pe_soda_ash_consumption, color=(166/255, 86/255, 40/255), lw=2)
    ax7.set_xlabel('Chemical Consumption [kg/hr]')
    ax7.set_ylabel('Cumulative Probability')
    ax7.set_ylim([0, 1])
    ax8.plot(qe_acid_consumption, pe_acid_consumption, color=(247/255, 129/255, 191/255), lw=2)
    ax8.set_xlabel('Chemical Consumption [kg/hr]')
    ax8.set_ylabel(' ')
    ax8.set_yticks([])
    ax9.plot(qe_polymer_consumption, pe_polymer_consumption, color=(153/255, 153/255, 153/255), lw=2)
    ax9.set_xlabel('Chemical Consumption [kg/hr]')
    ax9.set_ylabel(' ')
    ax9.set_yticks([])
    plt.show()
    chemical_consumption_cdfs = fileDir / 'Results' / 'Chemicals Consumed for Wastewater Treatment CDF.pdf'
    fig.savefig(str(chemical_consumption_cdfs), bbox_inches='tight')
    ax.clear()
    plt.close()
