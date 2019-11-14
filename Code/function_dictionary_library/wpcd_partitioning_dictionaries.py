as_dict = {'CP': {'removal': [0.99, 0.93, 0.98, 0.98, 0.998, 0.99, 0.94],
                  'effluent': [0.01, 0.07, 0.02, 0.02, 0.002, 0.01, 0.06]},
           # Data from the ERG study for the Allen, Belews Creek, Dickerson, Hatfields Ferry, Keystone, Miami Fort, and
           # Pleasant Prairie plants.
           'MBR': {'removal': [0.047], 'effluent': [0.953]},  # Data from EPRI's study at Pleasant Prairie.
           'BT': {'removal': [0.134, 0.76], 'effluent': [0.866, 0.24]},  # Data from the ERG study and EPRI's study at Pleasant Prai
           # rie.
           'IEX': {'removal': [0], 'effluent': [1]},
           'AlOx': {'removal': [0], 'effluent': [1]},
           'MVC': {'distillate': [0, 1, 0.210308, 0, 0.245147, 0.248949, 0, 0], 'brine': [1, 0, 0.789692, 1, 0.754853, 0.751051, 1, 1]}, #Data from the evaporator system at Brindisi, where no Arsenic was observed in the brine concentrator distillate (i.e, all of the Arsenic remained in the liquid state with none evaporating.
           'FeOx': {'removal': [0], 'effluent': [1]},  # Data from EPRI study of FGD sorbent performance.
           'ZVI': {'removal': [0.97], 'effluent': [0.03]}, #Data from the hybrid ZVI process reported by Huang et al. (2013)
           'Crys': {'sludge': [0, 1, 0.789692, 1, 0.754853, 0.751051, 1, 1], 'distillate': [1, 0, 0.210308, 0, 0.245147, 0.248949, 0, 0]}, # Data from the crystallizer system at Brindisi, where no Arsenic was observed in the crystallizer distillate.
           'GAC': {'removal': [0.44], 'effluent': [0.56]},
           'RO': {'permeate': [0.15, 0.103896, 0.16], 'brine': [0.85, 0.896104, 0.84]},
           'not installed': {'removal': [0], 'effluent': [1]}}

cl_dict = {'CP': {'removal': [0.11, 0, 0.095, 0.09, 0.30], 'effluent': [0.89, 1, 0.905, 0.91, 0.70]},  # Data from the ERG
           #  study for Allen, Belews Creeek, Dickerson, Keystone, and Miami Fort plants.
           'MBR': {'removal': [0], 'effluent': [1]},  # Data from EPRI's study at Pleasant Prairie.
           'BT': {'removal': [0, 0, 0.000606], 'effluent': [1, 1, 0.999394]},
           # Data from the ERG study on Allen and Belews Creek plants and EPRI's study at Pleasant Prairie.
           'IEX': {'removal': [0], 'effluent': [1]},
           'AlOx': {'removal': [0], 'effluent': [1]},
           'MVC': {'distillate': [0, 0.000223, 0, 0.000416, 5.18e-5, 0.000158, 5.97e-5, 5.27e-5, 4.5e-5, 0], 'brine': [1, 0.99977, 1, 0.999584, 0.999948, 0.999842, 0.99994, 0.999947, 0.999955, 1]}, #Data from the evaporator system at Brindisi, where no Arsenic was observed in the brine concentrator distillate (i.e, all of the Arsenic remained in the liquid state with none evaporating.
           'FeOx': {'removal': [0], 'effluent': [1]},
           'ZVI': {'removal': [1 - (16350/16450), 1 - (20340/20610)], 'effluent': [16350/16450, 20340/20610]},  # Data from the hybrid ZVI process reported by Huang et al. (2013)
           'Crys': {'sludge': [1, 0.999969, 0.999591, 0.999881, 0.999867], 'distillate': [0, 3.08259e-5, 0.000409, 0.000119, 0.000133]}, # Data from the crystallizer system at Brindisi, where no Arsenic was observed in the crystallizer distillate.
           'GAC': {'removal': [0], 'effluent': [1]},
           'RO': {'permeate': [0.00234, 0.001013, 6.89e-5, 0.005259], 'brine': [0.99766, 0.998987, 0.999931, 0.994741]},
           'not installed': {'removal': [0], 'effluent': [1]}}

pb_dict = {'CP': {'removal': [0.98, 0.996], 'effluent': [0.02, 0.004]},  # Data from the ERG study for the Dickerson
           # and Hatfields Ferry plants.
           'MBR': {'removal': [0], 'effluent': [1]},  # Data from EPRI's study at Pleasant Prairie.
           'BT': {'removal': [0], 'effluent': [1]},  # Data from the ERG study and EPRI's study at Pleasant Prairie.
           'IEX': {'removal': [0], 'effluent': [1]},
           'AlOx': {'removal': [0], 'effluent': [1]},
           'MVC': {'distillate': [0], 'brine': [1]}, #Data from the evaporator system at Brindisi, where no Arsenic was observed in the brine concentrator distillate (i.e, all of the Arsenic remained in the liquid state with none evaporating.
           'FeOx': {'removal': [0], 'effluent': [1]},
           'ZVI': {'removal': [0.97], 'effluent': [0.03]}, #Data from the hybrid ZVI process reported by Huang et al. (2013)
           'Crys': {'sludge': [1], 'distillate': [0]}, # Data from the crystallizer system at Brindisi, where no Arsenic was observed in the crystallizer distillate.
           'GAC': {'removal': [0], 'effluent': [1]},
           'RO': {'permeate': [0.15, 0.261438, 0.16], 'brine': [0.85, 0.738562, 0.84]},
           'not installed': {'removal': [0], 'effluent': [1]}}

hg_dict = {'CP': {'removal': [0.99, 0.999, 0.95, 0.999, 0.9997, 0.9994, 0.998],
                  'effluent': [0.01, 0.001, 0.05, 0.001, 0.0003, 0.0006, 0.003]},
           # Data from the ERG study from Allen, Belews Creek, Dickerson, Hatfields Ferry, Keystone, Miami Fort, and
           # Pleasant Prairie plants.
           'MBR': {'removal': [0.96], 'effluent': [0.04]},  # Data from EPRI's study at Pleasant Prairie.
           'BT': {'removal': [0.96, 0.93, 0.54], 'effluent': [0.04, 0.07, 0.46]},
           #  Data from the ERG study on the Allen and Belews Creek plants and EPRI's study at Pleasant Prairie.
           'IEX': {'removal': [0.97, 0.94, 0.86, 1, 0.84, 1, 0.67], 'effluent': [0.03, 0.06, 0.14, 0, 0.16, 0, 0.33]},  # Removal in CRB02, CRB05, GRY-L, CR11, CR20, and 1X8 resisns reported by (Ohki et al. 2011) and the FerrIX resin reported by Staicu et al. (2017)
           'AlOx': {'removal': [0.28, 0.44], 'effluent': [0.72,0.56]},  # Data for activated alumina based on Ohki et al. (2011)
           'MVC': {'distillate': [0.0499, 0.0587, 0.129, 0.242, 0.742, 0.999, 0.987431, 0.989987, 0.998205, 0.99611, 0.998928, 0.994592], 'brine': [0.0950, 0.941, 0.872, 0.758, 0.258, 0.001, 0.012569, 0.010013, 0.001795, 0.00389, 0.001072, 0.005408]}, #Data from the evaporator system at Brindisi and Iatan plants.
           'FeOx': {'removal': [0], 'effluent': [1]}, #Data from EPRI study on FGD wastewater treatment sorbents.
           'ZVI': {'removal': [0.999], 'effluent': [0.001]}, #Data for the hybrid zero-valent iron process reported by Huang et al. (2013)
           'Crys': {'sludge': [0.953, 0.968, 0.012569, 0.010013, 0.001795, 0.00389, 0.001072, 0.005408], 'distillate': [0.0474, 0.0321, 0.987431, 0.989987, 0.998205, 0.99611, 0.998928, 0.994592]}, # Data from the crystallizer system at Brindisi, where no Arsenic was observed in the crystallizer distillate.
           'GAC': {'removal':[0.72, 0.90], 'effluent': [0.28, 0.10]},
           'RO': {'permeate': [0.018899, 0.009994, 0.002107, 0.001852], 'brine': [0.981101, 0.990006, 0.997893, 0.998148]},
           'not installed': {'removal': [0], 'effluent': [1]}}

n_dict = {'CP': {'removal': [0.23, 0.06, 0.39, 0, 0.29, 0.12, 0], 'effluent': [0.77, 0.94, 0.61, 1, 0.71, 0.88, 1]},
          # Data from the ERG study on the Allen, Belews Creek, Dickerson, Hatfields Ferry, Keystone, Miami Fort, and
          # Pleasant Prairie plants
           'MBR': {'removal': [0], 'effluent': [1]},  # Data from EPRI's study at Pleasant Prairie.
           'BT': {'removal': [0.98, 0.99, 0.978], 'effluent': [0.02, 0.01, 0.022]},
          # Data from the ERG study on Allen and Belews Creek power plants and EPRI's study at Pleasant Prairie.
           'IEX': {'removal': [0], 'effluent': [1]},
           'AlOx': {'removal': [0], 'effluent': [1]},
           'MVC': {'distillate': [0.001130566, 0.001693958, 0.000358, 0, 0.302926, 0.380284, 0.240929, 0.375988, 0.420854, 0.310408], 'brine': [0.998869434, 0.998306042, 0.999642, 1, 0.697074, 0.619716, 0.759071, 0.624012, 0.579146, 0.689592]}, #Data from the evaporator system at Brindisi, and Iatan's maximum value since no nitrate/nitraite was observed in the distillate.
           'FeOx': {'removal': [0], 'effluent': [1]}, #Data from EPRI study on sorbents for FGD wastewater treatment.
           'ZVI': {'removal': [0.99], 'effluent': [0.01]}, #Data from the hybrid ZVI process reported by Huang et al. (2013)
           'Crys': {'sludge': [1, 0.999855, 0.697074, 0.619716, 0.759071, 0.624012, 0.579146, 0.689592], 'distillate': [0, 0.000144938, 0.302926, 0.380284, 0.240929, 0.375988, 0.420854, 0.310408]}, # Data from the crystallizer system at Brindisi, where no Arsenic was observed in the crystallizer distillate.
           'GAC': {'removal': [0], 'effluent': [1]},
           'RO': {'permeate': [0.002211, 0.002537, 0.005332, 0.002668], 'brine': [0.99766, 0.998987, 0.999931, 0.994741]},
           'not installed': {'removal': [0], 'effluent': [1]}}

se_dict = {'CP': {'removal': [0.58, 0.80, 0.87, 0.48, 0.91, 0.61, 0.82],
                  'effluent': [0.42, 0.2, 0.13, 0.52, 0.09, 0.39, 0.18]},
           # Data from the ERG study from the Allen, Belews Creek, Dickerson, Hatfields Ferry, Keystone, Miami Fort,
           # and Pleasant Prairie plants.
           'MBR': {'removal': [0.84], 'effluent': [0.16]},  # Data from EPRI's study at Pleasant Prairie.
           'BT': {'removal': [0.97, 0.95, 0.97, 0.99], 'effluent': [0.03, 0.05, 0.03, 0.01]},
           # Data from the ERG study on Allen and Belews Creek plants, EPRI's study at Pleasant Prairie,
           # and Sonstegard and Pickett (2005)
           'IEX': {'removal': [0.48, 0.46], 'effluent': [0.52, 0.54]},  # Removal in IX8 resin reported by Ohki et al. (2011) and the FerrIX resin reported by Staicu et al. (2017)
           'AlOx': {'removal': [0.18, 0.48], 'effluent': [0.82, 0.52]},  # Data for activated alumina based on Ohki et al. (2011)
           'MVC': {'distillate': [0, 0.033613445, 0, 0.0293, 0.002266, 0.00369, 0.006286, 0.00143, 0.00586, 0.011697], 'brine': [1, 0.966386555, 1, 0.971, 0.997734, 0.99631, 0.993714, 0.99857, 0.99414, 0.988303]}, #Data from the evaporator system at Brindisi, where no Arsenic was observed in the brine concentrator distillate (i.e, all of the Arsenic remained in the liquid state with none evaporating.
           'FeOx': {'removal': [0], 'effluent': [1]},
           'ZVI': {'removal': [0.998], 'effluent': [0.002]},  # Data from the hybrid zero-valent iron process reported by Huang et al. (2013)
           'Crys': {'sludge': [0.995246, 1, 0.997734, 0.99631, 0.993714, 0.99857, 0.99414, 0.988303], 'distillate': [0.004753623, 1, 0.002266, 0.00369, 0.006286, 0.00143, 0.00586, 0.011697]}, # Data from the crystallizer system at Brindisi, where no Arsenic was observed in the crystallizer distillate.
           'GAC': {'removal': [0], 'effluent': [1]},
           'RO': {'permeate': [0.006058, 0.003112, 0.004285, 0.003177], 'brine': [0.993942, 0.996888, 0.995715, 0.996823]},
           'not installed': {'removal': [0], 'effluent': [1]}}

