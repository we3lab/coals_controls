def apcd_user_inputs():
    csESP_input = input("Is there a cold side ESP installed? [y/n]")
    if (csESP_input == 'y') | (csESP_input.lower() == 'yes'):
        csESP = 1
    else:
        csESP = 0

    hsESP_input = input("Is there a hot side ESP installed? [y/n]")
    if (hsESP_input == 'y') | (hsESP_input.lower() == 'yes'):
        hsESP = 1
    else:
        hsESP = 0

    FF_input = input("Is there a fabric filter installed? [y/n]")
    if (FF_input == 'y') | (FF_input.lower() == 'yes'):
        FF = 1
    else:
        FF = 0

    SCR_input = input("Is there a selective catalytic reduction process installed? [y/n]")
    if (SCR_input == 'y') | (SCR_input.lower() == 'yes'):
        SCR = 1
    else:
        SCR = 0

    ACI_input = input('Is activated carbon injection used for mercury control? [y/n]')
    if (ACI_input == 'y') | (ACI_input.lower() == 'yes'):
        ACI = 1
    else:
        ACI = 0

    DSI_input = input("Is a dry sorbent injection system installed? [y/n]")
    if (DSI_input == 'y') | (DSI_input.lower() == 'yes'):
        DSI = 1
    else:
        DSI = 0

    wetFGD_input = input("Is a wet FGD system installed? [y/n]")
    if (wetFGD_input == 'y') | (wetFGD_input.lower() == 'yes'):
        wetFGD = 1
        wetFGD_reagent = input("What type of reagent is used in the wFGD? Choose one from [Mg-enhanced Lime/Limestone]")
        wetFGD_reagent = wetFGD_reagent.replace(" ","")
        #limestone 
        if wetFGD_reagent.lower() == "limestone":
            wetFGD_oxidation = input("What's the oxidation state? Choose one from [Forced/Inhibited]")
            #forced
            if wetFGD_oxidation.lower() == "forced":
                wetFGD_additive = input("What's the performance additive? Choose one from [DBA/None]")
                if wetFGD_additive.lower() == "dba":
                    wetFGD_type = "LS Forced DBA" #1st type
                else: wetFGD_type = "LS Forced None" #2nd type
            #inhibited
            elif wetFGD_oxidation.lower()=="inhibited": 
                wetFGD_additive = input("What's the performance additive? Choose one from [DBA/NaFo/None]")
                if wetFGD_additive.lower() == 'dba':
                    wetFGD_type = "LS Inhibited DBA" #3rd type
                elif wetFGD_additive.lower() == "none":
                    wetFGD_type = "LS Inhibited None" #4th type
                else: wetFGD_type = "LS Inhibited NaFo" #5th type
            else:
                wetFGD_type = 0
                print("Not a valid WFGD type.(Note: Limestone natural oxidation wFGD is not inlcuded in the model)")
        #Mg-enhanced lime
        elif wetFGD_reagent.lower() == "mg-enhancedlime": 
            wetFGD_oxidation = input("What's the oxidation state? Choose one from [Ext. Forced/Inhibited/Natural]")
            wetFGD_oxidation = wetFGD_oxidation.replace(" ","")
            if wetFGD_oxidation.lower() == "natural":
                wetFGD_type = "Mg-enhanced Lime Natural" #6th type
            elif wetFGD_oxidation.lower() == "inhibited":
                wetFGD_type = "Mg-enhanced Lime Inhibited" #7th type
            elif wetFGD_oxidation.lower() == "ext.forced":
                wetFGD_type = "Mg-enhanced Lime Ext. Forced" #8th type
            else: 
                wetFGD_type = 0
                print("Not a valid wFGD type.")
        else:
            wetFGD_type = 0
            print("Not a valid wFGD type.")
    else:
        wetFGD = 0
        wetFGD_type = 0 

    dryFGD_input = input("Is a dry FGD system installed? [y/n]")
    if (dryFGD_input == 'y') | (dryFGD_input.lower() == 'yes'):
        dryFGD = 1
    else:
        dryFGD = 0

    return csESP, hsESP, FF, SCR, ACI, wetFGD, dryFGD, DSI, wetFGD_type
    

