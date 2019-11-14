def as_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import as_dict
    import numpy as np

    arsenic_input = power_plant_inputs.Share_Arsenic
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    #Boiler Partitioning
    bottom_ash_solid = arsenic_input * np.mean(as_dict['Bottom_Ash']['solid'])
    bottom_ash_liquid = arsenic_input * np.mean(as_dict['Bottom_Ash']['liquid'])
    bottom_ash_gas = arsenic_input * np.mean(as_dict['Bottom_Ash']['gas'])

    #SCR Partitioning
    scr_solid = bottom_ash_gas * np.mean(as_dict[nox_control]['solid'])
    scr_liquid = bottom_ash_gas * np.mean(as_dict[nox_control]['liquid'])
    scr_gas = bottom_ash_gas * np.mean(as_dict[nox_control]['gas'])

    #ACI Partitioning
    aci_solid = scr_gas * np.mean(as_dict[hg_control]['solid'])
    aci_liquid = scr_gas * np.mean(as_dict[hg_control]['liquid'])
    aci_gas = scr_gas * np.mean(as_dict[hg_control]['gas'])

    #DSI Partitioning
    dsi_solid = aci_gas * np.mean(as_dict[sorbent]['solid'])
    dsi_liquid = aci_gas * np.mean(as_dict[sorbent]['liquid'])
    dsi_gas = aci_gas * np.mean(as_dict[sorbent]['gas'])

    #Partitioning in PM Control Systems
    pm_solid = dsi_gas * np.mean(as_dict[pm_control]['solid'])
    pm_liquid = dsi_gas * np.mean(as_dict[pm_control]['liquid'])
    pm_gas = dsi_gas * np.mean(as_dict[pm_control]['gas'])

    #Partitioning in SO2 Control Systems
    so2_solid = pm_gas * np.mean(as_dict[so2_control]['solid'])
    so2_liquid = pm_gas * np.mean(as_dict[so2_control]['liquid'])
    so2_gas = pm_gas * np.mean(as_dict[so2_control]['gas'])

    #Calucalate total partitioning
    as_solid = bottom_ash_solid + scr_solid + aci_solid + pm_solid + dsi_solid + so2_solid
    as_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + pm_liquid + dsi_liquid + so2_liquid
    as_gas = so2_gas

    return as_solid, as_liquid, as_gas

def cl_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import cl_dict
    import numpy as np

    chlorine_input = power_plant_inputs.Share_Chloride
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    #Boiler Partitioning
    bottom_ash_solid = chlorine_input * np.mean(cl_dict['Bottom_Ash']['solid'])
    bottom_ash_liquid = chlorine_input * np.mean(cl_dict['Bottom_Ash']['liquid'])
    bottom_ash_gas = chlorine_input * np.mean(cl_dict['Bottom_Ash']['gas'])

    #SCR Partitioning
    scr_solid = bottom_ash_gas * np.mean(cl_dict[nox_control]['solid'])
    scr_liquid = bottom_ash_gas * np.mean(cl_dict[nox_control]['liquid'])
    scr_gas = bottom_ash_gas * np.mean(cl_dict[nox_control]['gas'])

    #ACI Partitioning
    aci_solid = scr_gas * np.mean(cl_dict[hg_control]['solid'])
    aci_liquid = scr_gas * np.mean(cl_dict[hg_control]['liquid'])
    aci_gas = scr_gas * np.mean(cl_dict[hg_control]['gas'])

    #DSI Partitioning
    dsi_solid = aci_gas * np.mean(cl_dict[sorbent]['solid'])
    dsi_liquid = aci_gas * np.mean(cl_dict[sorbent]['liquid'])
    dsi_gas = aci_gas * np.mean(cl_dict[sorbent]['gas'])

    #Partitioning in PM Control Systems
    pm_solid = dsi_gas * np.mean(cl_dict[pm_control]['solid'])
    pm_liquid = dsi_gas * np.mean(cl_dict[pm_control]['liquid'])
    pm_gas = dsi_gas * np.mean(cl_dict[pm_control]['gas'])

    #Partitioning in SO2 Control Systems
    so2_solid = pm_gas * np.mean(cl_dict[so2_control]['solid'])
    so2_liquid = pm_gas * np.mean(cl_dict[so2_control]['liquid'])
    so2_gas = pm_gas * np.mean(cl_dict[so2_control]['gas'])

    #Calucalate total partitioning
    cl_solid = bottom_ash_solid + scr_solid + aci_solid + dsi_solid + pm_solid + so2_solid
    cl_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + dsi_liquid + pm_liquid + so2_liquid
    cl_gas = so2_gas

    return cl_solid, cl_liquid, cl_gas

def se_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import se_dict
    import numpy as np

    selenium_input = power_plant_inputs.Share_Selenium
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    #Boiler Partitioning
    bottom_ash_solid = selenium_input * np.mean(se_dict['Bottom_Ash']['solid'])
    bottom_ash_liquid = selenium_input * np.mean(se_dict['Bottom_Ash']['liquid'])
    bottom_ash_gas = selenium_input * np.mean(se_dict['Bottom_Ash']['gas'])

    #SCR Partitioning
    scr_solid = bottom_ash_gas * np.mean(se_dict[nox_control]['solid'])
    scr_liquid = bottom_ash_gas * np.mean(se_dict[nox_control]['liquid'])
    scr_gas = bottom_ash_gas * np.mean(se_dict[nox_control]['gas'])

    #ACI Partitioning
    aci_solid = scr_gas * np.mean(se_dict[hg_control]['solid'])
    aci_liquid = scr_gas * np.mean(se_dict[hg_control]['liquid'])
    aci_gas = scr_gas * np.mean(se_dict[hg_control]['gas'])

    #DSI Partitioning
    dsi_solid = aci_gas * np.mean(se_dict[sorbent]['solid'])
    dsi_liquid = aci_gas * np.mean(se_dict[sorbent]['liquid'])
    dsi_gas = aci_gas * np.mean(se_dict[sorbent]['gas'])

    #Partitioning in PM Control Systems
    pm_solid = dsi_gas * np.mean(se_dict[pm_control]['solid'])
    pm_liquid = dsi_gas * np.mean(se_dict[pm_control]['liquid'])
    pm_gas = dsi_gas * np.mean(se_dict[pm_control]['gas'])

    #Partitioning in SO2 Control Systems
    so2_solid = pm_gas * np.mean(se_dict[so2_control]['solid'])
    so2_liquid = pm_gas * np.mean(se_dict[so2_control]['liquid'])
    so2_gas = pm_gas * np.mean(se_dict[so2_control]['gas'])

    #Calucalate total partitioning
    se_solid = bottom_ash_solid + scr_solid + aci_solid + dsi_solid + pm_solid + so2_solid
    se_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + dsi_liquid + pm_liquid + so2_liquid
    se_gas = so2_gas

    return se_solid, se_liquid, se_gas

def hg_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import hg_dict
    import numpy as np

    mercury_input = power_plant_inputs.Share_Mercury
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    #Boiler Partitioning
    bottom_ash_solid = mercury_input * np.mean(hg_dict['Bottom_Ash']['solid'])
    bottom_ash_liquid = mercury_input * np.mean(hg_dict['Bottom_Ash']['liquid'])
    bottom_ash_gas = mercury_input * np.mean(hg_dict['Bottom_Ash']['gas'])

    #SCR Partitioning
    scr_solid = bottom_ash_gas * np.mean(hg_dict[nox_control]['solid'])
    scr_liquid = bottom_ash_gas * np.mean(hg_dict[nox_control]['liquid'])
    scr_gas = bottom_ash_gas * np.mean(hg_dict[nox_control]['gas'])

    #ACI Partitioning
    aci_solid = scr_gas * np.mean(hg_dict[hg_control]['solid'])
    aci_liquid = scr_gas * np.mean(hg_dict[hg_control]['liquid'])
    aci_gas = scr_gas * np.mean(hg_dict[hg_control]['gas'])

    #DSI Partitioning
    dsi_solid = aci_gas * np.mean(hg_dict[sorbent]['solid'])
    dsi_liquid = aci_gas * np.mean(hg_dict[sorbent]['liquid'])
    dsi_gas = aci_gas * np.mean(hg_dict[sorbent]['gas'])

    #Partitioning in PM Control Systems
    pm_solid = dsi_gas * np.mean(hg_dict[pm_control]['solid'])
    pm_liquid = dsi_gas * np.mean(hg_dict[pm_control]['liquid'])
    pm_gas = dsi_gas * np.mean(hg_dict[pm_control]['gas'])

    #Partitioning in SO2 Control Systems
    so2_solid = pm_gas * np.mean(hg_dict[so2_control]['solid'])
    so2_liquid = pm_gas * np.mean(hg_dict[so2_control]['liquid'])
    so2_gas = pm_gas * np.mean(hg_dict[so2_control]['gas'])

    #Calucalate total partitioning
    hg_solid = bottom_ash_solid + scr_solid + aci_solid +  dsi_solid + pm_solid + so2_solid
    hg_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + dsi_liquid +  pm_liquid + so2_liquid
    hg_gas = so2_gas

    return hg_solid, hg_liquid, hg_gas

def br_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import br_dict
    import numpy as np

    bromine_input = power_plant_inputs.Share_Bromide
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    #Boiler Partitioning
    bottom_ash_solid = bromine_input * np.mean(br_dict['Bottom_Ash']['solid'])
    bottom_ash_liquid = bromine_input * np.mean(br_dict['Bottom_Ash']['liquid'])
    bottom_ash_gas = bromine_input * np.mean(br_dict['Bottom_Ash']['gas'])

    #SCR Partitioning
    scr_solid = bottom_ash_gas * np.mean(br_dict[nox_control]['solid'])
    scr_liquid = bottom_ash_gas * np.mean(br_dict[nox_control]['liquid'])
    scr_gas = bottom_ash_gas * np.mean(br_dict[nox_control]['gas'])

    #ACI Partitioning
    aci_solid = scr_gas * np.mean(br_dict[hg_control]['solid'])
    aci_liquid = scr_gas * np.mean(br_dict[hg_control]['liquid'])
    aci_gas = scr_gas * np.mean(br_dict[hg_control]['gas'])

    #DSI Partitioning
    dsi_solid = aci_gas * np.mean(br_dict[sorbent]['solid'])
    dsi_liquid = aci_gas * np.mean(br_dict[sorbent]['liquid'])
    dsi_gas = aci_gas * np.mean(br_dict[sorbent]['gas'])

    #Partitioning in PM Control Systems
    pm_solid = dsi_gas * np.mean(br_dict[pm_control]['solid'])
    pm_liquid = dsi_gas * np.mean(br_dict[pm_control]['liquid'])
    pm_gas = dsi_gas * np.mean(br_dict[pm_control]['gas'])

    #Partitioning in SO2 Control Systems
    so2_solid = pm_gas * np.mean(br_dict[so2_control]['solid'])
    so2_liquid = pm_gas * np.mean(br_dict[so2_control]['liquid'])
    so2_gas = pm_gas * np.mean(br_dict[so2_control]['gas'])

    #Calucalate total partitioning
    br_solid = bottom_ash_solid + scr_solid + aci_solid + dsi_solid + pm_solid + so2_solid
    br_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + +dsi_liquid + pm_liquid + so2_liquid
    br_gas = so2_gas

    return br_solid, br_liquid, br_gas

def b_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import b_dict
    import numpy as np

    boron_input = power_plant_inputs.Share_Boron
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    #Boiler Partitioning
    bottom_ash_solid = boron_input * np.mean(b_dict['Bottom_Ash']['solid'])
    bottom_ash_liquid = boron_input * np.mean(b_dict['Bottom_Ash']['liquid'])
    bottom_ash_gas = boron_input * np.mean(b_dict['Bottom_Ash']['gas'])

    #SCR Partitioning
    scr_solid = bottom_ash_gas * np.mean(b_dict[nox_control]['solid'])
    scr_liquid = bottom_ash_gas * np.mean(b_dict[nox_control]['liquid'])
    scr_gas = bottom_ash_gas * np.mean(b_dict[nox_control]['gas'])

    #ACI Partitioning
    aci_solid = scr_gas * np.mean(b_dict[hg_control]['solid'])
    aci_liquid = scr_gas * np.mean(b_dict[hg_control]['liquid'])
    aci_gas = scr_gas * np.mean(b_dict[hg_control]['gas'])

    #DSI Partitioning
    dsi_solid = aci_gas * np.mean(b_dict[sorbent]['solid'])
    dsi_liquid = aci_gas * np.mean(b_dict[sorbent]['liquid'])
    dsi_gas = aci_gas * np.mean(b_dict[sorbent]['gas'])

    #Partitioning in PM Control Systems
    pm_solid = dsi_gas * np.mean(b_dict[pm_control]['solid'])
    pm_liquid = dsi_gas * np.mean(b_dict[pm_control]['liquid'])
    pm_gas = dsi_gas * np.mean(b_dict[pm_control]['gas'])

    #Partitioning in SO2 Control Systems
    so2_solid = pm_gas * np.mean(b_dict[so2_control]['solid'])
    so2_liquid = pm_gas * np.mean(b_dict[so2_control]['liquid'])
    so2_gas = pm_gas * np.mean(b_dict[so2_control]['gas'])

    #Calucalate total partitioning
    b_solid = bottom_ash_solid + scr_solid + aci_solid + dsi_solid + pm_solid + so2_solid
    b_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + dsi_liquid + pm_liquid + so2_liquid
    b_gas = so2_gas

    return b_solid, b_liquid, b_gas

def pb_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import pb_dict
    import numpy as np

    lead_input = power_plant_inputs.Share_Lead
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    #Boiler Partitioning
    bottom_ash_solid = lead_input * np.mean(pb_dict['Bottom_Ash']['solid'])
    bottom_ash_liquid = lead_input * np.mean(pb_dict['Bottom_Ash']['liquid'])
    bottom_ash_gas = lead_input * np.mean(pb_dict['Bottom_Ash']['gas'])

    #SCR Partitioning
    scr_solid = bottom_ash_gas * np.mean(pb_dict[nox_control]['solid'])
    scr_liquid = bottom_ash_gas * np.mean(pb_dict[nox_control]['liquid'])
    scr_gas = bottom_ash_gas * np.mean(pb_dict[nox_control]['gas'])

    #ACI Partitioning
    aci_solid = scr_gas * np.mean(pb_dict[hg_control]['solid'])
    aci_liquid = scr_gas * np.mean(pb_dict[hg_control]['liquid'])
    aci_gas = scr_gas * np.mean(pb_dict[hg_control]['gas'])

    #DSI Partitioning
    dsi_solid = aci_gas * np.mean(pb_dict[sorbent]['solid'])
    dsi_liquid = aci_gas * np.mean(pb_dict[sorbent]['liquid'])
    dsi_gas = aci_gas * np.mean(pb_dict[sorbent]['gas'])

    #Partitioning in PM Control Systems
    pm_solid = dsi_gas * np.mean(pb_dict[pm_control]['solid'])
    pm_liquid = dsi_gas * np.mean(pb_dict[pm_control]['liquid'])
    pm_gas = dsi_gas * np.mean(pb_dict[pm_control]['gas'])

    #Partitioning in SO2 Control Systems
    so2_solid = pm_gas * np.mean(pb_dict[so2_control]['solid'])
    so2_liquid = pm_gas * np.mean(pb_dict[so2_control]['liquid'])
    so2_gas = pm_gas * np.mean(pb_dict[so2_control]['gas'])

    #Calucalate total partitioning
    pb_solid = bottom_ash_solid + scr_solid + aci_solid + dsi_solid + pm_solid + so2_solid
    pb_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + dsi_liquid + pm_liquid + so2_liquid
    pb_gas = so2_gas

    return pb_solid, pb_liquid, pb_gas

def s_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import s_dict
    import numpy as np

    sulfur_input = power_plant_inputs.Share_Sulfur
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    #Boiler Partitioning
    bottom_ash_solid = sulfur_input * np.mean(s_dict['Bottom_Ash']['solid'])
    bottom_ash_liquid = sulfur_input * np.mean(s_dict['Bottom_Ash']['liquid'])
    bottom_ash_gas = sulfur_input * np.mean(s_dict['Bottom_Ash']['gas'])

    #SCR Partitioning
    scr_solid = bottom_ash_gas * np.mean(s_dict[nox_control]['solid'])
    scr_liquid = bottom_ash_gas * np.mean(s_dict[nox_control]['liquid'])
    scr_gas = bottom_ash_gas * np.mean(s_dict[nox_control]['gas'])

    #ACI Partitioning
    aci_solid = scr_gas * np.mean(s_dict[hg_control]['solid'])
    aci_liquid = scr_gas * np.mean(s_dict[hg_control]['liquid'])
    aci_gas = scr_gas * np.mean(s_dict[hg_control]['gas'])

    #DSI Partitioning
    dsi_solid = aci_gas * np.mean(s_dict[sorbent]['solid'])
    dsi_liquid = aci_gas * np.mean(s_dict[sorbent]['liquid'])
    dsi_gas = aci_gas * np.mean(s_dict[sorbent]['gas'])

    #Partitioning in PM Control Systems
    pm_solid = dsi_gas * np.mean(s_dict[pm_control]['solid'])
    pm_liquid = dsi_gas * np.mean(s_dict[pm_control]['liquid'])
    pm_gas = dsi_gas * np.mean(s_dict[pm_control]['gas'])

    #Partitioning in SO2 Control Systems
    so2_solid = pm_gas * np.mean(s_dict[so2_control]['solid'])
    so2_liquid = pm_gas * np.mean(s_dict[so2_control]['liquid'])
    so2_gas = pm_gas * np.mean(s_dict[so2_control]['gas'])

    #Calucalate total partitioning
    s_solid = bottom_ash_solid + scr_solid + aci_solid + dsi_solid + pm_solid + so2_solid
    s_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + dsi_liquid + pm_liquid + so2_liquid
    s_gas = so2_gas

    return s_solid, s_liquid, s_gas
