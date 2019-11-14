import numpy as np
import pandas as pd
import sys
import pathlib
from matplotlib import pyplot as plt

# Import the functions used throughout this project from the function dictionary library file
fileDir = pathlib.Path(__file__).parents[2]
code_library_folder = fileDir / 'Code' / 'function_dictionary_library'
sys.path.append(str(code_library_folder))
from partitioning_modeling_function import treatment_train_violation_checks, mc_treatment_train_violation_checks
from statistical_functions import ecdf

output_filepath = fileDir / 'Results' / 'Treatment Trains Violations Summary' / 'MC Bit csESP wetFGD cp bt zvi.xlsx'
figure_filepath = fileDir / 'Results' / 'Treatment Trains Violations Summary' / 'MC Bit csESP wetFGD cp bt zvi.tif'

# Order of inputs are:
coal_input = 'Bituminous' # rank or bed
csesp_input = 1 # 0/1 if a csESP is installed
hsesp_input = 0 # 0/1 if a hsESP is installed
ff_input = 0 # 0/1 if a fabric filter is installed
scr_input = 0 # 0/1 if a selective catalytic reduction is installed
aci_input = 0 # 0/1 if an activated carbon injection process is installed
wetfgd_input = 1 # 0/1 if a wetFGD process is installed
wetfgdtype_input = 'LS Forced DBA' # 'LS Forced DBA', 'LS Forced None', 'LS Inhibited DBA', 'LS Inhibited None', 'LS Inhibited NaFo',
                   # 'Mg-enhanced Lime Natural', 'Mg-enhanced Lime Inhibited', 'Mg-enhanced Lime Ext. Forced'
dryfgd_input = 0  # 0/1 if a dryFGD process is installed
elg_input = 1  # 0/1 if water treatment process is designed to achieve Selenium removal
zld_input = 0  # 0/1 if a zero liquid discharge process is installed
cp_input = 1  # 0/1 if a chemical precipitation process is installed
mbr_input = 0  # 0/1 if a membrane bioreactor is installed
bt_input = 1  # 0/1 if a biological treatment process is installed
mvc_input = 0  # 0/1 if a mechanical vapor compression process is installed
iex_input = 0  # 0/1 if an ion exchange process is installed
alox_input = 0  # 0/1 if an Aluminum Oxide process is installed
feox_input = 0  # 0/1 if an Iron Oxide process is installed
zvi_input = 1  # 0/1 if a zero-valent iron process is installed
crys_input = 0  # 0/1 if a crystallization process is installed
electricity_generated_input = 550 # Hourly generation in MWh

i = 0
violations_total = []
violations_as = []
violations_hg = []
violations_se = []
concentration_as = []
concentration_hg = []
concentration_se = []
concentration_cl = []
concentration_pb = []

while i < 200:
    print(i)
    total_violations, as_concentration, as_violations, hg_concentration, hg_violations, se_concentration, se_violations, \
    cl_concentration, pb_concentration = mc_treatment_train_violation_checks(coal_input, csesp_input, hsesp_input, ff_input,
                                                                            scr_input, aci_input, wetfgd_input,
                                                                            wetfgdtype_input, dryfgd_input, elg_input,
                                                                            zld_input, cp_input, mbr_input, bt_input,
                                                                            mvc_input, iex_input, alox_input, feox_input,
                                                                            zvi_input, crys_input,
                                                                            electricity_generated_input)
    violations_total.append(total_violations)
    violations_as.append(as_violations)
    violations_hg.append(hg_violations)
    violations_se.append(se_violations)
    concentration_as.append(as_concentration)
    concentration_hg.append(hg_concentration)
    concentration_se.append(se_concentration)
    concentration_cl.append(cl_concentration)
    concentration_pb.append(pb_concentration)
    i += 1


total_violations_summary = [np.percentile(violations_total, 5), np.percentile(violations_total, 25),
                            np.percentile(violations_total, 50), np.percentile(violations_total, 75),
                            np.percentile(violations_total, 95)]

as_violations_summary = [np.percentile(violations_as, 5), np.percentile(violations_as, 25),
                         np.percentile(violations_as, 50), np.percentile(violations_as, 75),
                         np.percentile(violations_as, 95)]

hg_violations_summary = [np.percentile(violations_hg, 5), np.percentile(violations_hg, 25),
                         np.percentile(violations_hg, 50), np.percentile(violations_hg, 75),
                         np.percentile(violations_hg, 95)]

se_violations_summary = [np.percentile(violations_se, 5), np.percentile(violations_se, 25),
                         np.percentile(violations_se, 50), np.percentile(violations_se, 75),
                         np.percentile(violations_se, 95)]


# Print ECDF of violations
qe_total_violations, pe_total_violations = ecdf(violations_total)
qe_as_violations, pe_as_violations = ecdf(violations_as)
qe_hg_violations, pe_hg_violations = ecdf(violations_hg)
qe_se_violations, pe_se_violations = ecdf(violations_se)
qe_as, pe_as = ecdf(concentration_as)
qe_hg, pe_hg = ecdf(concentration_hg)
qe_se, pe_se = ecdf(concentration_se)
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
fig.set_size_inches(11, 8.5)
ax1.plot(qe_as, pe_as, '-k', lw=2, label='Arsenic Concentration')
ax1.set_xlabel('As Effluent Concentration [mg/L]')
ax1.set_ylabel('Cumulative Probability')
ax1.set_ylim([0, 1])
ax2.plot(qe_se, pe_se, '-k', lw=2, label='Selenium Concentration')
ax2.set_xlabel('Se Effluent Concentration [mg/L]')
ax2.set_ylabel('Cumulative Probability')
ax2.set_ylim([0, 1])
ax3.plot(qe_hg, pe_hg, '-k', lw=2, label='Mercury Concentration')
ax3.set_xlabel('Hg Effluent Concentration [mg/L]')
ax3.set_ylabel('Cumulative Probability')
ax3.set_ylim([0, 1])
ax4.plot(qe_total_violations, pe_total_violations, '-k', lw=2, label='Total Violations')
ax4.plot(qe_as_violations, pe_as_violations, '-b', lw=2, label='Arsenic')
ax4.plot(qe_hg_violations, pe_hg_violations, '-r', lw=2, label='Mercury')
ax4.plot(qe_se_violations, pe_se_violations, '-g', lw=2, label='Selenium')
ax4.set_xlabel('Likelihood of Needing Further Treatment [%]')
ax4.set_ylabel('Cumulative Probability')
ax4.set_ylim([0, 1])
ax4.set_xlim([0, 100])
plt.show()
fig.savefig(figure_filepath, bbox_inches='tight')
plt.close()

# Calculate and report summary statistics for violation
violations_summary = np.array([total_violations_summary, as_violations_summary, hg_violations_summary,
                               se_violations_summary])
violations_summary = pd.DataFrame(violations_summary, index=['Total', 'As', 'Hg', 'Se'],
                                  columns=['5th_Percentile', '25th_Percentile', 'Median', '75th_Percentile',
                                           '95th_Percentile'])
print(violations_summary)
violations_summary.to_excel(output_filepath)
