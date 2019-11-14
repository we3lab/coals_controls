import numpy as np
import random as rand
import pathlib 
import sys
# For frozen Program:
fileDir = pathlib.Path(__file__).parents[0]

# For Original Python Code
# fileDir = pathlib.Path(__file__).parents[2]
# code_library_folder = fileDir / 'Code' / 'function_dictionary_library'
# sys.path.append(str(code_library_folder))

from apcd_partitioning_dictionaries import as_dict, cl_dict, se_dict, hg_dict, br_dict, b_dict, pb_dict, se_wFGD_dict, s_dict

# Note that Boron, Bromine, and Lead data is missing for all of these.  To account for that we use data for trace
# elements of a similar volatility.  These pairs are:
# Boron = Selenium (Intermediate Volatility Between Group 2 and 3)
# Bromine = Chloride (High Volatility Group 3)
# Lead = Arsenic (Medium Volatility Group 2)


# Start with particulate matter control.
def bottom_modeling(runs):
    # For Boron, Bromine, and Lead since Daniel Sun does not currently have data on partitioning in them.
    bottom_partitioning = np.zeros(shape=(runs, 4))
    bottom_partitioning[:, 2] = np.ones(shape=runs)

    # For Chlorine.
    Cl_bottom_partitioning = np.column_stack((cl_dict['Bottom_Ash']['solid'],
                                             cl_dict['Bottom_Ash']['liquid'],
                                             cl_dict['Bottom_Ash']['gas']))
    Cl_bottom = np.zeros(shape=(runs, 3))
    i = 0
    while i < len(Cl_bottom[:, 2]):
        Cl_bottom[i, :] = Cl_bottom_partitioning[rand.randint(0, len(Cl_bottom_partitioning[:, 1]) - 1), :]
        i += 1

    # For Bromine.
    Br_bottom_partitioning = np.column_stack((br_dict['Bottom_Ash']['solid'],
                                             br_dict['Bottom_Ash']['liquid'],
                                             br_dict['Bottom_Ash']['gas']))
    Br_bottom = np.zeros(shape=(runs, 3))
    i = 0
    while i < len(Br_bottom[:, 2]):
        Br_bottom[i, :] = Br_bottom_partitioning[rand.randint(0, len(Br_bottom_partitioning[:, 1]) - 1), :]
        i += 1

    # For Selenium.
    Se_bottom_partitioning = np.column_stack((se_dict['Bottom_Ash']['solid'],
                                             se_dict['Bottom_Ash']['liquid'],
                                             se_dict['Bottom_Ash']['gas']))
    Se_bottom = np.zeros(shape=(runs, 3))
    i = 0
    while i < len(Se_bottom[:, 2]):
        Se_bottom[i, :] = Se_bottom_partitioning[rand.randint(0, len(Se_bottom_partitioning[:, 1]) - 1), :]
        i += 1

    #For Boron.
    B_bottom_partitioning = np.column_stack((b_dict['Bottom_Ash']['solid'],
                                            b_dict['Bottom_Ash']['liquid'],
                                            b_dict['Bottom_Ash']['gas']))

    B_bottom = np.zeros(shape=(runs, 3))
    i = 0
    while i < len(B_bottom[:, 2]):
        B_bottom[i, :] = B_bottom_partitioning[rand.randint(0, len(B_bottom_partitioning[:, 1]) - 1), :]
        i += 1

    # For Arsenic.
    As_bottom_partitioning = np.column_stack((as_dict['Bottom_Ash']['solid'],
                                             as_dict['Bottom_Ash']['liquid'],
                                             as_dict['Bottom_Ash']['gas']))
    As_bottom = np.zeros(shape=(runs, 3))
    i = 0
    while i < len(As_bottom[:, 2]):
        As_bottom[i, :] = As_bottom_partitioning[rand.randint(0, len(As_bottom_partitioning[:, 1]) - 1), :]
        i += 1

    # For Lead.
    Pb_bottom_partitioning = np.column_stack((pb_dict['Bottom_Ash']['solid'],
                                             pb_dict['Bottom_Ash']['liquid'],
                                             pb_dict['Bottom_Ash']['gas']))

    Pb_bottom = np.zeros(shape=(runs, 3))
    i = 0
    while i < len(Pb_bottom[:, 2]):
        Pb_bottom[i, :] = Pb_bottom_partitioning[rand.randint(0, len(Pb_bottom_partitioning[:, 1]) - 1), :]
        i += 1

    #For Mercury
    Hg_bottom_partitioning = np.column_stack((hg_dict['Bottom_Ash']['solid'],
                                             hg_dict['Bottom_Ash']['liquid'],
                                             hg_dict['Bottom_Ash']['gas']))
    Hg_bottom = np.zeros(shape=(runs, 3))
    i = 0
    while i < len(Hg_bottom[:, 2]):
        Hg_bottom[i, :] = Hg_bottom_partitioning[rand.randint(0, len(Hg_bottom_partitioning[:, 1]) - 1), :]
        i += 1

    #For Sulfur
    S_bottom_partitioning = np.column_stack((s_dict['Bottom_Ash']['solid'],
                                             s_dict['Bottom_Ash']['liquid'],
                                             s_dict['Bottom_Ash']['gas']))
    S_bottom = np.zeros(shape=(runs, 3))
    i = 0
    while i < len(S_bottom[:, 2]):
        S_bottom[i, :] = S_bottom_partitioning[rand.randint(0, len(S_bottom_partitioning[:, 1]) - 1), :]
        i += 1

    return Cl_bottom, Se_bottom, B_bottom, Br_bottom, Pb_bottom, As_bottom, Hg_bottom, S_bottom


def csESP_modeling(csESP, runs):

    # Defines partitioning of csESP.

    if csESP == 0:
        #If there is no csESP installed, then there is no partitioning and everything stays in the gaseous phase.
        csESP_partitioning = np.zeros(shape=(runs, 3))
        csESP_partitioning[:, 2] = np.ones(shape=runs)

        Cl_csESP = csESP_partitioning
        Se_csESP = csESP_partitioning
        B_csESP = csESP_partitioning
        Br_csESP = csESP_partitioning
        Pb_csESP = csESP_partitioning
        As_csESP = csESP_partitioning
        Hg_csESP = csESP_partitioning
        S_csESP = csESP_partitioning

    elif csESP ==1:
        #For Bromine

        csESP_partitioning = np.zeros(shape=(runs,4))
        csESP_partitioning[:,2] = np.ones(shape=runs)

        #For Chlorine.
        Cl_csESP_partitioning = np.column_stack((cl_dict['csESP']['solid'],
                                                cl_dict['csESP']['liquid'],
                                                cl_dict['csESP']['gas']))
        Cl_csESP = np.zeros(shape=(runs,3))
        i=0
        while i<len(Cl_csESP[:,2]):
            Cl_csESP[i,:]=Cl_csESP_partitioning[rand.randint(0,len(Cl_csESP_partitioning[:,1])-1),:]
            i += 1

        # For Bromine.
        Br_csESP_partitioning = np.column_stack((br_dict['csESP']['solid'],
                                                br_dict['csESP']['liquid'],
                                                br_dict['csESP']['gas']))
        Br_csESP = np.zeros(shape=(runs,3))
        i=0
        while i<len(Br_csESP[:,2]):
            Br_csESP[i,:]=Br_csESP_partitioning[rand.randint(0, len(Br_csESP_partitioning[:,1])-1),:]
            i += 1

        # For Selenium.
        Se_csESP_partitioning = np.column_stack((se_dict['csESP']['solid'],
                                                se_dict['csESP']['liquid'],
                                                se_dict['csESP']['gas']))
        Se_csESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Se_csESP[:, 2]):
            Se_csESP[i, :] = Se_csESP_partitioning[rand.randint(0, len(Se_csESP_partitioning[:, 1])-1), :]
            i += 1

        #For Boron.
        B_csESP_partitioning = np.column_stack((b_dict['csESP']['solid'],
                                               b_dict['csESP']['liquid'],
                                               b_dict['csESP']['gas']))
        B_csESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(B_csESP[:, 2]):
            B_csESP[i, :] = B_csESP_partitioning[rand.randint(0, len(B_csESP_partitioning[:, 1])-1), :]
            i += 1

        #For Arsenic.
        As_csESP_partitioning = np.column_stack((as_dict['csESP']['solid'],
                                                as_dict['csESP']['liquid'],
                                                as_dict['csESP']['gas']))
        As_csESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(As_csESP[:,2]):
            As_csESP[i, :] = As_csESP_partitioning[rand.randint(0, len(As_csESP_partitioning[:, 1])-1), :]
            i += 1

        # For Lead.
        Pb_csESP_partitioning = np.column_stack((pb_dict['csESP']['solid'],
                                                pb_dict['csESP']['liquid'],
                                                pb_dict['csESP']['gas']))

        Pb_csESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(As_csESP[:,2]):
            Pb_csESP[i, :] = Pb_csESP_partitioning[rand.randint(0, len(Pb_csESP_partitioning[:, 1])-1), :]
            i += 1

        #For Mercury.
        Hg_csESP_partitioning = np.column_stack((hg_dict['csESP']['solid'],
                                                hg_dict['csESP']['liquid'],
                                                hg_dict['csESP']['gas']))
        Hg_csESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Hg_csESP[:,2]):
            Hg_csESP[i, :] = Hg_csESP_partitioning[rand.randint(0, len(Hg_csESP_partitioning[:, 1])-1), :]
            i += 1

        #For Sulfur.
        S_csESP_partitioning = np.column_stack((s_dict['csESP']['solid'],
                                                s_dict['csESP']['liquid'],
                                                s_dict['csESP']['gas']))
        S_csESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(S_csESP[:,2]):
            S_csESP[i, :] = S_csESP_partitioning[rand.randint(0, len(S_csESP_partitioning[:, 1])-1), :]
            i += 1

    return Cl_csESP, Se_csESP, B_csESP, Br_csESP, Pb_csESP, As_csESP, Hg_csESP, S_csESP

def hsESP_modeling(hsESP, runs):

    #Defines partitioning of hsESP.

    if hsESP == 0:
        #If there is no hsESP installed, then there is no partitioning and everything stays in the gaseous phase.
        hsESP_partitioning = np.zeros(shape=(runs, 3))
        hsESP_partitioning[:, 2] = np.ones(shape=runs)

        Cl_hsESP = hsESP_partitioning
        Se_hsESP = hsESP_partitioning
        B_hsESP = hsESP_partitioning
        Br_hsESP = hsESP_partitioning
        Pb_hsESP = hsESP_partitioning
        As_hsESP = hsESP_partitioning
        Hg_hsESP = hsESP_partitioning
        S_hsESP = hsESP_partitioning

    elif hsESP ==1:
        # Chlorine and Bromine currently lack trace element partitioning data.
        hsESP_partitioning = np.zeros(shape=(runs,4))
        hsESP_partitioning[:,2] = np.ones(shape=runs)

        # For Chlorine.

        Cl_hsESP_partitioning = np.column_stack((cl_dict['hsESP']['solid'],
                                                cl_dict['hsESP']['liquid'],
                                                cl_dict['hsESP']['gas']))

        Cl_hsESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Cl_hsESP[:, 2]):
            Cl_hsESP[i, :] = Cl_hsESP_partitioning[rand.randint(0, len(Cl_hsESP_partitioning[:, 1]) - 1), :]
            i += 1

        # For Selenium.
        Se_hsESP_partitioning = np.column_stack((se_dict['hsESP']['solid'],
                                                se_dict['hsESP']['liquid'],
                                                se_dict['hsESP']['gas']))
        Se_hsESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Se_hsESP[:, 2]):
            Se_hsESP[i, :] = Se_hsESP_partitioning[rand.randint(0, len(Se_hsESP_partitioning[:, 1])-1), :]
            i += 1

        # For Boron.
        B_hsESP_partitioning = np.column_stack((b_dict['hsESP']['solid'],
                                               b_dict['hsESP']['liquid'],
                                               b_dict['hsESP']['gas']))

        B_hsESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(B_hsESP[:, 2]):
            B_hsESP[i, :] = B_hsESP_partitioning[rand.randint(0, len(B_hsESP_partitioning[:, 1])-1), :]
            i += 1

        #For Arsenic.
        As_hsESP_partitioning = np.column_stack((as_dict['hsESP']['solid'],
                                                as_dict['hsESP']['liquid'],
                                                as_dict['hsESP']['gas']))
        As_hsESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(As_hsESP[:,2]):
            As_hsESP[i, :] = As_hsESP_partitioning[rand.randint(0, len(As_hsESP_partitioning[:, 1])-1), :]
            i += 1

        # For Lead.
        Pb_hsESP_partitioning = np.column_stack((pb_dict['hsESP']['solid'],
                                                pb_dict['hsESP']['liquid'],
                                                pb_dict['hsESP']['gas']))

        Pb_hsESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Pb_hsESP[:,2]):
            Pb_hsESP[i, :] = Pb_hsESP_partitioning[rand.randint(0, len(Pb_hsESP_partitioning[:, 1])-1), :]
            i += 1

        #For Mercury.
        Hg_hsESP_partitioning = np.column_stack((hg_dict['hsESP']['solid'],
                                                hg_dict['hsESP']['liquid'],
                                                hg_dict['hsESP']['gas']))
        Hg_hsESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Hg_hsESP[:,2]):
            Hg_hsESP[i, :] = Hg_hsESP_partitioning[rand.randint(0, len(Hg_hsESP_partitioning[:, 1])-1), :]
            i += 1

        # For Bromine.
        Br_hsESP_partitioning = np.column_stack((br_dict['hsESP']['solid'],
                                                br_dict['hsESP']['liquid'],
                                                br_dict['hsESP']['gas']))

        Br_hsESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Br_hsESP[:,2]):
            Br_hsESP[i, :] = Br_hsESP_partitioning[rand.randint(0, len(Br_hsESP_partitioning[:, 1])-1), :]
            i += 1

        # For Sulfur.
        S_hsESP_partitioning = np.column_stack((s_dict['hsESP']['solid'],
                                                s_dict['hsESP']['liquid'],
                                                s_dict['hsESP']['gas']))

        S_hsESP = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(S_hsESP[:,2]):
            S_hsESP[i, :] = S_hsESP_partitioning[rand.randint(0, len(S_hsESP_partitioning[:, 1])-1), :]
            i += 1

    return Cl_hsESP, Se_hsESP, B_hsESP, Br_hsESP, Pb_hsESP, As_hsESP, Hg_hsESP, S_hsESP


def FF_modeling(FF, runs):
    # Defines partitioning in fabric filters.  Note that this also includes bottom ash since Daniel Sun does not separate
    # bottom ash in his SI.  He also does not include partitioning information for Chlorine, Arsenic, Boron, Bromine, and
    # Lead.

    if FF == 0:
        # If there is no FF installed, then there is no partitioning and everything stays in the gaseous phase.
        FF_partitioning = np.zeros(shape=(runs, 3))
        FF_partitioning[:, 2] = np.ones(shape=runs)

        Cl_FF = FF_partitioning
        Se_FF = FF_partitioning
        B_FF = FF_partitioning
        Br_FF = FF_partitioning
        Pb_FF = FF_partitioning
        As_FF = FF_partitioning
        Hg_FF = FF_partitioning
        S_FF = FF_partitioning

    elif FF == 1:
        # Partitioning data is still missing for Chlorine and Bromine.
        FF_partitioning = np.zeros(shape=(runs,4))
        FF_partitioning[:,2] = np.ones(shape=runs)

        # For Chlorine.

        Cl_FF_partitioning = np.column_stack((cl_dict['FF']['solid'],
                                                cl_dict['FF']['liquid'],
                                                cl_dict['FF']['gas']))

        Cl_FF = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Cl_FF[:, 2]):
            Cl_FF[i, :] = Cl_FF_partitioning[rand.randint(0, len(Cl_FF_partitioning[:, 1]) - 1), :]
            i += 1

        # For Selenium.
        Se_FF_partitioning = np.column_stack((se_dict['FF']['solid'],
                                                se_dict['FF']['liquid'],
                                                se_dict['FF']['gas']))
        Se_FF = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Se_FF[:, 2]):
            Se_FF[i, :] = Se_FF_partitioning[rand.randint(0, len(Se_FF_partitioning[:, 1])-1), :]
            i += 1

        # For Boron.
        B_FF_partitioning = np.column_stack((b_dict['FF']['solid'],
                                               b_dict['FF']['liquid'],
                                               b_dict['FF']['gas']))

        B_FF = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(B_FF[:, 2]):
            B_FF[i, :] = B_FF_partitioning[rand.randint(0, len(B_FF_partitioning[:, 1])-1), :]
            i += 1

        #For Arsenic.
        As_FF_partitioning = np.column_stack((as_dict['FF']['solid'],
                                                as_dict['FF']['liquid'],
                                                as_dict['FF']['gas']))
        As_FF = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(As_FF[:,2]):
            As_FF[i, :] = As_FF_partitioning[rand.randint(0, len(As_FF_partitioning[:, 1])-1), :]
            i += 1

        # For Lead.
        Pb_FF_partitioning = np.column_stack((pb_dict['FF']['solid'],
                                                pb_dict['FF']['liquid'],
                                                pb_dict['FF']['gas']))

        Pb_FF = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Pb_FF[:,2]):
            Pb_FF[i, :] = Pb_FF_partitioning[rand.randint(0, len(Pb_FF_partitioning[:, 1])-1), :]
            i += 1

        #For Mercury.
        Hg_FF_partitioning = np.column_stack((hg_dict['FF']['solid'],
                                                hg_dict['FF']['liquid'],
                                                hg_dict['FF']['gas']))
        Hg_FF = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Hg_FF[:,2]):
            Hg_FF[i, :] = Hg_FF_partitioning[rand.randint(0, len(Hg_FF_partitioning[:, 1])-1), :]
            i += 1

        # For Bromine.
        Br_FF_partitioning = np.column_stack((br_dict['FF']['solid'],
                                                br_dict['FF']['liquid'],
                                                br_dict['FF']['gas']))

        Br_FF = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Br_FF[:,2]):
            Br_FF[i, :] = Br_FF_partitioning[rand.randint(0, len(Br_FF_partitioning[:, 1])-1), :]
            i += 1

        # For Sulfur.
        S_FF_partitioning = np.column_stack((s_dict['FF']['solid'],
                                             s_dict['FF']['liquid'],
                                             s_dict['FF']['gas']))

        S_FF = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(S_FF[:, 2]):
            S_FF[i, :] = S_FF_partitioning[rand.randint(0, len(S_FF_partitioning[:, 1])-1), :]
            i += 1

    return Cl_FF, Se_FF, B_FF, Br_FF, Pb_FF, As_FF, Hg_FF, S_FF

#Modeling partitioning in SCR systems

def SCR_modeling(SCR, runs):

    #Defines partitioning of selective catalytic reduction.  Note that I'm leaving this as not affecting partitioning
    # for the time being until I get creater clarity for what solid streams are produced for things to partition into.

    if SCR == 0:
        #If there is no SCR installed, then there is no partitioning and everything stays in the gaseous phase.
        SCR_partitioning = np.zeros(shape=(runs, 3))
        SCR_partitioning[:, 2] = np.ones(shape=runs)

        Cl_SCR = SCR_partitioning
        Se_SCR = SCR_partitioning
        B_SCR = SCR_partitioning
        Br_SCR = SCR_partitioning
        Pb_SCR = SCR_partitioning
        As_SCR = SCR_partitioning
        Hg_SCR = SCR_partitioning
        S_SCR = SCR_partitioning

    elif SCR == 1:
    # As it is modeled right now, no partitioning occurs in the SCR since there is no solid or liquid waste stream
    # produced in the process.
        SCR_partitioning = np.zeros(shape=(runs,4))
        SCR_partitioning[:,2] = np.ones(shape=runs)

        # For Chlorine.

        Cl_SCR_partitioning = np.column_stack((cl_dict['SCR']['solid'],
                                                cl_dict['SCR']['liquid'],
                                                cl_dict['SCR']['gas']))

        Cl_SCR = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Cl_SCR[:, 2]):
            Cl_SCR[i, :] = Cl_SCR_partitioning[rand.randint(0, len(Cl_SCR_partitioning[:, 1]) - 1), :]
            i += 1

        # For Selenium.
        Se_SCR_partitioning = np.column_stack((se_dict['SCR']['solid'],
                                                se_dict['SCR']['liquid'],
                                                se_dict['SCR']['gas']))
        Se_SCR = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Se_SCR[:, 2]):
            Se_SCR[i, :] = Se_SCR_partitioning[rand.randint(0, len(Se_SCR_partitioning[:, 1])-1), :]
            i += 1

        # For Boron.
        B_SCR_partitioning = np.column_stack((b_dict['SCR']['solid'],
                                               b_dict['SCR']['liquid'],
                                               b_dict['SCR']['gas']))

        B_SCR = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(B_SCR[:, 2]):
            B_SCR[i, :] = B_SCR_partitioning[rand.randint(0, len(B_SCR_partitioning[:, 1])-1), :]
            i += 1

        #For Arsenic.
        As_SCR_partitioning = np.column_stack((as_dict['SCR']['solid'],
                                                as_dict['SCR']['liquid'],
                                                as_dict['SCR']['gas']))
        As_SCR = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(As_SCR[:,2]):
            As_SCR[i, :] = As_SCR_partitioning[rand.randint(0, len(As_SCR_partitioning[:, 1])-1), :]
            i += 1

        # For Lead.
        Pb_SCR_partitioning = np.column_stack((pb_dict['SCR']['solid'],
                                                pb_dict['SCR']['liquid'],
                                                pb_dict['SCR']['gas']))

        Pb_SCR = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Pb_SCR[:,2]):
            Pb_SCR[i, :] = Pb_SCR_partitioning[rand.randint(0, len(Pb_SCR_partitioning[:, 1])-1), :]
            i += 1

        #For Mercury.
        Hg_SCR_partitioning = np.column_stack((hg_dict['SCR']['solid'],
                                                hg_dict['SCR']['liquid'],
                                                hg_dict['SCR']['gas']))
        Hg_SCR = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Hg_SCR[:,2]):
            Hg_SCR[i, :] = Hg_SCR_partitioning[rand.randint(0, len(Hg_SCR_partitioning[:, 1])-1), :]
            i += 1

        # For Bromine.
        Br_SCR_partitioning = np.column_stack((br_dict['SCR']['solid'],
                                                br_dict['SCR']['liquid'],
                                                br_dict['SCR']['gas']))

        Br_SCR = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Br_SCR[:,2]):
            Br_SCR[i, :] = Br_SCR_partitioning[rand.randint(0, len(Br_SCR_partitioning[:, 1])-1), :]
            i += 1

        # For Sulfur.
        S_SCR_partitioning = np.column_stack((s_dict['SCR']['solid'],
                                              s_dict['SCR']['liquid'],
                                              s_dict['SCR']['gas']))

        S_SCR = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(S_SCR[:,2]):
            S_SCR[i, :] = S_SCR_partitioning[rand.randint(0, len(S_SCR_partitioning[:, 1])-1), :]
            i += 1

    return Cl_SCR, Se_SCR, B_SCR, Br_SCR, Pb_SCR, As_SCR, Hg_SCR, S_SCR

#Modeling partitioning in ACI systems

def ACI_modeling(ACI, runs):

    #Defines partitioning of activated carbon injection.  Note that Daniel Sun has only noted partitioning for mercury,
    #so this does not include partitioning information for Chlorine, Arsenic, Selenium, Boron, Bromine, and Lead.

    if ACI == 0:
        #If there is no ACI installed, then there is no partitioning and everything stays in the gaseous phase.
        ACI_partitioning = np.zeros(shape=(runs, 3))
        ACI_partitioning[:, 2] = np.ones(shape=runs)

        Cl_ACI = ACI_partitioning
        Se_ACI = ACI_partitioning
        B_ACI = ACI_partitioning
        Br_ACI = ACI_partitioning
        Pb_ACI = ACI_partitioning
        As_ACI = ACI_partitioning
        Hg_ACI = ACI_partitioning
        S_ACI = ACI_partitioning

    elif ACI == 1:
        # This step only models removal of Hg.

        ACI_partitioning = np.zeros(shape=(runs,4))
        ACI_partitioning[:,2] = np.ones(shape=runs)

        # For Chlorine.

        Cl_ACI_partitioning = np.column_stack((cl_dict['ACI']['solid'],
                                                cl_dict['ACI']['liquid'],
                                                cl_dict['ACI']['gas']))

        Cl_ACI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Cl_ACI[:, 2]):
            Cl_ACI[i, :] = Cl_ACI_partitioning[rand.randint(0, len(Cl_ACI_partitioning[:, 1]) - 1), :]
            i += 1

        # For Selenium.
        Se_ACI_partitioning = np.column_stack((se_dict['ACI']['solid'],
                                                se_dict['ACI']['liquid'],
                                                se_dict['ACI']['gas']))
        Se_ACI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Se_ACI[:, 2]):
            Se_ACI[i, :] = Se_ACI_partitioning[rand.randint(0, len(Se_ACI_partitioning[:, 1])-1), :]
            i += 1

        # For Boron.
        B_ACI_partitioning = np.column_stack((b_dict['ACI']['solid'],
                                               b_dict['ACI']['liquid'],
                                               b_dict['ACI']['gas']))

        B_ACI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(B_ACI[:, 2]):
            B_ACI[i, :] = B_ACI_partitioning[rand.randint(0, len(B_ACI_partitioning[:, 1])-1), :]
            i += 1

        #For Arsenic.
        As_ACI_partitioning = np.column_stack((as_dict['ACI']['solid'],
                                                as_dict['ACI']['liquid'],
                                                as_dict['ACI']['gas']))
        As_ACI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(As_ACI[:,2]):
            As_ACI[i, :] = As_ACI_partitioning[rand.randint(0, len(As_ACI_partitioning[:, 1])-1), :]
            i += 1

        # For Lead.
        Pb_ACI_partitioning = np.column_stack((pb_dict['ACI']['solid'],
                                                pb_dict['ACI']['liquid'],
                                                pb_dict['ACI']['gas']))

        Pb_ACI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Pb_ACI[:,2]):
            Pb_ACI[i, :] = Pb_ACI_partitioning[rand.randint(0, len(Pb_ACI_partitioning[:, 1])-1), :]
            i += 1

        #For Mercury.
        Hg_ACI_partitioning = np.column_stack((hg_dict['ACI']['solid'],
                                                hg_dict['ACI']['liquid'],
                                                hg_dict['ACI']['gas']))
        Hg_ACI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Hg_ACI[:,2]):
            Hg_ACI[i, :] = Hg_ACI_partitioning[rand.randint(0, len(Hg_ACI_partitioning[:, 1])-1), :]
            i += 1

        # For Bromine.
        Br_ACI_partitioning = np.column_stack((br_dict['ACI']['solid'],
                                                br_dict['ACI']['liquid'],
                                                br_dict['ACI']['gas']))

        Br_ACI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Br_ACI[:,2]):
            Br_ACI[i, :] = Br_ACI_partitioning[rand.randint(0, len(Br_ACI_partitioning[:, 1])-1), :]
            i += 1

        # For Sulfur.
        S_ACI_partitioning = np.column_stack((s_dict['ACI']['solid'],
                                              s_dict['ACI']['liquid'],
                                              s_dict['ACI']['gas']))

        S_ACI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(S_ACI[:,2]):
            S_ACI[i, :] = S_ACI_partitioning[rand.randint(0, len(S_ACI_partitioning[:, 1])-1), :]
            i += 1

    return Cl_ACI, Se_ACI, B_ACI, Br_ACI, Pb_ACI, As_ACI, Hg_ACI, S_ACI

def DSI_modeling(DSI, runs):

    #Defines partitioning of activated carbon injection.  Note that Daniel Sun has only noted partitioning for mercury,
    #so this does not include partitioning information for Chlorine, Arsenic, Selenium, Boron, Bromine, and Lead.

    if DSI == 0:
        #If there is no DSI installed, then there is no partitioning and everything stays in the gaseous phase.
        DSI_partitioning = np.zeros(shape=(runs, 3))
        DSI_partitioning[:, 2] = np.ones(shape=runs)

        Cl_DSI = DSI_partitioning
        Se_DSI = DSI_partitioning
        B_DSI = DSI_partitioning
        Br_DSI = DSI_partitioning
        Pb_DSI = DSI_partitioning
        As_DSI = DSI_partitioning
        Hg_DSI = DSI_partitioning
        S_DSI = DSI_partitioning

    elif DSI == 1:
        # This step only models removal of Hg.

        DSI_partitioning = np.zeros(shape=(runs,4))
        DSI_partitioning[:,2] = np.ones(shape=runs)

        # For Chlorine.

        Cl_DSI_partitioning = np.column_stack((cl_dict['DSI']['solid'],
                                                cl_dict['DSI']['liquid'],
                                                cl_dict['DSI']['gas']))

        Cl_DSI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Cl_DSI[:, 2]):
            Cl_DSI[i, :] = Cl_DSI_partitioning[rand.randint(0, len(Cl_DSI_partitioning[:, 1]) - 1), :]
            i += 1

        # For Selenium.
        Se_DSI_partitioning = np.column_stack((se_dict['DSI']['solid'],
                                                se_dict['DSI']['liquid'],
                                                se_dict['DSI']['gas']))
        Se_DSI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Se_DSI[:, 2]):
            Se_DSI[i, :] = Se_DSI_partitioning[rand.randint(0, len(Se_DSI_partitioning[:, 1])-1), :]
            i += 1

        # For Boron.
        B_DSI_partitioning = np.column_stack((b_dict['DSI']['solid'],
                                               b_dict['DSI']['liquid'],
                                               b_dict['DSI']['gas']))

        B_DSI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(B_DSI[:, 2]):
            B_DSI[i, :] = B_DSI_partitioning[rand.randint(0, len(B_DSI_partitioning[:, 1])-1), :]
            i += 1

        #For Arsenic.
        As_DSI_partitioning = np.column_stack((as_dict['DSI']['solid'],
                                                as_dict['DSI']['liquid'],
                                                as_dict['DSI']['gas']))
        As_DSI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(As_DSI[:,2]):
            As_DSI[i, :] = As_DSI_partitioning[rand.randint(0, len(As_DSI_partitioning[:, 1])-1), :]
            i += 1

        # For Lead.
        Pb_DSI_partitioning = np.column_stack((pb_dict['DSI']['solid'],
                                                pb_dict['DSI']['liquid'],
                                                pb_dict['DSI']['gas']))

        Pb_DSI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Pb_DSI[:,2]):
            Pb_DSI[i, :] = Pb_DSI_partitioning[rand.randint(0, len(Pb_DSI_partitioning[:, 1])-1), :]
            i += 1

        #For Mercury.
        Hg_DSI_partitioning = np.column_stack((hg_dict['DSI']['solid'],
                                                hg_dict['DSI']['liquid'],
                                                hg_dict['DSI']['gas']))
        Hg_DSI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Hg_DSI[:,2]):
            Hg_DSI[i, :] = Hg_DSI_partitioning[rand.randint(0, len(Hg_DSI_partitioning[:, 1])-1), :]
            i += 1

        # For Bromine.
        Br_DSI_partitioning = np.column_stack((br_dict['DSI']['solid'],
                                                br_dict['DSI']['liquid'],
                                                br_dict['DSI']['gas']))

        Br_DSI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Br_DSI[:,2]):
            Br_DSI[i, :] = Br_DSI_partitioning[rand.randint(0, len(Br_DSI_partitioning[:, 1])-1), :]
            i += 1

        # For Sulfur.
        S_DSI_partitioning = np.column_stack((s_dict['DSI']['solid'],
                                              s_dict['DSI']['liquid'],
                                              s_dict['DSI']['gas']))

        S_DSI = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(S_DSI[:,2]):
            S_DSI[i, :] = S_DSI_partitioning[rand.randint(0, len(S_DSI_partitioning[:, 1])-1), :]
            i += 1

    return Cl_DSI, Se_DSI, B_DSI, Br_DSI, Pb_DSI, As_DSI, Hg_DSI, S_DSI

#Modeling partitioning in FGD systems.

def wetFGD_modeling(wetFGD, FGDtype, runs):

    #Defines partitioning of wetFGD.  He does not include partitioning information for Boron, Bromine, and Lead.

    if wetFGD == 0:
        #If there is no wetFGD installed, then there is no partitioning and everything stays in the gaseous phase.
        wetFGD_partitioning = np.zeros(shape=(runs, 3))
        wetFGD_partitioning[:, 2] = np.ones(shape=runs)

        Cl_wetFGD = wetFGD_partitioning
        Se_wetFGD = wetFGD_partitioning
        B_wetFGD = wetFGD_partitioning
        Br_wetFGD = wetFGD_partitioning
        Pb_wetFGD = wetFGD_partitioning
        As_wetFGD = wetFGD_partitioning
        Hg_wetFGD = wetFGD_partitioning
        Se_wetFGD_ww = 0
        S_wetFGD = wetFGD_partitioning

    elif wetFGD == 1:
        # Removal of bromine is treated as similar to chlorine for wetFGD processes, since they are both Type III trace
        # elements.

        wetFGD_partitioning = np.zeros(shape=(runs,4))
        wetFGD_partitioning[:,2] = np.ones(shape=runs)

        # For Chlorine.

        Cl_wetFGD_partitioning = np.column_stack((cl_dict['wetFGD']['solid'],
                                                cl_dict['wetFGD']['liquid'],
                                                cl_dict['wetFGD']['gas']))

        Cl_wetFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Cl_wetFGD[:, 2]):
            Cl_wetFGD[i, :] = Cl_wetFGD_partitioning[rand.randint(0, len(Cl_wetFGD_partitioning[:, 1]) - 1), :]
            i += 1

        # For Selenium.
        Se_wetFGD_partitioning = np.column_stack((se_dict['wetFGD']['solid'],
                                                se_dict['wetFGD']['liquid'],
                                                se_dict['wetFGD']['gas']))
        Se_wetFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Se_wetFGD[:, 2]):
            Se_wetFGD[i, :] = Se_wetFGD_partitioning[rand.randint(0, len(Se_wetFGD_partitioning[:, 1])-1), :]
            i += 1

        # For Selenium in waste water
        if FGDtype != 0:
            Se_wetFGD_ww = wetFGD_wastewater_Se_modeling(FGDtype, runs)
        else:
            Se_wetFGD_ww = 0

        # For Boron.
        B_wetFGD_partitioning = np.column_stack((b_dict['wetFGD']['solid'],
                                               b_dict['wetFGD']['liquid'],
                                               b_dict['wetFGD']['gas']))

        B_wetFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(B_wetFGD[:, 2]):
            B_wetFGD[i, :] = B_wetFGD_partitioning[rand.randint(0, len(B_wetFGD_partitioning[:, 1])-1), :]
            i += 1

        #For Arsenic.
        As_wetFGD_partitioning = np.column_stack((as_dict['wetFGD']['solid'],
                                                as_dict['wetFGD']['liquid'],
                                                as_dict['wetFGD']['gas']))
        As_wetFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(As_wetFGD[:,2]):
            As_wetFGD[i, :] = As_wetFGD_partitioning[rand.randint(0, len(As_wetFGD_partitioning[:, 1])-1), :]
            i += 1

        # For Lead.
        Pb_wetFGD_partitioning = np.column_stack((pb_dict['wetFGD']['solid'],
                                                pb_dict['wetFGD']['liquid'],
                                                pb_dict['wetFGD']['gas']))

        Pb_wetFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Pb_wetFGD[:,2]):
            Pb_wetFGD[i, :] = Pb_wetFGD_partitioning[rand.randint(0, len(Pb_wetFGD_partitioning[:, 1])-1), :]
            i += 1

        #For Mercury.
        Hg_wetFGD_partitioning = np.column_stack((hg_dict['wetFGD']['solid'],
                                                hg_dict['wetFGD']['liquid'],
                                                hg_dict['wetFGD']['gas']))
        Hg_wetFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Hg_wetFGD[:,2]):
            Hg_wetFGD[i, :] = Hg_wetFGD_partitioning[rand.randint(0, len(Hg_wetFGD_partitioning[:, 1])-1), :]
            i += 1

        # For Bromine.
        Br_wetFGD_partitioning = np.column_stack((br_dict['wetFGD']['solid'],
                                                br_dict['wetFGD']['liquid'],
                                                br_dict['wetFGD']['gas']))

        Br_wetFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Br_wetFGD[:,2]):
            Br_wetFGD[i, :] = Br_wetFGD_partitioning[rand.randint(0, len(Br_wetFGD_partitioning[:, 1])-1), :]
            i += 1

        # For Sulfur.
        S_wetFGD_partitioning = np.column_stack((s_dict['wetFGD']['solid'],
                                                s_dict['wetFGD']['liquid'],
                                                s_dict['wetFGD']['gas']))

        S_wetFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(S_wetFGD[:,2]):
            S_wetFGD[i, :] = S_wetFGD_partitioning[rand.randint(0, len(S_wetFGD_partitioning[:, 1])-1), :]
            i += 1

    return Cl_wetFGD, Se_wetFGD, B_wetFGD, Br_wetFGD, Pb_wetFGD, As_wetFGD, Hg_wetFGD, Se_wetFGD_ww, S_wetFGD

def wetFGD_wastewater_Se_modeling(FGDtype, runs):
    #takes a wetFGD type (string) and return the partitining modeling for that wetFGD system waste water
    Se_wetFGD_ww_paritioning = np.column_stack((se_wFGD_dict[FGDtype]['Se4'],
                                                se_wFGD_dict[FGDtype]['Se6'],
                                                se_wFGD_dict[FGDtype]['SeSO3'],
                                                se_wFGD_dict[FGDtype]['Others']))
    Se_wetFGD_ww = np.zeros(shape=(runs, 4))
    i = 0
    while i < len(Se_wetFGD_ww):
        Se_wetFGD_ww[i, :] = Se_wetFGD_ww_paritioning[rand.randint(0, len(Se_wetFGD_ww_paritioning[:, 1]) - 1), :]
        i += 1 
    return Se_wetFGD_ww


def dryFGD_modeling(dryFGD, runs):

    #Defines partitioning of dry FGD systems.  Note that Daniel Sun did not include any dryFGD's in his analysis, so
    #there are currently no partitioning coefficients for this technology.

    if dryFGD == 0:
        #If there is no dry FGD system installed, then there is no partitioning and everything stays in the gaseous
        #phase.
        dryFGD_partitioning = np.zeros(shape=(runs, 3))
        dryFGD_partitioning[:, 2] = np.ones(shape=runs)

        Cl_dryFGD = dryFGD_partitioning
        Se_dryFGD = dryFGD_partitioning
        B_dryFGD = dryFGD_partitioning
        Br_dryFGD = dryFGD_partitioning
        Pb_dryFGD = dryFGD_partitioning
        As_dryFGD = dryFGD_partitioning
        Hg_dryFGD = dryFGD_partitioning
        S_dryFGD = dryFGD_partitioning

    elif dryFGD ==1:
        # Removal of Lead, Bromine and Chlorine, is not modeled currently.

        dryFGD_partitioning = np.zeros(shape=(runs,4))
        dryFGD_partitioning[:,2] = np.ones(shape=runs)

        # For Chlorine.

        Cl_dryFGD_partitioning = np.column_stack((cl_dict['dryFGD']['solid'],
                                                cl_dict['dryFGD']['liquid'],
                                                cl_dict['dryFGD']['gas']))

        Cl_dryFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Cl_dryFGD[:, 2]):
            Cl_dryFGD[i, :] = Cl_dryFGD_partitioning[rand.randint(0, len(Cl_dryFGD_partitioning[:, 1]) - 1), :]
            i += 1

        # For Selenium.
        Se_dryFGD_partitioning = np.column_stack((se_dict['dryFGD']['solid'],
                                                se_dict['dryFGD']['liquid'],
                                                se_dict['dryFGD']['gas']))
        Se_dryFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Se_dryFGD[:, 2]):
            Se_dryFGD[i, :] = Se_dryFGD_partitioning[rand.randint(0, len(Se_dryFGD_partitioning[:, 1])-1), :]
            i += 1

        # For Boron.
        B_dryFGD_partitioning = np.column_stack((b_dict['dryFGD']['solid'],
                                               b_dict['dryFGD']['liquid'],
                                               b_dict['dryFGD']['gas']))

        B_dryFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(B_dryFGD[:, 2]):
            B_dryFGD[i, :] = B_dryFGD_partitioning[rand.randint(0, len(B_dryFGD_partitioning[:, 1])-1), :]
            i += 1

        #For Arsenic.
        As_dryFGD_partitioning = np.column_stack((as_dict['dryFGD']['solid'],
                                                as_dict['dryFGD']['liquid'],
                                                as_dict['dryFGD']['gas']))
        As_dryFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(As_dryFGD[:,2]):
            As_dryFGD[i, :] = As_dryFGD_partitioning[rand.randint(0, len(As_dryFGD_partitioning[:, 1])-1), :]
            i += 1

        # For Lead.
        Pb_dryFGD_partitioning = np.column_stack((pb_dict['dryFGD']['solid'],
                                                pb_dict['dryFGD']['liquid'],
                                                pb_dict['dryFGD']['gas']))

        Pb_dryFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Pb_dryFGD[:,2]):
            Pb_dryFGD[i, :] = Pb_dryFGD_partitioning[rand.randint(0, len(Pb_dryFGD_partitioning[:, 1])-1), :]
            i += 1

        #For Mercury.
        Hg_dryFGD_partitioning = np.column_stack((hg_dict['dryFGD']['solid'],
                                                hg_dict['dryFGD']['liquid'],
                                                hg_dict['dryFGD']['gas']))
        Hg_dryFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Hg_dryFGD[:,2]):
            Hg_dryFGD[i, :] = Hg_dryFGD_partitioning[rand.randint(0, len(Hg_dryFGD_partitioning[:, 1])-1), :]
            i += 1

        # For Bromine.
        Br_dryFGD_partitioning = np.column_stack((br_dict['dryFGD']['solid'],
                                                br_dict['dryFGD']['liquid'],
                                                br_dict['dryFGD']['gas']))

        Br_dryFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(Br_dryFGD[:,2]):
            Br_dryFGD[i, :] = Br_dryFGD_partitioning[rand.randint(0, len(Br_dryFGD_partitioning[:, 1])-1), :]
            i += 1

        # For Sulfur.
        S_dryFGD_partitioning = np.column_stack((s_dict['dryFGD']['solid'],
                                                 s_dict['dryFGD']['liquid'],
                                                 s_dict['dryFGD']['gas']))

        S_dryFGD = np.zeros(shape=(runs, 3))
        i = 0
        while i < len(S_dryFGD[:,2]):
            S_dryFGD[i, :] = S_dryFGD_partitioning[rand.randint(0, len(S_dryFGD_partitioning[:, 1])-1), :]
            i += 1

    return Cl_dryFGD, Se_dryFGD, B_dryFGD, Br_dryFGD, Pb_dryFGD, As_dryFGD, Hg_dryFGD, S_dryFGD

def wetFGD_SCR_modeling(runs):
    '''For the Hg partiioning when wetFGD and SCR both exist'''

    Hg_wetFGD_SCR_partitioning = np.column_stack((hg_dict['wetFGD+SCR']['solid'],
                                              hg_dict['wetFGD+SCR']['liquid'],
                                              hg_dict['wetFGD+SCR']['gas']))
    Hg_wetFGD_SCR = np.zeros(shape=(runs, 3))
    i = 0
    while i < len(Hg_wetFGD_SCR[:, 2]):
        Hg_wetFGD_SCR[i, :] = Hg_wetFGD_SCR_partitioning[rand.randint(0, len(Hg_wetFGD_SCR_partitioning[:, 1]) - 1), :]
        i += 1
    return Hg_wetFGD_SCR


