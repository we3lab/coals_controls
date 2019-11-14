from tkinter import *
from tkinter import filedialog
import os
import pathlib
import sys
import numpy as np
from math import log10, floor
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.pyplot import figure

### IMPORTANT ###

# To freeze the file, lines in some files must be changed. The files are attached below:
# coal_ecdf.py, Se_lit_based_dictionary.py, apcd_partitioning_dictionaries.py, APCD_partition_modeling.py
# The changes to be made are marked with "For frozen code" and "For original python code"
# The code right below does not need to be changed

# Frozen refers to making the .exe file,
if getattr(sys, 'frozen', False):
    # frozen
    fileDir = os.path.dirname(sys.executable)
    code_library_folder = fileDir+'/function_dictionary_library'
    user_specified_folder = fileDir+'/user_specified_trace_element_partitioning'
    data_folder = fileDir +'/exe.win32-3.7/Data'
    intermediate_folder = fileDir + '/exe.win32-3.7/Intermediate'
    sys.path.append(code_library_folder)
    sys.path.append(user_specified_folder)
    sys.path.append(data_folder)

# Unfrozen refers to run the program in Python
else:
    # unfrozen
    fileDir = pathlib.Path(__file__).parents[2]
    code_library_folder = fileDir / 'Code' / 'function_dictionary_library'
    user_specified_folder = fileDir / 'Code' / 'user_specified_trace_element_partitioning'
    sys.path.append(str(code_library_folder))
    sys.path.append(str(user_specified_folder))

# Import the functions from other .py files
from coal_ecdf import coal_ecdf
from statistical_functions import ecdf, random_value_from_ecdf
from fuel_and_energy_modeling import coal_combustion
from APCD_partition_modeling import bottom_modeling, csESP_modeling, hsESP_modeling, FF_modeling, SCR_modeling, \
    ACI_modeling, DSI_modeling, wetFGD_modeling, dryFGD_modeling, wetFGD_wastewater_Se_modeling, wetFGD_SCR_modeling
from wastewater_functions import wastewater_generation, fgd_wastewater_concentration, \
    fgd_wastewater_generation_for_corrosion_limits, wastewater_treatment_electricity_consumption, \
    wastewater_chemical_consumption
from WPCD_partition_modeling import cp_modeling, mbr_modeling, bt_modeling, mvc_modeling, iex_modeling, alox_modeling, \
    feox_modeling, zvi_modeling, crys_modeling, gac_modeling, ro_modeling
from mass_partitioning_calculation import apcd_mass_partitioning, wpcd_mass_partitioning
from elg_compliance_check import elg_compliance_check
from median_partitioning_scenario import partitioning_scenario

def menu_option_selected():
    print('Called the callback!')

# Create the Notebook class
class Notebook(Frame):
    """Notebook Widget"""

    def __init__(self, parent, activerelief=RAISED, inactiverelief=RIDGE, xpad=4, ypad=6, activefg='black',
                 inactivefg='black', **kw):
        """Construct a Notebook Widget

        Notebook(self, parent, activerelief = RAISED, inactiverelief = RIDGE, xpad = 4, ypad = 6, activefg = 'black', inactivefg = 'black', **kw)

        Valid resource names: background, bd, bg, borderwidth, class,
        colormap, container, cursor, height, highlightbackground,
        highlightcolor, highlightthickness, relief, takefocus, visual, width, activerelief,
        inactiverelief, xpad, ypad.

        xpad and ypad are values to be used as ipady and ipadx
        with the Label widgets that make up the tabs. activefg and inactivefg define what
        color the text on the tabs when they are selected, and when they are not

        """
        # Make various argument available to the rest of the class
        self.activefg = activefg
        self.inactivefg = inactivefg
        self.deletedTabs = []
        self.xpad = xpad
        self.ypad = ypad
        self.activerelief = activerelief
        self.inactiverelief = inactiverelief
        self.kwargs = kw
        self.tabVars = {}  # This dictionary holds the label and frame instances of each tab
        self.tabs = 0  # Keep track of the number of tabs
        self.noteBookFrame = Frame(parent)  # Create a frame to hold everything together
        self.BFrame = Frame(self.noteBookFrame)  # Create a frame to put the "tabs" in
        self.noteBook = Frame(self.noteBookFrame, relief=RAISED, bd=2,
                              **kw)  # Create the frame that will parent the frames for each tab
        self.noteBook.grid_propagate(0)  # self.noteBook has a bad habit of resizing itself, this line prevents that
        Frame.__init__(self)
        self.noteBookFrame.grid()
        self.BFrame.grid(row=0, sticky=W)
        self.noteBook.grid(row=1, column=0, columnspan=27)

    def change_tab(self, IDNum):
        """Internal Function"""

        for i in (a for a in range(0, len(self.tabVars.keys()))):
            if i not in self.deletedTabs:  # Make sure tab hasn't been deleted
                if i != IDNum:  # Check to see if the tab is the one that is currently selected
                    self.tabVars[i][1].grid_remove()  # Remove the Frame corresponding to each tab that is not selected
                    self.tabVars[i][0][
                        'relief'] = self.inactiverelief  # Change the relief of all tabs that are not selected to "Groove"
                    self.tabVars[i][0][
                        'fg'] = self.inactivefg  # Set the fg of the tab, showing it is selected, default is black
                else:  # When on the tab that is currently selected...
                    self.tabVars[i][1].grid()  # Re-grid the frame that corresponds to the tab
                    self.tabVars[IDNum][0][
                        'relief'] = self.activerelief  # Change the relief to "Raised" to show the tab is selected
                    self.tabVars[i][0][
                        'fg'] = self.activefg  # Set the fg of the tab, showing it is not selected, default is black

    def add_tab(self, width=2, **kw):
        """Creates a new tab, and returns it's corresponding frame

        """

        temp = self.tabs  # Temp is used so that the value of self.tabs will not throw off the argument sent by the label's event binding
        self.tabVars[self.tabs] = [Label(self.BFrame, relief=RIDGE, **kw)]  # Create the tab
        self.tabVars[self.tabs][0].bind("<Button-1>", lambda Event: self.change_tab(temp))  # Makes the tab "clickable"
        self.tabVars[self.tabs][0].pack(side=LEFT, ipady=self.ypad,
                                        ipadx=self.xpad)  # Packs the tab as far to the left as possible
        self.tabVars[self.tabs].append(
            Frame(self.noteBook, **self.kwargs))  # Create Frame, and append it to the dictionary of tabs
        self.tabVars[self.tabs][1].grid(row=0, column=0)  # Grid the frame ontop of any other already existing frames
        self.change_tab(0)  # Set focus to the first tab
        self.tabs += 1  # Update the tab count
        return self.tabVars[temp][1]  # Return a frame to be used as a parent to other widgets

    def destroy_tab(self, tab):
        """Delete a tab from the notebook, as well as it's corresponding frame

        """

        self.iteratedTabs = 0  # Keep track of the number of loops made
        for b in self.tabVars.values():  # Iterate through the dictionary of tabs
            if b[1] == tab:  # Find the NumID of the given tab
                b[0].destroy()  # Destroy the tab's frame, along with all child widgets
                self.tabs -= 1  # Subtract one from the tab count
                self.deletedTabs.append(
                    self.iteratedTabs)  # Apend the NumID of the given tab to the list of deleted tabs
                break  # Job is done, exit the loop
            self.iteratedTabs += 1  # Add one to the loop count

    def focus_on(self, tab):
        """Locate the IDNum of the given tab and use
        change_tab to give it focus

        """

        self.iteratedTabs = 0  # Keep track of the number of loops made
        for b in self.tabVars.values():  # Iterate through the dictionary of tabs
            if b[1] == tab:  # Find the NumID of the given tab
                self.change_tab(
                    self.iteratedTabs)  # send the tab's NumID to change_tab to set focus, mimicking that of each tab's event bindings
                break  # Job is done, exit the loop
            self.iteratedTabs += 1  # Add one to the loop count

def main():

    def combine_funcs(*funcs):
        '''Combines function for the command'''
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)

        return combined_func
    # Create the notebook
    root = Tk()
    root.resizable(0, 0)

    # Create the menu.
    menu = Menu(root)
    root.config(menu=menu)

    # Add the title and tabs to the GUI
    root.title("TEP Model")
    note = Notebook(root, width=650, height=570, activefg='black', inactivefg='gray')  # Create a Notebook Instance
    note.grid()


    tab1 = note.add_tab(text='Fuel/Overview', width=5)
    tab2 = note.add_tab(text='APCD Inputs', width=5)
    tab3 = note.add_tab(text='WPCD Inputs', width=5)
    tab4 = note.add_tab(text='APCD Results', width=5)
    tab5 = note.add_tab(text='WPCD Results', width=5)
    tab6 = note.add_tab(text='Graphs', width=5)

# Inputs
# These functions limit the type of inputs for each blank
    def limit_positive_float_input(P):

        '''This function ensures the input is a positive floating point number or integer.'''
        if str(P) == '':
            return True
        if str(P).count('.') > 1:
            return False
        if str(P).isalpha():
            return False
        if str(P).startswith('0'):
            return False
        return True

    def limit_positive_int_input(P):
        '''This function will limit the input to be positive integers'''
        if str(P).startswith('0'):
            return False
        if str(P) == '':
            return True
        if not str(P).isnumeric():
            return False
        else:
            return True

    vcmd_float = (tab1.register(limit_positive_float_input))
    vcmd_int = (tab1.register(limit_positive_int_input))

# Tab 1
    Label(tab1, text='Coal Type', font=('Arial', 10, 'bold')).grid(column=1, row=0, pady=(30, 0), padx=275)

    coal_type = StringVar(root)
    coal_type_choices = ['Appalachian Low Sulfur', 'Appalachian Med Sulfur',
                         'Beulah-Zap', 'Illinois #6', 'ND Lignite', 'Pocahontas #3', 'Upper Freeport', 'WPC Utah',
                         'Wyodak',
                         'Wyodak Anderson', 'Wyoming PRB', 'Bituminous', 'Subbituminous', 'Lignite']
    coal_type.set('Appalachian Low Sulfur')
    coal_type_popup_menu = OptionMenu(tab1, coal_type, *coal_type_choices).grid(column=1, row=1, sticky=N)
    Label(tab1, text='').grid(row=2, column=1, sticky=N)
    Label(tab1, text='Electricity Generated (MWh)', font=('Arial', 10, 'bold')).grid(
        row=3, column=1, sticky=N)
    power_input = Entry(tab1, validate='all', validatecommand=(vcmd_float, '%P'))
    power_input.grid(row=4, column=1)
    Label(tab1, text='').grid(row=5, column=1, sticky=N)
    Label(tab1, text='Number of Runs for Monte Carlo Analysis', font=('Arial', 10, 'bold')).grid(row=6, column=1, sticky=N)
    runs_input = Entry(tab1, validate='all', validatecommand=(vcmd_int, '%P'))
    runs_input.grid(row=7, column=1)
    Label(tab1, text='').grid(row=8, column=1, sticky=N)
    Label(tab1, text='Instructions', font=('Arial', 12, 'bold')).grid(row=9, column=1, sticky=N)
    Label(tab1, text='1. Enter the basic information about the power plant on this tab.').grid(row=10, column=1, sticky=N)
    Label(tab1, text='2. Go to the "APCD Input" tab and select APCD used.').grid(row=11, column=1, sticky=N)
    Label(tab1, text='3. Go to the "WPCD Input" tab and select WPCD used.').grid(row=12, column=1, sticky=N)
    Label(tab1, text='4. Find the "Calculate" under "Analysis" menubar and get the results').grid(row=13, column=1, sticky=N)

## Save Function
    def save_inputs():
        '''This function will save input to an excel file to the destination'''

        try:
            values = [coal_type.get(), int(power_input.get()), int(runs_input.get())]
            input_summary = pd.DataFrame(data=values, index=['Coal type', 'Electricity generated', 'Monte Carlo runs'],
                                         columns=['Values'])
        # If the user did not enter anything for the power and the number of runs
        except ValueError:
            values = [coal_type.get(), power_input.get(), runs_input.get()]
            input_summary = pd.DataFrame(data=values, index=['Coal type', 'Electricity generated', 'Monte Carlo runs'],
                                         columns=['Values'])
        # Save the APCD and WPCD inputs
        apcd_values = [int(csESP_input.get()), int(hsESP_input.get()), int(FF_input.get()), int(SCR_input.get()),
                       int(ACI_input.get()), int(DSI_input.get()), int(dryFGD_input.get()), int(wetFGD_input.get()),
                       reagent_type.get(), oxstate_type.get(), pa_type.get()]

        wpcd_values = [int(cp_input.get()), comp_standard.get(), int(bt_input.get()), int(mbr_input.get()),
                       int(zvi_input.get()), int(alox_input.get()), int(feox_input.get()), int(iex_input.get()),
                       int(gac_input.get()), int(mvc_input.get()), int(ro_input.get()), int(crys_input.get())]

        apcd_summary = pd.DataFrame(data=apcd_values, index=['csESP', 'hsESP', 'FF', 'SCR', 'ACI', 'DSI', 'dry FGD',
                                                             'wet FGD', 'Reagent type',
                                                             'Oxidation state', 'Performance Additive'],
                                    columns=['Values'])
        wpcd_summary = pd.DataFrame(data=wpcd_values, index=['Chemical Precipitation', 'Compliance Standard',
                                                             'ABMet Bio Treatment', 'Membrane Bio-reactor',
                                                             'Zero-Valent Iron',
                                                             'AlOx', 'FeOx', 'IEX', 'Activated Carbon', 'MVC', 'RO',
                                                             'Crystallizer'], columns=['Values'])
        # Try to save the file
        try:
            output_file_path = filedialog.askdirectory()
            writer = pd.ExcelWriter(str(output_file_path) + '/' + 'Inputs.xlsx', engine='openpyxl')
            input_summary.to_excel(writer, sheet_name='Inputs')
            apcd_summary.to_excel(writer, sheet_name='Inputs', startrow=0, startcol=3)
            wpcd_summary.to_excel(writer, sheet_name='Inputs', startrow=0, startcol=6)
            writer.save()
        # If the user did not enter a file directory, an error will pop up
        except NameError:
            window2 = Toplevel(root)
            window2.grid()
            window2.title("Error")
            Label(window2, text='File directory not selected', font=('Arial', 10)).grid(row=0, column=0)
            button = Button(window2, text="Dismiss", command=window2.destroy).grid(row=1, column=0)

    # Only save APCD result
    def save_air_file():
        '''This function will save the apcd result'''
        try:
            output_file_path = filedialog.askdirectory()
            writer = pd.ExcelWriter(str(output_file_path) + '/' + 'air_pollution_partitioning_result.xlsx',
                                    engine='openpyxl')
            profile_df.to_excel(writer, sheet_name='AP result')
            writer.save()
        except NameError:
            window2 = Toplevel(root)
            window2.grid()
            window2.title("Error")
            Label(window2, text='File directory not selected', font=('Arial', 10)).grid(row=0, column=0)
            button = Button(window2, text="Dismiss", command=window2.destroy).grid(row=1, column=0)

    # Only save WPCD result
    def save_ww_file():
        '''This function will save the wastewater summary to an excel file to the destination'''
        try:
            output_file_path = filedialog.askdirectory()
            writer = pd.ExcelWriter(str(output_file_path) + '/' + 'water_pollution_partitioning_result.xlsx',
                                    engine='openpyxl')
            concentration_summary.to_excel(writer, sheet_name='WP Result')
            writer.save()
        except NameError:
            window2 = Toplevel(root)
            window2.grid()
            window2.title("Error")
            Label(window2, text='Wet FGD or File Directory not selected', font=('Arial', 10)).grid(row=0, column=0)
            button = Button(window2, text="Dismiss", command=window2.destroy).grid(row=1, column=0)

    def save_all():

        try:
            values = [coal_type.get(), int(power_input.get()), int(runs_input.get())]
            input_summary = pd.DataFrame(data=values, index=['Coal type', 'Electricity generated', 'Monte Carlo runs'],
                                         columns=['Values'])
        except ValueError:
            values = [coal_type.get(), power_input.get(), runs_input.get()]
            input_summary = pd.DataFrame(data=values, index=['Coal type', 'Electricity generated', 'Monte Carlo runs'],
                                         columns=['Values'])

        apcd_values = [int(csESP_input.get()), int(hsESP_input.get()), int(FF_input.get()), int(SCR_input.get()),
                       int(ACI_input.get()), int(DSI_input.get()), int(dryFGD_input.get()), int(wetFGD_input.get()),
                       reagent_type.get(), oxstate_type.get(), pa_type.get()]

        wpcd_values = [int(cp_input.get()), comp_standard.get(), int(bt_input.get()), int(mbr_input.get()),
                       int(zvi_input.get()), int(alox_input.get()), int(feox_input.get()), int(iex_input.get()),
                       int(gac_input.get()), int(mvc_input.get()), int(ro_input.get()), int(crys_input.get())]

        apcd_summary = pd.DataFrame(data=apcd_values, index=['csESP', 'hsESP', 'FF', 'SCR', 'ACI', 'DSI', 'dry FGD',
                                                             'wet FGD', 'Reagent type',
                                                             'Oxidation state', 'Performance Additive'],
                                    columns=['Values'])
        wpcd_summary = pd.DataFrame(data=wpcd_values, index=['Chemical Precipitation', 'Compliance Standard',
                                                             'ABMet Bio Treatment', 'Membrane Bio-reactor',
                                                             'Zero-Valent Iron',
                                                             'AlOx', 'FeOx', 'IEX', 'Activated Carbon', 'MVC', 'RO',
                                                             'Crystallizer'], columns=['Values'])
        output_file_name = filedialog.askdirectory()
        writer = pd.ExcelWriter(str(output_file_name) + '/results.xlsx', engine='openpyxl')
        input_summary.to_excel(writer, sheet_name='Inputs')
        apcd_summary.to_excel(writer, sheet_name='Inputs', startrow=0, startcol=3)
        wpcd_summary.to_excel(writer, sheet_name='Inputs', startrow=0, startcol=6)
        try:
            profile_df.to_excel(writer, sheet_name='AP result')
            concentration_summary.to_excel(writer, sheet_name='WP Result')
        except NameError:
            pass
        writer.save()
##########Tab2##########

    Label(tab2, text='Air Pollution Control Devices (APCD)', font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=50, pady=(30, 0))
    csESP_input = BooleanVar(root)
    hsESP_input = BooleanVar(root)

    def csESP_hsESP_FF():
        '''The user can only select one of the three APCDs (csESP, hsESP, FF)'''
        if hsESP_input.get() == 0:
            csESP_button.config(state=NORMAL)
            FF_button.config(state=NORMAL)
        if csESP_input.get() == 0:
            hsESP_button.config(state=NORMAL)
            FF_button.config(state=NORMAL)
        if FF_input.get() == 0:
            hsESP_button.config(state=NORMAL)
            csESP_button.config(state=NORMAL)
        if csESP_input.get() == 1:
            FF_button.config(state=DISABLED)
            hsESP_button.config(state=DISABLED)
        if hsESP_input.get() == 1:
            csESP_button.config(state=DISABLED)
            FF_button.config(state=DISABLED)
        if FF_input.get() == 1:
            hsESP_button.config(state=DISABLED)
            csESP_button.config(state=DISABLED)

    def dryFGD_wetFGD_cp():
        '''Disable options (dry FGD, wet FGD, chemical precipitation)'''
        if wetFGD_input.get() == 0:
            dryFGD_button.config(state=NORMAL)
            bt_input.set(False)
            mbr_input.set(False)
            zvi_input.set(False)
            alox_input.set(False)
            feox_input.set(False)
            iex_input.set(False)
            gac_input.set(False)
            mvc_input.set(False)
            ro_input.set(False)
            crys_input.set(False)
            bt_button.config(state=DISABLED)
            mbr_button.config(state=DISABLED)
            zvi_button.config(state=DISABLED)
            alox_button.config(state=DISABLED)
            feox_button.config(state=DISABLED)
            iex_button.config(state=DISABLED)
            gac_button.config(state=DISABLED)
            mvc_button.config(state=DISABLED)
            ro_button.config(state=DISABLED)
            crys_button.config(state=DISABLED)
            comp_standard_popup_menu.config(state='disabled')
            comp_standard.set('')
        if wetFGD_input.get() == 1:
            dryFGD_button.config(state=DISABLED)
            # bt_button.config(state=NORMAL)
            # mbr_button.config(state=NORMAL)
            # zvi_button.config(state=NORMAL)
            # alox_button.config(state=NORMAL)
            # feox_button.config(state=NORMAL)
            # iex_button.config(state=NORMAL)
            # gac_button.config(state=NORMAL)
            # mvc_button.config(state=NORMAL)
            # ro_button.config(state=NORMAL)
            # crys_button.config(state=NORMAL)
            comp_standard_popup_menu.config(state='normal')
        if dryFGD_input.get() == 0:
            wetFGD_button.config(state=NORMAL)
            cp_button.config(state=NORMAL)
        # if cp_input.get() == 1:
        #     dryFGD_button.config(state=NORMAL)
        if dryFGD_input.get() == 1:
            wetFGD_button.config(state=DISABLED)
            cp_button.config(state=DISABLED)
        # if cp_input.get() == 0:
        #     dryFGD_button.config(state=DISABLED)

    def comp_st(selection):
        if comp_standard.get() == 'existing source standard elg':
            mvc_input.set(False)
            ro_input.set(False)
            crys_input.set(False)
            mvc_button.config(state=DISABLED)
            ro_button.config(state=DISABLED)
            crys_button.config(state=DISABLED)
            bt_button.config(state=NORMAL)
            mbr_button.config(state=NORMAL)
            zvi_button.config(state=NORMAL)
            alox_button.config(state=NORMAL)
            feox_button.config(state=NORMAL)
            iex_button.config(state=NORMAL)
            gac_button.config(state=NORMAL)

        elif comp_standard.get() == 'new source VIP standard zld':
            mvc_button.config(state=NORMAL)
            ro_button.config(state=NORMAL)
            crys_button.config(state=NORMAL)
            bt_input.set(False)
            mbr_input.set(False)
            zvi_input.set(False)
            alox_input.set(False)
            feox_input.set(False)
            iex_input.set(False)
            gac_input.set(False)
            bt_button.config(state=DISABLED)
            mbr_button.config(state=DISABLED)
            zvi_button.config(state=DISABLED)
            alox_button.config(state=DISABLED)
            feox_button.config(state=DISABLED)
            iex_button.config(state=DISABLED)
            gac_button.config(state=DISABLED)
        elif comp_standard.get() == 'none':
            mvc_input.set(False)
            ro_input.set(False)
            crys_input.set(False)
            bt_input.set(False)
            mbr_input.set(False)
            zvi_input.set(False)
            alox_input.set(False)
            feox_input.set(False)
            iex_input.set(False)
            gac_input.set(False)
            mvc_button.config(state=NORMAL)
            ro_button.config(state=NORMAL)
            crys_button.config(state=NORMAL)
            bt_button.config(state=NORMAL)
            mbr_button.config(state=NORMAL)
            zvi_button.config(state=NORMAL)
            alox_button.config(state=NORMAL)
            feox_button.config(state=NORMAL)
            iex_button.config(state=NORMAL)
            gac_button.config(state=NORMAL)
        else:
            bt_input.set(False)
            mbr_input.set(False)
            zvi_input.set(False)
            alox_input.set(False)
            feox_input.set(False)
            iex_input.set(False)
            gac_input.set(False)
            mvc_input.set(False)
            ro_input.set(False)
            crys_input.set(False)
            bt_button.config(state=DISABLED)
            mbr_button.config(state=DISABLED)
            zvi_button.config(state=DISABLED)
            alox_button.config(state=DISABLED)
            feox_button.config(state=DISABLED)
            iex_button.config(state=DISABLED)
            gac_button.config(state=DISABLED)
            mvc_button.config(state=DISABLED)
            ro_button.config(state=DISABLED)
            crys_button.config(state=DISABLED)

    def wetFGD_dropdown():
        '''Dropdown menu for wet FGD'''
        # If the user selects wet FGD, enable the three options, else set them to none and disable the options
        if wetFGD_input.get() == 1:
            reagent_type_popup_menu.config(state='normal')
            oxstate_type_popup_menu.config(state='normal')
            pa_type_popup_menu.config(state='normal')
        else:
            reagent_type.set('')
            oxstate_type.set('')
            pa_type.set('')
            reagent_type_popup_menu.config(state='disabled')
            oxstate_type_popup_menu.config(state='disabled')
            pa_type_popup_menu.config(state='disabled')

    def reagent_type_option(selection):
        if reagent_type.get() == 'Limestone':
            # 0: Forced ; 1: Inhibited, 2: Natural 3: Ext. Forced

            oxstate_type_popup_menu['menu'].entryconfigure(0, state='normal')
            oxstate_type_popup_menu['menu'].entryconfigure(1, state='normal')
            oxstate_type_popup_menu['menu'].entryconfigure(2, state='disabled')
            oxstate_type_popup_menu['menu'].entryconfigure(3, state='disabled')
            pa_type_popup_menu.config(state='normal')

        else:
            # For 'Mg-enhanced' Lime, we don't have enough data for performance additives
            pa_type.set('')
            pa_type_popup_menu.config(state='disabled')
            window2 = Toplevel(root)
            window2.grid()
            window2.title("Note")
            Label(window2, text='Currently, we do not have enough data\n'
                             'for performance additives with Mg-enhanced Lime.', font=('Arial', 10)).grid(row=0, column=0)
            button = Button(window2, text="Dismiss", command=window2.destroy).grid(row=1, column=0)

            # no_data_msg = Label(tab2, text='Currently, we do not have enough data\n'
            #                  'for performance additives with Mg-enhanced Lime.', font=('Arial', 10))
            # no_data_msg.grid(row=9, column=2)
            oxstate_type_popup_menu['menu'].entryconfigure(0, state='disabled')
            oxstate_type_popup_menu['menu'].entryconfigure(1, state='normal')
            oxstate_type_popup_menu['menu'].entryconfigure(2, state='normal')
            oxstate_type_popup_menu['menu'].entryconfigure(3, state='normal')

    def ox_state_option(selection):
        if oxstate_type.get() == 'Forced':
            # 0: DBA, 1: NaFo, 2: None
            pa_type_popup_menu.config(state='normal')
            pa_type_popup_menu['menu'].entryconfigure(0, state='normal')
            pa_type_popup_menu['menu'].entryconfigure(1, state='disabled')
            pa_type_popup_menu['menu'].entryconfigure(2, state='normal')

        elif oxstate_type.get() == 'Inhibited' and reagent_type.get() == 'Limestone':
            pa_type_popup_menu.config(state='normal')
            pa_type_popup_menu['menu'].entryconfigure(0, state='normal')
            pa_type_popup_menu['menu'].entryconfigure(1, state='normal')
            pa_type_popup_menu['menu'].entryconfigure(2, state='normal')
        elif reagent_type.get() == 'Mg-enhanced Lime':
            pa_type_popup_menu.config(state='disabled')

    Label(tab3, text='', font=('Arial', 10)).grid(row=1, column=1)

    Label(tab2, text='Particulate Control', font=('Arial', 10), padx=50).grid(row=2, column=1, sticky=W)
    csESP_button = Checkbutton(tab2, text='cold side ESP', variable=csESP_input, command=csESP_hsESP_FF, padx=50)
    csESP_button.grid(row=3, column=1, sticky=W)
    hsESP_button = Checkbutton(tab2, text='hot side ESP', variable=hsESP_input, state=NORMAL, command=csESP_hsESP_FF, padx=50)
    hsESP_button.grid(row=4, column=1, sticky=W)
    FF_input = BooleanVar(root)
    FF_button = Checkbutton(tab2, text='FF', variable=FF_input, command=csESP_hsESP_FF, padx=50)
    FF_button.grid(row=5, column=1, sticky=W)
    Label(tab2, text='', padx=50).grid(row=6, column=1)
    Label(tab2, text='NOx Control', font=('Arial', 10), padx=50).grid(row=7, column=1, sticky=W)
    SCR_input = BooleanVar(root)
    SCR_button = Checkbutton(tab2, text='SCR', variable=SCR_input, padx=50).grid(row=8, column=1, sticky=W)
    Label(tab2, text='', padx=50).grid(row=9, column=1)
    Label(tab2, text='Hg Control', font=('Arial', 10), padx=50).grid(row=10, column=1, sticky=W)
    ACI_input = BooleanVar(root)
    ACI_button = Checkbutton(tab2, text='ACI', variable=ACI_input, padx=50).grid(row=11, column=1, sticky=W)
    Label(tab2, text='', padx=50).grid(row=12, column=1)
    Label(tab2, text='SO2 Control', font=('Arial', 10), padx=50).grid(row=13, column=1, sticky=W)
    DSI_input = BooleanVar(root)
    DSI_button = Checkbutton(tab2, text='DSI', variable=DSI_input, padx=50).grid(row=14, column=1, sticky=W)
    dryFGD_input = BooleanVar(root)
    dryFGD_button = Checkbutton(tab2, text='dry FGD', variable=dryFGD_input, command=dryFGD_wetFGD_cp, padx=50)
    dryFGD_button.grid(row=15, column=1, sticky=W)
    wetFGD_input = BooleanVar(root)
    wetFGD_button = Checkbutton(tab2, text='wet FGD', variable=wetFGD_input,
                                command=combine_funcs(dryFGD_wetFGD_cp, wetFGD_dropdown), padx=50)
    wetFGD_button.grid(row=16, column=1, sticky=W)
    Label(tab2, text='wet FGD Options', font=('Arial', 10, 'bold')).grid(row=0, column=2, pady=(30, 0))
    Label(tab2, text='', padx=50).grid(row=1, column=2)
    Label(tab2, text='Type of Reagent used for FGD System', font=('Arial', 10)).grid(row=2, column=2, sticky=NW)
    reagent_type = StringVar(root)
    reagent_type_choices = ['Mg-enhanced Lime', 'Limestone']
    reagent_type.set('')
    reagent_type_popup_menu = OptionMenu(tab2, reagent_type, *reagent_type_choices, command=reagent_type_option)
    reagent_type_popup_menu.config(state='disabled')
    reagent_type_popup_menu.grid(row=3, column=2, columnspan=2, sticky=W)
    Label(tab2, text='Oxidation State', font=('Arial', 10)).grid(row=5, column=2, sticky=NW)
    oxstate_type = StringVar(root)
    oxstate_type_choices = ['Forced', 'Inhibited', 'Natural', 'Ext. Forced']
    oxstate_type.set('')
    oxstate_type_popup_menu = OptionMenu(tab2, oxstate_type, *oxstate_type_choices, command=ox_state_option)
    oxstate_type_popup_menu.config(state='disabled')
    oxstate_type_popup_menu.grid(row=6, column=2, columnspan=2, sticky=NW)

    Label(tab2, text='Performance Additive', font=('Arial', 10)).grid(row=8, column=2, sticky=NW)
    pa_type = StringVar(root)
    pa_type_choices = ['DBA', 'NaFo', 'None']
    pa_type.set('')
    pa_type_popup_menu = OptionMenu(tab2, pa_type, *pa_type_choices)
    pa_type_popup_menu.config(state='disabled')
    pa_type_popup_menu.grid(row=9, column=2, columnspan=2, sticky=NW)

    # WPCD Options
    Label(tab3, text='Water Pollution Control Devices (WPCD)', font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=50, pady=(30, 0))
    Label(tab3, text='').grid(row=1, column=0, sticky=W)
    Label(tab3, text='Pretreatment', font=('Arial', 10), padx=50).grid(row=2, column=0, sticky=W)


    cp_input = BooleanVar(root)
    cp_button = Checkbutton(tab3, text='Chemical Precipitation', variable=cp_input, command=dryFGD_wetFGD_cp, padx=50)
    cp_button.grid(row=3, column=0, sticky=W)

    Label(tab3, text='').grid(row=4, column=0)

    Label(tab3, text='Compliance Standard', font=('Arial', 10), padx=50).grid(row=5, column=0, sticky=W)
    comp_standard = StringVar(root)
    comp_standard_choices = ['existing source standard elg', 'new source VIP standard zld', 'none']
    comp_standard.set('')
    comp_standard_popup_menu = OptionMenu(tab3, comp_standard, *comp_standard_choices, command=comp_st)
    comp_standard_popup_menu.config(state=DISABLED)
    comp_standard_popup_menu.grid(row=6, column=0, sticky=W, padx=50)
    Label(tab3, text='').grid(row=7, column=0)
    Label(tab3, text='Selenium Removal', font=('Arial', 10), padx=50).grid(row=8, column=0, sticky=W)

    mbr_input = BooleanVar(root)
    mbr_button = Checkbutton(tab3, text='Membrane Bio-reactor', variable=mbr_input, state=DISABLED, padx=50)
    mbr_button.grid(row=9, column=0, sticky=W)

    bt_input = BooleanVar(root)
    bt_button = Checkbutton(tab3, text='ABMet Bio Treatment', variable=bt_input, state=DISABLED, padx=50)
    bt_button.grid(row=10, column=0, sticky=W)

    Label(tab3, text='').grid(row=11, column=0, sticky=W)
    Label(tab3, text='Volume Reduction', font=('Arial', 10), padx=50).grid(row=12, column=0, sticky=W)

    mvc_input = BooleanVar(root)
    mvc_button = Checkbutton(tab3, text='MVC', variable=mvc_input, state=DISABLED, padx=50)
    mvc_button.grid(row=13, column=0, sticky=W)

    ro_input = BooleanVar(root)
    ro_button = Checkbutton(tab3, text='RO', variable=ro_input, state=DISABLED, padx=50)
    ro_button.grid(row=14, column=0, sticky=W)

    crys_input = BooleanVar(root)
    crys_button = Checkbutton(tab3, text='Crystallizer', variable=crys_input, state=DISABLED, padx=50)
    crys_button.grid(row=15, column=0, sticky=W)

    Label(tab3, text='Polishing Processes', font=('Arial', 10)).grid(row=8, column=1, sticky=W)

    zvi_input = BooleanVar(root)
    zvi_button = Checkbutton(tab3, text='Zero-Valent Iron', variable=zvi_input, state=DISABLED)
    zvi_button.grid(row=9, column=1, sticky=W)

    alox_input = BooleanVar(root)
    alox_button = Checkbutton(tab3, text='AlOx', variable=alox_input, state=DISABLED)
    alox_button.grid(row=10, column=1, sticky=W)

    feox_input = BooleanVar(root)
    feox_button = Checkbutton(tab3, text='FeOx', variable=feox_input, state=DISABLED)
    feox_button.grid(row=11, column=1, sticky=W)

    iex_input = BooleanVar(root)
    iex_button = Checkbutton(tab3, text='IEX', variable=iex_input, state=DISABLED)
    iex_button.grid(row=12, column=1, sticky=W)

    gac_input = BooleanVar(root)
    gac_button = Checkbutton(tab3, text='Activated Carbon', variable=gac_input, state=DISABLED)
    gac_button.grid(row=13, column=1, sticky=W)

    ###############################
    ####### All the graphs ########
    def show_coal_ecdf():
        qe_coal_combusted, pe_coal_combusted = ecdf(coal_combusted)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_coal_combusted, pe_coal_combusted, '-k', lw=2, label='Coal Combusted')
        ax.set_xlabel('Coal Combusted [kg/hr]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        plt.show()
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_Cl_ecdf():
        # Plot Chlorine Fate ECDFs
        qe_Cl_fate_solid, pe_Cl_fate_solid = ecdf(Cl_fate[:, 0])  # solid
        qe_Cl_fate_liquid, pe_Cl_fate_liquid = ecdf(Cl_fate[:, 1])  # liquid
        qe_Cl_fate_gas, pe_Cl_fate_gas = ecdf(Cl_fate[:, 2])  # gas
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_Cl_fate_solid, pe_Cl_fate_solid, '-k', lw=2, label='Solid')
        ax.plot(qe_Cl_fate_liquid, pe_Cl_fate_liquid, '-b', lw=2, label='Liquid')
        ax.plot(qe_Cl_fate_gas, pe_Cl_fate_gas, '-r', lw=2, label='Gas')
        ax.set_xlabel('Chlorine Mass [mg]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        fig.legend(bbox_to_anchor=(0.91, 0.275), frameon=False)
        plt.show()
        Chloride_CDF = fileDir / 'Results' / 'Mass Balance' / 'Chloride CDF.pdf'
        fig.savefig(str(Chloride_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_Se_ecdf():
        qe_Se_fate_solid, pe_Se_fate_solid = ecdf(Se_fate[:, 0])
        qe_Se_fate_liquid, pe_Se_fate_liquid = ecdf(Se_fate[:, 1])
        qe_Se_fate_gas, pe_Se_fate_gas = ecdf(Se_fate[:, 2])
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_Se_fate_solid, pe_Se_fate_solid, '-k', lw=2, label='Solid')
        ax.plot(qe_Se_fate_liquid, pe_Se_fate_liquid, '-b', lw=2, label='Liquid')
        ax.plot(qe_Se_fate_gas, pe_Se_fate_gas, '-r', lw=2, label='Gas')
        ax.set_xlabel('Selenium Mass [mg]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        fig.legend(bbox_to_anchor=(0.91, 0.275), frameon=False)
        plt.show()
        Selenium_CDF = fileDir / 'Results' / 'Mass Balance' / 'Selenium CDF.pdf'
        fig.savefig(str(Selenium_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_B_ecdf():
        # Plot Boron Fate ECDFs
        qe_B_fate_solid, pe_B_fate_solid = ecdf(B_fate[:, 0])
        qe_B_fate_liquid, pe_B_fate_liquid = ecdf(B_fate[:, 1])
        qe_B_fate_gas, pe_B_fate_gas = ecdf(B_fate[:, 2])
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_B_fate_solid, pe_B_fate_solid, '-k', lw=2, label='Solid')
        ax.plot(qe_B_fate_liquid, pe_B_fate_liquid, '-b', lw=2, label='Liquid')
        ax.plot(qe_B_fate_gas, pe_B_fate_gas, '-r', lw=2, label='Gas')
        ax.set_xlabel('Boron Mass [mg]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        fig.legend(bbox_to_anchor=(0.91, 0.275), frameon=False)
        plt.show()
        Boron_CDF = fileDir / 'Results' / 'Mass Balance' / 'Boron CDF.pdf'
        fig.savefig(str(Boron_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_Br_ecdf():
        qe_Br_fate_solid, pe_Br_fate_solid = ecdf(Br_fate[:, 0])
        qe_Br_fate_liquid, pe_Br_fate_liquid = ecdf(Br_fate[:, 1])
        qe_Br_fate_gas, pe_Br_fate_gas = ecdf(Br_fate[:, 2])
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_Br_fate_solid, pe_Br_fate_solid, '-k', lw=2, label='Solid')
        ax.plot(qe_Br_fate_liquid, pe_Br_fate_liquid, '-b', lw=2, label='Liquid')
        ax.plot(qe_Br_fate_gas, pe_Br_fate_gas, '-r', lw=2, label='Gas')
        ax.set_xlabel('Bromide Mass [mg]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        fig.legend(bbox_to_anchor=(0.91, 0.275), frameon=False)
        plt.show()
        Bromide_CDF = fileDir / 'Results' / 'Mass Balance' / 'Bromide CDF.pdf'
        fig.savefig(str(Bromide_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_Pb_ecdf():
        qe_Pb_fate_solid, pe_Pb_fate_solid = ecdf(Pb_fate[:, 0])
        qe_Pb_fate_liquid, pe_Pb_fate_liquid = ecdf(Pb_fate[:, 1])
        qe_Pb_fate_gas, pe_Pb_fate_gas = ecdf(Pb_fate[:, 2])
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_Pb_fate_solid, pe_Pb_fate_solid, '-k', lw=2, label='Solid')
        ax.plot(qe_Pb_fate_liquid, pe_Pb_fate_liquid, '-b', lw=2, label='Liquid')
        ax.plot(qe_Pb_fate_gas, pe_Pb_fate_gas, '-r', lw=2, label='Gas')
        ax.set_xlabel('Lead Mass [mg]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        fig.legend(bbox_to_anchor=(0.91, 0.275), frameon=False)
        plt.show()
        Lead_CDF = fileDir / 'Results' / 'Mass Balance' / 'Lead CDF.pdf'
        fig.savefig(str(Lead_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_As_ecdf():
        # Plot Arsenic Fate ECDFs
        qe_As_fate_solid, pe_As_fate_solid = ecdf(As_fate[:, 0])  # solid
        qe_As_fate_liquid, pe_As_fate_liquid = ecdf(As_fate[:, 1])  # liquid
        qe_As_fate_gas, pe_As_fate_gas = ecdf(As_fate[:, 2])  # gas
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_As_fate_solid, pe_As_fate_solid, '-k', lw=2, label='Solid')
        ax.plot(qe_As_fate_liquid, pe_As_fate_liquid, '-b', lw=2, label='Liquid')
        ax.plot(qe_As_fate_gas, pe_As_fate_gas, '-r', lw=2, label='Gas')
        ax.set_xlabel('Arsenic Mass [mg]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        fig.legend(bbox_to_anchor=(0.91, 0.275), frameon=False)
        plt.show()
        Arsenic_CDF = fileDir / 'Results' / 'Mass Balance' / 'Arsenic CDF.pdf'
        fig.savefig(str(Arsenic_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_Hg_ecdf():
        qe_Hg_fate_solid, pe_Hg_fate_solid = ecdf(Hg_fate[:, 0])
        qe_Hg_fate_liquid, pe_Hg_fate_liquid = ecdf(Hg_fate[:, 1])
        qe_Hg_fate_gas, pe_Hg_fate_gas = ecdf(Hg_fate[:, 2])
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_Hg_fate_solid, pe_Hg_fate_solid, '-k', lw=2, label='Solid')
        ax.plot(qe_Hg_fate_liquid, pe_Hg_fate_liquid, '-b', lw=2, label='Liquid')
        ax.plot(qe_Hg_fate_gas, pe_Hg_fate_gas, '-r', lw=2, label='Gas')
        ax.set_xlabel('Mercury Mass [mg]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        fig.legend(bbox_to_anchor=(0.91, 0.275), frameon=False)
        plt.show()
        Mercury_CDF = fileDir / 'Results' / 'Mass Balance' / 'Mercury CDF.pdf'
        fig.savefig(str(Mercury_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_S_ecdf():
        qe_S_fate_solid, pe_S_fate_solid = ecdf(S_fate[:, 0])
        qe_S_fate_liquid, pe_S_fate_liquid = ecdf(S_fate[:, 1])
        qe_S_fate_gas, pe_S_fate_gas = ecdf(S_fate[:, 2])
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_S_fate_solid, pe_S_fate_solid, '-k', lw=2, label='Solid')
        ax.plot(qe_S_fate_liquid, pe_S_fate_liquid, '-b', lw=2, label='Liquid')
        ax.plot(qe_S_fate_gas, pe_S_fate_gas, '-r', lw=2, label='Gas')
        ax.set_xlabel('Sulfur Mass [mg]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        fig.legend(bbox_to_anchor=(0.91, 0.275), frameon=False)
        plt.show()
        Sulfur_CDF = fileDir / 'Results' / 'Mass Balance' / 'Sulfur CDF.pdf'
        fig.savefig(str(Sulfur_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_wastewater_ecdf():
        qe_wastewater, pe_wastewater = ecdf(wastewater_production)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_wastewater, pe_wastewater, '-k', lw=2)
        ax.set_xlabel('Wastewater Flow Rate [m^3/hr]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        # fig.legend(bbox_to_anchor=(0.91, 0.275))
        Wastewater_CDF = fileDir / 'Results' / 'Mass Balance' / 'Wastewater Flowrate.pdf'
        fig.savefig(str(Wastewater_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_FGD_boxplot():
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
        # fig.savefig(folder_path, bbox_inches='tight')
        plt.show()
        plt.close()

    def show_As_pdf():
        fig = figure(num=None, figsize=(3.3, 3.3), dpi=80, facecolor="w", edgecolor='k')

        log_effluent = np.log10(as_fgd_effluent_concentration)
        log_effluent = log_effluent[~np.isinf(log_effluent)]

        ax = sns.distplot(log_effluent, color=[153 / 255, 153 / 255, 153 / 255], hist=False,
                          kde=True,
                          kde_kws={'linewidth': 2})
        kde_x, kde_y = ax.lines[0].get_data()
        ax.fill_between(kde_x, kde_y, where=(kde_x > np.log10(0.008)), interpolate=True,
                        color=[153 / 255, 153 / 255, 153 / 255])

        log_conc = np.log10(As_concentration)
        log_conc = log_conc[~np.isinf(log_conc)]
        sns.distplot(log_conc, color=[228 / 255, 26 / 255, 28 / 255], hist=False, kde=True,
                     kde_kws={'linewidth': 2}, label='Influent')
        cp, mbr, bt, iex, alox, feox, zvi, gac = [WPCD_info['cp'],
                                                  WPCD_info['mbr'],
                                                  WPCD_info['bt'],
                                                  WPCD_info['iex'],
                                                  WPCD_info['alox'],
                                                  WPCD_info['feox'],
                                                  WPCD_info['zvi'],
                                                  WPCD_info['gac']]

        if cp == 1 and (mbr + bt + iex + alox + feox + zvi != 0):
            log_as_cp = np.log10(fgd_wastewater_concentration(as_mass_cp[:, 1], wastewater_production))
            log_as_cp = log_as_cp[~np.isinf(log_as_cp)]
            sns.distplot(log_as_cp,
                         color=[55 / 255, 126 / 255, 184 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                         label='CP')
        if mbr == 1 and (bt + iex + alox + feox + zvi != 0):
            log_as_mbr = np.log10(fgd_wastewater_concentration(as_mass_mbr[:, 1], wastewater_production))
            log_as_mbr = log_as_mbr[~np.isinf(log_as_mbr)]
            sns.distplot(log_as_mbr,
                         color=[77 / 255, 175 / 255, 74 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                         label='MBR')
        if bt == 1 and (iex + alox + feox + zvi + gac != 0):
            log_as_bt = np.log10(fgd_wastewater_concentration(as_mass_bt[:, 1], wastewater_production))
            log_as_bt = log_as_bt[~np.isinf(log_as_bt)]
            sns.distplot(log_as_bt,
                         color=[152 / 255, 78 / 255, 163 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                         label='Bio')
        if iex == 1 and (alox + feox + zvi + gac != 0):
            log_as_iex = np.log10(fgd_wastewater_concentration(as_mass_iex[:, 1], wastewater_production))
            log_as_iex = log_as_iex[~np.isinf(log_as_iex)]
            sns.distplot(log_as_iex,
                         color=[255 / 255, 127 / 255, 0 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                         label='IEx')
        if alox == 1 and (feox + zvi + gac != 0):
            log_as_alox = np.log10(fgd_wastewater_concentration(as_mass_alox[:, 1], wastewater_production))
            log_as_alox = log_as_alox[~np.isinf(log_as_alox)]

            sns.distplot(log_as_alox,
                         color=[255 / 255, 255 / 255, 51 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                         label='AlOx')
        if feox == 1 and (zvi + gac != 0):
            log_as_feox = np.log10(fgd_wastewater_concentration(as_mass_feox[:, 1], wastewater_production))
            log_as_feox = log_as_feox[~np.isinf(log_as_feox)]
            sns.distplot(log_as_feox,
                         color=[166 / 255, 86 / 255, 40 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                         label='FeOx')
        if zvi == 1 and gac != 0:
            log_as_zvi = np.log10(fgd_wastewater_concentration(as_mass_alox[:, 1], wastewater_production))
            log_as_zvi = log_as_zvi[~np.isinf(log_as_zvi)]
            sns.distplot(log_as_zvi,
                         color=[247 / 255, 129 / 255, 191 / 255], hist=False, kde=True, kde_kws={'linewidth': 2},
                         label='ZVI')
        ax = sns.distplot(log_effluent, color=[153 / 255, 153 / 255, 153 / 255], hist=False,
                          kde=True,
                          kde_kws={'linewidth': 2}, label='Effluent')
        plt.axvline(np.log10(0.008), color='black')
        ax.set_xlabel('Arsenic Concentration [mg/L]', fontsize=12, fontname='Arial')
        ax.set_ylabel('Probability Density', fontsize=12, fontname='Arial')
        ax.set_ylim([0, 0.4])
        ax.set_xlim([-12, 6])
        plt.yticks([0, 0.1, 0.2, 0.3, 0.4], fontsize=10, fontname='Arial')
        plt.xticks([-12, -9, -6, -3, 0, 3, 6])
        plt.legend(prop={'family': 'Arial', 'size': 10}, loc='upper left', frameon=False)
        ax.set_position([0.2, 0.15, 0.75, 0.75])
        plt.show()

    def show_Se_pdf():
        cp, mbr, bt, iex, alox, feox, zvi, gac = [WPCD_info['cp'],
                                                  WPCD_info['mbr'],
                                                  WPCD_info['bt'],
                                                  WPCD_info['iex'],
                                                  WPCD_info['alox'],
                                                  WPCD_info['feox'],
                                                  WPCD_info['zvi'],
                                                  WPCD_info['gac']]
        fig = figure(num=None, figsize=(3.3, 3.3), dpi=80, facecolor="w", edgecolor='k')
        ax = sns.distplot(np.log10(se_fgd_effluent_concentration), color=[153 / 255, 153 / 255, 153 / 255], hist=False,
                          kde=True,
                          kde_kws={'linewidth': 2})
        kde_x, kde_y = ax.lines[0].get_data()
        ax.fill_between(kde_x, kde_y, where=(kde_x > np.log10(0.012)), interpolate=True,
                        color=[153 / 255, 153 / 255, 153 / 255])
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
        ax = sns.distplot(np.log10(se_fgd_effluent_concentration), color=[153 / 255, 153 / 255, 153 / 255], hist=False,
                          kde=True,
                          kde_kws={'linewidth': 2}, label='Effluent')
        plt.axvline(np.log10(0.012), color='black')
        ax.set_xlabel('Selenium Concentration [mg/L]', fontsize=12, fontname='Arial')
        ax.set_ylabel('Probability Density', fontsize=12, fontname='Arial')
        ax.set_ylim([0, 0.4])
        plt.yticks([0, 0.1, 0.2, 0.3, 0.4], fontsize=10, fontname='Arial')
        plt.legend(prop={'family': 'Arial', 'size': 10}, frameon=False)
        plt.show()

    def show_Hg_pdf():
        cp, mbr, bt, iex, alox, feox, zvi, gac = [WPCD_info['cp'],
                                                  WPCD_info['mbr'],
                                                  WPCD_info['bt'],
                                                  WPCD_info['iex'],
                                                  WPCD_info['alox'],
                                                  WPCD_info['feox'],
                                                  WPCD_info['zvi'],
                                                  WPCD_info['gac']]
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

    # Cl, Se, B, Br, Pb, As, Hg

    def show_Cl_inf_ecdf():
        Cl_conc = influent_concentration[0]
        qe_Cl_concentration, pe_Cl_concentration = ecdf(Cl_conc)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_Cl_concentration, pe_Cl_concentration, '-k', lw=2)
        ax.set_xlabel('Chlorine concentration [g/m^3]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        Chloride_CDF = fileDir / 'Results' / 'Mass Balance' / 'Chloride Concentration CDF.pdf'
        fig.savefig(str(Chloride_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_Se_inf_ecdf():
        Se_conc = influent_concentration[1]
        qe_Se_concentration, pe_Se_concentration = ecdf(Se_concentration)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_Se_concentration, pe_Se_concentration, '-k', lw=2)
        ax.set_xlabel('Selenium concentration [g/m^3]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        Selenium_CDF = fileDir / 'Results' / 'Mass Balance' / 'Selenium Concentration CDF.pdf'
        fig.savefig(str(Selenium_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_B_inf_ecdf():
        B_conc = influent_concentration[2]
        qe_B_concentration, pe_B_concentration = ecdf(B_concentration)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_B_concentration, pe_B_concentration, '-k', lw=2)
        ax.set_xlabel('Boron concentration [g/m^3]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        Boron_CDF = fileDir / 'Results' / 'Mass Balance' / 'Boron Concentration CDF.pdf'
        fig.savefig(str(Boron_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_Br_inf_ecdf():
        Br_conc = influent_concentration[3]
        qe_Br_concentration, pe_Br_concentration = ecdf(Br_conc)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_Br_concentration, pe_Br_concentration, '-k', lw=2)
        ax.set_xlabel('Bromine concentration [g/m^3]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        Bromine_CDF = fileDir / 'Results' / 'Mass Balance' / 'Bromine Concentration CDF.pdf'
        fig.savefig(str(Bromine_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_Pb_inf_ecdf():
        Pb_conc = influent_concentration[4]
        qe_Pb_concentration, pe_Pb_concentration = ecdf(Pb_conc)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_Pb_concentration, pe_Pb_concentration, '-k', lw=2)
        ax.set_xlabel('Lead concentration [g/m^3]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        Lead_CDF = fileDir / 'Results' / 'Mass Balance' / 'Lead Concentration CDF.pdf'
        fig.savefig(str(Lead_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_As_inf_ecdf():
        As_conc = influent_concentration[5]
        qe_As_concentration, pe_As_concentration = ecdf(As_conc)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_As_concentration, pe_As_concentration, '-k', lw=2)
        ax.set_xlabel('Arsenic Concentration [mg/L]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        Arsenic_CDF = fileDir / 'Results' / 'FGD Wastewater Effluent' / 'Arsenic Concentration CDF.pdf'
        fig.savefig(str(Arsenic_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_Hg_inf_ecdf():
        Hg_conc = influent_concentration[6]
        qe_Hg_concentration, pe_Hg_concentration = ecdf(Hg_conc)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_Hg_concentration, pe_Hg_concentration, '-k', lw=2)
        ax.set_xlabel('Mercury concentration [mg/L]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        Mercury_CDF = fileDir / 'Results' / 'FGD Wastewater Effluent' / 'Mercury Concentration CDF.pdf'
        fig.savefig(str(Mercury_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_As_eff_ecdf():
        qe_As_concentration, pe_As_concentration = ecdf(as_fgd_effluent_concentration)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_As_concentration, pe_As_concentration, '-k', lw=2)
        ax.set_xlabel('Arsenic Concentration [mg/L]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        Arsenic_CDF = fileDir / 'Results' / 'FGD Wastewater Effluent' / 'Arsenic Concentration CDF.pdf'
        fig.savefig(str(Arsenic_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_Cl_eff_ecdf():
        qe_Cl_concentration, pe_Cl_concentration = ecdf(cl_fgd_effluent_concentration)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_Cl_concentration, pe_Cl_concentration, '-k', lw=2)
        ax.set_xlabel('Chloride Concentration [mg/L]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        Chlorine_CDF = fileDir / 'Results' / 'FGD Wastewater Effluent' / 'Chloride Concentration CDF.pdf'
        fig.savefig(str(Chlorine_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_Hg_eff_ecdf():
        qe_Hg_concentration, pe_Hg_concentration = ecdf(hg_fgd_effluent_concentration)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_Hg_concentration, pe_Hg_concentration, '-k', lw=2)
        ax.set_xlabel('Mercury concentration [mg/L]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        Mercury_CDF = fileDir / 'Results' / 'FGD Wastewater Effluent' / 'Mercury Concentration CDF.pdf'
        fig.savefig(str(Mercury_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_Se_eff_ecdf():
        qe_Se_concentration, pe_Se_concentration = ecdf(se_fgd_effluent_concentration)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_Se_concentration, pe_Se_concentration, '-k', lw=2)
        ax.set_xlabel('Selenium concentration [mg/L]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        Selenium_CDF = fileDir / 'Results' / 'FGD Wastewater Effluent' / 'Selenium Concentration CDF.pdf'
        fig.savefig(str(Selenium_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def ww_electricity_consumption():
        cp, mbr, bt, iex, alox, feox, zvi, gac, crys, mvc = [WPCD_info['cp'],
                                                             WPCD_info['mbr'],
                                                             WPCD_info['bt'],
                                                             WPCD_info['iex'],
                                                             WPCD_info['alox'],
                                                             WPCD_info['feox'],
                                                             WPCD_info['zvi'],
                                                             WPCD_info['gac'],
                                                             WPCD_info['crys'],
                                                             WPCD_info['mvc']]
        electricity_used_for_wastewater_treatment, cost_of_electricity = \
            wastewater_treatment_electricity_consumption(wastewater_production, cp, mbr, bt, mvc, iex, alox, feox, zvi,
                                                         crys)
        qe_electricity_consumption, pe_electricity_consumption = ecdf(electricity_used_for_wastewater_treatment)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_electricity_consumption, pe_electricity_consumption, '-k', lw=2)
        ax.set_xlabel('Electricity Consumed [kWh/hr]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        Selenium_CDF = fileDir / 'Results' / 'Electricity Consumed for Wastewater Treatment CDF.pdf'
        fig.savefig(str(Selenium_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def ww_electricity_cost():
        cp, mbr, bt, iex, alox, feox, zvi, gac, crys, mvc = [WPCD_info['cp'],
                                                             WPCD_info['mbr'],
                                                             WPCD_info['bt'],
                                                             WPCD_info['iex'],
                                                             WPCD_info['alox'],
                                                             WPCD_info['feox'],
                                                             WPCD_info['zvi'],
                                                             WPCD_info['gac'],
                                                             WPCD_info['crys'],
                                                             WPCD_info['mvc']]
        electricity_used_for_wastewater_treatment, cost_of_electricity = \
            wastewater_treatment_electricity_consumption(wastewater_production, cp, mbr, bt, mvc, iex, alox, feox, zvi,
                                                         crys)
        qe_electricity_cost, pe_electricity_cost = ecdf(cost_of_electricity)
        fig, ax = plt.subplots(1, 1)
        fig.figsize = (2.8, 2.8)
        # ax.hold(True)
        ax.plot(qe_electricity_cost, pe_electricity_cost, '-k', lw=2)
        ax.set_xlabel('Electricity Cost [$/hr]')
        ax.set_ylabel('Cumulative Probability')
        ax.set_ylim([0, 1])
        # ax.set_adjustable(box = )
        plt.show()
        Selenium_CDF = fileDir / 'Results' / 'Electricity Consumed for Wastewater Treatment CDF.pdf'
        fig.savefig(str(Selenium_CDF), bbox_inches='tight')
        # ax.hold(False)
        ax.clear()
        plt.close()

    def show_Se_speciation():
        if type(Se_wetFGD_ww) != 0:
            # calculate the Se speciation in wetFGD waste water
            Se_speciation_button.config(state=NORMAL)
            Se_speciation = np.zeros(shape=[basic_info['mc runs'], 4])
            for i in range(0, 4):
                Se_speciation[:, i] = Se_concentration * Se_wetFGD_ww[:, i]  # [g/m^3]
            qe_Se4, pe_Se4 = ecdf(Se_speciation[:, 0])
            qe_Se6, pe_Se6 = ecdf(Se_speciation[:, 1])
            qe_SeSO3, pe_SeSO3 = ecdf(Se_speciation[:, 2])
            qe_Others, pe_Others = ecdf(Se_speciation[:, 3])
            qe_se_Total, pe_se_Total = ecdf(
                Se_speciation[:, 0] + Se_speciation[:, 1] + Se_speciation[:, 2] + Se_speciation[:, 3])
            fig, ax = plt.subplots(1, 1)
            fig.figsize = (2.8, 2.8)
            #        ax.hold(True)
            ax.plot(qe_Se4, pe_Se4, '-m', lw=2, label='Se4')
            ax.plot(qe_Se6, pe_Se6, '-b', lw=2, label='Se6')
            ax.plot(qe_SeSO3, pe_SeSO3, '-r', lw=2, label='SeSO3')
            ax.plot(qe_Others, pe_Others, '-g', lw=2, label='Others')
            ax.plot(qe_se_Total, pe_se_Total, '-k', lw=2, label="Total")
            ax.set_xlabel('Selenium Speciation Concentration [g/m^3]')
            ax.set_ylabel('Cumulative Probability')
            ax.legend(frameon=False)
            ax.set_ylim([0, 1])
            # #ax.set_adjustable(box = )
            plt.show()
            Selenium_CDF = fileDir / 'Results' / 'Mass Balance' / 'Selenium Speciation CDF.pdf'
            fig.savefig(str(Selenium_CDF), bbox_inches='tight')
            #        ax.hold(False)
            ax.clear()
            plt.close()

    def chemical_consumption():
        # Model chemical consumption
        cp, mbr, bt, iex, alox, feox, zvi, gac, crys, mvc = [WPCD_info['cp'],
                                                             WPCD_info['mbr'],
                                                             WPCD_info['bt'],
                                                             WPCD_info['iex'],
                                                             WPCD_info['alox'],
                                                             WPCD_info['feox'],
                                                             WPCD_info['zvi'],
                                                             WPCD_info['gac'],
                                                             WPCD_info['crys'],
                                                             WPCD_info['mvc']]
        lime_consumption, organosulfide_consumption, iron_chloride_consumption, nutrient_consumption, coagulant_consumption, \
        antiscalant_consumption, soda_ash_consumption, acid_consumption, polymer_consumption = \
            wastewater_chemical_consumption(wastewater_production, cp, mbr, bt, mvc, iex, alox, feox, zvi, crys)

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
        if qe_lime_consumption.all() == 0 and pe_lime_consumption.all() == 0:
            textstr1 = '\n No lime will be used\nin the process.'
            ax1.text(0.08, 0.4, textstr1, fontsize=9, font='Arial')
            ax1.set_ylabel('Cumulative Probability')
        else:
            line1, = ax1.plot(qe_lime_consumption, pe_lime_consumption, color=(228 / 255, 26 / 255, 28 / 255), lw=2,
                              label='Lime')
            ax1.set_xlabel(' ')
            ax1.set_ylabel('Cumulative Probability')
            ax1.set_ylim([0, 1])
            line1.set_label('Lime')
            ax1.legend(loc='lower right', frameon=False)
        if qe_organosulfide_consumption.all() == 0 and pe_organosulfide_consumption.all() == 0:
            textstr2 = '\n No organosulfide will be used\nin the process.'
            ax2.text(0.08, 0.4, textstr2, fontsize=9)
        else:
            line2, = ax2.plot(qe_organosulfide_consumption, pe_organosulfide_consumption,
                              color=(55 / 255, 126 / 255, 184 / 255),
                              lw=2, label='Organosulfide')
            ax2.set_xlabel(' ')
            ax2.set_ylabel(' ')
            ax2.set_yticks([])
            line2.set_label('Organosulfide')
            ax2.legend(loc='lower right', frameon=False)
        if qe_iron_chloride_consumption.all() == 0 and pe_iron_chloride_consumption.all() == 0:
            textstr3 = '\n No iron chloride will be used\nin the process.'
            ax3.text(0.08, 0.4, textstr3, fontsize=9)
        else:
            line3, = ax3.plot(qe_iron_chloride_consumption, pe_iron_chloride_consumption,
                              color=(77 / 255, 175 / 255, 74 / 255),
                              lw=2, label='Iron Chloride')
            ax3.set_xlabel(' ')
            ax3.set_ylabel(' ')
            ax3.set_yticks([])
            line3.set_label('Iron Chloride')
            ax3.legend(loc='lower right', frameon=False)
        if qe_nutrient_consumption.all() == 0 and pe_nutrient_consumption.all() == 0:
            textstr4 = '\n No nutrient will be used\nin the process.'
            ax4.text(0.08, 0.4, textstr4, fontsize=9)
        else:
            line4, = ax4.plot(qe_nutrient_consumption, pe_nutrient_consumption, color=(152 / 255, 78 / 255, 163 / 255),
                              lw=2,
                              label='Nutrient')
            ax4.set_xlabel('')
            ax4.set_ylabel('Cumulative Probability')
            ax4.set_ylim([0, 1])
            line4.set_label('Nutrient')
            ax4.legend(loc='lower right', frameon=False)

        if qe_coagulant_consumption.all() == 0 and pe_coagulant_consumption.all() == 0:
            textstr5 = '\n No coagulant will be used\nin the process.'
            ax5.text(0.08, 0.4, textstr5, fontsize=9)
        else:
            line5, = ax5.plot(qe_coagulant_consumption, pe_coagulant_consumption, color=(255 / 255, 127 / 255, 0 / 255),
                              lw=2,
                              label='Coagulant')
            ax5.set_xlabel(' ')
            ax5.set_ylabel(' ')
            ax5.set_yticks([])
            line5.set_label('Coagulant')
            ax5.legend(loc='lower right', frameon=False)

        if qe_antiscalant_consumption.all() == 0 and pe_antiscalant_consumption.all() == 0:
            textstr6 = '\n No antiscalant will be used\nin the process.'
            ax6.text(0.08, 0.4, textstr6, fontsize=9)
        else:
            line6, = ax6.plot(qe_antiscalant_consumption, pe_antiscalant_consumption,
                              color=(255 / 255, 255 / 255, 51 / 255), lw=2,
                              label='Antiscalant')
            ax6.set_xlabel(' ')
            ax6.set_ylabel(' ')
            ax6.set_yticks([])
            line6.set_label('Antiscalant')
            ax6.legend(loc='lower right', frameon=False)
        if qe_soda_ash_consumption.all() == 0 and pe_soda_ash_consumption.all() == 0:
            textstr7 = '\n No soda ash will be used\nin the process.'
            ax7.text(0.08, 0.4, textstr7, fontsize=9)
        else:
            line7, = ax7.plot(qe_soda_ash_consumption, pe_soda_ash_consumption, color=(166 / 255, 86 / 255, 40 / 255),
                              lw=2,
                              label='Soda Ash')
            ax7.set_xlabel('Chemical Consumption [kg/hr]')
            ax7.set_ylabel('Cumulative Probability')
            ax7.set_ylim([0, 1])
            line7.set_label('Soda Ash')
            ax7.legend(loc='lower right', frameon=False)

        if qe_acid_consumption.all() == 0 and pe_acid_consumption.all() == 0:
            textstr8 = '\n No acid will be used\nin the process.'
            ax8.text(0.08, 0.4, textstr8, fontsize=9)
        else:
            line8, = ax8.plot(qe_acid_consumption, pe_acid_consumption, color=(247 / 255, 129 / 255, 191 / 255), lw=2,
                              label='acid')
            ax8.set_xlabel('Chemical Consumption [kg/hr]')
            ax8.set_ylabel(' ')
            ax8.set_yticks([])
            line8.set_label('Acid')
            ax8.legend(loc='lower right', frameon=False)
        if qe_polymer_consumption.all() == 0 and pe_polymer_consumption.all() == 0:
            textstr9 = '\n No polymer will be used\nin the process.'
            ax8.text(0.08, 0.4, textstr9, fontsize=9)
        else:
            line9, = ax9.plot(qe_polymer_consumption, pe_polymer_consumption, color=(153 / 255, 153 / 255, 153 / 255),
                              lw=2, label='polymer')
            ax9.set_xlabel('Chemical Consumption [kg/hr]')
            ax9.set_ylabel(' ')
            ax9.set_yticks([])
            line9.set_label('Polymer')
            ax9.legend(loc='lower right', frameon=False)
            plt.show()

        chemical_consumption_cdfs = fileDir / 'Results' / 'Chemicals Consumed for Wastewater Treatment CDF.pdf'
        fig.savefig(str(chemical_consumption_cdfs), bbox_inches='tight')
        # ax.clear()
        plt.close()

    coal_ecdf_button = Button(tab6, text='Coal ecdf', command=show_coal_ecdf, state=DISABLED)
    coal_ecdf_button.grid(row=12, column=0)
    Label(tab6, text='Trace Elements', font=('Arial', 10, 'bold')).grid(row=0, column=0)
    Label(tab6, text='APCD Partitioning', font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=20)
    Label(tab6, text='Wastewater', font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=20, columnspan=4)
    Label(tab6, text='Influent', font=('Arial', 10, 'bold')).grid(row=1, column=2, padx=30)
    Label(tab6, text='Treatment\nEfficiency', font=('Arial', 10, 'bold')).grid(row=1, column=3)
    Label(tab6, text='Effluent', font=('Arial', 10, 'bold')).grid(row=1, column=4, padx=30)
    Label(tab6, text='Cl', font=('Arial', 10)).grid(row=2, column=0)
    Label(tab6, text='Se', font=('Arial', 10)).grid(row=3, column=0)
    Label(tab6, text='B', font=('Arial', 10)).grid(row=4, column=0)
    Label(tab6, text='Br', font=('Arial', 10)).grid(row=5, column=0)
    Label(tab6, text='Pb', font=('Arial', 10)).grid(row=6, column=0)
    Label(tab6, text='As', font=('Arial', 10)).grid(row=7, column=0)
    Label(tab6, text='Hg', font=('Arial', 10)).grid(row=8, column=0)
    Label(tab6, text='S', font=('Arial', 10)).grid(row=9, column=0)
    Label(tab6, text='').grid(row=10, column=0)
    Label(tab6, text='Misc. Graphs', font=('Arial', 10, 'bold')).grid(row=11, column=0)

    Cl_ecdf_button = Button(tab6, text='Cl ecdf', command=show_Cl_ecdf, state=DISABLED)
    Cl_ecdf_button.grid(row=2, column=1)
    Se_ecdf_button = Button(tab6, text='Se ecdf', command=show_Se_ecdf, state=DISABLED)
    Se_ecdf_button.grid(row=3, column=1)
    B_ecdf_button = Button(tab6, text='B ecdf', command=show_B_ecdf, state=DISABLED)
    B_ecdf_button.grid(row=4, column=1)
    Br_ecdf_button = Button(tab6, text='Br ecdf', command=show_Br_ecdf, state=DISABLED)
    Br_ecdf_button.grid(row=5, column=1)
    Pb_ecdf_button = Button(tab6, text='Pb ecdf', command=show_Pb_ecdf, state=DISABLED)
    Pb_ecdf_button.grid(row=6, column=1)
    As_ecdf_button = Button(tab6, text='As ecdf', command=show_As_ecdf, state=DISABLED)
    As_ecdf_button.grid(row=7, column=1)
    Hg_ecdf_button = Button(tab6, text='Hg ecdf', command=show_Hg_ecdf, state=DISABLED)
    Hg_ecdf_button.grid(row=8, column=1)
    S_ecdf_button = Button(tab6, text='S ecdf', command=show_S_ecdf, state=DISABLED)
    S_ecdf_button.grid(row=9, column=1)

    # Cl, Se, B, Br, Pb, As, Hg
    Cl_inf_ecdf_button = Button(tab6, text='Cl ecdf', command=show_Cl_inf_ecdf, state=DISABLED)
    Cl_inf_ecdf_button.grid(row=2, column=2)
    Se_inf_ecdf_button = Button(tab6, text='Se ecdf', command=show_Se_inf_ecdf, state=DISABLED)
    Se_inf_ecdf_button.grid(row=3, column=2)
    B_inf_ecdf_button = Button(tab6, text='B ecdf', command=show_B_inf_ecdf, state=DISABLED)
    B_inf_ecdf_button.grid(row=4, column=2)
    Br_inf_ecdf_button = Button(tab6, text='Br ecdf', command=show_Br_inf_ecdf, state=DISABLED)
    Br_inf_ecdf_button.grid(row=5, column=2)
    Pb_inf_ecdf_button = Button(tab6, text='Pb ecdf', command=show_Pb_inf_ecdf, state=DISABLED)
    Pb_inf_ecdf_button.grid(row=6, column=2)
    As_inf_ecdf_button = Button(tab6, text='As ecdf', command=show_As_inf_ecdf, state=DISABLED)
    As_inf_ecdf_button.grid(row=7, column=2)
    Hg_inf_ecdf_button = Button(tab6, text='Hg ecdf', command=show_Hg_inf_ecdf, state=DISABLED)
    Hg_inf_ecdf_button.grid(row=8, column=2)

    As_eff_ecdf_button = Button(tab6, text='As ecdf', command=show_As_eff_ecdf, state=DISABLED)
    As_eff_ecdf_button.grid(row=7, column=4)
    Cl_eff_ecdf_button = Button(tab6, text='Cl ecdf', command=show_Cl_eff_ecdf, state=DISABLED)
    Cl_eff_ecdf_button.grid(row=2, column=4)
    Se_eff_ecdf_button = Button(tab6, text='Se ecdf', command=show_Se_eff_ecdf, state=DISABLED)
    Se_eff_ecdf_button.grid(row=3, column=4)
    Hg_eff_ecdf_button = Button(tab6, text='Hg ecdf', command=show_Hg_eff_ecdf, state=DISABLED)
    Hg_eff_ecdf_button.grid(row=8, column=4)

    wastewater_ecdf_button = Button(tab6, text='Wastewater flow ecdf', command=show_wastewater_ecdf, state=DISABLED)
    wastewater_ecdf_button.grid(row=13, column=0)
    FGD_boxplot_button = Button(tab6, text='Wastewater Concentration Boxplot', command=show_FGD_boxplot, state=DISABLED)
    FGD_boxplot_button.grid(row=14, column=0)
    As_distplot_button = Button(tab6, text='As epdf', command=show_As_pdf, state=DISABLED)
    As_distplot_button.grid(row=7, column=3)
    Se_distplot_button = Button(tab6, text='Se epdf', command=show_Se_pdf, state=DISABLED)
    Se_distplot_button.grid(row=3, column=3)
    Hg_distplot_button = Button(tab6, text='Hg epdf', command=show_Hg_pdf, state=DISABLED)
    Hg_distplot_button.grid(row=8, column=3)
    electricity_consumption_button = Button(tab6, text='Electricity Consumption for \n wastewater treatment',
                                            command=ww_electricity_consumption, state=DISABLED)
    electricity_consumption_button.grid(row=15, column=0)
    electricity_cost_button = Button(tab6, text='Electricity Cost for \n wastewater treatment',
                                     command=ww_electricity_cost, state=DISABLED)
    electricity_cost_button.grid(row=16, column=0)
    chemical_consumption_button = Button(tab6, text='Chemical Consumption for \n wastewater treatment',
                                         command=chemical_consumption, state=DISABLED)
    chemical_consumption_button.grid(row=17, column=0)
    Se_speciation_button = Button(tab6, text='Se Speciation in wastewater', command=show_Se_speciation, state=DISABLED)
    Se_speciation_button.grid(row=18, column=0)

# Errors and round significant figures
    def wrong_power_input():
        window1 = Toplevel(root)
        window1.grid()
        window1.title("Error")
        Label(window1, text='Please Enter a valid electricity generated for the power plant', font=('Arial', 10)).grid(
            row=0, column=0)
        button = Button(window1, text="Dismiss", command=window1.destroy).grid(row=1, column=0)

    def no_APCD():
        window2 = Toplevel(root)
        window2.grid()
        window2.title("Error")
        Label(window2, text='Please select at least one APCD', font=('Arial', 10)).grid(row=0, column=0)
        button = Button(window2, text="Dismiss", command=window2.destroy).grid(row=1, column=0)

    def no_MC_runs():
        window3 = Toplevel(root)
        window3.grid()
        window3.title("Error")
        Label(window3, text='Please enter valid number of Monte Carlo Runs', font=('Arial', 10)).grid(row=0, column=0)
        button = Button(window3, text="Dismiss", command=window3.destroy).grid(row=1, column=0)

    def check_MC_runs():
        if runs_input.get() == '':
            return no_MC_runs()

    def check_input():
        '''This function will check if the power is selected
        and at least one APCD is selected'''
        if power_input.get() == '':
            return wrong_power_input()

    def check_input_apcd():
        lst = [csESP_input.get(), hsESP_input.get(), FF_input.get(), SCR_input.get(), ACI_input.get(), DSI_input.get(),
               dryFGD_input.get(), wetFGD_input.get()]
        if all(value is False for value in lst):
            return no_APCD()

    def round_sig(x, sig=3):
        try:
            return round(x, sig - int(floor(log10(abs(x)))) - 1)
        except ValueError:
            return 0

# Outputs
########################################################

    def gather_input():
        '''This function will collect all inputs and store them in a dictionary'''
        basic_info = {'coal type': coal_type.get(), 'electricity': int(power_input.get()), 'mc runs': int(runs_input.get())}

        APCD_info = {'csESP': int(csESP_input.get()), 'hsESP': int(hsESP_input.get()), 'FF': int(FF_input.get()),
                     'SCR': int(SCR_input.get()), 'ACI': int(ACI_input.get()), 'DSI': int(DSI_input.get()),
                     'dry FGD': int(dryFGD_input.get()), 'wet FGD': wetFGD_input.get(), 'reagent type': reagent_type.get(),
                     'ox state': oxstate_type.get(), 'pa': pa_type.get()}

        WPCD_info = {'cp': int(cp_input.get()), 'comp':comp_standard.get(), 'bt': int(bt_input.get()), 'mbr': int(mbr_input.get()),
                     'zvi': int(zvi_input.get()),
                     'alox': int(alox_input.get()), 'feox': int(feox_input.get()), 'iex': int(iex_input.get()),
                     'gac': int(gac_input.get()), 'mvc': int(mvc_input.get()), 'ro': int(ro_input.get()),
                     'crys': int(crys_input.get())}

        return basic_info, APCD_info, WPCD_info

    def calculate_inputs(coal_type, runs, power):

        qe_cl, pe_cl, qe_se, pe_se, qe_b, pe_b, qe_br, pe_br, qe_pb, pe_pb, qe_as, pe_as, qe_hg, pe_hg, qe_heat, pe_heat, \
        qe_s, pe_s, gross_heat_rate, fgd_water_treatment = coal_ecdf(coal_type)

        mc_cl_concentration = random_value_from_ecdf(qe_cl, pe_cl, runs)  # Concentration is in [mg/kg]
        mc_se_concentration = random_value_from_ecdf(qe_se, pe_se, runs)  # Concentration is in [mg/kg]
        mc_b_concentration = random_value_from_ecdf(qe_b, pe_b, runs)  # Concentration is in [mg/kg]
        mc_br_concentration = random_value_from_ecdf(qe_br, pe_br, runs)  # Concentration is in [mg/kg]
        mc_pb_concentration = random_value_from_ecdf(qe_pb, pe_pb, runs)  # Concentration is in [mg/kg]
        mc_as_concentration = random_value_from_ecdf(qe_as, pe_as, runs)  # Concentration is in [mg/kg]
        mc_hg_concentration = random_value_from_ecdf(qe_hg, pe_hg, runs)  # Concentration is in [mg/kg]
        mc_s_concentration = random_value_from_ecdf(qe_s, pe_s, runs)  # Concentration is in [%]
        mc_heat_concentration = random_value_from_ecdf(qe_heat, pe_heat,
                                                       runs)  # Concentration is in [Btu/lb]
        coal_combusted = coal_combustion(power, mc_heat_concentration, gross_heat_rate)

        cl_mass_entering = mc_cl_concentration * coal_combusted  # [mg/hr] of chlorine entering the plant
        se_mass_entering = mc_se_concentration * coal_combusted  # [mg/hr] of selenium entering the plant
        b_mass_entering = mc_b_concentration * coal_combusted  # [mg/hr] of boron entering the plant
        br_mass_entering = mc_br_concentration * coal_combusted  # [mg/hr] of bromine entering the plant
        pb_mass_entering = mc_pb_concentration * coal_combusted  # [mg/hr] of lead entering the plant
        as_mass_entering = mc_as_concentration * coal_combusted  # [mg/hr] of arsenic entering the plant
        hg_mass_entering = mc_hg_concentration * coal_combusted  # [mg/hr] of mercury entering the plant

        # Note that sulfur concentrations are reported in terms of %.
        # To maintain consistency with the other units, we convert the masses to mg

        s_mass_entering = mc_s_concentration * coal_combusted * 10000  # [mg/hr] of sulfur entering the plant

        input_element_values = [coal_combusted, cl_mass_entering, se_mass_entering, b_mass_entering, br_mass_entering,
                                pb_mass_entering, as_mass_entering, hg_mass_entering, s_mass_entering]
        return input_element_values

    def wetfgd_type(dictionary):
        '''This function returns the wet FGD type  based on the user's selection'''

        result = ''
        if dictionary['reagent type'] == 'Limestone':
            if dictionary['ox state'] == 'Forced':
                if dictionary['pa'] == 'DBA':
                    result = "LS Forced DBA"
                else:
                    result = "LS Forced None"
            elif dictionary['ox state'] == 'Inhibited':
                if dictionary['pa'] == 'DBA':
                    result = 'LS Inhibited DBA'
                elif dictionary['pa'] == 'None':
                    result = 'LS Inhibited None'
                else:
                    result = 'LS Inhibited NaFo'

        # No Performance Additive for now because of lack of data
        elif dictionary['reagent type'] == 'Mg-enhanced Lime':
            if dictionary['ox state'] == 'Natural':
                result = 'Mg-enhanced Lime Natural'
            elif dictionary['ox state'] == 'Inhibited':
                result = 'Mg-enhanced Lime Inhibited'
            else:
                result = 'Mg-enhanced Lime Ext. Forced'
        else:
            result = 0
        return result

    def apcd_partition_calculation(basic_info_dict, APCD_info_dict, input_elements):
        global Se_wetFGD_ww

        Cl_mass_entering, Se_mass_entering, B_mass_entering, Br_mass_entering, \
        Pb_mass_entering, As_mass_entering, Hg_mass_entering, S_mass_entering = input_elements

        wFGD_type = wetfgd_type(APCD_info_dict)

        # Get the partitioning of APCDs

        Cl_bottom, Se_bottom, B_bottom, Br_bottom, Pb_bottom, As_bottom, Hg_bottom, S_bottom = bottom_modeling(basic_info_dict['mc runs'])
        Cl_csESP, Se_csESP, B_csESP, Br_csESP, Pb_csESP, As_csESP, Hg_csESP, S_csESP = csESP_modeling(APCD_info_dict['csESP'], basic_info_dict['mc runs'])
        Cl_hsESP, Se_hsESP, B_hsESP, Br_hsESP, Pb_hsESP, As_hsESP, Hg_hsESP, S_hsESP = hsESP_modeling(APCD_info_dict['hsESP'], basic_info_dict['mc runs'])
        Cl_FF, Se_FF, B_FF, Br_FF, Pb_FF, As_FF, Hg_FF, S_FF = FF_modeling(APCD_info_dict['FF'], basic_info_dict['mc runs'])
        Cl_SCR, Se_SCR, B_SCR, Br_SCR, Pb_SCR, As_SCR, Hg_SCR, S_SCR = SCR_modeling(APCD_info_dict['SCR'], basic_info_dict['mc runs'])
        Cl_ACI, Se_ACI, B_ACI, Br_ACI, Pb_ACI, As_ACI, Hg_ACI, S_ACI = ACI_modeling(APCD_info_dict['ACI'], basic_info_dict['mc runs'])
        Cl_DSI, Se_DSI, B_DSI, Br_DSI, Pb_DSI, As_DSI, Hg_DSI, S_DSI = DSI_modeling(APCD_info_dict['DSI'], basic_info_dict['mc runs'])
        Cl_wetFGD, Se_wetFGD, B_wetFGD, Br_wetFGD, Pb_wetFGD, As_wetFGD, Hg_wetFGD, Se_wetFGD_ww, S_wetFGD = wetFGD_modeling(
            APCD_info_dict['wet FGD'], wFGD_type, basic_info_dict['mc runs'])
        Cl_dryFGD, Se_dryFGD, B_dryFGD, Br_dryFGD, Pb_dryFGD, As_dryFGD, Hg_dryFGD, S_dryFGD = dryFGD_modeling(APCD_info_dict['dry FGD'],
                                                                                                               basic_info_dict['mc runs'])
        if APCD_info_dict['wet FGD'] == 1 and APCD_info_dict['SCR'] == 1:
            # Find the wetFGD + SCR coefficients for Hg
            Hg_wetFGD_SCR = wetFGD_SCR_modeling(basic_info_dict['mc runs'])
            Cl_mass_bottom, Se_mass_bottom, B_mass_bottom, Br_mass_bottom, Pb_mass_bottom, As_mass_bottom, Hg_mass_bottom, \
            S_mass_bottom = apcd_mass_partitioning(basic_info_dict['mc runs'], Cl_mass_entering, Cl_bottom,
                                                   Se_mass_entering, Se_bottom,
                                                   B_mass_entering,
                                                   B_bottom, Br_mass_entering, Br_bottom, Pb_mass_entering, Pb_bottom,
                                                   As_mass_entering, As_bottom, Hg_mass_entering, Hg_bottom,
                                                   S_mass_entering,
                                                   S_bottom)

            Cl_mass_dryFGD, Se_mass_dryFGD, B_mass_dryFGD, Br_mass_dryFGD, Pb_mass_dryFGD, As_mass_dryFGD, Hg_mass_dryFGD, \
            S_mass_dryFGD = apcd_mass_partitioning(basic_info_dict['mc runs'], Cl_mass_bottom[:, 2], Cl_dryFGD,
                                                   Se_mass_bottom[:, 2], Se_dryFGD,
                                                   B_mass_bottom[:, 2], B_dryFGD, Br_mass_bottom[:, 2], Br_dryFGD,
                                                   Pb_mass_bottom[:, 2], Pb_dryFGD, As_mass_bottom[:, 2], As_dryFGD,
                                                   Hg_mass_bottom[:, 2], Hg_dryFGD, S_mass_bottom[:, 2], S_dryFGD)

            Cl_mass_csESP, Se_mass_csESP, B_mass_csESP, Br_mass_csESP, Pb_mass_csESP, As_mass_csESP, Hg_mass_csESP, S_mass_csESP = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_dryFGD[:, 2], Cl_csESP, Se_mass_dryFGD[:, 2], Se_csESP, B_mass_dryFGD[:, 2], B_csESP,
                Br_mass_dryFGD[:, 2],
                Br_csESP, Pb_mass_dryFGD[:, 2], Pb_csESP, As_mass_dryFGD[:, 2], As_csESP, Hg_mass_dryFGD[:, 2],
                Hg_csESP,
                S_mass_dryFGD[:, 2], S_csESP)

            Cl_mass_hsESP, Se_mass_hsESP, B_mass_hsESP, Br_mass_hsESP, Pb_mass_hsESP, As_mass_hsESP, Hg_mass_hsESP, S_mass_hsESP = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_csESP[:, 2], Cl_hsESP, Se_mass_csESP[:, 2], Se_hsESP, B_mass_csESP[:, 2], B_hsESP,
                Br_mass_csESP[:, 2],
                Br_hsESP, Pb_mass_csESP[:, 2], Pb_hsESP, As_mass_csESP[:, 2], As_hsESP, Hg_mass_csESP[:, 2], Hg_hsESP,
                S_mass_csESP[:, 2], S_hsESP)

            Cl_mass_FF, Se_mass_FF, B_mass_FF, Br_mass_FF, Pb_mass_FF, As_mass_FF, Hg_mass_FF, S_mass_FF = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_hsESP[:, 2], Cl_FF, Se_mass_hsESP[:, 2], Se_FF, B_mass_hsESP[:, 2], B_FF, Br_mass_hsESP[:, 2],
                Br_FF,
                Pb_mass_hsESP[:, 2], Pb_FF, As_mass_hsESP[:, 2], As_FF, Hg_mass_hsESP[:, 2], Hg_FF, S_mass_hsESP[:, 2],
                S_FF)

            Cl_mass_ACI, Se_mass_ACI, B_mass_ACI, Br_mass_ACI, Pb_mass_ACI, As_mass_ACI, Hg_mass_ACI, S_mass_ACI = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_FF[:, 2], Cl_ACI, Se_mass_FF[:, 2], Se_ACI, B_mass_FF[:, 2], B_ACI, Br_mass_FF[:, 2],
                Br_ACI, Pb_mass_FF[:, 2], Pb_ACI, As_mass_FF[:, 2], As_ACI, Hg_mass_FF[:, 2], Hg_ACI,
                S_mass_FF[:, 2],
                S_ACI)

            Cl_mass_DSI, Se_mass_DSI, B_mass_DSI, Br_mass_DSI, Pb_mass_DSI, As_mass_DSI, Hg_mass_DSI, S_mass_DSI = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_ACI[:, 2], Cl_DSI, Se_mass_ACI[:, 2], Se_DSI, B_mass_ACI[:, 2], B_DSI, Br_mass_ACI[:, 2],
                Br_DSI, Pb_mass_ACI[:, 2], Pb_DSI, As_mass_ACI[:, 2], As_DSI, Hg_mass_ACI[:, 2], Hg_DSI,
                S_mass_ACI[:, 2],
                S_DSI)

            # Changes done here
            # Force the Hg partition to be zeros
            Hg_dummy_matrix = np.zeros(shape=(basic_info_dict['mc runs'], 3))
            Hg_dummy_matrix[:, 2] = np.ones(shape=basic_info_dict['mc runs'])

            Cl_mass_SCR, Se_mass_SCR, B_mass_SCR, Br_mass_SCR, Pb_mass_SCR, As_mass_SCR, Hg_mass_SCR, S_mass_SCR = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_DSI[:, 2], Cl_SCR, Se_mass_DSI[:, 2], Se_SCR, B_mass_DSI[:, 2], B_SCR, Br_mass_DSI[:, 2], Br_SCR,
                Pb_mass_DSI[:, 2],
                Pb_SCR, As_mass_DSI[:, 2], As_SCR, Hg_mass_DSI[:, 2], Hg_dummy_matrix, S_mass_DSI[:, 2], S_SCR)

            # For wetFGD partitioning, change the Hg partitioning to use the matrix from Hg_wetFGD_SCR
            Cl_mass_wetFGD, Se_mass_wetFGD, B_mass_wetFGD, Br_mass_wetFGD, Pb_mass_wetFGD, As_mass_wetFGD, Hg_mass_wetFGD, S_mass_wetFGD = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_SCR[:, 2], Cl_wetFGD, Se_mass_SCR[:, 2], Se_wetFGD, B_mass_SCR[:, 2], B_wetFGD,
                Br_mass_SCR[:, 2],
                Br_wetFGD, Pb_mass_SCR[:, 2], Pb_wetFGD, As_mass_SCR[:, 2], As_wetFGD, Hg_mass_SCR[:, 2], Hg_wetFGD,
                S_mass_SCR[:, 2],
                S_wetFGD)

            Cl_mass_dryFGD, Se_mass_dryFGD, B_mass_dryFGD, Br_mass_dryFGD, Pb_mass_dryFGD, As_mass_dryFGD, Hg_mass_dryFGD, S_mass_dryFGD = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_wetFGD[:, 2], Cl_dryFGD, Se_mass_wetFGD[:, 2], Se_dryFGD, B_mass_wetFGD[:, 2], B_dryFGD,
                Br_mass_wetFGD[:, 2],
                Br_dryFGD, Pb_mass_wetFGD[:, 2], Pb_dryFGD, As_mass_wetFGD[:, 2], As_dryFGD, Hg_mass_wetFGD[:, 2],
                Hg_dryFGD,
                S_mass_wetFGD[:, 2], S_dryFGD)
        else:
            # Calculate partitioning, original code
            Cl_mass_bottom, Se_mass_bottom, B_mass_bottom, Br_mass_bottom, Pb_mass_bottom, As_mass_bottom, Hg_mass_bottom, \
            S_mass_bottom = apcd_mass_partitioning(basic_info_dict['mc runs'], Cl_mass_entering, Cl_bottom,
                                                   Se_mass_entering, Se_bottom,
                                                   B_mass_entering,
                                                   B_bottom, Br_mass_entering, Br_bottom, Pb_mass_entering, Pb_bottom,
                                                   As_mass_entering, As_bottom, Hg_mass_entering, Hg_bottom,
                                                   S_mass_entering,
                                                   S_bottom)

            Cl_mass_dryFGD, Se_mass_dryFGD, B_mass_dryFGD, Br_mass_dryFGD, Pb_mass_dryFGD, As_mass_dryFGD, Hg_mass_dryFGD, \
            S_mass_dryFGD = apcd_mass_partitioning(basic_info_dict['mc runs'], Cl_mass_bottom[:, 2], Cl_dryFGD,
                                                   Se_mass_bottom[:, 2], Se_dryFGD,
                                                   B_mass_bottom[:, 2], B_dryFGD, Br_mass_bottom[:, 2], Br_dryFGD,
                                                   Pb_mass_bottom[:, 2], Pb_dryFGD, As_mass_bottom[:, 2], As_dryFGD,
                                                   Hg_mass_bottom[:, 2], Hg_dryFGD, S_mass_bottom[:, 2], S_dryFGD)

            Cl_mass_csESP, Se_mass_csESP, B_mass_csESP, Br_mass_csESP, Pb_mass_csESP, As_mass_csESP, Hg_mass_csESP, S_mass_csESP = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_dryFGD[:, 2], Cl_csESP, Se_mass_dryFGD[:, 2], Se_csESP, B_mass_dryFGD[:, 2], B_csESP,
                Br_mass_dryFGD[:, 2],
                Br_csESP, Pb_mass_dryFGD[:, 2], Pb_csESP, As_mass_dryFGD[:, 2], As_csESP, Hg_mass_dryFGD[:, 2],
                Hg_csESP,
                S_mass_dryFGD[:, 2], S_csESP)

            Cl_mass_hsESP, Se_mass_hsESP, B_mass_hsESP, Br_mass_hsESP, Pb_mass_hsESP, As_mass_hsESP, Hg_mass_hsESP, S_mass_hsESP = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_csESP[:, 2], Cl_hsESP, Se_mass_csESP[:, 2], Se_hsESP, B_mass_csESP[:, 2], B_hsESP,
                Br_mass_csESP[:, 2],
                Br_hsESP, Pb_mass_csESP[:, 2], Pb_hsESP, As_mass_csESP[:, 2], As_hsESP, Hg_mass_csESP[:, 2], Hg_hsESP,
                S_mass_csESP[:, 2], S_hsESP)

            Cl_mass_FF, Se_mass_FF, B_mass_FF, Br_mass_FF, Pb_mass_FF, As_mass_FF, Hg_mass_FF, S_mass_FF = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_hsESP[:, 2], Cl_FF, Se_mass_hsESP[:, 2], Se_FF, B_mass_hsESP[:, 2], B_FF, Br_mass_hsESP[:, 2],
                Br_FF,
                Pb_mass_hsESP[:, 2], Pb_FF, As_mass_hsESP[:, 2], As_FF, Hg_mass_hsESP[:, 2], Hg_FF, S_mass_hsESP[:, 2],
                S_FF)

            Cl_mass_SCR, Se_mass_SCR, B_mass_SCR, Br_mass_SCR, Pb_mass_SCR, As_mass_SCR, Hg_mass_SCR, S_mass_SCR = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_FF[:, 2], Cl_SCR, Se_mass_FF[:, 2], Se_SCR, B_mass_FF[:, 2], B_SCR, Br_mass_FF[:, 2], Br_SCR,
                Pb_mass_FF[:, 2],
                Pb_SCR, As_mass_FF[:, 2], As_SCR, Hg_mass_FF[:, 2], Hg_SCR, S_mass_FF[:, 2], S_SCR)

            Cl_mass_ACI, Se_mass_ACI, B_mass_ACI, Br_mass_ACI, Pb_mass_ACI, As_mass_ACI, Hg_mass_ACI, S_mass_ACI = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_SCR[:, 2], Cl_ACI, Se_mass_SCR[:, 2], Se_ACI, B_mass_SCR[:, 2], B_ACI, Br_mass_SCR[:, 2],
                Br_ACI, Pb_mass_SCR[:, 2], Pb_ACI, As_mass_SCR[:, 2], As_ACI, Hg_mass_SCR[:, 2], Hg_ACI,
                S_mass_SCR[:, 2],
                S_ACI)

            Cl_mass_DSI, Se_mass_DSI, B_mass_DSI, Br_mass_DSI, Pb_mass_DSI, As_mass_DSI, Hg_mass_DSI, S_mass_DSI = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_ACI[:, 2], Cl_DSI, Se_mass_ACI[:, 2], Se_DSI, B_mass_ACI[:, 2], B_DSI, Br_mass_ACI[:, 2],
                Br_DSI, Pb_mass_ACI[:, 2], Pb_DSI, As_mass_ACI[:, 2], As_DSI, Hg_mass_ACI[:, 2], Hg_DSI,
                S_mass_ACI[:, 2],
                S_DSI)

            Cl_mass_wetFGD, Se_mass_wetFGD, B_mass_wetFGD, Br_mass_wetFGD, Pb_mass_wetFGD, As_mass_wetFGD, Hg_mass_wetFGD, S_mass_wetFGD = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_DSI[:, 2], Cl_wetFGD, Se_mass_DSI[:, 2], Se_wetFGD, B_mass_DSI[:, 2], B_wetFGD,
                Br_mass_DSI[:, 2],
                Br_wetFGD, Pb_mass_DSI[:, 2], Pb_wetFGD, As_mass_DSI[:, 2], As_wetFGD, Hg_mass_DSI[:, 2], Hg_wetFGD,
                S_mass_DSI[:, 2],
                S_wetFGD)

            Cl_mass_dryFGD, Se_mass_dryFGD, B_mass_dryFGD, Br_mass_dryFGD, Pb_mass_dryFGD, As_mass_dryFGD, Hg_mass_dryFGD, S_mass_dryFGD = apcd_mass_partitioning(
                basic_info_dict['mc runs'],
                Cl_mass_wetFGD[:, 2], Cl_dryFGD, Se_mass_wetFGD[:, 2], Se_dryFGD, B_mass_wetFGD[:, 2], B_dryFGD,
                Br_mass_wetFGD[:, 2],
                Br_dryFGD, Pb_mass_wetFGD[:, 2], Pb_dryFGD, As_mass_wetFGD[:, 2], As_dryFGD, Hg_mass_wetFGD[:, 2],
                Hg_dryFGD,
                S_mass_wetFGD[:, 2], S_dryFGD)

         # Calculate total mass splits.  All units are in [mg/hr]
        Cl_fate = Cl_mass_bottom + Cl_mass_csESP + Cl_mass_hsESP + Cl_mass_FF + Cl_mass_SCR + Cl_mass_ACI + Cl_mass_DSI + Cl_mass_wetFGD + Cl_mass_dryFGD

        Cl_fate[:, 2] = Cl_mass_dryFGD[:, 2]

        Se_fate = Se_mass_bottom + Se_mass_csESP + Se_mass_hsESP + Se_mass_FF + Se_mass_SCR + Se_mass_ACI + Se_mass_DSI + Se_mass_wetFGD + Se_mass_dryFGD
        Se_fate[:, 2] = Se_mass_dryFGD[:, 2]

        B_fate = B_mass_bottom + B_mass_csESP + B_mass_hsESP + B_mass_FF + B_mass_SCR + B_mass_ACI + B_mass_DSI + B_mass_wetFGD + B_mass_dryFGD
        B_fate[:, 2] = B_mass_dryFGD[:, 2]

        Br_fate = Br_mass_bottom + Br_mass_csESP + Br_mass_hsESP + Br_mass_FF + Br_mass_SCR + Br_mass_ACI + Br_mass_DSI + Br_mass_wetFGD + Br_mass_dryFGD
        Br_fate[:, 2] = Br_mass_dryFGD[:, 2]

        Pb_fate = Pb_mass_bottom + Pb_mass_csESP + Pb_mass_hsESP + Pb_mass_FF + Pb_mass_SCR + Pb_mass_ACI + Pb_mass_DSI + Pb_mass_wetFGD + Pb_mass_dryFGD
        Pb_fate[:, 2] = Pb_mass_dryFGD[:, 2]

        As_fate = As_mass_bottom + As_mass_csESP + As_mass_hsESP + As_mass_FF + As_mass_SCR + As_mass_ACI + As_mass_DSI + As_mass_wetFGD + As_mass_dryFGD
        As_fate[:, 2] = As_mass_dryFGD[:, 2]

        Hg_fate = Hg_mass_bottom + Hg_mass_csESP + Hg_mass_hsESP + Hg_mass_FF + Hg_mass_SCR + Hg_mass_ACI + Hg_mass_ACI + Hg_mass_wetFGD + Hg_mass_dryFGD
        Hg_fate[:, 2] = Hg_mass_dryFGD[:, 2]

        S_fate = S_mass_bottom + S_mass_csESP + S_mass_hsESP + S_mass_FF + S_mass_SCR + S_mass_ACI + S_mass_DSI + S_mass_wetFGD + S_mass_dryFGD
        S_fate[:, 2] = S_mass_dryFGD[:, 2]

        elements_fate = [Cl_fate, Se_fate, B_fate, Br_fate, Pb_fate, As_fate, Hg_fate, S_fate]
        return elements_fate

    def calculate_input():
        # Start Creating new labels for printing the input
        global coal_combusted, gross_heat_rate, Cl_fate, Se_fate, B_fate, Br_fate, Pb_fate, As_fate, Hg_fate, S_fate, \
            wastewater_production, Cl_concentration, Se_concentration, B_concentration, Br_concentration, Pb_concentration, \
            As_concentration, Hg_concentration, label_lst, as_fgd_effluent_concentration, pb_fgd_effluent_concentration, \
            as_mass_alox, as_mass_bt, as_mass_cp, as_mass_crys, as_mass_distillate, as_mass_feox, as_mass_gac, as_mass_iex, as_mass_mbr, \
            as_mass_mvc, as_mass_ro, as_mass_zvi, cl_fgd_effluent_concentration, hg_fgd_effluent_concentration, \
            se_fgd_effluent_concentration, concentration_summary, wastewater_production, influent_concentration, \
            se_mass_cp, se_mass_alox, se_mass_bt, se_mass_crys, se_mass_feox, se_mass_gac, se_mass_mbr, se_mass_iex, \
            se_mass_mvc, se_mass_ro, se_mass_zvi, APCD_info, WPCD_info, basic_info, hg_mass_cp, hg_mass_mbr, hg_mass_bt, \
            hg_mass_feox, hg_mass_alox, hg_mass_iex, hg_mass_gac, hg_mass_zvi, profile_df, coal_profile

        # This part effectively clears the output
        try:
            for label in label_lst:
                label.config(text=' ')
        except NameError:
            pass


        basic_info, APCD_info, WPCD_info = gather_input()

        coal_combusted, cl_mass_entering, se_mass_entering, b_mass_entering, br_mass_entering, \
        pb_mass_entering, as_mass_entering, hg_mass_entering, s_mass_entering = calculate_inputs(basic_info['coal type'],
                                                                                                 basic_info['mc runs'],
                                                                                                 basic_info['electricity'])

        input_values = [coal_combusted, cl_mass_entering, se_mass_entering, b_mass_entering, br_mass_entering,
                        pb_mass_entering, as_mass_entering, hg_mass_entering, s_mass_entering]

        Label(tab4, text='Coal Combusted\n[metric tons/hr]', font=('Arial', 10, 'bold')).grid(row=1, column=0, rowspan=2)
        Label(tab4, text='Cl mass [kg/hr]', font=('Arial', 10, 'bold')).grid(row=3, column=0, rowspan=2)
        Label(tab4, text='Se mass [kg/hr]', font=('Arial', 10, 'bold')).grid(row=5, column=0, rowspan=2)
        Label(tab4, text='B mass [kg/hr]', font=('Arial', 10, 'bold')).grid(row=7, column=0, rowspan=2)
        Label(tab4, text='Br mass [kg/hr]', font=('Arial', 10, 'bold')).grid(row=9, column=0, rowspan=2)
        Label(tab4, text='Pb mass [kg/hr]', font=('Arial', 10, 'bold')).grid(row=11, column=0, rowspan=2)
        Label(tab4, text='As mass [kg/hr]', font=('Arial', 10, 'bold')).grid(row=13, column=0, rowspan=2)
        Label(tab4, text='Hg mass [g/hr]', font=('Arial', 10, 'bold')).grid(row=15, column=0, rowspan=2)
        Label(tab4, text='S mass [kg/hr]', font=('Arial', 10, 'bold')).grid(row=17, column=0, rowspan=2)
        Label(tab4, text='Median', font=('Arial', 10)).grid(row=1, column=1, padx=30)
        Label(tab4, text='Median', font=('Arial', 10)).grid(row=3, column=1, padx=30)
        Label(tab4, text='Median', font=('Arial', 10)).grid(row=5, column=1, padx=30)
        Label(tab4, text='Median', font=('Arial', 10)).grid(row=7, column=1, padx=30)
        Label(tab4, text='Median', font=('Arial', 10)).grid(row=9, column=1, padx=30)
        Label(tab4, text='Median', font=('Arial', 10)).grid(row=11, column=1, padx=30)
        Label(tab4, text='Median', font=('Arial', 10)).grid(row=13, column=1, padx=30)
        Label(tab4, text='Median', font=('Arial', 10)).grid(row=15, column=1, padx=30)
        Label(tab4, text='Median', font=('Arial', 10)).grid(row=17, column=1, padx=30)
        Label(tab4, text='25th-75th', font=('Arial', 10)).grid(row=2, column=1)
        Label(tab4, text='25th-75th', font=('Arial', 10)).grid(row=4, column=1)
        Label(tab4, text='25th-75th', font=('Arial', 10)).grid(row=6, column=1)
        Label(tab4, text='25th-75th', font=('Arial', 10)).grid(row=8, column=1)
        Label(tab4, text='25th-75th', font=('Arial', 10)).grid(row=10, column=1)
        Label(tab4, text='25th-75th', font=('Arial', 10)).grid(row=12, column=1)
        Label(tab4, text='25th-75th', font=('Arial', 10)).grid(row=14, column=1)
        Label(tab4, text='25th-75th', font=('Arial', 10)).grid(row=16, column=1)
        Label(tab4, text='25th-75th', font=('Arial', 10)).grid(row=18, column=1)

        Label(tab4, text='Input', font=('Arial', 10, 'bold')).grid(row=0, column=2)
        Label(tab4, text='Solid', font=('Arial', 10, 'bold')).grid(row=0, column=3, padx=10)
        Label(tab4, text='Liquid', font=('Arial', 10, 'bold')).grid(row=0, column=4, padx=10)
        Label(tab4, text='Gas', font=('Arial', 10, 'bold')).grid(row=0, column=5, padx=10)
        #Label(tab4, text='Note: The values for the median, 25th percentile or 75th percentile do not add up exactly because the values in each category are used')

        Cl_fate, Se_fate, B_fate, Br_fate, Pb_fate, As_fate, Hg_fate, S_fate = \
            apcd_partition_calculation(basic_info, APCD_info, input_values[1:])

        ###############Generate Labels for APCD partitioning result#######################
        coal_median_entering = round_sig(float(np.median(input_values[0]))) / 1e3
        cl_median_entering = round_sig(np.median(cl_mass_entering) / 1e6)
        se_median_entering = round_sig(np.median(se_mass_entering) / 1e6)
        b_median_entering = round_sig(np.median(b_mass_entering) / 1e6)
        br_median_entering = round_sig(np.median(br_mass_entering) / 1e6)
        pb_median_entering = round_sig(np.median(pb_mass_entering) / 1e6)
        as_median_entering = round_sig(np.median(as_mass_entering) / 1e6)
        hg_median_entering = round_sig(np.median(hg_mass_entering) / 1e3)
        s_median_entering = round_sig(np.median(s_mass_entering) / 1e6)

        coal_label = Label(tab4, text=coal_median_entering, font=('Arial', 10))
        coal_label.grid(row=1, column=2)
        Cl_input_label = Label(tab4, text='', font=('Arial', 10))
        Cl_input_label.config(text=cl_median_entering)
        Cl_input_label.grid(row=3, column=2)
        Se_input_label = Label(tab4, text=se_median_entering, font=('Arial', 10))
        Se_input_label.grid(row=5, column=2)
        B_input_label = Label(tab4, text=b_median_entering, font=('Arial', 10))
        B_input_label.grid(row=7, column=2)
        Br_input_label = Label(tab4, text=br_median_entering, font=('Arial', 10))
        Br_input_label.grid(row=9, column=2)
        Pb_input_label = Label(tab4, text=pb_median_entering, font=('Arial', 10))
        Pb_input_label.grid(row=11, column=2)
        As_input_label = Label(tab4, text=as_median_entering, font=('Arial', 10))
        As_input_label.grid(row=13, column=2)
        Hg_input_label = Label(tab4, text=hg_median_entering,font=('Arial', 10))
        Hg_input_label.grid(row=15, column=2)
        S_input_label = Label(tab4, text=s_median_entering, font=('Arial', 10))
        S_input_label.grid(row=17, column=2)

        cl_median_solid = round_sig(np.median(Cl_fate[:, 0]) / 1e6)
        se_median_solid = round_sig(np.median(Se_fate[:, 0]) / 1e6)
        b_median_solid = round_sig(np.median(B_fate[:, 0]) / 1e6)
        br_median_solid = round_sig(np.median(Br_fate[:, 0]) / 1e6)
        pb_median_solid = round_sig(np.median(Pb_fate[:, 0]) / 1e6)
        as_median_solid = round_sig(np.median(As_fate[:, 0]) / 1e6)
        hg_median_solid = round_sig(np.median(Hg_fate[:, 0]) / 1e3)
        s_median_solid = round_sig(np.median(S_fate[:, 0]) / 1e6)

        Cl_solid_label = Label(tab4, text=cl_median_solid, font=('Arial', 10))
        Cl_solid_label.grid(row=3, column=3)
        Se_solid_label = Label(tab4, text=se_median_solid, font=('Arial', 10))
        Se_solid_label.grid(row=5, column=3)
        B_solid_label = Label(tab4, text=b_median_solid, font=('Arial', 10))
        B_solid_label.grid(row=7, column=3)
        Br_solid_label = Label(tab4, text=br_median_solid, font=('Arial', 10))
        Br_solid_label.grid(row=9, column=3)
        Pb_solid_label = Label(tab4, text=pb_median_solid, font=('Arial', 10))
        Pb_solid_label.grid(row=11, column=3)
        As_solid_label = Label(tab4, text=as_median_solid, font=('Arial', 10))
        As_solid_label.grid(row=13, column=3)
        Hg_solid_label = Label(tab4, text=hg_median_solid, font=('Arial', 10))
        Hg_solid_label.grid(row=15, column=3)
        S_solid_label = Label(tab4, text=s_median_solid, font=('Arial', 10))
        S_solid_label.grid(row=17, column=3)

        cl_median_liquid = round_sig(np.median(Cl_fate[:, 1]) / 1e6)
        se_median_liquid = round_sig(np.median(Se_fate[:, 1]) / 1e6)
        b_median_liquid = round_sig(np.median(B_fate[:, 1]) / 1e6)
        br_median_liquid = round_sig(np.median(Br_fate[:, 1]) / 1e6)
        pb_median_liquid = round_sig(np.median(Pb_fate[:, 1]) / 1e6)
        as_median_liquid = round_sig(np.median(As_fate[:, 1]) / 1e6)
        hg_median_liquid = round_sig(np.median(Hg_fate[:, 1]) / 1e3)
        s_median_liquid = round_sig(np.median(S_fate[:, 1]) / 1e6)

        Cl_liquid_label = Label(tab4, text=cl_median_liquid, font=('Arial', 10))
        Cl_liquid_label.grid(row=3, column=4)
        Se_liquid_label = Label(tab4, text=se_median_liquid, font=('Arial', 10))
        Se_liquid_label.grid(row=5, column=4)
        B_liquid_label = Label(tab4, text=b_median_liquid, font=('Arial', 10))
        B_liquid_label.grid(row=7, column=4)
        Br_liquid_label = Label(tab4, text=br_median_liquid, font=('Arial', 10))
        Br_liquid_label.grid(row=9, column=4)
        Pb_liquid_label = Label(tab4, text=pb_median_liquid, font=('Arial', 10))
        Pb_liquid_label.grid(row=11, column=4)
        As_liquid_label = Label(tab4, text=as_median_liquid, font=('Arial', 10))
        As_liquid_label.grid(row=13, column=4)
        Hg_liquid_label = Label(tab4, text=hg_median_liquid, font=('Arial', 10))
        Hg_liquid_label.grid(row=15, column=4)
        S_liquid_label = Label(tab4, text=s_median_liquid, font=('Arial', 10))
        S_liquid_label.grid(row=17, column=4)

        cl_median_gas = round_sig(np.median(Cl_fate[:, 2]) / 1e6)
        se_median_gas = round_sig(np.median(Se_fate[:, 2]) / 1e6)
        b_median_gas = round_sig(np.median(B_fate[:, 2]) / 1e6)
        br_median_gas = round_sig(np.median(Br_fate[:, 2]) / 1e6)
        pb_median_gas = round_sig(np.median(Pb_fate[:, 2]) / 1e6)
        as_median_gas = round_sig(np.median(As_fate[:, 2]) / 1e6)
        hg_median_gas = round_sig(np.median(Hg_fate[:, 2]) / 1e3)
        s_median_gas = round_sig(np.median(S_fate[:, 2]) / 1e6)

        Cl_gas_label = Label(tab4, text=cl_median_gas, font=('Arial', 10))
        Cl_gas_label.grid(row=3, column=5)
        Se_gas_label = Label(tab4, text=se_median_gas, font=('Arial', 10))
        Se_gas_label.grid(row=5, column=5)
        B_gas_label = Label(tab4, text=b_median_gas, font=('Arial', 10))
        B_gas_label.grid(row=7, column=5)
        Br_gas_label = Label(tab4, text=br_median_gas, font=('Arial', 10))
        Br_gas_label.grid(row=9, column=5)
        Pb_gas_label = Label(tab4, text=pb_median_gas, font=('Arial', 10))
        Pb_gas_label.grid(row=11, column=5)
        As_gas_label = Label(tab4, text=as_median_gas, font=('Arial', 10))
        As_gas_label.grid(row=13, column=5)
        Hg_gas_label = Label(tab4, text=hg_median_gas, font=('Arial', 10))
        Hg_gas_label.grid(row=15, column=5)
        S_gas_label = Label(tab4, text=s_median_gas, font=('Arial', 10))
        S_gas_label.grid(row=17, column=5)

        coal_25_entering = round_sig(float(np.percentile(input_values[0], 25) / 1e3))
        coal_75_entering = round_sig(float(np.percentile(input_values[0], 75) / 1e3))
        cl_25_entering = round_sig(np.percentile(cl_mass_entering, 25) / 1e6)
        cl_75_entering = round_sig(np.percentile(cl_mass_entering, 75) / 1e6)
        se_25_entering = round_sig(np.percentile(se_mass_entering, 25) / 1e6)
        se_75_entering = round_sig(np.percentile(se_mass_entering, 75) / 1e6)
        b_25_entering = round_sig(np.percentile(b_mass_entering, 25) / 1e6)
        b_75_entering = round_sig(np.percentile(b_mass_entering, 75) / 1e6)
        br_25_entering = round_sig(np.percentile(br_mass_entering, 25) / 1e6)
        br_75_entering = round_sig(np.percentile(br_mass_entering, 75) / 1e6)
        pb_25_entering = round_sig(np.percentile(pb_mass_entering, 25) / 1e6)
        pb_75_entering = round_sig(np.percentile(pb_mass_entering, 75) / 1e6)
        as_25_entering = round_sig(np.percentile(as_mass_entering, 25) / 1e6)
        as_75_entering = round_sig(np.percentile(as_mass_entering, 75) / 1e6)
        hg_25_entering = round_sig(np.percentile(hg_mass_entering, 25) / 1e3)
        hg_75_entering = round_sig(np.percentile(hg_mass_entering, 75) / 1e3)
        s_25_entering = round_sig(np.percentile(s_mass_entering, 25) / 1e6)
        s_75_entering = round_sig(np.percentile(s_mass_entering, 75) / 1e6)

        coal_input_range = str(coal_25_entering) + '-' + str(coal_75_entering)
        Cl_input_range = str(cl_25_entering) + '-' + str(cl_75_entering)
        Se_input_range = str(se_25_entering) + '-' + str(se_75_entering)
        B_input_range = str(b_25_entering) + '-' + str(b_75_entering)
        Br_input_range = str(br_25_entering) + '-' + str(br_75_entering)
        Pb_input_range = str(pb_25_entering) + '-' + str(pb_75_entering)
        As_input_range = str(as_25_entering) + '-' + str(as_75_entering)
        Hg_input_range = str(hg_25_entering) + '-' + str(hg_75_entering)
        S_input_range = str(s_25_entering) + '-' + str(s_75_entering)


        # Se_input_range = str(round_sig(np.percentile(se_mass_entering, 25) / 1e6)) + '-' + str(
        #     round_sig(np.percentile(se_mass_entering, 75) / 1e6))
        # B_input_range = str(round_sig(np.percentile(b_mass_entering, 25) / 1e6)) + '-' + str(
        #     round_sig(np.percentile(b_mass_entering, 75) / 1e6))
        # Br_input_range = str(round_sig(np.percentile(br_mass_entering, 25) / 1e6)) + '-' + str(
        #     round_sig(np.percentile(br_mass_entering, 75) / 1e6))
        # Pb_input_range = str(round_sig(np.percentile(pb_mass_entering, 25) / 1e6)) + '-' + str(
        #     round_sig(np.percentile(pb_mass_entering, 75) / 1e6))
        # As_input_range = str(round_sig(np.percentile(as_mass_entering, 25) / 1e6)) + '-' + str(
        #     round_sig(np.percentile(as_mass_entering, 75) / 1e6))
        # Hg_input_range = str(round_sig(np.percentile(hg_mass_entering, 25) / 1e3)) + '-' + str(
        #     round_sig(np.percentile(hg_mass_entering, 75) / 1e3))
        # S_input_range = str(round_sig(np.percentile(s_mass_entering, 25) / 1e6)) + '-' + str(
        #     round_sig(np.percentile(s_mass_entering, 75) / 1e6))

        coal_input_range_label = Label(tab4, text=coal_input_range, font=('Arial', 10))
        coal_input_range_label.grid(row=2, column=2)
        Cl_input_range_label = Label(tab4, text=Cl_input_range, font=('Arial', 10))
        Cl_input_range_label.grid(row=4, column=2)
        Se_input_range_label = Label(tab4, text=Se_input_range, font=('Arial', 10))
        Se_input_range_label.grid(row=6, column=2)
        B_input_range_label = Label(tab4, text=B_input_range, font=('Arial', 10))
        B_input_range_label.grid(row=8, column=2)
        Br_input_range_label = Label(tab4, text=Br_input_range, font=('Arial', 10))
        Br_input_range_label.grid(row=10, column=2)
        Pb_input_range_label = Label(tab4, text=Pb_input_range, font=('Arial', 10))
        Pb_input_range_label.grid(row=12, column=2)
        As_input_range_label = Label(tab4, text=As_input_range, font=('Arial', 10))
        As_input_range_label.grid(row=14, column=2)
        Hg_input_range_label = Label(tab4, text=Hg_input_range, font=('Arial', 10))
        Hg_input_range_label.grid(row=16, column=2)
        S_input_range_label = Label(tab4, text=S_input_range, font=('Arial', 10))
        S_input_range_label.grid(row=18, column=2)

        cl_25_solid = round_sig(np.percentile(Cl_fate[:, 0], 25) / 1e6)
        cl_75_solid = round_sig(np.percentile(Cl_fate[:, 0], 75) / 1e6)
        se_25_solid = round_sig(np.percentile(Se_fate[:, 0], 25) / 1e6)
        se_75_solid = round_sig(np.percentile(Se_fate[:, 0], 75) / 1e6)
        b_25_solid = round_sig(np.percentile(B_fate[:, 0], 25) / 1e6)
        b_75_solid = round_sig(np.percentile(B_fate[:, 0], 75) / 1e6)
        br_25_solid = round_sig(np.percentile(Br_fate[:, 0], 25) / 1e6)
        br_75_solid = round_sig(np.percentile(Br_fate[:, 0], 75) / 1e6)
        pb_25_solid = round_sig(np.percentile(Pb_fate[:, 0], 25) / 1e6)
        pb_75_solid = round_sig(np.percentile(Pb_fate[:, 0], 75) / 1e6)
        as_25_solid = round_sig(np.percentile(As_fate[:, 0], 25) / 1e6)
        as_75_solid = round_sig(np.percentile(As_fate[:, 0], 75) / 1e6)
        hg_25_solid = round_sig(np.percentile(Hg_fate[:, 0], 25) / 1e3)
        hg_75_solid = round_sig(np.percentile(Hg_fate[:, 0], 75) / 1e3)
        s_25_solid = round_sig(np.percentile(S_fate[:, 0], 25) / 1e6)
        s_75_solid = round_sig(np.percentile(S_fate[:, 0], 75) / 1e6)

        Cl_solid_range = str(cl_25_solid) + '-' + str(cl_75_solid)
        Se_solid_range = str(se_25_solid) + '-' + str(se_75_solid)
        B_solid_range = str(b_25_solid) + '-' + str(b_75_solid)
        Br_solid_range = str(br_25_solid) + '-' + str(br_75_solid)
        Pb_solid_range = str(pb_25_solid) + '-' + str(pb_75_solid)
        As_solid_range = str(as_25_solid) + '-' + str(as_75_solid)
        Hg_solid_range = str(hg_25_solid) + '-' + str(hg_75_solid)
        S_solid_range = str(s_25_solid) + '-' + str(s_75_solid)

        cl_25_liquid= round_sig(np.percentile(Cl_fate[:, 1], 25) / 1e6)
        cl_75_liquid = round_sig(np.percentile(Cl_fate[:, 1], 75) / 1e6)
        se_25_liquid = round_sig(np.percentile(Se_fate[:, 1], 25) / 1e6)
        se_75_liquid = round_sig(np.percentile(Se_fate[:, 1], 75) / 1e6)
        b_25_liquid = round_sig(np.percentile(B_fate[:, 1], 25) / 1e6)
        b_75_liquid = round_sig(np.percentile(B_fate[:, 1], 75) / 1e6)
        br_25_liquid = round_sig(np.percentile(Br_fate[:, 1], 25) / 1e6)
        br_75_liquid = round_sig(np.percentile(Br_fate[:, 1], 75) / 1e6)
        pb_25_liquid = round_sig(np.percentile(Pb_fate[:, 1], 25) / 1e6)
        pb_75_liquid = round_sig(np.percentile(Pb_fate[:, 1], 75) / 1e6)
        as_25_liquid = round_sig(np.percentile(As_fate[:, 1], 25) / 1e6)
        as_75_liquid = round_sig(np.percentile(As_fate[:, 1], 75) / 1e6)
        hg_25_liquid = round_sig(np.percentile(Hg_fate[:, 1], 25) / 1e3)
        hg_75_liquid = round_sig(np.percentile(Hg_fate[:, 1], 75) / 1e3)
        s_25_liquid = round_sig(np.percentile(S_fate[:, 1], 25) / 1e6)
        s_75_liquid = round_sig(np.percentile(S_fate[:, 1], 75) / 1e6)

        Cl_liquid_range = str(cl_25_liquid) + '-' + str(cl_75_liquid)
        Se_liquid_range = str(se_25_liquid) + '-' + str(se_75_liquid)
        B_liquid_range = str(b_25_liquid) + '-' + str(b_75_liquid)
        Br_liquid_range = str(br_25_liquid) + '-' + str(br_75_liquid)
        Pb_liquid_range = str(pb_25_liquid) + '-' + str(pb_75_liquid)
        As_liquid_range = str(as_25_liquid) + '-' + str(as_75_liquid)
        Hg_liquid_range = str(hg_25_liquid) + '-' + str(hg_75_liquid)
        S_liquid_range = str(s_25_liquid) + '-' + str(s_75_liquid)

        # Cl_liquid_range = str(round_sig(np.percentile(Cl_fate[:, 1], 25) / 1e6)) + '-' + str(
        #     round_sig(np.percentile(Cl_fate[:, 1], 75) / 1e6))
        # Se_liquid_range = str(round_sig(np.percentile(Se_fate[:, 1], 25) / 1e6)) + '-' + str(
        #     round_sig(np.percentile(Se_fate[:, 1], 75) / 1e6))
        # B_liquid_range = str(round_sig(np.percentile(B_fate[:, 1], 25) / 1e6)) + '-' + str(
        #     round_sig(np.percentile(B_fate[:, 1], 75) / 1e6))
        # Br_liquid_range = str(round_sig(np.percentile(Br_fate[:, 1], 25) / 1e6)) + '-' + str(
        #     round_sig(np.percentile(Br_fate[:, 1], 75) / 1e6))
        # Pb_liquid_range = str(round_sig(np.percentile(Pb_fate[:, 1], 25) / 1e6)) + '-' + str(
        #     round_sig(np.percentile(Pb_fate[:, 1], 75) / 1e6))
        # As_liquid_range = str(round_sig(np.percentile(As_fate[:, 1], 25) / 1e6)) + '-' + str(
        #     round_sig(np.percentile(As_fate[:, 1], 75) / 1e6))
        # Hg_liquid_range = str(round_sig(np.percentile(Hg_fate[:, 1], 25) / 1e3)) + '-' + str(
        #     round_sig(np.percentile(Hg_fate[:, 1], 75) / 1e3))
        # S_liquid_range = str(round_sig(np.percentile(S_fate[:, 1], 25) / 1e6)) + '-' + str(
        #     round_sig(np.percentile(S_fate[:, 1], 75) / 1e6))

        cl_25_gas = round_sig(np.percentile(Cl_fate[:, 2], 25) / 1e6)
        cl_75_gas = round_sig(np.percentile(Cl_fate[:, 2], 75) / 1e6)
        se_25_gas = round_sig(np.percentile(Se_fate[:, 2], 25) / 1e6)
        se_75_gas = round_sig(np.percentile(Se_fate[:, 2], 75) / 1e6)
        b_25_gas = round_sig(np.percentile(B_fate[:, 2], 25) / 1e6)
        b_75_gas = round_sig(np.percentile(B_fate[:, 2], 75) / 1e6)
        br_25_gas = round_sig(np.percentile(Br_fate[:, 2], 25) / 1e6)
        br_75_gas = round_sig(np.percentile(Br_fate[:, 2], 75) / 1e6)
        pb_25_gas = round_sig(np.percentile(Pb_fate[:, 2], 25) / 1e6)
        pb_75_gas = round_sig(np.percentile(Pb_fate[:, 2], 75) / 1e6)
        as_25_gas = round_sig(np.percentile(As_fate[:, 2], 25) / 1e6)
        as_75_gas = round_sig(np.percentile(As_fate[:, 2], 75) / 1e6)
        hg_25_gas = round_sig(np.percentile(Hg_fate[:, 2], 25) / 1e3)
        hg_75_gas = round_sig(np.percentile(Hg_fate[:, 2], 75) / 1e3)
        s_25_gas = round_sig(np.percentile(S_fate[:, 2], 25) / 1e6)
        s_75_gas = round_sig(np.percentile(S_fate[:, 2], 75) / 1e6)

        Cl_gas_range = str(cl_25_gas) + '-' + str(cl_75_gas)
        Se_gas_range = str(se_25_gas) + '-' + str(se_75_gas)
        B_gas_range = str(b_25_gas) + '-' + str(b_75_gas)
        Br_gas_range = str(br_25_gas) + '-' + str(br_75_gas)
        Pb_gas_range = str(pb_25_gas) + '-' + str(pb_75_gas)
        As_gas_range = str(as_25_gas) + '-' + str(as_75_gas)
        Hg_gas_range = str(hg_25_gas) + '-' + str(hg_75_gas)
        S_gas_range = str(s_25_gas) + '-' + str(s_75_gas)

        coal_profile = [coal_median_entering, coal_25_entering, coal_75_entering]

        Cl_profile = [cl_25_entering, cl_median_entering, cl_75_entering, cl_median_solid, cl_25_solid, cl_75_solid,
                      cl_median_liquid, cl_25_liquid, cl_75_liquid, cl_median_gas, cl_25_gas, cl_75_gas]

        Se_profile = [se_25_entering, se_median_entering, se_75_entering, se_median_solid, se_25_solid, se_75_solid,
                      se_median_liquid, se_25_liquid, se_75_liquid, se_median_gas, se_25_gas, se_75_gas]

        B_profile = [b_25_entering, b_median_entering, b_75_entering, b_median_solid, b_25_solid, b_75_solid,
                      b_median_liquid, b_25_liquid, b_75_liquid, b_median_gas, b_25_gas, b_75_gas]

        Br_profile = [br_25_entering, br_median_entering, br_75_entering, br_median_solid, br_25_solid, br_75_solid,
                      br_median_liquid, br_25_liquid, br_75_liquid, br_median_gas, br_25_gas, br_75_gas]

        Pb_profile = [pb_25_entering, pb_median_entering, pb_75_entering, pb_median_solid, pb_25_solid, pb_75_solid,
                      pb_median_liquid, pb_25_liquid, pb_75_liquid, pb_median_gas, pb_25_gas, pb_75_gas]

        As_profile = [as_25_entering, as_median_entering, as_75_entering, as_median_solid, as_25_solid, as_75_solid,
                      as_median_liquid, as_25_liquid, as_75_liquid, as_median_gas, as_25_gas, as_75_gas]

        Hg_profile = [hg_25_entering, hg_median_entering, hg_75_entering, hg_median_solid, hg_25_solid, hg_75_solid,
                      hg_median_liquid, hg_25_liquid, hg_75_liquid, hg_median_gas, hg_25_gas, hg_75_gas]

        S_profile = [s_25_entering, s_median_entering, s_75_entering, s_median_solid, s_25_solid, s_75_solid,
                      s_median_liquid, s_25_liquid, s_75_liquid, s_median_gas, s_25_gas, s_75_gas]

        profile_summary = [Cl_profile, Se_profile, B_profile, Br_profile, Pb_profile, As_profile, Hg_profile, S_profile]
        profile_df = pd.DataFrame(profile_summary, index=['Cl (kg/hr)', 'Se (kg/hr)', 'B (kg/hr)', 'Br (kg/hr)', 'Pb (kg/hr)',
                                                          'As (kg/hr)', 'Hg (g/hr)', 'S (kg/hr)'],
                                  columns=['25th Input', 'Median Input', '75th input', 'Median Solid', '25th Solid', '75th Solid', 'Median Liquid',
                                           '25th Liquid', '75th Liquid', 'Median Gas', '25th Gas', '75th Gas'])


        Cl_solid_range_label = Label(tab4, text=Cl_solid_range, font=('Arial', 10))
        Cl_solid_range_label.grid(row=4, column=3)
        Se_solid_range_label = Label(tab4, text=Se_solid_range, font=('Arial', 10))
        Se_solid_range_label.grid(row=6, column=3)
        B_solid_range_label = Label(tab4, text=B_solid_range, font=('Arial', 10))
        B_solid_range_label.grid(row=8, column=3)
        Br_solid_range_label = Label(tab4, text=Br_solid_range, font=('Arial', 10))
        Br_solid_range_label.grid(row=10, column=3)
        Pb_solid_range_label = Label(tab4, text=Pb_solid_range, font=('Arial', 10))
        Pb_solid_range_label.grid(row=12, column=3)
        As_solid_range_label = Label(tab4, text=As_solid_range, font=('Arial', 10))
        As_solid_range_label.grid(row=14, column=3)
        Hg_solid_range_label = Label(tab4, text=Hg_solid_range, font=('Arial', 10))
        Hg_solid_range_label.grid(row=16, column=3)
        S_solid_range_label = Label(tab4, text=S_solid_range, font=('Arial', 10))
        S_solid_range_label.grid(row=18, column=3)

        Cl_liquid_range_label = Label(tab4, text=Cl_liquid_range, font=('Arial', 10))
        Cl_liquid_range_label.grid(row=4, column=4)
        Se_liquid_range_label = Label(tab4, text=Se_liquid_range, font=('Arial', 10))
        Se_liquid_range_label.grid(row=6, column=4)
        B_liquid_range_label = Label(tab4, text=B_liquid_range, font=('Arial', 10))
        B_liquid_range_label.grid(row=8, column=4)
        Br_liquid_range_label = Label(tab4, text=Br_liquid_range, font=('Arial', 10))
        Br_liquid_range_label.grid(row=10, column=4)
        Pb_liquid_range_label = Label(tab4, text=Pb_liquid_range, font=('Arial', 10))
        Pb_liquid_range_label.grid(row=12, column=4)
        As_liquid_range_label = Label(tab4, text=As_liquid_range, font=('Arial', 10))
        As_liquid_range_label.grid(row=14, column=4)
        Hg_liquid_range_label = Label(tab4, text=Hg_liquid_range, font=('Arial', 10))
        Hg_liquid_range_label.grid(row=16, column=4)
        S_liquid_range_label = Label(tab4, text=S_liquid_range, font=('Arial', 10))
        S_liquid_range_label.grid(row=18, column=4)

        Cl_gas_range_label = Label(tab4, text=Cl_gas_range, font=('Arial', 10))
        Cl_gas_range_label.grid(row=4, column=5)
        Se_gas_range_label = Label(tab4, text=Se_gas_range, font=('Arial', 10))
        Se_gas_range_label.grid(row=6, column=5)
        B_gas_range_label = Label(tab4, text=B_gas_range, font=('Arial', 10))
        B_gas_range_label.grid(row=8, column=5)
        Br_gas_range_label = Label(tab4, text=Br_gas_range, font=('Arial', 10))
        Br_gas_range_label.grid(row=10, column=5)
        Pb_gas_range_label = Label(tab4, text=Pb_gas_range, font=('Arial', 10))
        Pb_gas_range_label.grid(row=12, column=5)
        As_gas_range_label = Label(tab4, text=As_gas_range, font=('Arial', 10))
        As_gas_range_label.grid(row=14, column=5)
        Hg_gas_range_label = Label(tab4, text=Hg_gas_range, font=('Arial', 10))
        Hg_gas_range_label.grid(row=16, column=5)
        S_gas_range_label = Label(tab4, text=S_gas_range, font=('Arial', 10))
        S_gas_range_label.grid(row=18, column=5)

        label_lst = [coal_label, Cl_input_label, Se_input_label, B_input_label, Br_input_label, Pb_input_label,
                     As_input_label, Hg_input_label, S_input_label, coal_input_range_label, Cl_input_range_label,
                     Se_input_range_label, B_input_range_label, Br_input_range_label, Pb_input_range_label,
                     As_input_range_label, Hg_input_range_label, S_input_range_label, Cl_solid_range_label,
                     Se_solid_range_label, B_solid_range_label, Br_solid_range_label, Pb_solid_range_label,
                     As_solid_range_label, Hg_solid_range_label, S_solid_range_label, Cl_liquid_range_label,
                     Se_liquid_range_label, B_liquid_range_label, Br_liquid_range_label, Pb_liquid_range_label,
                     As_liquid_range_label, Hg_liquid_range_label, S_liquid_range_label, Cl_gas_range_label,
                     Se_gas_range_label, B_gas_range_label, Br_gas_range_label, Pb_gas_range_label,
                     As_gas_range_label, Hg_gas_range_label, S_gas_range_label, Cl_gas_label, Se_gas_label,
                     B_gas_label, Br_gas_label, Pb_gas_label, As_gas_label, Hg_gas_label, S_gas_label, Cl_liquid_label,
                     Se_liquid_label, B_liquid_label, Br_liquid_label, Pb_liquid_label, As_liquid_label, Hg_liquid_label,
                     S_liquid_label, Cl_solid_label, Se_solid_label, B_solid_label, Br_solid_label, Pb_solid_label,
                     As_solid_label, Hg_solid_label, S_solid_label]

        #############The button will be working if the calculation finishes
        coal_ecdf_button.config(state=NORMAL)
        Cl_ecdf_button.config(state=NORMAL)
        Se_ecdf_button.config(state=NORMAL)
        B_ecdf_button.config(state=NORMAL)
        Br_ecdf_button.config(state=NORMAL)
        Pb_ecdf_button.config(state=NORMAL)
        As_ecdf_button.config(state=NORMAL)
        Hg_ecdf_button.config(state=NORMAL)
        S_ecdf_button.config(state=NORMAL)


        # This wet FGD type naming results from previously defined functions
        if APCD_info['wet FGD'] == 1:
            wastewater_production = fgd_wastewater_generation_for_corrosion_limits(
                Cl_fate[:, 1])  # [m^3/hr] of FGD wastewater produced
            # Calculate trace element concentration in the FGD wastewater influent
            Cl_concentration = fgd_wastewater_concentration(Cl_fate[:, 1], wastewater_production)  # [g/m^3]
            Se_concentration = fgd_wastewater_concentration(Se_fate[:, 1], wastewater_production)  # [g/m^3]
            B_concentration = fgd_wastewater_concentration(B_fate[:, 1], wastewater_production)  # [g/m^3]
            Br_concentration = fgd_wastewater_concentration(Br_fate[:, 1], wastewater_production)  # [g/m^3]
            Pb_concentration = fgd_wastewater_concentration(Pb_fate[:, 1], wastewater_production)  # [g/m^3]
            As_concentration = fgd_wastewater_concentration(As_fate[:, 1], wastewater_production)  # [g/m^3]
            As_concentration = As_concentration[As_concentration != 0]
            Hg_concentration = fgd_wastewater_concentration(Hg_fate[:, 1], wastewater_production)  # [g/m^3]

            influent_concentration = [Cl_concentration, Se_concentration, B_concentration, Br_concentration,
                                      Pb_concentration, As_concentration, Hg_concentration]

            cl_conc_distribution = [np.percentile(Cl_concentration, 25), np.percentile(Cl_concentration, 50),
                                    np.percentile(Cl_concentration, 75)]
            se_conc_distribution = [np.percentile(Se_concentration, 25), np.percentile(Se_concentration, 50),
                                    np.percentile(Se_concentration, 75)]
            as_conc_distribution = [np.percentile(As_concentration, 25), np.percentile(As_concentration, 50),
                                    np.percentile(As_concentration, 75)]
            hg_conc_distribution = [np.percentile(Hg_concentration, 25), np.percentile(Hg_concentration, 50),
                                    np.percentile(Hg_concentration, 75)]
            b_conc_distribution = [np.percentile(B_concentration, 25), np.percentile(B_concentration, 50),
                                    np.percentile(B_concentration, 75)]
            br_conc_distribution = [np.percentile(Br_concentration, 25), np.percentile(Br_concentration, 50),
                                    np.percentile(Br_concentration, 75)]
            pb_conc_distribution = [np.percentile(Pb_concentration, 25), np.percentile(Pb_concentration, 50),
                                    np.percentile(Pb_concentration, 75)]

            # Create FGD Wastewater concentration data frame.
            concentration_summary = np.array(
                [as_conc_distribution, b_conc_distribution, br_conc_distribution, cl_conc_distribution,
                 hg_conc_distribution, pb_conc_distribution, se_conc_distribution])
            concentration_summary = pd.DataFrame(concentration_summary, index=['As [g/m^3]', 'B [g/m^3]', 'Br [g/m^3]', 'Cl [g/m^3]', 'Hg [g/m^3]', 'Pb [g/m^3]', 'Se [g/m^3]'],
                                                 columns=['25th_Percentile', 'Median',
                                                          '75th_Percentile'])

            as_cp, cl_cp, pb_cp, hg_cp, se_cp = cp_modeling(WPCD_info['cp'], basic_info['mc runs'])
            as_mass_cp, cl_mass_cp, pb_mass_cp, hg_mass_cp, se_mass_cp = wpcd_mass_partitioning(basic_info['mc runs'],
                                                                                                As_fate[:, 1], as_cp,
                                                                                                Cl_fate[:, 1], cl_cp,
                                                                                                Pb_fate[:, 1], pb_cp,
                                                                                                Hg_fate[:, 1], hg_cp,
                                                                                                Se_fate[:, 1], se_cp)

            # Check for the compliance standard here
            if WPCD_info['comp'] == 'existing source standard elg':

                as_mbr, cl_mbr, pb_mbr, hg_mbr, se_mbr = mbr_modeling(WPCD_info['mbr'], basic_info['mc runs'])
                as_bt, cl_bt, pb_bt, hg_bt, se_bt = bt_modeling(WPCD_info['bt'], basic_info['mc runs'])
                as_iex, cl_iex, pb_iex, hg_iex, se_iex = iex_modeling(WPCD_info['iex'], basic_info['mc runs'])
                as_alox, cl_alox, pb_alox, hg_alox, se_alox = alox_modeling(WPCD_info['alox'], basic_info['mc runs'])
                as_feox, cl_feox, pb_feox, hg_feox, se_feox = feox_modeling(WPCD_info['feox'], basic_info['mc runs'])
                as_zvi, cl_zvi, pb_zvi, hg_zvi, se_zvi = zvi_modeling(WPCD_info['zvi'], basic_info['mc runs'])
                as_gac, cl_gac, pb_gac, hg_gac, se_gac = gac_modeling(WPCD_info['gac'], basic_info['mc runs'])

                as_mass_mbr, cl_mass_mbr, pb_mass_mbr, hg_mass_mbr, se_mass_mbr = wpcd_mass_partitioning(
                    basic_info['mc runs'], as_mass_cp[:, 1], as_mbr,
                    cl_mass_cp[:, 1], cl_mbr,
                    pb_mass_cp[:, 1], pb_mbr,
                    hg_mass_cp[:, 1], hg_mbr,
                    se_mass_cp[:, 1], se_mbr)

                as_mass_bt, cl_mass_bt, pb_mass_bt, hg_mass_bt, se_mass_bt = wpcd_mass_partitioning(
                    basic_info['mc runs'], as_mass_mbr[:, 1], as_bt,
                    cl_mass_mbr[:, 1], cl_bt,
                    pb_mass_mbr[:, 1], pb_bt,
                    hg_mass_mbr[:, 1], hg_bt,
                    se_mass_mbr[:, 1], se_bt)


                as_mass_iex, cl_mass_iex, pb_mass_iex, hg_mass_iex, se_mass_iex = wpcd_mass_partitioning(
                    basic_info['mc runs'],
                    as_mass_bt[:, 1],
                    as_iex,
                    cl_mass_bt[:, 1],
                    cl_iex,
                    pb_mass_bt[:, 1],
                    pb_iex,
                    hg_mass_bt[:, 1],
                    hg_iex,
                    se_mass_bt[:, 1],
                    se_iex)

                as_mass_alox, cl_mass_alox, pb_mass_alox, hg_mass_alox, se_mass_alox = wpcd_mass_partitioning(
                    basic_info['mc runs'],
                    as_mass_iex[:, 1], as_alox,
                    cl_mass_iex[:, 1], cl_alox,
                    pb_mass_iex[:, 1], pb_alox,
                    hg_mass_iex[:, 1], hg_alox,
                    se_mass_iex[:, 1], se_alox)

                as_mass_feox, cl_mass_feox, pb_mass_feox, hg_mass_feox, se_mass_feox = wpcd_mass_partitioning(
                    basic_info['mc runs'], as_mass_alox[:, 1],as_feox,
                    cl_mass_alox[:, 1],cl_feox,
                    pb_mass_alox[:, 1],pb_feox,
                    hg_mass_alox[:, 1],hg_feox,
                    se_mass_alox[:, 1],se_feox)


                as_mass_zvi, cl_mass_zvi, pb_mass_zvi, hg_mass_zvi, se_mass_zvi = wpcd_mass_partitioning(
                    basic_info['mc runs'],
                    as_mass_feox[:, 1],
                    as_zvi,
                    cl_mass_feox[:, 1],
                    cl_zvi,
                    pb_mass_feox[:, 1],
                    pb_zvi,
                    hg_mass_feox[:, 1],
                    hg_zvi,
                    se_mass_feox[:, 1],
                    se_zvi)

                as_mass_gac, cl_mass_gac, pb_mass_gac, hg_mass_gac, se_mass_gac = wpcd_mass_partitioning(
                    basic_info['mc runs'],
                    as_mass_zvi[:, 1],
                    as_gac,
                    cl_mass_zvi[:, 1],
                    cl_gac,
                    pb_mass_zvi[:, 1],
                    pb_gac,
                    hg_mass_zvi[:, 1],
                    hg_gac,
                    se_mass_zvi[:, 1],
                    se_gac)

                as_fgd_effluent_concentration = fgd_wastewater_concentration(as_mass_gac[:, 1], wastewater_production)
                cl_fgd_effluent_concentration = fgd_wastewater_concentration(cl_mass_gac[:, 1], wastewater_production)
                pb_fgd_effluent_concentration = fgd_wastewater_concentration(pb_mass_gac[:, 1], wastewater_production)
                hg_fgd_effluent_concentration = fgd_wastewater_concentration(hg_mass_gac[:, 1], wastewater_production)
                se_fgd_effluent_concentration = fgd_wastewater_concentration(se_mass_gac[:, 1], wastewater_production)
                Cl_flow_label = Label(tab5, text='Cl flow\n[g/m^3]', font=('Arial', 10, 'bold'), padx=50)
                Cl_flow_label.grid(row=3, column=3, rowspan=2)
                Label(tab5, text='Se flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=5, column=3, rowspan=2)
                Label(tab5, text='B flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=7, column=3, rowspan=2)
                Label(tab5, text='Br flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=9, column=3, rowspan=2)
                Label(tab5, text='Pb flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=11, column=3, rowspan=2)
                Label(tab5, text='As flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=13, column=3, rowspan=2)
                Label(tab5, text='Hg flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=15, column=3, rowspan=2)

            elif WPCD_info['comp'] == 'new source VIP standard zld':
                as_mvc, cl_mvc, pb_mvc, hg_mvc, se_mvc = mvc_modeling(WPCD_info['mvc'], basic_info['mc runs'])
                as_ro, cl_ro, pb_ro, hg_ro, se_ro = ro_modeling(WPCD_info['ro'], basic_info['mc runs'])
                as_crys, cl_crys, pb_crys, hg_crys, se_crys = crys_modeling(WPCD_info['crys'], basic_info['mc runs'])

                as_mass_mvc, cl_mass_mvc, pb_mass_mvc, hg_mass_mvc, se_mass_mvc = wpcd_mass_partitioning(
                    basic_info['mc runs'],
                    as_mass_cp[:, 1],
                    as_mvc,
                    cl_mass_cp[:, 1],
                    cl_mvc,
                    pb_mass_cp[:, 1],
                    pb_mvc,
                    hg_mass_cp[:, 1],
                    hg_mvc,
                    se_mass_cp[:, 1],
                    se_mvc)

                as_mass_ro, cl_mass_ro, pb_mass_ro, hg_mass_ro, se_mass_ro = wpcd_mass_partitioning(basic_info['mc runs'],
                                                                                                    as_mass_mvc[:, 1],
                                                                                                    as_ro,
                                                                                                        cl_mass_mvc[:, 1],
                                                                                                    cl_ro,
                                                                                                    pb_mass_mvc[:, 1],
                                                                                                    pb_ro,
                                                                                                    hg_mass_mvc[:, 1],
                                                                                                    hg_ro,
                                                                                                    se_mass_mvc[:, 1],
                                                                                                    se_ro)

                as_mass_crys, cl_mass_crys, pb_mass_crys, hg_mass_crys, se_mass_crys = wpcd_mass_partitioning(
                    basic_info['mc runs'],
                    as_mass_ro[:,
                    1], as_crys,
                    cl_mass_ro[:,
                    1], cl_crys,
                    pb_mass_ro[:,
                    1], pb_crys,
                    hg_mass_ro[:,
                    1], hg_crys,
                    se_mass_ro[:,
                    1], se_crys)

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

                effluent_concentraion = [as_fgd_effluent_concentration, cl_fgd_effluent_concentration, pb_fgd_effluent_concentration,
                                         hg_fgd_effluent_concentration, se_fgd_effluent_concentration]
                Cl_flow_label = Label(tab5, text='Cl flow\n[g/m^3]', font=('Arial', 10, 'bold'), padx=50)
                Cl_flow_label.grid(row=3, column=3, rowspan=2)
                Label(tab5, text='Se flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=5, column=3, rowspan=2)
                Label(tab5, text='B flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=7, column=3, rowspan=2)
                Label(tab5, text='Br flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=9, column=3, rowspan=2)
                Label(tab5, text='Pb flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=11, column=3, rowspan=2)
                Label(tab5, text='As flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=13, column=3, rowspan=2)
                Label(tab5, text='Hg flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=15, column=3, rowspan=2)

            else:
                as_mbr, cl_mbr, pb_mbr, hg_mbr, se_mbr = mbr_modeling(WPCD_info['mbr'], basic_info['mc runs'])
                as_bt, cl_bt, pb_bt, hg_bt, se_bt = bt_modeling(WPCD_info['bt'], basic_info['mc runs'])
                as_iex, cl_iex, pb_iex, hg_iex, se_iex = iex_modeling(WPCD_info['iex'], basic_info['mc runs'])
                as_alox, cl_alox, pb_alox, hg_alox, se_alox = alox_modeling(WPCD_info['alox'], basic_info['mc runs'])
                as_feox, cl_feox, pb_feox, hg_feox, se_feox = feox_modeling(WPCD_info['feox'], basic_info['mc runs'])
                as_zvi, cl_zvi, pb_zvi, hg_zvi, se_zvi = zvi_modeling(WPCD_info['zvi'], basic_info['mc runs'])
                as_gac, cl_gac, pb_gac, hg_gac, se_gac = gac_modeling(WPCD_info['gac'], basic_info['mc runs'])

                as_mass_mbr, cl_mass_mbr, pb_mass_mbr, hg_mass_mbr, se_mass_mbr = wpcd_mass_partitioning(
                    basic_info['mc runs'], as_mass_cp[:, 1], as_mbr,
                    cl_mass_cp[:, 1], cl_mbr,
                    pb_mass_cp[:, 1], pb_mbr,
                    hg_mass_cp[:, 1], hg_mbr,
                    se_mass_cp[:, 1], se_mbr)

                as_mass_bt, cl_mass_bt, pb_mass_bt, hg_mass_bt, se_mass_bt = wpcd_mass_partitioning(
                    basic_info['mc runs'], as_mass_mbr[:, 1], as_bt,
                    cl_mass_mbr[:, 1], cl_bt,
                    pb_mass_mbr[:, 1], pb_bt,
                    hg_mass_mbr[:, 1], hg_bt,
                    se_mass_mbr[:, 1], se_bt)

                as_mass_iex, cl_mass_iex, pb_mass_iex, hg_mass_iex, se_mass_iex = wpcd_mass_partitioning(
                    basic_info['mc runs'],
                    as_mass_bt[:, 1],
                    as_iex,
                    cl_mass_bt[:, 1],
                    cl_iex,
                    pb_mass_bt[:, 1],
                    pb_iex,
                    hg_mass_bt[:, 1],
                    hg_iex,
                    se_mass_bt[:, 1],
                    se_iex)

                as_mass_alox, cl_mass_alox, pb_mass_alox, hg_mass_alox, se_mass_alox = wpcd_mass_partitioning(
                    basic_info['mc runs'],
                    as_mass_iex[:, 1], as_alox,
                    cl_mass_iex[:, 1], cl_alox,
                    pb_mass_iex[:, 1], pb_alox,
                    hg_mass_iex[:, 1], hg_alox,
                    se_mass_iex[:, 1], se_alox)

                as_mass_feox, cl_mass_feox, pb_mass_feox, hg_mass_feox, se_mass_feox = wpcd_mass_partitioning(
                    basic_info['mc runs'], as_mass_alox[:, 1], as_feox,
                    cl_mass_alox[:, 1], cl_feox,
                    pb_mass_alox[:, 1], pb_feox,
                    hg_mass_alox[:, 1], hg_feox,
                    se_mass_alox[:, 1], se_feox)

                as_mass_zvi, cl_mass_zvi, pb_mass_zvi, hg_mass_zvi, se_mass_zvi = wpcd_mass_partitioning(
                    basic_info['mc runs'],
                    as_mass_feox[:, 1],
                    as_zvi,
                    cl_mass_feox[:, 1],
                    cl_zvi,
                    pb_mass_feox[:, 1],
                    pb_zvi,
                    hg_mass_feox[:, 1],
                    hg_zvi,
                    se_mass_feox[:, 1],
                    se_zvi)

                as_mass_gac, cl_mass_gac, pb_mass_gac, hg_mass_gac, se_mass_gac = wpcd_mass_partitioning(
                    basic_info['mc runs'],
                    as_mass_zvi[:, 1],
                    as_gac,
                    cl_mass_zvi[:, 1],
                    cl_gac,
                    pb_mass_zvi[:, 1],
                    pb_gac,
                    hg_mass_zvi[:, 1],
                    hg_gac,
                    se_mass_zvi[:, 1],
                    se_gac)

                as_mvc, cl_mvc, pb_mvc, hg_mvc, se_mvc = mvc_modeling(WPCD_info['mvc'], basic_info['mc runs'])
                as_ro, cl_ro, pb_ro, hg_ro, se_ro = ro_modeling(WPCD_info['ro'], basic_info['mc runs'])
                as_crys, cl_crys, pb_crys, hg_crys, se_crys = crys_modeling(WPCD_info['crys'], basic_info['mc runs'])

                as_mass_mvc, cl_mass_mvc, pb_mass_mvc, hg_mass_mvc, se_mass_mvc = wpcd_mass_partitioning(
                    basic_info['mc runs'],
                    as_mass_cp[:, 1],
                    as_mvc,
                    cl_mass_cp[:, 1],
                    cl_mvc,
                    pb_mass_cp[:, 1],
                    pb_mvc,
                    hg_mass_cp[:, 1],
                    hg_mvc,
                    se_mass_cp[:, 1],
                    se_mvc)

                as_mass_ro, cl_mass_ro, pb_mass_ro, hg_mass_ro, se_mass_ro = wpcd_mass_partitioning(
                    basic_info['mc runs'],
                    as_mass_mvc[:, 1],
                    as_ro,
                    cl_mass_mvc[:, 1],
                    cl_ro,
                    pb_mass_mvc[:, 1],
                    pb_ro,
                    hg_mass_mvc[:, 1],
                    hg_ro,
                    se_mass_mvc[:, 1],
                    se_ro)

                as_mass_crys, cl_mass_crys, pb_mass_crys, hg_mass_crys, se_mass_crys = wpcd_mass_partitioning(
                    basic_info['mc runs'],
                    as_mass_ro[:,
                    1], as_crys,
                    cl_mass_ro[:,
                    1], cl_crys,
                    pb_mass_ro[:,
                    1], pb_crys,
                    hg_mass_ro[:,
                    1], hg_crys,
                    se_mass_ro[:,
                    1], se_crys)

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

                effluent_concentraion = [as_fgd_effluent_concentration, cl_fgd_effluent_concentration,
                                         pb_fgd_effluent_concentration,
                                         hg_fgd_effluent_concentration, se_fgd_effluent_concentration]
                Cl_flow_label = Label(tab5, text='Cl flow\n[g/m^3]', font=('Arial', 10, 'bold'), padx=50)
                Cl_flow_label.grid(row=3, column=3, rowspan=2)
                Label(tab5, text='Se flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=5, column=3, rowspan=2)
                Label(tab5, text='B flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=7, column=3, rowspan=2)
                Label(tab5, text='Br flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=9, column=3, rowspan=2)
                Label(tab5, text='Pb flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=11, column=3, rowspan=2)
                Label(tab5, text='As flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=13, column=3, rowspan=2)
                Label(tab5, text='Hg flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=15, column=3, rowspan=2)

            # Formulate the labels if the wet FGD exists
            Label(tab5, text='Influent', font=('Arial', 10, 'bold')).grid(row=0, column=1)
            Label(tab5, text='Effluent', font=('Arial', 10, 'bold')).grid(row=0, column=4)
            Label(tab5, text='Cl flow\n[g/m^3]', font=('Arial', 10, 'bold')).grid(row=3, column=0, rowspan=2)
            Label(tab5, text='Se flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=5, column=0, rowspan=2)
            Label(tab5, text='B flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=7, column=0, rowspan=2)
            Label(tab5, text='Br flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=9, column=0, rowspan=2)
            Label(tab5, text='Pb flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=11, column=0, rowspan=2)
            Label(tab5, text='As flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=13, column=0, rowspan=2)
            Label(tab5, text='Hg flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=15, column=0, rowspan=2)

            Label(tab5, text='Cl flow\n[g/m^3]', font=('Arial', 10, 'bold')).grid(row=3, column=3, rowspan=2)
            Label(tab5, text='Se flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=5, column=3, rowspan=2)
            Label(tab5, text='B flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=7, column=3, rowspan=2)
            Label(tab5, text='Br flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=9, column=3, rowspan=2)
            Label(tab5, text='Pb flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=11, column=3, rowspan=2)
            Label(tab5, text='As flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=13, column=3, rowspan=2)
            Label(tab5, text='Hg flow\n[\u03bcg/m^3]', font=('Arial', 10, 'bold')).grid(row=15, column=3, rowspan=2)
            # Label(tab5, text='S mass [g/m^3]', font=('Arial', 10, 'bold')).grid(row=17, column=0, rowspan=2)

            try:
                for i in range(len(influent_concentration)):
                    if i != 0:
                        med_flow_label = Label(tab5, text=round_sig(np.median(influent_concentration[i])*1E6), font=('Arial', 10))
                        med_flow_label.grid(row=i * 2 + 3, column=1)
                        perc_flow_label = Label(tab5, text=str(round_sig(np.percentile(influent_concentration[i], 25)*1E6)) + ' - '
                                         + str(round_sig(np.percentile(influent_concentration[i], 75)*1E6)), font=('Arial', 10))
                        perc_flow_label.grid(row=i * 2 + 4, column=1)
                    else:
                        med_flow_label = Label(tab5, text=round_sig(np.median(influent_concentration[i])),
                                               font=('Arial', 10))
                        med_flow_label.grid(row=i * 2 + 3, column=1)
                        perc_flow_label = Label(tab5, text=str(round_sig(np.percentile(influent_concentration[i], 25))) + ' - '
                                                + str(round_sig(np.percentile(influent_concentration[i], 75))), font=('Arial', 10))
                        perc_flow_label.grid(row=i * 2 + 4, column=1)

                    label_lst += [med_flow_label, perc_flow_label]
            except NameError:
                pass

            # As, Cl, Pb, Hg, Se
            as_eff_label = Label(tab5, text=round_sig(np.median(as_fgd_effluent_concentration)*1E6), font=('Arial', 10))
            as_eff_label.grid(row=13, column=4)
            cl_eff_label = Label(tab5, text=round_sig(np.median(cl_fgd_effluent_concentration)), font=('Arial', 10))
            cl_eff_label.grid(row=3, column=4)
            pb_eff_label = Label(tab5, text=round_sig(np.median(pb_fgd_effluent_concentration)*1E6), font=('Arial', 10))
            pb_eff_label.grid(row=11, column=4)
            hg_eff_label = Label(tab5, text=round_sig(np.median(hg_fgd_effluent_concentration)*1E6), font=('Arial', 10))
            hg_eff_label.grid(row=15, column=4)
            se_eff_label = Label(tab5, text=round_sig(np.median(se_fgd_effluent_concentration)*1E6), font=('Arial', 10))
            se_eff_label.grid(row=5, column=4)
            as_eff_range_label = Label(tab5, text=str(round_sig(np.percentile(as_fgd_effluent_concentration, 25)*1E6)) + '-' +
                             str(round_sig(np.percentile(as_fgd_effluent_concentration, 75)*1E6)), font=('Arial', 10))
            as_eff_range_label.grid(row=14, column=4)
            cl_eff_range_label = Label(tab5, text=str(round_sig(np.percentile(cl_fgd_effluent_concentration, 25))) + '-' +
                             str(round_sig(np.percentile(cl_fgd_effluent_concentration, 75))), font=('Arial', 10))
            cl_eff_range_label.grid(row=4, column=4)
            pb_eff_range_label = Label(tab5, text=str(round_sig(np.percentile(pb_fgd_effluent_concentration, 25)*1E6)) + '-' +
                             str(round_sig(np.percentile(pb_fgd_effluent_concentration, 75)*1E6)), font=('Arial', 10))
            pb_eff_range_label.grid(row=12, column=4)
            hg_eff_range_label = Label(tab5, text=str(round_sig(np.percentile(hg_fgd_effluent_concentration, 25)*1E6)) + '-' +
                             str(round_sig(np.percentile(hg_fgd_effluent_concentration, 75)*1E6)), font=('Arial', 10))
            hg_eff_range_label.grid(row=16, column=4)
            se_eff_range_label = Label(tab5, text=str(round_sig(np.percentile(se_fgd_effluent_concentration, 25)*1E6)) + '-' +
                             str(round_sig(np.percentile(se_fgd_effluent_concentration, 75)*1E6)), font=('Arial', 10))
            se_eff_range_label.grid(row=6, column=4)
            label_lst += [as_eff_label, cl_eff_label, pb_eff_label, hg_eff_label, se_eff_label, as_eff_range_label,
                          cl_eff_range_label, pb_eff_range_label, hg_eff_range_label, se_eff_range_label]

            Cl_inf_ecdf_button.config(state=NORMAL)
            Se_inf_ecdf_button.config(state=NORMAL)
            B_inf_ecdf_button.config(state=NORMAL)
            Br_inf_ecdf_button.config(state=NORMAL)
            Pb_inf_ecdf_button.config(state=NORMAL)
            As_inf_ecdf_button.config(state=NORMAL)
            Hg_inf_ecdf_button.config(state=NORMAL)

            Cl_eff_ecdf_button.config(state=NORMAL)
            Se_eff_ecdf_button.config(state=NORMAL)
            As_eff_ecdf_button.config(state=NORMAL)
            Hg_eff_ecdf_button.config(state=NORMAL)

            As_distplot_button.config(state=NORMAL)
            Se_distplot_button.config(state=NORMAL)
            Hg_distplot_button.config(state=NORMAL)

            wastewater_ecdf_button.config(state=NORMAL)
            electricity_consumption_button.config(state=NORMAL)
            electricity_cost_button.config(state=NORMAL)
            chemical_consumption_button.config(state=NORMAL)
            FGD_boxplot_button.config(state=NORMAL)

            # Config all the related buttons to be working

            if type(Se_wetFGD_ww) != 0:
                # calculate the Se speciation in wetFGD waste water
                Se_speciation_button.config(state=NORMAL)


        else:
            wastewater_production = 0
            notification_label = Label(tab5, text='', font=('Arial', 10))
            # notification_label.config(state=DISABLED)
            notification_label.grid(row=0, column=0)
            notification_label.config(text='Please select wet FGD for WPCD results.')
            label_lst += [notification_label]

    def open_input():
        '''This file will open the input values from the previously written results'''

        input_file_name = filedialog.askopenfilename()
        basic_info = pd.read_excel(input_file_name, usecols='B')
        ct, el, mc = np.array(basic_info).reshape(3,)
        apcd_info = pd.read_excel(input_file_name, usecols='E')
        csesp, hsesp, ff, scr, aci, dsi, dryfgd, wetfgd, rt, ox, pa = np.array(apcd_info).reshape(11,)
        wpcd_info = pd.read_excel(input_file_name, usecols='H')
        cp, cs, bt, mbr, zvi, alox, feox, iex, gac, mvc, ro, crys = np.array(wpcd_info).reshape(12,)
        coal_type.set(ct)
        power_input.insert(0, el)
        runs_input.insert(0, int(mc))
        csESP_input.set(csesp)
        hsESP_input.set(hsesp)
        FF_input.set(ff)
        SCR_input.set(scr)
        ACI_input.set(aci)
        DSI_input.set(dsi)
        dryFGD_input.set(dryfgd)
        wetFGD_input.set(wetfgd)
        reagent_type.set(rt)
        oxstate_type.set(ox)
        pa_type.set(pa)
        cp_input.set(cp)
        comp_standard.set(cs)
        bt_input.set(bt)
        mbr_input.set(mbr)
        zvi_input.set(zvi)
        alox_input.set(alox)
        feox_input.set(feox)
        iex_input.set(iex)
        gac_input.set(gac)
        mvc_input.set(mvc)
        ro_input.set(ro)
        crys_input.set(crys)

    filemenu = Menu(menu)
    savemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New", command=menu_option_selected)
    filemenu.add_cascade(label="Save Options", menu=savemenu, command=menu_option_selected)
    savemenu.add_cascade(label="Save All", command=save_all)
    savemenu.add_cascade(label="Save Inputs", command=save_inputs)
    savemenu.add_cascade(label="Save APCD Results", command=save_air_file)
    savemenu.add_cascade(label="Save WPCD Results", command=save_ww_file)
    filemenu.add_command(label="Open", command=combine_funcs(menu_option_selected, open_input))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About", command=menu_option_selected)
    analysismenu = Menu(menu)
    menu.add_cascade(label='Analysis', menu=analysismenu)
    analysismenu.add_command(label='Calculate',
                             command=combine_funcs(check_input, check_input_apcd, check_MC_runs, calculate_input))


    root.mainloop()


if __name__ == '__main__':
    main()
