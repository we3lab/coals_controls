# Import standard python packages
import pandas as pd
import pathlib
import copy
import sys

# For frozen program
fileDir = pathlib.Path(__file__).parents[1]

# For Original Python Code
# fileDir = pathlib.Path(__file__).parents[2]


#the same as sheet titltes 
FGD_List = ["Mg-enhanced Lime Natural", "Mg-enhanced Lime Ext. Forced", "Mg-enhanced Lime Inhibited", 
					"LS Inhibited DBA", "LS Inhibited NaFo", "LS Inhibited None", "LS Forced DBA", "LS Forced None"]

def readData(FGDtype):
	filename = fileDir / 'newData' / 'EPRI Data' / 'Literature-based EPRI Data.xlsx'
	FGDdataframe = pd.read_excel(filename, sheet_name=FGDtype,
                                 skiprows=0, usecols=[6, 7, 8, 9],
                                 names=['Se4', 'Se6', 'SeSO3', 'Others'])
	return FGDdataframe

#to build a dictionary{FGDtype1:{Se4:[],Se6: [],SeSO3:[],others:[]},FGDtype2:FGDtype1:{Se4:[],Se6: [],SeSO3:[],others:[]}}
def buidDictionary(FGDlist):
	dic1 = {}
	for FGD in FGDlist:
		dic2 = {}
		tempDataFrame = readData(FGD)
		dic2["Se4"] = tempDataFrame.Se4.tolist()
		dic2["Se6"] = tempDataFrame.Se6.tolist()
		dic2["SeSO3"] = tempDataFrame.SeSO3.tolist()
		dic2["Others"] = tempDataFrame.Others.tolist()
		dic1[FGD] = dic2
	return dic1

se_wFGD_dictionary = buidDictionary(FGD_List)











