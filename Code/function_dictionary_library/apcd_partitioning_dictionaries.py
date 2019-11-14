import pandas as pd
import pathlib
import numpy as np
import sys
import os
from Se_lit_based_dictionary import se_wFGD_dictionary

# For frozen code
fileDir = pathlib.Path(__file__).parents[1]
# For Original Python Code
# fileDir = pathlib.Path(__file__).parents[2]


as_dict = {  # Studies for bottom ash partitioning coefficients (in order):  Cheng et al. (2009), Rubin (1999),
    # Klein et al. (1975), Swanson et al. (2013), Sander (1991), Maier (1990), 3 units from Yokoyama et al (1991),
    # Cheng et al. (2009), Otero-Rey et al. (2003), 4 units from Zheng et al. (2017).
           'Bottom_Ash': {'gas': [0.936, 0.986, 1, 0.99, 0.893, 0.996, 0.9924, 0.9969, 0.9905, 0.96, 0.995, 0.987,
                                  0.972, 0.974, 0.974],
                          'solid': [0.064, 0.014, 0, 0.01, 0.107, 0.004, 0.0076, 0.0031, 0.0095, 0.04, 0.005, 0.013,
                                    0.028, 0.026, 0.026],
                          'liquid': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
             # Studies for csESp partitioning coefficients (in order): Helble et al. (2000), Klein et al. (1975), Rubin
    #  (1999), Swanson et al. (2013), Ottero-Rey et al. (2003), 2 units from Weng et al. (2017), Swanson et al. (2013),
    # Yokoyama et al. (1991), Chent et al. (2009), Zhao et al. (2016), Zheng et al. (2017), Zhao et al. (2017).
           'csESP': {'gas': [0.04, 0.18, 0.03, 0.01, 0.0413, 0.0178, 0.5, 0.003426, 0.05644, 0.000494, 0.176, 0.000393],
                     'solid': [0.96, 0.82, 0.97, 0.99, 0.9587, 0.9822, 0.5, 0.996574, 0.94356, 0.9995, 0.824, 0.9996],
                     'liquid': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
             #Studies for hsESP partitioning coeffients (in order):  2 units from Yokoyama et al. (1991)
           'hsESP': {'gas': [0.01324, 0.0104],
                     'solid': [0.9868, 0.9896],
                     'liquid': [0, 0]},
             #Studies for fabric filter partitioning coeffients (in order): 3 diff erent loads from Zhao et al. (2017)
           'FF': {'gas': [0.00146, 0.00091, 0.00098],
                  'solid': [0.99854, 0.99909, 0.99902],
                  'liquid': [0, 0, 0]},
             #Studies for selective catalytic reduction coefficients (in order):
           'SCR': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
             #Studies for activated carbon injection coefficients (in order):
           'ACI': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
           # Studies for direct sorbent injection coefficients (in order):
           'DSI': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
             #Studies for wetFGD partitioning coefficients (in order): Ondov et al. (1979), Zhu et al. (2014),
    # Alvarez-Ayuso (2006), Zhao et al. (2017), Gutberlet et al. (1985)
           'wetFGD': {'gas': [0, 0.07, 0, 0.727273, 0],
                      'solid': [1-6.5e-5, 0.93, 1, 0.17198, 0.941558],
                      'liquid': [6.5e-5, 0, 0, 0.10075, 0.058442]},
             #Studies for dryFGD partitioning coefficients (in order): Karlsson (1986) and Sander (1991)
           'dryFGD': {'gas': [0.0051, 0.11],
                      'solid': [0.995, 0.89],
                      'liquid': [0, 0]},
           'not installed': {'gas': [1],
                    'solid': [0],
                    'liquid': [0]}}

cl_dict = { #Studies for bottom ash partitioning coefficeints (in order):  Cheng et al. (2009), Rubin (1999) and Klein et al. (1975), Otero-Rey et al. (2003)
           'Bottom_Ash': {'gas': [0.9982, 0.999, 0.994, 0.98],
                          'solid': [0.0018, 0.001, 0.006, 0.02],
                          'liquid': [0, 0, 0, 0]},
             #Studies for csESp partitioning coefficients (in order): Klein et al. (1975), Rubin (1999), Otero-Rey et al. (2003), Cheng et al. (2009).
           'csESP': {'gas': [0.98, 1, 0.85, 0.96377],
                     'solid': [0.02, 0, 0.15, 0.03623],
                     'liquid': [0, 0, 0, 0]},
             #Studies for hsESP partitioning coeffients (in order):
           'hsESP': {'gas': [1],
                     'solid': [0],
                     'liquid': [0]},
             #Studies for fabric filter partitioning coeffients (in order):
           'FF': {'gas': [1],
                  'solid': [0],
                  'liquid': [0]},
             #Studies for selective catalytic reduction coefficients (in order):
           'SCR': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
             #Studies for activated carbon injection coefficients (in order):
           'ACI': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
           # Studies for direct sorbent injection coefficients (in order):
           'DSI': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
             #Studies for wetFGD partitioning coefficients (in order): Ondov et al. (1979).
           'wetFGD': {'gas': [0.04],
                      'solid': [0],
                      'liquid': [0.96]},
             #Studies for dryFGD partitioning coefficients (in order):
           'dryFGD': {'gas': [1],
                      'solid': [0],
                      'liquid': [0]},
           'not installed': {'gas': [1],
                    'solid': [0],
                    'liquid': [0]}}

se_dict = {  # Studies for bottom ash partitioning coefficeints (in order):  Cheng et al. (2009), Rubin (1999), Klein et
    # al. (1975), Swanson et al. (2013), Sander (1991), Maier (1990), Yokoyama et al. (1991), Otero-Rey et al. (2003),
    # and 4 studies from Zheng et al. (2017).
           'Bottom_Ash': {'gas': [0.931, 0.985, 0.837, 1, 0.998, 0.994226, 0.9963, 0.988, 0.96375, 0.959, 0.971, 0.919,
                                  0.9999, 0.965],
                          'solid': [0.069, 0.015, 0.163, 0, 0.002, 0.005774, 0.0037, 0.012, 0.03625, 0.041, 0.029,
                                    0.081, 0.0001, 0.035],
                          'liquid': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
             # Studies for csESp partitioning coefficients (in order): Brekke et al. (1995), Helble et al. (2000), Klein
    # et al. (1975), Rubin (1999), Swanson et al. (2013), Guo et al. (2004, 2007), Otero-Rey (2003, Cheng et al. (2009),
    #  and Zheng et al. (2017).
           'csESP': {'gas': [0.80, 0.51, 0.03, 0.39, 0.80, 0.02, 0.04, 0.50967, 0.165],
                     'solid': [0.20, 0.49, 0.97, 0.61, 0.20, 0.98, 0.96, 0.49033, 0.835],
                     'liquid': [0, 0, 0, 0, 0, 0, 0, 0, 0]},
             #Studies for hsESP partitioning coeffients (in order): Swanson et al. (2013) and 2 studies from Yokoyama et al. (1991)
           'hsESP': {'gas': [0.80, 0.46462, 0.51802],
                     'solid': [0.20, 0.53538, 0.48198],
                     'liquid': [0, 0, 0]},
             #Studies for fabric filter partitioning coeffients (in order):  Brekke et al. (1995)
           'FF': {'gas': [0.35],
                  'solid': [0.65],
                  'liquid': [0]},
             #Studies for selective catalytic reduction coefficients (in order):
           'SCR': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
             #Studies for activated carbon injection coefficients (in order):
           'ACI': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
           # Studies for direct sorbent injection coefficients (in order):
           'DSI': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
             #Studies for wetFGD partitioning coefficients (in order): Ondov et al. (1979), Zhu et al. (2014),
    # Alvarez-Ayuso et al. (1960), Gutberlet et al. (1985).
           'wetFGD': {'gas': [0.01, 0.03, 0, 0.40],
                      'solid': [0.99, 0.96, 0.98, 0.55],
                      'liquid': [0.002, 0.01, 0.02, 0.049]},
             #Studies for dryFGD partitioning coefficients (in order): Sander (1991)
           'dryFGD': {'gas': [0.010],
                      'solid': [0.990],
                      'liquid': [0]},
           'not installed': {'gas': [1],
                    'solid': [0],
                    'liquid': [0]}}

se_wFGD_dict = se_wFGD_dictionary
#studies for limestone forced oxidation systems partitioning coefficients: EPRI 1019870(2010)
#other wFGD systems: EPRI 1017952(2009)

hg_dict = {  # Studies for bottom ash partitioning coefficeints (in order):  Cheng et al. (2009), Rubin (1999), Klein et
    # al. (1975), Devito et al. (2002), Swanson et al. (2013), Sander (1991), Maier (1990), Yokoyama et al. (1991),
    # Otero-Rey et al. (2003), 5 studies by Wang et al. (2008), 4 studies by Zheng et al. (2017).
           'Bottom_Ash': {'gas': [0.99818, 0.992, 0.981, 0.971, 1, 0.998, 1, 0.999, 0.9967, 0.9942, 0.996, 0.9999,
                                  0.9999, 0.9951, 0.99997, 0.982, 0.999, 0.9996, 0.99998, 0.999],
                          'solid': [0.00182, 0.008, 0.019, 0.029, 0, 0.002, 0, 0.001, 0.0033, 0.0058, 0.004, 0.0001,
                                    0.0001, 0.005, 0.00003, 0.018, 0.001, 0.0004, 0.00002, 0.001],
                          'liquid': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
             # Studies for csESp partitioning coefficients (in order): Brekke et al. (1995), Brown et al. (1999), Helble
    #  (2000), Klein et al. (1975), Rubin (1999), .Swanson et al. (2013), Aunela-Tapola (1998), Goodarzi (2004), Guo et
    # al. (2004), Otero-Rey et al. (2003), 3 studies by Wang et al. (2008), 4 studies by Zheng et al. (2017).
           'csESP': {'gas': [0.70, 0.29, 0.71, 0.94, 0.74, 0.98, 0.39, 0.62, 0.86, 0.77, 0.98, 0.66657, 0.85415,
                             0.44491, 0.82888, 0.9394, 0.788, 0.952, 0.481, 0.659, 0.579, 0.585],
                     'solid': [0.30, 0.67, 0.29, 0.06, 0.26, 0.02, 0.56, 0.38, 0.14, 0.27, 0.02, 0.33343, 0.14585,
                               0.55509, 0.17112, 0.061, 0.211, 0.0484, 0.519, 0.341, 0.421, 0.415],
                     'liquid': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
             #Studies for hsESP partitioning coeffients (in order): Goodarzi (2004) and Swanson et al. (2013)
           'hsESP': {'gas': [0.97, 0.98, 0.74255, 0.97968],
                     'solid': [0.03, 0.02, 0.25745, 0.02032],
                     'liquid': [0, 0, 0, 0]},
             #Studies for fabric filter partitioning coeffients (in order):  Brown et al. (1999), Chu and Porcella (1995), Brekke et al. (2015), 2 studies by Wang et al. (2008)
           'FF': {'gas': [0.23, 0.70, 0.40, 0.130, 0.737],
                  'solid': [0.77, 0.30, 0.60, 0.870, 0.263],
                  'liquid': [0, 0, 0, 0, 0]},
             #Studies for selective catalytic reduction coefficients (in order):
           'SCR': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
             #Studies for activated carbon injection coefficients (in order):  Flora et al. (2003), NRML (2005) and NRML (2005)
           'ACI': {'gas': [0.81203, 0.286325, 0.410256],
                   'solid': [0.18797, 0.713675, 0.589744],
                   'liquid': [0, 0, 0]},
             #Studies for direct sorbent injection coefficients (in order):
           'DSI': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
             #Studies for wetFGD partitioning coefficients (in order): Pavlish et al. (2003), Chu and Porcella (1995),
             # Devito et al. (2002), Lee et al. (2006), Zhu et al. (2014), Pavlish et al. (2003), Alvarez-Ayuso et al. (2006), Gutberlet et al. (1985).
             # EPRI Report 1014095 Site 4, 6, 7
           'wetFGD': {'gas': [0.834586, 0.789641, 0.531214, 0.387643, 0.416357, 0.564103, 0.369231, 0.700114, 0.200772,
                              0.257, 0.3613614],
                      'solid': [0.142857, 0.181643, 0.554929, 0.598, 0.526214, 0.405128, 0.558974, 0.230331, 0.763192,
                                0.697, 0.612613],
                      'liquid': [0.022556, 0.028714, 0.057429, 0.014357, 0.057429, 0.030769, 0.071795, 0.069555, 0.036036,
                                 0.046, 0.026026]},
             #Studies for dryFGD partitioning coefficients (in order): Karlsson (1986) and Sander (1991)
           'dryFGD': {'gas': [0.281, 0.462],
                      'solid': [0.719, 0.538],
                      'liquid': [0, 0]},
           #  # Studies for activated carbon injection and fabric filter (in order): EPRI report 1012676 Big Brown Unit 2 (2 different coals)， Presque Isle Units 7-9
           # 'FF+ACI': {'gas': [0.5, 0.36, 0.09],
           #            'solid': [0.5, 0.64, 0.91],
           #            'liquid': [0, 0, 0]},
           #  #Studies for activated carbon injection and cold-side ESP (in order): EPRI report 1012676 Independence Unit 2, Labadie Unit 2
           #  'csESP+ACI':{'gas':[0.25, 0.58],
           #               'solid':[0.75, 0.42],
           #               'liquid':[0, 0]},
            # #Studies for fabric filter and wet FGD (in order): EPRI report 1014095 Site 11
            # 'FF+wetFGD': {'gas':[0.36],
            #               'solid': [0.64],
            #               'liquid': [0]},
            # # Studies for fabric filter, selective catalytic reduction, and wetFGD (in order): EPRI report 1014095 Site 11
            # 'FF+SCR+wetFGD':{'gas':[0.35],
            #                  'solid':[0.65],
            #                  'liquid':[0]},
            # Studies for selective catalytic reduction and wet FGD partitioning coefficients (in order): EPRI 1014095 Site 4, 5, 6, 7, W1, L1, 3, 8, 9, 10
            'wetFGD+SCR':{'gas':[0.063676, 0.1422723, 0.1169231, 0.1725888, 0.1415479, 0.0835322, 0.2651992, 0.3016393,
                                 0.1256713, 0.125],
                          'solid':[0.917511, 0.623337, 0.435897, 0.579695, 0.821792, 0.596659, 0.727463, 0.691803,
                                   0.819549, 0.646694],
                          'liquid':[0.018813, 0.234391, 0.447179, 0.247716, 0.0366, 0.319809, 0.007338, 0.006557,
                                    0.05478, 0.228306]},
           'not installed': {'gas': [1],
                    'solid': [0],
                    'liquid': [0]}}

br_dict = cl_dict

b_dict = { #Studies for bottom ash partitioning coefficeints (in order):  Sander (1991), Maier (1990), Yokoyama (1991), Cheng et al. (2009).
           'Bottom_Ash': {'gas': [0.97955, 0.9702, 0.9725, 0.9784, 1],
                          'solid': [0.02045, 0.0298, 0.0275, 0.0216, 0],
                          'liquid': [0, 0, 0, 0, 0]},
             #Studies for csESp partitioning coefficients (in order): Yokoyama (1991) and Cheng et al. (2009).
           'csESP': {'gas': [0.042259, 0.87377],
                     'solid': [0.95774, 0.12623],
                     'liquid': [0, 0]},
             #Studies for hsESP partitioning coeffients (in order): Swanson et al. (2013)
           'hsESP': {'gas': [0.17964, 0.04068],
                     'solid': [0.82036, 0.95932],
                     'liquid': [0, 0]},
             #Studies for fabric filter partitioning coeffients (in order):  Currently based on selenium.
           'FF': {'gas': [0.35],
                  'solid': [0.65],
                  'liquid': [0]},
             #Studies for selective catalytic reduction coefficients (in order):  Currently based on selenium.
           'SCR': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
             #Studies for activated carbon injection coefficients (in order):  Currently based on selenium.
           'ACI': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
           # Studies for direct sorbent injection coefficients (in order):
           'DSI': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
             #Studies for wetFGD partitioning coefficients (in order): Currently based on selenium.
           'wetFGD': {'gas': [0.01, 0.03, 0, 0.40],
                      'solid': [0.99, 0.96, 0.98, 0.55],
                      'liquid': [0.002, 0.01, 0.02, 0.049]},
             #Studies for dryFGD partitioning coefficients (in order): Sander (1991)
           'dryFGD': {'gas': [0.03636],
                      'solid': [0.96364],
                      'liquid': [0]},
           'not installed': {'gas': [1],
                    'solid': [0],
                    'liquid': [0]}}

pb_dict = {  # Studies for bottom ash partitioning coefficeints (in order):  Swanson et al. (2013), Sander (1991), and
    # Yokoyama et al. (1991), 2 studies from Klein et al. (1975), and 4 studies from Zheng et al. (2017).
           'Bottom_Ash': {'gas': [0.94, 0.94, 0.9922, 0.9778, 0.9817, 0.935, 0.931, 0.934, 0.990, 0.995, 0.982],
                          'solid': [0.06, 0.06, 0.0078, 0.022, 0.0183, 0.065, 0.069, 0.066, 0.010, 0.005, 0.018],
                          'liquid': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
             # Studies for csESp partitioning coefficients (in order): Swanson et al. (2013) and Yokoyama et al. (1991),
    # 3 studies by Deng et al. (2014), and Zhao et al. (2017).
           'csESP': {'gas': [0.41935, 0.01885, 0.090, 0.099, 0.0998, 0.0004],
                     'solid': [0.58065, 0.98115, 0.910, 0.901, 0.9002, 0.9996],
                     'liquid': [0, 0, 0, 0, 0, 0]},
             #Studies for hsESP partitioning coeffients (in order):  2 studies by Yokoyama (1992).
           'hsESP': {'gas': [0.035, 0.003],
                     'solid': [0.965, 0.997],
                     'liquid': [0, 0]},
             #Studies for fabric filter partitioning coeffients (in order): 2 studies by Deng et al. (2014).
           'FF': {'gas': [0.041, 0.056],
                  'solid': [0.959, 0.944],
                  'liquid': [0, 0]},
             #Studies for selective catalytic reduction coefficients (in order): From Arsenic
           'SCR': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
             #Studies for activated carbon injection coefficients (in order):  From Arsenic
           'ACI': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
           # Studies for direct sorbent injection coefficients (in order):
           'DSI': {'gas': [1],
                   'solid': [0],
                   'liquid': [0]},
             #Studies for wetFGD partitioning coefficients (in order): Zhao et al. (2017)
           'wetFGD': {'gas': [0.46865],
                      'solid': [0.51648],
                      'liquid': [0.014878]},
             #Studies for dryFGD partitioning coefficients (in order): Sander et al. (1991)
           'dryFGD': {'gas': [0],
                      'solid': [1],
                      'liquid': [0]},
           'not installed': {'gas': [1],
                    'solid': [0],
                    'liquid': [0]}}

wet_fgd_removal_filename = fileDir / 'Intermediate' / 'Wet FGD Removal.xlsx'
wet_fgd_removal = pd.read_excel(wet_fgd_removal_filename, usecols=[0, 1], names=['Removal', 'Remaining'])
wet_fgd_removal_performance = wet_fgd_removal['Removal'].values.tolist()
wet_fgd_remaining_performance = wet_fgd_removal['Remaining'].values.tolist()

dry_fgd_removal_filename = fileDir / 'Intermediate' / 'Dry FGD Removal.xlsx'
dry_fgd_removal = pd.read_excel(dry_fgd_removal_filename, usecols=[0, 1], names=['Removal', 'Remaining'])
dry_fgd_removal_performance = dry_fgd_removal['Removal'].values.tolist()
dry_fgd_remaining_performance = dry_fgd_removal['Remaining'].values.tolist()

s_dict = {'Bottom_Ash': {'gas': [1],
                         'solid': [0],
                         'liquid': [0]},
          'csESP': {'gas': [1],
                    'solid': [0],
                    'liquid': [0]},
          'hsESP': {'gas': [1],
                    'solid': [0],
                    'liquid': [0]},
          'FF': {'gas': [1],
                 'solid': [0],
                 'liquid': [0]},
          'SCR': {'gas': [1],
                  'solid': [0],
                  'liquid': [0]},
          'ACI': {'gas': [1],
                  'solid': [0],
                  'liquid': [0]},
          'DSI': {'gas': [1],
                  'solid': [0],
                  'liquid': [0]},
             #Studies for wetFGD partitioning coefficients (in order):  EIA Form 860 Schedule 6_2 Year 2017.
          'wetFGD': {'gas': wet_fgd_remaining_performance,
                      'solid': wet_fgd_removal_performance,
                      'liquid': np.zeros(shape=(len(wet_fgd_removal_performance), 1))},
             #Studies for dryFGD partitioning coefficients (in order):  EIA Form 860 Schedule 6_2 Year 2017.
          'dryFGD': {'gas': dry_fgd_remaining_performance,
                     'solid': dry_fgd_removal_performance,
                     'liquid': np.zeros(shape=(len(dry_fgd_removal_performance), 1))},
          'not installed': {'gas': [1],
                            'solid': [0],
                            'liquid': [0]}}
