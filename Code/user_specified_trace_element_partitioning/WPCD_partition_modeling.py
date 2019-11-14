import numpy as np
import random as rand
import pathlib
import sys

fileDir = pathlib.Path(__file__).parents[2]
code_library_folder = fileDir / 'Code' / 'function_dictionary_library'
sys.path.append(str(code_library_folder))
from wpcd_partitioning_dictionaries import as_dict, cl_dict, pb_dict, hg_dict, n_dict, se_dict


def alox_modeling(alox, runs):
    if alox == 0:
        alox_removal = np.zeros(shape=(runs, 3))
        alox_removal[:, 1] = np.ones(shape=runs)

        as_alox = alox_removal
        cl_alox = alox_removal
        pb_alox = alox_removal
        hg_alox = alox_removal
        n_alox = alox_removal
        se_alox = alox_removal

    elif alox == 1:
        alox_removal = np.zeros(shape=(runs, 3))
        alox_removal[:, 1] = np.ones(shape=runs)

        # For Arsenic.
        as_alox_removal = np.column_stack((as_dict['AlOx']['removal'], as_dict['AlOx']['effluent']))
        as_alox = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(as_alox[:, 1]):
            as_alox[i, :] = as_alox_removal[rand.randint(0, len(as_alox_removal) - 1), :]
            i += 1

        # For Chlorides.
        cl_alox_removal = np.column_stack((cl_dict['AlOx']['removal'], cl_dict['AlOx']['effluent']))
        cl_alox = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(cl_alox[:, 1]):
            cl_alox[i, :] = cl_alox_removal[rand.randint(0, len(cl_alox_removal) - 1), :]
            i += 1

        # For Lead.
        pb_alox_removal = np.column_stack((pb_dict['AlOx']['removal'], pb_dict['AlOx']['effluent']))
        pb_alox = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(pb_alox[:, 1]):
            pb_alox[i, :] = pb_alox_removal[rand.randint(0, len(pb_alox_removal) - 1), :]
            i += 1

        # For Mercury.
        hg_alox_removal = np.column_stack((hg_dict['AlOx']['removal'], hg_dict['AlOx']['effluent']))
        hg_alox = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(hg_alox[:, 1]):
            hg_alox[i, :] = hg_alox_removal[rand.randint(0, len(hg_alox_removal) - 1), :]
            i += 1

        # For Nitrogen.
        n_alox_removal = np.column_stack((n_dict['AlOx']['removal'], n_dict['AlOx']['effluent']))
        n_alox = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(n_alox[:, 1]):
            n_alox[i, :] = n_alox_removal[rand.randint(0, len(n_alox_removal) - 1), :]
            i += 1

        # For Selenium.
        se_alox_removal = np.column_stack((se_dict['AlOx']['removal'], se_dict['AlOx']['effluent']))
        se_alox = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(se_alox[:, 1]):
            se_alox[i, :] = se_alox_removal[rand.randint(0, len(se_alox_removal) - 1), :]
            i += 1

    return as_alox, cl_alox, pb_alox, hg_alox, se_alox #, n_alox


def bt_modeling(bt, runs):
    if bt == 0:
        bt_removal = np.zeros(shape=(runs, 3))
        bt_removal[:, 1] = np.ones(shape=runs)

        as_bt = bt_removal
        cl_bt = bt_removal
        pb_bt = bt_removal
        hg_bt = bt_removal
        n_bt = bt_removal
        se_bt = bt_removal

    elif bt == 1:
        bt_removal = np.zeros(shape=(runs, 3))
        bt_removal[:, 1] = np.ones(shape=runs)

        # For Arsenic.
        as_bt_removal = np.column_stack((as_dict['BT']['removal'], as_dict['BT']['effluent']))
        as_bt = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(as_bt[:, 1]):
            as_bt[i, :] = as_bt_removal[rand.randint(0, len(as_bt_removal) - 1), :]
            i += 1

        # For Chlorides.
        cl_bt_removal = np.column_stack((cl_dict['BT']['removal'], cl_dict['BT']['effluent']))
        cl_bt = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(cl_bt[:, 1]):
            cl_bt[i, :] = cl_bt_removal[rand.randint(0, len(cl_bt_removal) - 1), :]
            i += 1

        # For Lead.
        pb_bt_removal = np.column_stack((pb_dict['BT']['removal'], pb_dict['BT']['effluent']))
        pb_bt = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(pb_bt[:, 1]):
            pb_bt[i, :] = pb_bt_removal[rand.randint(0, len(pb_bt_removal) - 1), :]
            i += 1

        # For Mercury.
        hg_bt_removal = np.column_stack((hg_dict['BT']['removal'], hg_dict['BT']['effluent']))
        hg_bt = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(hg_bt[:, 1]):
            hg_bt[i, :] = hg_bt_removal[rand.randint(0, len(hg_bt_removal) - 1), :]
            i += 1

        # For Nitrogen.
        n_bt_removal = np.column_stack((n_dict['BT']['removal'], n_dict['BT']['effluent']))
        n_bt = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(n_bt[:, 1]):
            n_bt[i, :] = n_bt_removal[rand.randint(0, len(n_bt_removal) - 1), :]
            i += 1

        # For Selenium.
        se_bt_removal = np.column_stack((se_dict['BT']['removal'], se_dict['BT']['effluent']))
        se_bt = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(se_bt[:, 1]):
            se_bt[i, :] = se_bt_removal[rand.randint(0, len(se_bt_removal) - 1), :]
            i += 1

    return as_bt, cl_bt, pb_bt, hg_bt, se_bt #, n_bt


def cp_modeling(cp, runs):
    if cp == 0:
        cp_removal = np.zeros(shape=(runs, 3))
        cp_removal[:, 1] = np.ones(shape=runs)

        as_cp = cp_removal
        cl_cp = cp_removal
        pb_cp = cp_removal
        hg_cp = cp_removal
        n_cp = cp_removal
        se_cp = cp_removal

    elif cp == 1:
        cp_removal = np.zeros(shape=(runs, 3))
        cp_removal[:, 1] = np.ones(shape=runs)

        # For Arsenic.
        as_cp_removal = np.column_stack((as_dict['CP']['removal'], as_dict['CP']['effluent']))
        as_cp = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(as_cp[:, 1]):
            as_cp[i, :] = as_cp_removal[rand.randint(0, len(as_cp_removal) - 1), :]
            i += 1

        # For Chlorides.
        cl_cp_removal = np.column_stack((cl_dict['CP']['removal'], cl_dict['CP']['effluent']))
        cl_cp = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(cl_cp[:, 1]):
            cl_cp[i, :] = cl_cp_removal[rand.randint(0, len(cl_cp_removal) - 1), :]
            i += 1

        # For Lead.
        pb_cp_removal = np.column_stack((pb_dict['CP']['removal'], pb_dict['CP']['effluent']))
        pb_cp = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(pb_cp[:, 1]):
            pb_cp[i, :] = pb_cp_removal[rand.randint(0, len(pb_cp_removal) - 1), :]
            i += 1

        # For Mercury.
        hg_cp_removal = np.column_stack((hg_dict['CP']['removal'], hg_dict['CP']['effluent']))
        hg_cp = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(hg_cp[:, 1]):
            hg_cp[i, :] = hg_cp_removal[rand.randint(0, len(hg_cp_removal) - 1), :]
            i += 1

        # For Nitrogen.
        n_cp_removal = np.column_stack((n_dict['CP']['removal'], n_dict['CP']['effluent']))
        n_cp = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(n_cp[:, 1]):
            n_cp[i, :] = n_cp_removal[rand.randint(0, len(n_cp_removal) - 1), :]
            i += 1

        # For Selenium.
        se_cp_removal = np.column_stack((se_dict['CP']['removal'], se_dict['CP']['effluent']))
        se_cp = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(se_cp[:, 1]):
            se_cp[i, :] = se_cp_removal[rand.randint(0, len(se_cp_removal) - 1), :]
            i += 1

    return as_cp, cl_cp, pb_cp, hg_cp, se_cp #, n_cp


def crys_modeling(crys, runs):
    if crys == 0:
        crys_removal = np.zeros(shape=(runs, 3))
        crys_removal[:, 1] = np.ones(shape=runs)

        as_crys = crys_removal
        cl_crys = crys_removal
        pb_crys = crys_removal
        hg_crys = crys_removal
        n_crys = crys_removal
        se_crys = crys_removal

    elif crys == 1:
        crys_removal = np.zeros(shape=(runs, 3))
        crys_removal[:, 1] = np.ones(shape=runs)

        # For Arsenic.
        as_crys_removal = np.column_stack((as_dict['Crys']['sludge'], as_dict['Crys']['distillate']))
        as_crys = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(as_crys[:, 1]):
            as_crys[i, :] = as_crys_removal[rand.randint(0, len(as_crys_removal) - 1), :]
            i += 1

        # For Chlorides.
        cl_crys_removal = np.column_stack((cl_dict['Crys']['sludge'], cl_dict['Crys']['distillate']))
        cl_crys = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(cl_crys[:, 1]):
            cl_crys[i, :] = cl_crys_removal[rand.randint(0, len(cl_crys_removal) - 1), :]
            i += 1

        # For Lead.
        pb_crys_removal = np.column_stack((pb_dict['Crys']['sludge'], pb_dict['Crys']['distillate']))
        pb_crys = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(pb_crys[:, 1]):
            pb_crys[i, :] = pb_crys_removal[rand.randint(0, len(pb_crys_removal) - 1), :]
            i += 1

        # For Mercury.
        hg_crys_removal = np.column_stack((hg_dict['Crys']['sludge'], hg_dict['Crys']['distillate']))
        hg_crys = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(hg_crys[:, 1]):
            hg_crys[i, :] = hg_crys_removal[rand.randint(0, len(hg_crys_removal) - 1), :]
            i += 1

        # For Nitrogen.
        n_crys_removal = np.column_stack((n_dict['Crys']['sludge'], n_dict['Crys']['distillate']))
        n_crys = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(n_crys[:, 1]):
            n_crys[i, :] = n_crys_removal[rand.randint(0, len(n_crys_removal) - 1), :]
            i += 1

        # For Selenium.
        se_crys_removal = np.column_stack((se_dict['Crys']['sludge'], se_dict['Crys']['distillate']))
        se_crys = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(se_crys[:, 1]):
            se_crys[i, :] = se_crys_removal[rand.randint(0, len(se_crys_removal) - 1), :]
            i += 1

    return as_crys, cl_crys, pb_crys, hg_crys, se_crys #, n_crys


def feox_modeling(feox, runs):
    if feox == 0:
        feox_removal = np.zeros(shape=(runs, 3))
        feox_removal[:, 1] = np.ones(shape=runs)

        as_feox = feox_removal
        cl_feox = feox_removal
        pb_feox = feox_removal
        hg_feox = feox_removal
        n_feox = feox_removal
        se_feox = feox_removal

    elif feox == 1:
        feox_removal = np.zeros(shape=(runs, 3))
        feox_removal[:, 1] = np.ones(shape=runs)

        # For Arsenic.
        as_feox_removal = np.column_stack((as_dict['FeOx']['removal'], as_dict['FeOx']['effluent']))
        as_feox = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(as_feox[:, 1]):
            as_feox[i, :] = as_feox_removal[rand.randint(0, len(as_feox_removal) - 1), :]
            i += 1

        # For Chlorides.
        cl_feox_removal = np.column_stack((cl_dict['FeOx']['removal'], cl_dict['FeOx']['effluent']))
        cl_feox = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(cl_feox[:, 1]):
            cl_feox[i, :] = cl_feox_removal[rand.randint(0, len(cl_feox_removal) - 1), :]
            i += 1

        # For Lead.
        pb_feox_removal = np.column_stack((pb_dict['FeOx']['removal'], pb_dict['FeOx']['effluent']))
        pb_feox = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(pb_feox[:, 1]):
            pb_feox[i, :] = pb_feox_removal[rand.randint(0, len(pb_feox_removal) - 1), :]
            i += 1

        # For Mercury.
        hg_feox_removal = np.column_stack((hg_dict['FeOx']['removal'], hg_dict['FeOx']['effluent']))
        hg_feox = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(hg_feox[:, 1]):
            hg_feox[i, :] = hg_feox_removal[rand.randint(0, len(hg_feox_removal) - 1), :]
            i += 1

        # For Nitrogen.
        n_feox_removal = np.column_stack((n_dict['FeOx']['removal'], n_dict['FeOx']['effluent']))
        n_feox = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(n_feox[:, 1]):
            n_feox[i, :] = n_feox_removal[rand.randint(0, len(n_feox_removal) - 1), :]
            i += 1

        # For Selenium.
        se_feox_removal = np.column_stack((se_dict['FeOx']['removal'], se_dict['FeOx']['effluent']))
        se_feox = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(se_feox[:, 1]):
            se_feox[i, :] = se_feox_removal[rand.randint(0, len(se_feox_removal) - 1), :]
            i += 1

    return as_feox, cl_feox, pb_feox, hg_feox, se_feox #, n_feox


def iex_modeling(iex, runs):
    if iex == 0:
        iex_removal = np.zeros(shape=(runs, 3))
        iex_removal[:, 1] = np.ones(shape=runs)

        as_iex = iex_removal
        cl_iex = iex_removal
        pb_iex = iex_removal
        hg_iex = iex_removal
        n_iex = iex_removal
        se_iex = iex_removal

    elif iex == 1:
        iex_removal = np.zeros(shape=(runs, 3))
        iex_removal[:, 1] = np.ones(shape=runs)

        # For Arsenic.
        as_iex_removal = np.column_stack((as_dict['IEX']['removal'], as_dict['IEX']['effluent']))
        as_iex = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(as_iex[:, 1]):
            as_iex[i, :] = as_iex_removal[rand.randint(0, len(as_iex_removal) - 1), :]
            i += 1

        # For Chlorides.
        cl_iex_removal = np.column_stack((cl_dict['IEX']['removal'], cl_dict['IEX']['effluent']))
        cl_iex = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(cl_iex[:, 1]):
            cl_iex[i, :] = cl_iex_removal[rand.randint(0, len(cl_iex_removal) - 1), :]
            i += 1

        # For Lead.
        pb_iex_removal = np.column_stack((pb_dict['IEX']['removal'], pb_dict['IEX']['effluent']))
        pb_iex = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(pb_iex[:, 1]):
            pb_iex[i, :] = pb_iex_removal[rand.randint(0, len(pb_iex_removal) - 1), :]
            i += 1

        # For Mercury.
        hg_iex_removal = np.column_stack((hg_dict['IEX']['removal'], hg_dict['IEX']['effluent']))
        hg_iex = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(hg_iex[:, 1]):
            hg_iex[i, :] = hg_iex_removal[rand.randint(0, len(hg_iex_removal) - 1), :]
            i += 1

        # For Nitrogen.
        n_iex_removal = np.column_stack((n_dict['IEX']['removal'], n_dict['IEX']['effluent']))
        n_iex = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(n_iex[:, 1]):
            n_iex[i, :] = n_iex_removal[rand.randint(0, len(n_iex_removal) - 1), :]
            i += 1

        # For Selenium.
        se_iex_removal = np.column_stack((se_dict['IEX']['removal'], se_dict['IEX']['effluent']))
        se_iex = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(se_iex[:, 1]):
            se_iex[i, :] = se_iex_removal[rand.randint(0, len(se_iex_removal) - 1), :]
            i += 1

    return as_iex, cl_iex, pb_iex, hg_iex, se_iex #, n_iex


def mbr_modeling(mbr, runs):
    if mbr == 0:
        mbr_removal = np.zeros(shape=(runs, 3))
        mbr_removal[:, 1] = np.ones(shape=runs)

        as_mbr = mbr_removal
        cl_mbr = mbr_removal
        pb_mbr = mbr_removal
        hg_mbr = mbr_removal
        n_mbr = mbr_removal
        se_mbr = mbr_removal

    elif mbr == 1:
        mbr_removal = np.zeros(shape=(runs, 3))
        mbr_removal[:, 1] = np.ones(shape=runs)

        # For Arsenic.
        as_mbr_removal = np.column_stack((as_dict['MBR']['removal'], as_dict['MBR']['effluent']))
        as_mbr = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(as_mbr[:, 1]):
            as_mbr[i, :] = as_mbr_removal[rand.randint(0, len(as_mbr_removal) - 1), :]
            i += 1

        # For Chlorides.
        cl_mbr_removal = np.column_stack((cl_dict['MBR']['removal'], cl_dict['MBR']['effluent']))
        cl_mbr = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(cl_mbr[:, 1]):
            cl_mbr[i, :] = cl_mbr_removal[rand.randint(0, len(cl_mbr_removal) - 1), :]
            i += 1

        # For Lead.
        pb_mbr_removal = np.column_stack((pb_dict['MBR']['removal'], pb_dict['MBR']['effluent']))
        pb_mbr = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(pb_mbr[:, 1]):
            pb_mbr[i, :] = pb_mbr_removal[rand.randint(0, len(pb_mbr_removal) - 1), :]
            i += 1

        # For Mercury.
        hg_mbr_removal = np.column_stack((hg_dict['MBR']['removal'], hg_dict['MBR']['effluent']))
        hg_mbr = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(hg_mbr[:, 1]):
            hg_mbr[i, :] = hg_mbr_removal[rand.randint(0, len(hg_mbr_removal) - 1), :]
            i += 1

        # For Nitrogen.
        n_mbr_removal = np.column_stack((n_dict['MBR']['removal'], n_dict['MBR']['effluent']))
        n_mbr = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(n_mbr[:, 1]):
            n_mbr[i, :] = n_mbr_removal[rand.randint(0, len(n_mbr_removal) - 1), :]
            i += 1

        # For Selenium.
        se_mbr_removal = np.column_stack((se_dict['MBR']['removal'], se_dict['MBR']['effluent']))
        se_mbr = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(se_mbr[:, 1]):
            se_mbr[i, :] = se_mbr_removal[rand.randint(0, len(se_mbr_removal) - 1), :]
            i += 1

    return as_mbr, cl_mbr, pb_mbr, hg_mbr, se_mbr #, n_mbr


def mvc_modeling(mvc, runs):
    if mvc == 0:
        mvc_removal = np.zeros(shape=(runs, 3))
        mvc_removal[:, 1] = np.ones(shape=runs)

        as_mvc = mvc_removal
        cl_mvc = mvc_removal
        pb_mvc = mvc_removal
        hg_mvc = mvc_removal
        n_mvc = mvc_removal
        se_mvc = mvc_removal

    elif mvc == 1:
        mvc_removal = np.zeros(shape=(runs, 3))
        mvc_removal[:, 1] = np.ones(shape=runs)

        # For Arsenic.
        as_mvc_removal = np.column_stack((as_dict['MVC']['distillate'], as_dict['MVC']['brine']))
        as_mvc = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(as_mvc[:, 1]):
            as_mvc[i, :] = as_mvc_removal[rand.randint(0, len(as_mvc_removal) - 1), :]
            i += 1

        # For Chlorides.
        cl_mvc_removal = np.column_stack((cl_dict['MVC']['distillate'], cl_dict['MVC']['brine']))
        cl_mvc = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(cl_mvc[:, 1]):
            cl_mvc[i, :] = cl_mvc_removal[rand.randint(0, len(cl_mvc_removal) - 1), :]
            i += 1

        # For Lead.
        pb_mvc_removal = np.column_stack((pb_dict['MVC']['distillate'], pb_dict['MVC']['brine']))
        pb_mvc = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(pb_mvc[:, 1]):
            pb_mvc[i, :] = pb_mvc_removal[rand.randint(0, len(pb_mvc_removal) - 1), :]
            i += 1

        # For Mercury.
        hg_mvc_removal = np.column_stack((hg_dict['MVC']['distillate'], hg_dict['MVC']['brine']))
        hg_mvc = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(hg_mvc[:, 1]):
            hg_mvc[i, :] = hg_mvc_removal[rand.randint(0, len(hg_mvc_removal) - 1), :]
            i += 1

        # For Nitrogen.
        n_mvc_removal = np.column_stack((n_dict['MVC']['distillate'], n_dict['MVC']['brine']))
        n_mvc = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(n_mvc[:, 1]):
            n_mvc[i, :] = n_mvc_removal[rand.randint(0, len(n_mvc_removal) - 1), :]
            i += 1

        # For Selenium.
        se_mvc_removal = np.column_stack((se_dict['MVC']['distillate'], se_dict['MVC']['brine']))
        se_mvc = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(se_mvc[:, 1]):
            se_mvc[i, :] = se_mvc_removal[rand.randint(0, len(se_mvc_removal) - 1), :]
            i += 1

    return as_mvc, cl_mvc, pb_mvc, hg_mvc, se_mvc #, n_mvc


def zvi_modeling(zvi, runs):
    if zvi == 0:
        zvi_removal = np.zeros(shape=(runs, 3))
        zvi_removal[:, 1] = np.ones(shape=runs)

        as_zvi = zvi_removal
        cl_zvi = zvi_removal
        pb_zvi = zvi_removal
        hg_zvi = zvi_removal
        n_zvi = zvi_removal
        se_zvi = zvi_removal

    elif zvi == 1:
        zvi_removal = np.zeros(shape=(runs, 3))
        zvi_removal[:, 1] = np.ones(shape=runs)

        # For Arsenic.
        as_zvi_removal = np.column_stack((as_dict['ZVI']['removal'], as_dict['ZVI']['effluent']))
        as_zvi = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(as_zvi[:, 1]):
            as_zvi[i, :] = as_zvi_removal[rand.randint(0, len(as_zvi_removal) - 1), :]
            i += 1

        # For Chlorides.
        cl_zvi_removal = np.column_stack((cl_dict['ZVI']['removal'], cl_dict['ZVI']['effluent']))
        cl_zvi = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(cl_zvi[:, 1]):
            cl_zvi[i, :] = cl_zvi_removal[rand.randint(0, len(cl_zvi_removal) - 1), :]
            i += 1

        # For Lead.
        pb_zvi_removal = np.column_stack((pb_dict['ZVI']['removal'], pb_dict['ZVI']['effluent']))
        pb_zvi = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(pb_zvi[:, 1]):
            pb_zvi[i, :] = pb_zvi_removal[rand.randint(0, len(pb_zvi_removal) - 1), :]
            i += 1

        # For Mercury.
        hg_zvi_removal = np.column_stack((hg_dict['ZVI']['removal'], hg_dict['ZVI']['effluent']))
        hg_zvi = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(hg_zvi[:, 1]):
            hg_zvi[i, :] = hg_zvi_removal[rand.randint(0, len(hg_zvi_removal) - 1), :]
            i += 1

        # For Nitrogen.
        n_zvi_removal = np.column_stack((n_dict['ZVI']['removal'], n_dict['ZVI']['effluent']))
        n_zvi = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(n_zvi[:, 1]):
            n_zvi[i, :] = n_zvi_removal[rand.randint(0, len(n_zvi_removal) - 1), :]
            i += 1

        # For Selenium.
        se_zvi_removal = np.column_stack((se_dict['ZVI']['removal'], se_dict['ZVI']['effluent']))
        se_zvi = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(se_zvi[:, 1]):
            se_zvi[i, :] = se_zvi_removal[rand.randint(0, len(se_zvi_removal) - 1), :]
            i += 1

    return as_zvi, cl_zvi, pb_zvi, hg_zvi, se_zvi #, n_zvi

def gac_modeling(gac, runs):
    if gac == 0:
        gac_removal = np.zeros(shape=(runs, 3))
        gac_removal[:, 1] = np.ones(shape=runs)

        as_gac = gac_removal
        cl_gac = gac_removal
        pb_gac = gac_removal
        hg_gac = gac_removal
        n_gac = gac_removal
        se_gac = gac_removal

    elif gac == 1:
        gac_removal = np.zeros(shape=(runs, 3))
        gac_removal[:, 1] = np.ones(shape=runs)

        # For Arsenic.
        as_gac_removal = np.column_stack((as_dict['GAC']['removal'], as_dict['GAC']['effluent']))
        as_gac = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(as_gac[:, 1]):
            as_gac[i, :] = as_gac_removal[rand.randint(0, len(as_gac_removal) - 1), :]
            i += 1

        # For Chlorides.
        cl_gac_removal = np.column_stack((cl_dict['GAC']['removal'], cl_dict['GAC']['effluent']))
        cl_gac = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(cl_gac[:, 1]):
            cl_gac[i, :] = cl_gac_removal[rand.randint(0, len(cl_gac_removal) - 1), :]
            i += 1

        # For Lead.
        pb_gac_removal = np.column_stack((pb_dict['GAC']['removal'], pb_dict['GAC']['effluent']))
        pb_gac = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(pb_gac[:, 1]):
            pb_gac[i, :] = pb_gac_removal[rand.randint(0, len(pb_gac_removal) - 1), :]
            i += 1

        # For Mercury.
        hg_gac_removal = np.column_stack((hg_dict['GAC']['removal'], hg_dict['GAC']['effluent']))
        hg_gac = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(hg_gac[:, 1]):
            hg_gac[i, :] = hg_gac_removal[rand.randint(0, len(hg_gac_removal) - 1), :]
            i += 1

        # For Nitrogen.
        n_gac_removal = np.column_stack((n_dict['GAC']['removal'], n_dict['GAC']['effluent']))
        n_gac = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(n_gac[:, 1]):
            n_gac[i, :] = n_gac_removal[rand.randint(0, len(n_gac_removal) - 1), :]
            i += 1

        # For Selenium.
        se_gac_removal = np.column_stack((se_dict['GAC']['removal'], se_dict['GAC']['effluent']))
        se_gac = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(se_gac[:, 1]):
            se_gac[i, :] = se_gac_removal[rand.randint(0, len(se_gac_removal) - 1), :]
            i += 1

    return as_gac, cl_gac, pb_gac, hg_gac, se_gac #, n_gac

def ro_modeling(ro, runs):
    if ro == 0:
        ro_removal = np.zeros(shape=(runs, 3))
        ro_removal[:, 1] = np.ones(shape=runs)

        as_ro = ro_removal
        cl_ro = ro_removal
        pb_ro = ro_removal
        hg_ro = ro_removal
        n_ro = ro_removal
        se_ro = ro_removal

    elif ro == 1:
        ro_removal = np.zeros(shape=(runs, 3))
        ro_removal[:, 1] = np.ones(shape=runs)

        # For Arsenic.
        as_ro_removal = np.column_stack((as_dict['RO']['permeate'], as_dict['RO']['brine']))
        as_ro = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(as_ro[:, 1]):
            as_ro[i, :] = as_ro_removal[rand.randint(0, len(as_ro_removal) - 1), :]
            i += 1

        # For Chlorides.
        cl_ro_removal = np.column_stack((cl_dict['RO']['permeate'], cl_dict['RO']['brine']))
        cl_ro = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(cl_ro[:, 1]):
            cl_ro[i, :] = cl_ro_removal[rand.randint(0, len(cl_ro_removal) - 1), :]
            i += 1

        # For Lead.
        pb_ro_removal = np.column_stack((pb_dict['RO']['permeate'], pb_dict['RO']['brine']))
        pb_ro = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(pb_ro[:, 1]):
            pb_ro[i, :] = pb_ro_removal[rand.randint(0, len(pb_ro_removal) - 1), :]
            i += 1

        # For Mercury.
        hg_ro_removal = np.column_stack((hg_dict['RO']['permeate'], hg_dict['RO']['brine']))
        hg_ro = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(hg_ro[:, 1]):
            hg_ro[i, :] = hg_ro_removal[rand.randint(0, len(hg_ro_removal) - 1), :]
            i += 1

        # For Nitrogen.
        n_ro_removal = np.column_stack((n_dict['RO']['permeate'], n_dict['RO']['brine']))
        n_ro = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(n_ro[:, 1]):
            n_ro[i, :] = n_ro_removal[rand.randint(0, len(n_ro_removal) - 1), :]
            i += 1

        # For Selenium.
        se_ro_removal = np.column_stack((se_dict['RO']['permeate'], se_dict['RO']['brine']))
        se_ro = np.zeros(shape=(runs, 2))
        i = 0
        while i < len(se_ro[:, 1]):
            se_ro[i, :] = se_ro_removal[rand.randint(0, len(se_ro_removal) - 1), :]
            i += 1

    return as_ro, cl_ro, pb_ro, hg_ro, se_ro #, n_ro