def as_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import as_dict
    import numpy as np
    import pandas as pd

    arsenic_input = power_plant_inputs.Arsenic_Inputs
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    # Boiler Partitioning
    bottom_ash_solid = np.multiply(arsenic_input, np.mean(as_dict['Bottom_Ash']['solid']))
    bottom_ash_liquid = np.multiply(arsenic_input, np.mean(as_dict['Bottom_Ash']['liquid']))
    bottom_ash_gas = np.multiply(arsenic_input, np.mean(as_dict['Bottom_Ash']['gas']))

    # SCR Partitioning
    scr_solid = np.multiply(bottom_ash_gas, np.mean(as_dict[nox_control]['solid']))
    scr_liquid = np.multiply(bottom_ash_gas, np.mean(as_dict[nox_control]['liquid']))
    scr_gas = np.multiply(bottom_ash_gas,  np.mean(as_dict[nox_control]['gas']))

    # ACI Partitioning
    aci_solid = np.multiply(scr_gas, np.mean(as_dict[hg_control]['solid']))
    aci_liquid = np.multiply(scr_gas, np.mean(as_dict[hg_control]['liquid']))
    aci_gas = np.multiply(scr_gas, np.mean(as_dict[hg_control]['gas']))

    # DSI Partitioning
    dsi_solid = np.multiply(aci_gas, np.mean(as_dict[sorbent]['solid']))
    dsi_liquid = np.multiply(aci_gas, np.mean(as_dict[sorbent]['liquid']))
    dsi_gas = np.multiply(aci_gas, np.mean(as_dict[sorbent]['gas']))

    # Partitioning in PM Control Systems
    pm_solid = np.multiply(dsi_gas, np.mean(as_dict[pm_control]['solid']))
    pm_liquid = np.multiply(dsi_gas, np.mean(as_dict[pm_control]['liquid']))
    pm_gas = np.multiply(dsi_gas, np.mean(as_dict[pm_control]['gas']))

    # Partitioning in SO2 Control Systems
    so2_solid = np.multiply(pm_gas, np.mean(as_dict[so2_control]['solid']))
    so2_liquid = np.multiply(pm_gas, np.mean(as_dict[so2_control]['liquid']))
    so2_gas = np.multiply(pm_gas, np.mean(as_dict[so2_control]['gas']))

    # Calculate total partitioning
    as_solid = bottom_ash_solid + scr_solid + aci_solid + dsi_solid + pm_solid + so2_solid
    as_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + dsi_liquid + pm_liquid + so2_liquid
    as_gas = so2_gas

    as_solid = pd.Series(as_solid)
    as_liquid = pd.Series(as_liquid)
    as_gas = pd.Series(as_gas)

    as_solid = as_solid.values
    as_liquid = as_liquid.values
    as_gas = as_gas.values

    return as_solid, as_liquid, as_gas


def cl_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import cl_dict
    import numpy as np
    import pandas as pd

    chlorine_input = power_plant_inputs.Chloride_Inputs
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    # Boiler Partitioning
    bottom_ash_solid = np.multiply(chlorine_input, np.mean(cl_dict['Bottom_Ash']['solid']))
    bottom_ash_liquid = np.multiply(chlorine_input, np.mean(cl_dict['Bottom_Ash']['liquid']))
    bottom_ash_gas = np.multiply(chlorine_input, np.mean(cl_dict['Bottom_Ash']['gas']))

    # SCR Partitioning
    scr_solid = np.multiply(bottom_ash_gas, np.mean(cl_dict[nox_control]['solid']))
    scr_liquid = np.multiply(bottom_ash_gas, np.mean(cl_dict[nox_control]['liquid']))
    scr_gas = np.multiply(bottom_ash_gas, np.mean(cl_dict[nox_control]['gas']))

    # ACI Partitioning
    aci_solid = np.multiply(scr_gas, np.mean(cl_dict[hg_control]['solid']))
    aci_liquid = np.multiply(scr_gas, np.mean(cl_dict[hg_control]['liquid']))
    aci_gas = np.multiply(scr_gas, np.mean(cl_dict[hg_control]['gas']))

    # DSI Partitioning
    dsi_solid = np.multiply(aci_gas, np.mean(cl_dict[sorbent]['solid']))
    dsi_liquid = np.multiply(aci_gas, np.mean(cl_dict[sorbent]['liquid']))
    dsi_gas = np.multiply(aci_gas, np.mean(cl_dict[sorbent]['gas']))

    # Partitioning in PM Control Systems
    pm_solid = np.multiply(dsi_gas, np.mean(cl_dict[pm_control]['solid']))
    pm_liquid = np.multiply(dsi_gas, np.mean(cl_dict[pm_control]['liquid']))
    pm_gas = np.multiply(dsi_gas, np.mean(cl_dict[pm_control]['gas']))

    # Partitioning in SO2 Control Systems
    so2_solid = np.multiply(pm_gas, np.mean(cl_dict[so2_control]['solid']))
    so2_liquid = np.multiply(pm_gas, np.mean(cl_dict[so2_control]['liquid']))
    so2_gas = np.multiply(pm_gas, np.mean(cl_dict[so2_control]['gas']))

    # Calculate total partitioning
    cl_solid = bottom_ash_solid + scr_solid + aci_solid + dsi_solid + pm_solid + so2_solid
    cl_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + dsi_liquid + pm_liquid + so2_liquid
    cl_gas = so2_gas

    cl_solid = pd.Series(cl_solid)
    cl_liquid = pd.Series(cl_liquid)
    cl_gas = pd.Series(cl_gas)

    cl_solid = cl_solid.values
    cl_liquid = cl_liquid.values
    cl_gas = cl_gas.values

    return cl_solid, cl_liquid, cl_gas


def se_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import se_dict
    import numpy as np
    import pandas as pd

    selenium_input = power_plant_inputs.Selenium_Inputs
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    # Boiler Partitioning
    bottom_ash_solid = np.multiply(selenium_input, np.mean(se_dict['Bottom_Ash']['solid']))
    bottom_ash_liquid = np.multiply(selenium_input, np.mean(se_dict['Bottom_Ash']['liquid']))
    bottom_ash_gas = np.multiply(selenium_input, np.mean(se_dict['Bottom_Ash']['gas']))

    # SCR Partitioning
    scr_solid = np.multiply(bottom_ash_gas, np.mean(se_dict[nox_control]['solid']))
    scr_liquid = np.multiply(bottom_ash_gas, np.mean(se_dict[nox_control]['liquid']))
    scr_gas = np.multiply(bottom_ash_gas, np.mean(se_dict[nox_control]['gas']))

    # ACI Partitioning
    aci_solid = np.multiply(scr_gas, np.mean(se_dict[hg_control]['solid']))
    aci_liquid = np.multiply(scr_gas, np.mean(se_dict[hg_control]['liquid']))
    aci_gas = np.multiply(scr_gas, np.mean(se_dict[hg_control]['gas']))

    # DSI Partitioning
    dsi_solid = np.multiply(aci_gas, np.mean(se_dict[sorbent]['solid']))
    dsi_liquid = np.multiply(aci_gas, np.mean(se_dict[sorbent]['liquid']))
    dsi_gas = np.multiply(aci_gas, np.mean(se_dict[sorbent]['gas']))

    # Partitioning in PM Control Systems
    pm_solid = np.multiply(dsi_gas, np.mean(se_dict[pm_control]['solid']))
    pm_liquid = np.multiply(dsi_gas, np.mean(se_dict[pm_control]['liquid']))
    pm_gas = np.multiply(dsi_gas, np.mean(se_dict[pm_control]['gas']))

    # Partitioning in SO2 Control Systems
    so2_solid = np.multiply(pm_gas, np.mean(se_dict[so2_control]['solid']))
    so2_liquid = np.multiply(pm_gas, np.mean(se_dict[so2_control]['liquid']))
    so2_gas = np.multiply(pm_gas, np.mean(se_dict[so2_control]['gas']))

    # Calculate total partitioning
    se_solid = bottom_ash_solid + scr_solid + aci_solid + dsi_solid + pm_solid + so2_solid
    se_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + dsi_liquid + pm_liquid + so2_liquid
    se_gas = so2_gas

    se_solid = pd.Series(se_solid)
    se_liquid = pd.Series(se_liquid)
    se_gas = pd.Series(se_gas)

    se_solid = se_solid.values
    se_liquid = se_liquid.values
    se_gas = se_gas.values

    return se_solid, se_liquid, se_gas


def hg_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import hg_dict
    import numpy as np
    import pandas as pd

    mercury_input = power_plant_inputs.Mercury_Inputs
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    # Boiler Partitioning
    bottom_ash_solid = np.multiply(mercury_input, np.mean(hg_dict['Bottom_Ash']['solid']))
    bottom_ash_liquid = np.multiply(mercury_input, np.mean(hg_dict['Bottom_Ash']['liquid']))
    bottom_ash_gas = np.multiply(mercury_input, np.mean(hg_dict['Bottom_Ash']['gas']))

    # SCR Partitioning
    scr_solid = np.multiply(bottom_ash_gas, np.mean(hg_dict[nox_control]['solid']))
    scr_liquid = np.multiply(bottom_ash_gas, np.mean(hg_dict[nox_control]['liquid']))
    scr_gas = np.multiply(bottom_ash_gas, np.mean(hg_dict[nox_control]['gas']))

    # ACI Partitioning
    aci_solid = np.multiply(scr_gas, np.mean(hg_dict[hg_control]['solid']))
    aci_liquid = np.multiply(scr_gas, np.mean(hg_dict[hg_control]['liquid']))
    aci_gas = np.multiply(scr_gas, np.mean(hg_dict[hg_control]['gas']))

    # DSI Partitioning
    dsi_solid = np.multiply(aci_gas, np.mean(hg_dict[sorbent]['solid']))
    dsi_liquid = np.multiply(aci_gas, np.mean(hg_dict[sorbent]['liquid']))
    dsi_gas = np.multiply(aci_gas, np.mean(hg_dict[sorbent]['gas']))

    # Partitioning in PM Control Systems
    pm_solid = np.multiply(dsi_gas, np.mean(hg_dict[pm_control]['solid']))
    pm_liquid = np.multiply(dsi_gas, np.mean(hg_dict[pm_control]['liquid']))
    pm_gas = np.multiply(dsi_gas, np.mean(hg_dict[pm_control]['gas']))

    # Partitioning in SO2 Control Systems
    so2_solid = np.multiply(pm_gas, np.mean(hg_dict[so2_control]['solid']))
    so2_liquid = np.multiply(pm_gas, np.mean(hg_dict[so2_control]['liquid']))
    so2_gas = np.multiply(pm_gas, np.mean(hg_dict[so2_control]['gas']))

    # Calculate total partitioning
    hg_solid = bottom_ash_solid + scr_solid + aci_solid + dsi_solid + pm_solid + so2_solid
    hg_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + dsi_liquid + pm_liquid + so2_liquid
    hg_gas = so2_gas

    hg_solid = pd.Series(hg_solid)
    hg_liquid = pd.Series(hg_liquid)
    hg_gas = pd.Series(hg_gas)

    hg_solid = hg_solid.values
    hg_liquid = hg_liquid.values
    hg_gas = hg_gas.values

    return hg_solid, hg_liquid, hg_gas


def br_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import br_dict
    import numpy as np
    import pandas as pd

    bromine_input = power_plant_inputs.Bromide_Inputs
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    # Boiler Partitioning
    bottom_ash_solid = np.multiply(bromine_input, np.mean(br_dict['Bottom_Ash']['solid']))
    bottom_ash_liquid = np.multiply(bromine_input, np.mean(br_dict['Bottom_Ash']['liquid']))
    bottom_ash_gas = np.multiply(bromine_input, np.mean(br_dict['Bottom_Ash']['gas']))

    # SCR Partitioning
    scr_solid = np.multiply(bottom_ash_gas, np.mean(br_dict[nox_control]['solid']))
    scr_liquid = np.multiply(bottom_ash_gas, np.mean(br_dict[nox_control]['liquid']))
    scr_gas = np.multiply(bottom_ash_gas, np.mean(br_dict[nox_control]['gas']))

    # ACI Partitioning
    aci_solid = np.multiply(scr_gas, np.mean(br_dict[hg_control]['solid']))
    aci_liquid = np.multiply(scr_gas, np.mean(br_dict[hg_control]['liquid']))
    aci_gas = np.multiply(scr_gas, np.mean(br_dict[hg_control]['gas']))

    # DSI Partitioning
    dsi_solid = np.multiply(aci_gas, np.mean(br_dict[sorbent]['solid']))
    dsi_liquid = np.multiply(aci_gas, np.mean(br_dict[sorbent]['liquid']))
    dsi_gas = np.multiply(aci_gas, np.mean(br_dict[sorbent]['gas']))

    # Partitioning in PM Control Systems
    pm_solid = np.multiply(dsi_gas, np.mean(br_dict[pm_control]['solid']))
    pm_liquid = np.multiply(dsi_gas, np.mean(br_dict[pm_control]['liquid']))
    pm_gas = np.multiply(dsi_gas, np.mean(br_dict[pm_control]['gas']))

    # Partitioning in SO2 Control Systems
    so2_solid = np.multiply(pm_gas, np.mean(br_dict[so2_control]['solid']))
    so2_liquid = np.multiply(pm_gas, np.mean(br_dict[so2_control]['liquid']))
    so2_gas = np.multiply(pm_gas, np.mean(br_dict[so2_control]['gas']))

    # Calculate total partitioning
    br_solid = bottom_ash_solid + scr_solid + aci_solid + dsi_solid + pm_solid + so2_solid
    br_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + dsi_liquid + pm_liquid + so2_liquid
    br_gas = so2_gas

    br_solid = pd.Series(br_solid)
    br_liquid = pd.Series(br_liquid)
    br_gas = pd.Series(br_gas)

    br_solid = br_solid.values
    br_liquid = br_liquid.values
    br_gas = br_gas.values

    return br_solid, br_liquid, br_gas


def b_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import b_dict
    import numpy as np
    import pandas as pd

    boron_input = power_plant_inputs.Boron_Inputs
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    # Boiler Partitioning
    bottom_ash_solid = np.multiply(boron_input, np.mean(b_dict['Bottom_Ash']['solid']))
    bottom_ash_liquid = np.multiply(boron_input, np.mean(b_dict['Bottom_Ash']['liquid']))
    bottom_ash_gas = np.multiply(boron_input, np.mean(b_dict['Bottom_Ash']['gas']))

    # SCR Partitioning
    scr_solid = np.multiply(bottom_ash_gas, np.mean(b_dict[nox_control]['solid']))
    scr_liquid = np.multiply(bottom_ash_gas, np.mean(b_dict[nox_control]['liquid']))
    scr_gas = np.multiply(bottom_ash_gas, np.mean(b_dict[nox_control]['gas']))

    # ACI Partitioning
    aci_solid = np.multiply(scr_gas, np.mean(b_dict[hg_control]['solid']))
    aci_liquid = np.multiply(scr_gas, np.mean(b_dict[hg_control]['liquid']))
    aci_gas = np.multiply(scr_gas, np.mean(b_dict[hg_control]['gas']))

    # DSI Partitioning
    dsi_solid = np.multiply(aci_gas, np.mean(b_dict[sorbent]['solid']))
    dsi_liquid = np.multiply(aci_gas, np.mean(b_dict[sorbent]['liquid']))
    dsi_gas = np.multiply(aci_gas, np.mean(b_dict[sorbent]['gas']))

    # Partitioning in PM Control Systems
    pm_solid = np.multiply(dsi_gas, np.mean(b_dict[pm_control]['solid']))
    pm_liquid = np.multiply(dsi_gas, np.mean(b_dict[pm_control]['liquid']))
    pm_gas = np.multiply(dsi_gas, np.mean(b_dict[pm_control]['gas']))

    # Partitioning in SO2 Control Systems
    so2_solid = np.multiply(pm_gas, np.mean(b_dict[so2_control]['solid']))
    so2_liquid = np.multiply(pm_gas, np.mean(b_dict[so2_control]['liquid']))
    so2_gas = np.multiply(pm_gas, np.mean(b_dict[so2_control]['gas']))

    # Calculate total partitioning
    b_solid = bottom_ash_solid + scr_solid + aci_solid + dsi_solid + pm_solid + so2_solid
    b_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + dsi_liquid + pm_liquid + so2_liquid
    b_gas = so2_gas

    b_solid = pd.Series(b_solid)
    b_liquid = pd.Series(b_liquid)
    b_gas = pd.Series(b_gas)

    b_solid = b_solid.values
    b_liquid = b_liquid.values
    b_gas = b_gas.values

    return b_solid, b_liquid, b_gas


def pb_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import pb_dict
    import numpy as np
    import pandas as pd

    lead_input = power_plant_inputs.Lead_Inputs
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control
    sorbent = power_plant_inputs.DSI_Usage

    # Boiler Partitioning
    bottom_ash_solid = np.multiply(lead_input, np.mean(pb_dict['Bottom_Ash']['solid']))
    bottom_ash_liquid = np.multiply(lead_input, np.mean(pb_dict['Bottom_Ash']['liquid']))
    bottom_ash_gas = np.multiply(lead_input, np.mean(pb_dict['Bottom_Ash']['gas']))

    # SCR Partitioning
    scr_solid = np.multiply(bottom_ash_gas, np.mean(pb_dict[nox_control]['solid']))
    scr_liquid = np.multiply(bottom_ash_gas, np.mean(pb_dict[nox_control]['liquid']))
    scr_gas = np.multiply(bottom_ash_gas, np.mean(pb_dict[nox_control]['gas']))

    # ACI Partitioning
    aci_solid = np.multiply(scr_gas, np.mean(pb_dict[hg_control]['solid']))
    aci_liquid = np.multiply(scr_gas, np.mean(pb_dict[hg_control]['liquid']))
    aci_gas = np.multiply(scr_gas, np.mean(pb_dict[hg_control]['gas']))

    # DSI Partitioning
    dsi_solid = np.multiply(aci_gas, np.mean(pb_dict[sorbent]['solid']))
    dsi_liquid = np.multiply(aci_gas, np.mean(pb_dict[sorbent]['liquid']))
    dsi_gas = np.multiply(aci_gas, np.mean(pb_dict[sorbent]['gas']))

    # Partitioning in PM Control Systems
    pm_solid = np.multiply(dsi_gas, np.mean(pb_dict[pm_control]['solid']))
    pm_liquid = np.multiply(dsi_gas, np.mean(pb_dict[pm_control]['liquid']))
    pm_gas = np.multiply(dsi_gas, np.mean(pb_dict[pm_control]['gas']))

    # Partitioning in SO2 Control Systems
    so2_solid = np.multiply(pm_gas, np.mean(pb_dict[so2_control]['solid']))
    so2_liquid = np.multiply(pm_gas, np.mean(pb_dict[so2_control]['liquid']))
    so2_gas = np.multiply(pm_gas, np.mean(pb_dict[so2_control]['gas']))

    # Calculate total partitioning
    pb_solid = bottom_ash_solid + scr_solid + aci_solid + dsi_solid + pm_solid + so2_solid
    pb_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + dsi_liquid + pm_liquid + so2_liquid
    pb_gas = so2_gas

    pb_solid = pd.Series(pb_solid)
    pb_liquid = pd.Series(pb_liquid)
    pb_gas = pd.Series(pb_gas)

    pb_solid = pb_solid.values
    pb_liquid = pb_liquid.values
    pb_gas = pb_gas.values

    return pb_solid, pb_liquid, pb_gas

def s_partitioning(power_plant_inputs):
    from apcd_partitioning_dictionaries import s_dict
    import numpy as np
    import pandas as pd

    sulfur_input = power_plant_inputs.Sulfur_Inputs
    pm_control = power_plant_inputs.PM_Control
    so2_control = power_plant_inputs.SO2_Control
    nox_control = power_plant_inputs.NOx_Control
    hg_control = power_plant_inputs.Hg_Control

    #Boiler Partitioning
    bottom_ash_solid = np.multiply(sulfur_input, np.mean(s_dict['Bottom_Ash']['solid']))
    bottom_ash_liquid = np.multiply(sulfur_input, np.mean(s_dict['Bottom_Ash']['liquid']))
    bottom_ash_gas = np.multiply(sulfur_input, np.mean(s_dict['Bottom_Ash']['gas']))

    #SCR Partitioning
    scr_solid = np.multiply(bottom_ash_gas, np.mean(s_dict[nox_control]['solid']))
    scr_liquid = np.multiply(bottom_ash_gas, np.mean(s_dict[nox_control]['liquid']))
    scr_gas = np.multiply(bottom_ash_gas, np.mean(s_dict[nox_control]['gas']))

    #ACI Partitioning
    aci_solid = np.multiply(scr_gas, np.mean(s_dict[hg_control]['solid']))
    aci_liquid = np.multiply(scr_gas, np.mean(s_dict[hg_control]['liquid']))
    aci_gas = np.multiply(scr_gas, np.mean(s_dict[hg_control]['gas']))

    #Partitioning in PM Control Systems
    pm_solid = np.multiply(aci_gas, np.mean(s_dict[pm_control]['solid']))
    pm_liquid = np.multiply(aci_gas, np.mean(s_dict[pm_control]['liquid']))
    pm_gas = np.multiply(aci_gas, np.mean(s_dict[pm_control]['gas']))

    #Partitioning in SO2 Control Systems
    so2_solid = np.multiply(pm_gas, np.mean(s_dict[so2_control]['solid']))
    so2_liquid = np.multiply(pm_gas, np.mean(s_dict[so2_control]['liquid']))
    so2_gas = np.multiply(pm_gas, np.mean(s_dict[so2_control]['gas']))

    #Calucalate total partitioning
    s_solid = bottom_ash_solid + scr_solid + aci_solid + pm_solid + so2_solid
    s_liquid = bottom_ash_liquid + scr_liquid + aci_liquid + pm_liquid + so2_liquid
    s_gas = so2_gas

    s_solid = pd.Series(s_solid)
    s_liquid = pd.Series(s_liquid)
    s_gas = pd.Series(s_gas)

    s_solid = s_solid.values
    s_liquid = s_liquid.values
    s_gas = s_gas.values

    return s_solid, s_liquid, s_gas
