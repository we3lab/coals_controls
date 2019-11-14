import numpy as np
import random as rand
import pathlib
import sys

fileDir = pathlib.Path(__file__).parents[2]
code_library_folder = fileDir / 'Code' / 'function_dictionary_library'
sys.path.append(str(code_library_folder))
from wpcd_partitioning_dictionaries import as_dict, cl_dict, pb_dict, hg_dict, n_dict, se_dict
from statistical_functions import ecdf, random_value_from_ecdf


def alox_modeling(alox, runs):
    if alox == 0:
        alox_removal = np.ones(shape=(runs,1))

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
        qe_as_alox, pe_as_alox = ecdf(as_dict['AlOx']['effluent'])
        as_alox = random_value_from_ecdf(qe_as_alox, pe_as_alox, runs)

        # For Chlorides.
        qe_cl_alox, pe_cl_alox = ecdf(cl_dict['AlOx']['effluent'])
        cl_alox = random_value_from_ecdf(qe_cl_alox, pe_cl_alox, runs)

        # For Lead.
        qe_pb_alox, pe_pb_alox = ecdf(pb_dict['AlOx']['effluent'])
        pb_alox = random_value_from_ecdf(qe_pb_alox, pe_pb_alox, runs)

        # For Mercury.
        qe_hg_alox, pe_hg_alox = ecdf(hg_dict['AlOx']['effluent'])
        hg_alox = random_value_from_ecdf(qe_hg_alox, pe_hg_alox, runs)

        # For Nitrogen.
        qe_n_alox, pe_n_alox = ecdf(n_dict['AlOx']['effluent'])
        n_alox = random_value_from_ecdf(qe_n_alox, pe_n_alox, runs)

        # For Selenium.
        qe_se_alox, pe_se_alox = ecdf(se_dict['AlOx']['effluent'])
        se_alox = random_value_from_ecdf(qe_se_alox, pe_se_alox, runs)

    return as_alox, cl_alox, pb_alox, hg_alox, se_alox #, n_alox


def bt_modeling(bt, runs):
    if bt == 0:
        bt_removal = np.ones(shape=(runs,1))

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
        qe_as_bt, pe_as_bt = ecdf(as_dict['BT']['effluent'])
        as_bt = random_value_from_ecdf(qe_as_bt, pe_as_bt, runs)

        # For Chlorides.
        qe_cl_bt, pe_cl_bt = ecdf(cl_dict['BT']['effluent'])
        cl_bt = random_value_from_ecdf(qe_cl_bt, pe_cl_bt, runs)

        # For Lead.
        qe_pb_bt, pe_pb_bt = ecdf(pb_dict['BT']['effluent'])
        pb_bt = random_value_from_ecdf(qe_pb_bt, pe_pb_bt, runs)

        # For Mercury.
        qe_hg_bt, pe_hg_bt = ecdf(hg_dict['BT']['effluent'])
        hg_bt = random_value_from_ecdf(qe_hg_bt, pe_hg_bt, runs)

        # For Nitrogen.
        qe_n_bt, pe_n_bt = ecdf(n_dict['BT']['effluent'])
        n_bt = random_value_from_ecdf(qe_n_bt, pe_n_bt, runs)

        # For Selenium.
        qe_se_bt, pe_se_bt = ecdf(se_dict['BT']['effluent'])
        se_bt = random_value_from_ecdf(qe_se_bt, pe_se_bt, runs)

    return as_bt, cl_bt, pb_bt, hg_bt, se_bt #, n_bt


def cp_modeling(cp, runs):
    if cp == 0:
        cp_removal = np.ones(shape=(runs, 1))

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
        qe_as_cp, pe_as_cp = ecdf(as_dict['CP']['effluent'])
        as_cp = random_value_from_ecdf(qe_as_cp, pe_as_cp, runs)

        # For Chlorides.
        qe_cl_cp, pe_cl_cp = ecdf(cl_dict['CP']['effluent'])
        cl_cp = random_value_from_ecdf(qe_cl_cp, pe_cl_cp, runs)

        # For Lead.
        qe_pb_cp, pe_pb_cp = ecdf(pb_dict['CP']['effluent'])
        pb_cp = random_value_from_ecdf(qe_pb_cp, pe_pb_cp, runs)

        # For Mercury.
        qe_hg_cp, pe_hg_cp = ecdf(hg_dict['CP']['effluent'])
        hg_cp = random_value_from_ecdf(qe_hg_cp, pe_hg_cp, runs)

        # For Nitrogen.
        qe_n_cp, pe_n_cp = ecdf(n_dict['CP']['effluent'])
        n_cp = random_value_from_ecdf(qe_n_cp, pe_n_cp, runs)

        # For Selenium.
        qe_se_cp, pe_se_cp = ecdf(se_dict['CP']['effluent'])
        se_cp = random_value_from_ecdf(qe_se_cp, pe_se_cp, runs)

    return as_cp, cl_cp, pb_cp, hg_cp, se_cp #, n_cp


def crys_modeling(crys, runs):
    if crys == 0:
        crys_removal = np.ones(shape=(runs, 1))

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
        qe_as_crys, pe_as_crys = ecdf(as_dict['Crys']['distillate'])
        as_crys = random_value_from_ecdf(qe_as_crys, pe_as_crys, runs)

        # For Chlorides.
        qe_cl_crys, pe_cl_crys = ecdf(cl_dict['Crys']['distillate'])
        cl_crys = random_value_from_ecdf(qe_cl_crys, pe_cl_crys, runs)

        # For Lead.
        qe_pb_crys, pe_pb_crys = ecdf(pb_dict['Crys']['distillate'])
        pb_crys = random_value_from_ecdf(qe_pb_crys, pe_pb_crys, runs)

        # For Mercury.
        qe_hg_crys, pe_hg_crys = ecdf(hg_dict['Crys']['distillate'])
        hg_crys = random_value_from_ecdf(qe_hg_crys, pe_hg_crys, runs)

        # For Nitrogen.
        qe_n_crys, pe_n_crys = ecdf(n_dict['Crys']['distillate'])
        n_crys = random_value_from_ecdf(qe_n_crys, pe_n_crys, runs)

        # For Selenium.
        qe_se_crys, pe_se_crys = ecdf(se_dict['Crys']['distillate'])
        se_crys = random_value_from_ecdf(qe_se_crys, pe_se_crys, runs)

    return as_crys, cl_crys, pb_crys, hg_crys, se_crys #, n_crys


def feox_modeling(feox, runs):
    if feox == 0:
        feox_removal = np.ones(shape=(runs, 1))

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
        qe_as_feox, pe_as_feox = ecdf(as_dict['FeOx']['effluent'])
        as_feox = random_value_from_ecdf(qe_as_feox, pe_as_feox, runs)

        # For Chlorides.
        qe_cl_feox, pe_cl_feox = ecdf(cl_dict['FeOx']['effluent'])
        cl_feox = random_value_from_ecdf(qe_cl_feox, pe_cl_feox, runs)

        # For Lead.
        qe_pb_feox, pe_pb_feox = ecdf(pb_dict['FeOx']['effluent'])
        pb_feox = random_value_from_ecdf(qe_pb_feox, pe_pb_feox, runs)

        # For Mercury.
        qe_hg_feox, pe_hg_feox = ecdf(hg_dict['FeOx']['effluent'])
        hg_feox = random_value_from_ecdf(qe_hg_feox, pe_hg_feox, runs)

        # For Nitrogen.
        qe_n_feox, pe_n_feox = ecdf(n_dict['FeOx']['effluent'])
        n_feox = random_value_from_ecdf(qe_n_feox, pe_n_feox, runs)

        # For Selenium.
        qe_se_feox, pe_se_feox = ecdf(se_dict['FeOx']['effluent'])
        se_feox = random_value_from_ecdf(qe_se_feox, pe_se_feox, runs)

    return as_feox, cl_feox, pb_feox, hg_feox, se_feox #, n_feox


def iex_modeling(iex, runs):
    if iex == 0:
        iex_removal = np.ones(shape=(runs, 1))

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
        qe_as_iex, pe_as_iex = ecdf(as_dict['IEX']['effluent'])
        as_iex = random_value_from_ecdf(qe_as_iex, pe_as_iex, runs)

        # For Chlorides.
        qe_cl_iex, pe_cl_iex = ecdf(cl_dict['IEX']['effluent'])
        cl_iex = random_value_from_ecdf(qe_cl_iex, pe_cl_iex, runs)

        # For Lead.
        qe_pb_iex, pe_pb_iex = ecdf(pb_dict['IEX']['effluent'])
        pb_iex = random_value_from_ecdf(qe_pb_iex, pe_pb_iex, runs)

        # For Mercury.
        qe_hg_iex, pe_hg_iex = ecdf(hg_dict['IEX']['effluent'])
        hg_iex = random_value_from_ecdf(qe_hg_iex, pe_hg_iex, runs)

        # For Nitrogen.
        qe_n_iex, pe_n_iex = ecdf(n_dict['IEX']['effluent'])
        n_iex = random_value_from_ecdf(qe_n_iex, pe_n_iex, runs)

        # For Selenium.
        qe_se_iex, pe_se_iex = ecdf(se_dict['IEX']['effluent'])
        se_iex = random_value_from_ecdf(qe_se_iex, pe_se_iex, runs)

    return as_iex, cl_iex, pb_iex, hg_iex, se_iex #, n_iex


def mbr_modeling(mbr, runs):
    if mbr == 0:
        mbr_removal = np.ones(shape=(runs, 1))

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
        qe_as_mbr, pe_as_mbr = ecdf(as_dict['MBR']['effluent'])
        as_mbr = random_value_from_ecdf(qe_as_mbr, pe_as_mbr, runs)

        # For Chlorides.
        qe_cl_mbr, pe_cl_mbr = ecdf(cl_dict['MBR']['effluent'])
        cl_mbr = random_value_from_ecdf(qe_cl_mbr, pe_cl_mbr, runs)

        # For Lead.
        qe_pb_mbr, pe_pb_mbr = ecdf(pb_dict['MBR']['effluent'])
        pb_mbr = random_value_from_ecdf(qe_pb_mbr, pe_pb_mbr, runs)

        # For Mercury.
        qe_hg_mbr, pe_hg_mbr = ecdf(hg_dict['MBR']['effluent'])
        hg_mbr = random_value_from_ecdf(qe_hg_mbr, pe_hg_mbr, runs)

        # For Nitrogen.
        qe_n_mbr, pe_n_mbr = ecdf(n_dict['MBR']['effluent'])
        n_mbr = random_value_from_ecdf(qe_n_mbr, pe_n_mbr, runs)

        # For Selenium.
        qe_se_mbr, pe_se_mbr = ecdf(se_dict['MBR']['effluent'])
        se_mbr = random_value_from_ecdf(qe_se_mbr, pe_se_mbr, runs)

    return as_mbr, cl_mbr, pb_mbr, hg_mbr, se_mbr #, n_mbr


def mvc_modeling(mvc, runs):
    if mvc == 0:
        mvc_removal = np.ones(shape=(runs, 1))

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
        qe_as_mvc, pe_as_mvc = ecdf(as_dict['MVC']['brine'])
        as_mvc = random_value_from_ecdf(qe_as_mvc, pe_as_mvc, runs)

        # For Chlorides.
        qe_cl_mvc, pe_cl_mvc = ecdf(cl_dict['MVC']['brine'])
        cl_mvc = random_value_from_ecdf(qe_cl_mvc, pe_cl_mvc, runs)

        # For Lead.
        qe_pb_mvc, pe_pb_mvc = ecdf(pb_dict['MVC']['brine'])
        pb_mvc = random_value_from_ecdf(qe_pb_mvc, pe_pb_mvc, runs)

        # For Mercury.
        qe_hg_mvc, pe_hg_mvc = ecdf(hg_dict['MVC']['brine'])
        hg_mvc = random_value_from_ecdf(qe_hg_mvc, pe_hg_mvc, runs)

        # For Nitrogen.
        qe_n_mvc, pe_n_mvc = ecdf(n_dict['MVC']['brine'])
        n_mvc = random_value_from_ecdf(qe_n_mvc, pe_n_mvc, runs)

        # For Selenium.
        qe_se_mvc, pe_se_mvc = ecdf(se_dict['MVC']['brine'])
        se_mvc = random_value_from_ecdf(qe_se_mvc, pe_se_mvc, runs)

    return as_mvc, cl_mvc, pb_mvc, hg_mvc, se_mvc #, n_mvc


def zvi_modeling(zvi, runs):
    if zvi == 0:
        zvi_removal = np.ones(shape=(runs, 1))

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
        qe_as_zvi, pe_as_zvi = ecdf(as_dict['ZVI']['effluent'])
        as_zvi = random_value_from_ecdf(qe_as_zvi, pe_as_zvi, runs)

        # For Chlorides.
        qe_cl_zvi, pe_cl_zvi = ecdf(cl_dict['ZVI']['effluent'])
        cl_zvi = random_value_from_ecdf(qe_cl_zvi, pe_cl_zvi, runs)

        # For Lead.
        qe_pb_zvi, pe_pb_zvi = ecdf(pb_dict['ZVI']['effluent'])
        pb_zvi = random_value_from_ecdf(qe_pb_zvi, pe_pb_zvi, runs)

        # For Mercury.
        qe_hg_zvi, pe_hg_zvi = ecdf(hg_dict['ZVI']['effluent'])
        hg_zvi = random_value_from_ecdf(qe_hg_zvi, pe_hg_zvi, runs)

        # For Nitrogen.
        qe_n_zvi, pe_n_zvi = ecdf(n_dict['ZVI']['effluent'])
        n_zvi = random_value_from_ecdf(qe_n_zvi, pe_n_zvi, runs)

        # For Selenium.
        qe_se_zvi, pe_se_zvi = ecdf(se_dict['ZVI']['effluent'])
        se_zvi = random_value_from_ecdf(qe_se_zvi, pe_se_zvi, runs)

    return as_zvi, cl_zvi, pb_zvi, hg_zvi, se_zvi #, n_zvi
