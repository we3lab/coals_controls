def pm_classification(process_type):
    import pandas as pd
    #Fabric Filter Classification includes shake and deflate baghouse (BS), pulse baghouse (BP), and reverse air
    #baghouse (BR).
    if process_type == 'BS' or process_type == 'BP' or process_type == 'BR':
        pm_process_classification = 'FF'
    #Cold-side ESPs include those with (EC) and without (EK) flue gas conditioning.
    elif process_type == 'EC' or process_type == 'EK':
        pm_process_classification = 'csESP'
    #Hot-side ESPs include those with (EH) and without (EW) flue gas conditioning.
    elif process_type == 'EH' or process_type == 'EW':
        pm_process_classification = 'hsESP'
    #Cyclones include those with multiple cyclones (MC) and single cyclones (SC).
#    elif process_type == 'MC' or process_type == 'SC':
#        pm_process_classification = 'Cyc'
    #Scrubbers include those that are jet bubbling reactors (JB), mechanically aided type (MA), packed type (PA), spray
    # type (SP), tray type (TR) and veturi type (VE).
#    elif process_type == 'JB' or process_type == 'MA' or process_type == 'PA' or process_type == 'SP' or process_type == 'TR' or process_type == 'VE':
#        pm_process_classification = 'Scrub'
    #elif pd.isnull(process_type):
    #    pm_process_classification = 'none'
    else:
        pm_process_classification = 'not installed'

    return (pm_process_classification)

def so2_classification(process_type):
    import pandas as pd
    #Wet scrubbers include those that are jet bubbling reactors (JB), mechanically aided type (MA), packed type (PA),
    #spary type (SP), tray type (TR) and veturi type (VE).
    if process_type == 'JB' or process_type == 'MA' or process_type == 'PA' or process_type == 'SP' or process_type == 'TR' or process_type == 'VE':
        so2_process_classification = 'wetFGD'
    #Dry scrubbers include those that are circulating dry scrubbers (CD), spray dryer type (SD), and dry sorbent
    #injection (DSI).
    elif process_type == 'CD' or process_type == 'SD' or process_type == "DSI":
        so2_process_classification = 'dryFGD'
    #elif pd.isnull(process_type):
    #    so2_process_classification = 'none'
    else:
        so2_process_classification = 'not installed'
    return (so2_process_classification)

def dsi_classification(process_type):
    import pandas as pd
    if process_type == 'DSI':
        dsi_process_classification = 'DSI'
    else:
        dsi_process_classification = 'not installed'
    return (dsi_process_classification)

def nox_classification(process_type):
    import pandas as pd
    # Selective catalytic reduction is abbreviated SR in the EIA database.
    if process_type == 'SR':
        nox_process_classification = 'SCR'
    # Other types of process that exist, but are not considered for our analysis include:  flue gas recirculation, fuel
    # reburning, water injection, low excess air, low NOx burner, ammonia injection, overfire air, repower unit, slagging,
    # selective noncatalytic reduction and steam injection.
    #elif pd.isnull(process_type):
    #    nox_process_classification = 'none'
    else:
        nox_process_classification = 'not installed'

    return (nox_process_classification)

def hg_classification(process_type):
    import pandas as pd
    # Activated carbon injection is abbreviated as ACI in the EIA database.
    if type(process_type) == str: 
        process_type = process_type.lower()
        process_type = process_type.strip()
    if process_type == 'aci' or process_type == "y" or process_type == "activated carbon injection" or process_type == "carbon injection":
        hg_process_classification = 'ACI'
    # Other processes listed in the EIA database include baghouses, dry scrubbers, lime injection, electrostatic
    # precipitators and wet scrubbers,
    #elif pd.isnull(process_type):
    #    hg_process_classification = 'none'
    else:
        hg_process_classification = 'not installed'

    return (hg_process_classification)