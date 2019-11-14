def elg_compliance_check(elg, zld, as_concentration, cl_concentration, hg_concentration, se_concentration):

    #ELG standards
    as_elg_standard = 8/1000
    as_vip_standard = 4/1000
    hg_elg_standard = 356/1000000
    hg_vip_standard = 24/1000000
    se_elg_standard = 12/1000
    se_vip_standard = 5/1000
    #n_vip_standard = 4.4
    tds_vip_standard = 24

    # Check violations of the ELGs
    i = 0
    elg_violation_count = 0
    vip_violation_count = 0
    while i < len(as_concentration):
        if as_concentration[i] > as_elg_standard or hg_concentration[i] > hg_elg_standard or se_concentration[i] > se_elg_standard:
            elg_violation_count += 1
        if as_concentration[i] > as_vip_standard or hg_concentration[i] > hg_vip_standard or se_concentration[i] > se_vip_standard or cl_concentration[i] > tds_vip_standard:
            vip_violation_count += 1
        i += 1

    as_elg_violation_count = 0
    as_vip_violation_count = 0
    hg_elg_violation_count = 0
    hg_vip_violation_count = 0
    se_elg_violation_count = 0
    se_vip_violation_count = 0
    n_elg_violation_count = 0
    tds_vip_violation_count = 0
    if vip_violation_count > 0:
        # Arsenic violations count
        i = 0
        while i < len(as_concentration):
            if as_concentration[i] > as_elg_standard:
                as_elg_violation_count += 1
            if as_concentration[i] > as_vip_standard:
                as_vip_violation_count += 1
            i += 1

        # Mercury violations count
        i = 0
        while i < len(hg_concentration):
            if hg_concentration[i] > hg_elg_standard:
                hg_elg_violation_count += 1
            if hg_concentration[i] > hg_vip_standard:
                hg_vip_violation_count += 1
            i += 1

        # Selenium violations count
        i = 0
        while i < len(se_concentration):
            if se_concentration[i] > se_elg_standard:
                se_elg_violation_count += 1
            if se_concentration[i] > se_vip_standard:
                se_vip_violation_count += 1
            i += 1

        # Nitrate/Nitrite violations count
        #i = 0
        #while i < len(se_concentration):
        #    if n_concentration[i] > n_elg_standard:
        #        n_elg_violation_count += 1
        #    i += 1

        # TDS violations count
        i = 0
        while i < len(cl_concentration):
            if cl_concentration[i] > tds_vip_standard:
                tds_vip_violation_count += 1
            i += 1

    #Calculate rate of sample violations.
    total_elg_violations = 100 * elg_violation_count/len(as_concentration)
    total_vip_violations = 100 * vip_violation_count/len(as_concentration)
    as_elg_violations = 100 * as_elg_violation_count/len(as_concentration)
    as_vip_violations = 100 * as_vip_violation_count/len(as_concentration)
    hg_elg_violations = 100 * hg_elg_violation_count/len(hg_concentration)
    hg_vip_violations = 100 * hg_vip_violation_count/len(hg_concentration)
    se_elg_violations = 100 * se_elg_violation_count/len(se_concentration)
    se_vip_violations = 100 * se_vip_violation_count/len(se_concentration)
    #n_elg_violations = 100 * n_elg_violation_count/len(n_concentration)
    tds_vip_violations = 100 * tds_vip_violation_count/len(cl_concentration)

    if elg == 1:
        if total_elg_violations > 0:
            print(
                '{}% of effluent samples violate the ELGs.  {}% of these samples violate the As standard; {}% violate the Hg standard; {}% violate the Se standard.'.format(
                    total_elg_violations, as_elg_violations, hg_elg_violations, se_elg_violations))
        elif total_elg_violations == 0:
            print('This treatment train is unlikely to lead to violations of the ELGs.')

    if zld == 1:
        if total_vip_violations > 0:
            print('{}% of effluent samples violate the VIP standard.  {}% of these samples violate the As standard; {}% violate the Hg standard; {}% violate the Se standard.'.format(
                    total_vip_violations, as_vip_violations, hg_vip_violations, se_vip_violations))
        elif total_vip_violations == 0:
            print('This treatment train is unlikely to lead to violations of the Voluntary Incentives Program.')


def elg_compliance_check_simulation(elg, zld, as_concentration, cl_concentration, hg_concentration, se_concentration):

    #ELG standards
    as_elg_standard = 8/1000
    as_vip_standard = 4/1000
    hg_elg_standard = 356/1000000
    hg_vip_standard = 24/1000000
    se_elg_standard = 12/1000
    se_vip_standard = 5/1000
    #n_vip_standard = 4.4
    tds_vip_standard = 24

    # Check violations of the ELGs
    i = 0
    elg_violation_count = 0
    vip_violation_count = 0
    while i < len(as_concentration):
        if as_concentration[i] > as_elg_standard or hg_concentration[i] > hg_elg_standard or se_concentration[i] > se_elg_standard:
            elg_violation_count += 1
        if as_concentration[i] > as_vip_standard or hg_concentration[i] > hg_vip_standard or se_concentration[i] > se_vip_standard or cl_concentration[i] > tds_vip_standard:
            vip_violation_count += 1
        i += 1

    if vip_violation_count > 0:
        # Arsenic violations count
        i = 0
        as_elg_violation_count = 0
        as_vip_violation_count = 0
        while i < len(as_concentration):
            if as_concentration[i] > as_elg_standard:
                as_elg_violation_count += 1
            if as_concentration[i] > as_vip_standard:
                as_vip_violation_count += 1
            i += 1

        # Mercury violations count
        i = 0
        hg_elg_violation_count = 0
        hg_vip_violation_count = 0
        while i < len(hg_concentration):
            if hg_concentration[i] > hg_elg_standard:
                hg_elg_violation_count += 1
            if hg_concentration[i] > hg_vip_standard:
                hg_vip_violation_count += 1
            i += 1

        # Selenium violations count
        i = 0
        se_elg_violation_count = 0
        se_vip_violation_count = 0
        while i < len(se_concentration):
            if se_concentration[i] > se_elg_standard:
                se_elg_violation_count += 1
            if se_concentration[i] > se_vip_standard:
                se_vip_violation_count += 1
            i += 1

        # Nitrate/Nitrite violations count
        #i = 0
        #n_elg_violation_count = 0
        #while i < len(se_concentration):
        #    if n_concentration[i] > n_elg_standard:
        #        n_elg_violation_count += 1
        #    i += 1

        # TDS violations count
        i = 0
        tds_vip_violation_count = 0
        while i < len(cl_concentration):
            if cl_concentration[i] > tds_vip_standard:
                tds_vip_violation_count += 1
            i += 1

    #Calculate rate of sample violations.
    total_elg_violations = 100 * elg_violation_count/len(as_concentration)
    total_vip_violations = 100 * vip_violation_count/len(as_concentration)
    as_elg_violations = 100 * as_elg_violation_count/len(as_concentration)
    as_vip_violations = 100 * as_vip_violation_count/len(as_concentration)
    hg_elg_violations = 100 * hg_elg_violation_count/len(hg_concentration)
    hg_vip_violations = 100 * hg_vip_violation_count/len(hg_concentration)
    se_elg_violations = 100 * se_elg_violation_count/len(se_concentration)
    se_vip_violations = 100 * se_vip_violation_count/len(se_concentration)
    #n_elg_violations = 100 * n_elg_violation_count/len(n_concentration)
    tds_vip_violations = 100 * tds_vip_violation_count/len(cl_concentration)

    if elg == 1:
        return total_elg_violations, as_elg_violations, hg_elg_violations, se_elg_violations,
    if zld == 1:
        return total_vip_violations, as_vip_violations, hg_vip_violations, se_vip_violations

def elg_compliance_check_simulation_no_as(elg, zld, as_concentration, cl_concentration, hg_concentration, se_concentration):

    #ELG standards
    as_elg_standard = 8/1000
    as_vip_standard = 4/1000
    hg_elg_standard = 356/1000000
    hg_vip_standard = 24/1000000
    se_elg_standard = 12/1000
    se_vip_standard = 5/1000
    #n_vip_standard = 4.4
    tds_vip_standard = 24

    # Check violations of the ELGs
    i = 0
    elg_violation_count = 0
    vip_violation_count = 0
    while i < len(as_concentration):
        if hg_concentration[i] > hg_elg_standard or se_concentration[i] > se_elg_standard:
            elg_violation_count += 1
        if hg_concentration[i] > hg_vip_standard or se_concentration[i] > se_vip_standard or cl_concentration[i] > tds_vip_standard:
            vip_violation_count += 1
        i += 1

    if vip_violation_count > 0:
        # Arsenic violations count
        i = 0
        as_elg_violation_count = 0
        as_vip_violation_count = 0
        while i < len(as_concentration):
            if as_concentration[i] > as_elg_standard:
                as_elg_violation_count += 1
            if as_concentration[i] > as_vip_standard:
                as_vip_violation_count += 1
            i += 1

        # Mercury violations count
        i = 0
        hg_elg_violation_count = 0
        hg_vip_violation_count = 0
        while i < len(hg_concentration):
            if hg_concentration[i] > hg_elg_standard:
                hg_elg_violation_count += 1
            if hg_concentration[i] > hg_vip_standard:
                hg_vip_violation_count += 1
            i += 1

        # Selenium violations count
        i = 0
        se_elg_violation_count = 0
        se_vip_violation_count = 0
        while i < len(se_concentration):
            if se_concentration[i] > se_elg_standard:
                se_elg_violation_count += 1
            if se_concentration[i] > se_vip_standard:
                se_vip_violation_count += 1
            i += 1

        # Nitrate/Nitrite violations count
        #i = 0
        #n_elg_violation_count = 0
        #while i < len(se_concentration):
        #    if n_concentration[i] > n_elg_standard:
        #        n_elg_violation_count += 1
        #    i += 1

        # TDS violations count
        i = 0
        tds_vip_violation_count = 0
        while i < len(cl_concentration):
            if cl_concentration[i] > tds_vip_standard:
                tds_vip_violation_count += 1
            i += 1

    #Calculate rate of sample violations.
    total_elg_violations = 100 * elg_violation_count/len(as_concentration)
    total_vip_violations = 100 * vip_violation_count/len(as_concentration)
    as_elg_violations = 100 * as_elg_violation_count/len(as_concentration)
    as_vip_violations = 100 * as_vip_violation_count/len(as_concentration)
    hg_elg_violations = 100 * hg_elg_violation_count/len(hg_concentration)
    hg_vip_violations = 100 * hg_vip_violation_count/len(hg_concentration)
    se_elg_violations = 100 * se_elg_violation_count/len(se_concentration)
    se_vip_violations = 100 * se_vip_violation_count/len(se_concentration)
    #n_elg_violations = 100 * n_elg_violation_count/len(n_concentration)
    tds_vip_violations = 100 * tds_vip_violation_count/len(cl_concentration)

    if elg == 1:
        return total_elg_violations, as_elg_violations, hg_elg_violations, se_elg_violations,
    if zld == 1:
        return total_vip_violations, as_vip_violations, hg_vip_violations, se_vip_violations
