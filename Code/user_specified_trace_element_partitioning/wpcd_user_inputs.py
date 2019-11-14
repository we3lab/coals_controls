def wpcd_user_inputs():

    cp_input = input("Is there chemical precipitation installed? [y/n]")
    if (cp_input == 'y') | (cp_input.lower() == 'yes'):
        cp = 1
    else:
        cp = 0

    elg_input = input("Is the process designed primarily to remove Selenium? [y/n]")
    if (elg_input == 'y') | (elg_input.lower() == 'yes'):
        elg = 1
    else:
        elg = 0

    zld_input = input("Is the process designed to eliminate liquid discharge of pollutants? [y/n]")
    if (zld_input == 'y') | (zld_input.lower() == 'yes'):
        zld = 1
    else:
        zld = 0

    if elg == 1:
        mbr_input = input("Is there a membrane bioreactor installed? [y/n]")
        if (mbr_input == 'y') | (mbr_input.lower() == 'yes'):
            mbr = 1
        else:
            mbr = 0

        bt_input = input("Is there an ABMet process installed? [y/n]")
        if (bt_input == 'y') | (bt_input.lower() == 'yes'):
            bt = 1
        else:
            bt = 0

        iex_input = input("Is there an ion exchange system installed?  [y/n]")
        if (iex_input == 'y') | (iex_input.lower() == 'yes'):
            iex = 1
        else:
            iex = 0

        alox_input = input("Is there an granular aluminum oxide sorbent system installed?  [y/n]")
        if (alox_input == 'y') | (alox_input.lower() == 'yes'):
            alox = 1
        else:
            alox = 0

        feox_input = input("Is there an granular ferric oxide sorbent system installed?  [y/n]")
        if (feox_input == 'y') | (feox_input.lower() == 'yes'):
            feox = 1
        else:
            feox = 0

        zvi_input = input("Is there a zero valent iron system installed?  [y/n]")
        if (zvi_input == 'y') | (zvi_input.lower() == 'yes'):
            zvi = 1
        else:
            zvi = 0

        gac_input = input("Is there an activated carbon system installed?  [y/n]")
        if (gac_input == 'y') | (gac_input.lower() == 'yes'):
            gac = 1
        else:
            gac = 0

        mvc = 0
        ro = 0
        crys = 0

    if zld == 1:
        mvc_input = input("Is there a mechanical vapor compression process installed? [y/n]")
        if (mvc_input == 'y') | (mvc_input.lower() == 'yes'):
            mvc = 1
        else:
            mvc = 0

        ro_input = input("Is there a reverse osmosis process installed? [y/n]")
        if (ro_input == 'y') | (ro_input.lower() == 'yes'):
            ro = 1
        else:
            ro = 0

        crys_input = input("Is there a crystalizer installed? [y/n]")
        if (crys_input == 'y') | (crys_input.lower() == 'yes'):
            crys = 1
        else:
            crys = 0

        mbr = 0
        bt = 0
        iex = 0
        alox = 0
        feox = 0
        zvi = 0
        gac = 0


    return elg, zld, cp, mbr, bt, mvc, iex, alox, feox, zvi, crys, gac, ro
    

