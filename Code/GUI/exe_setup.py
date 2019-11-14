import sys
import os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = "C:/users/Jiachen Liu/AppData/Local/Programs/Python/Python37/tcl/tcl8.6"
os.environ['TK_LIBRARY'] = "C:/users/Jiachen Liu/AppData/Local/Programs/Python/Python37/tcl/tk8.6"

build_exe_options = {"includes":["tkinter", "numpy.core._methods", "numpy.lib.format", "numpy.core._dtype_ctypes",
                                 "matplotlib.backends.backend_tkagg", "seaborn.cm",
                                 "scipy._distributor_init","scipy.sparse.csgraph._validation"],

                     "include_files":[r'C:/users/Jiachen Liu/AppData/Local/Programs/Python/Python37/DLLs/tcl86t.dll',
                                      r'C:/users/Jiachen Liu/AppData/Local/Programs/Python/Python37/DLLs/tk86t.dll',
                                      r'C:/users/Jiachen Liu/Documents/Github/cfpp_trace_element_fate_model/Code/function_dictionary_library',
                                      r'C:/users/Jiachen Liu/Documents/Github/cfpp_trace_element_fate_model/Code/user_specified_trace_element_partitioning',
                                      r'C:/users/Jiachen Liu/Documents/Github/cfpp_trace_element_fate_model/newData',
                                      r'C:/users/Jiachen Liu/Documents/Github/cfpp_trace_element_fate_model/Intermediate'],

                     "excludes":["scipy.spatial.cKDTree"]}
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('COALS.py', base=base)
]

setup(name='COALS Controls Model',
      version='0.1',
      description='COALS Controls Model',
      options={"build_exe": build_exe_options},
      executables=executables
      )
