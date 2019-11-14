# COALQUAL reports everything in terms of state names instead of state abbreviations. This code takes a state name and
# returns the respective state abbreviation.

# This function takes one input:  A string containing a state name
# This function returns one output:  A string containing the abbreviation for the state.

# This function is used in the following codes:  coal_data_processing_functions.py

def state_name_to_abbreviation(state):
    state = state.upper()
    if state == 'ALABAMA':
        Abbreviation = 'AL'
    elif state == 'ALASKA':
        Abbreviation = 'AK'
    elif state == 'ARIZONA':
        Abbreviation = 'AZ'
    elif state == 'ARKANSAS':
        Abbreviation = 'AR'
    elif state == 'CALIFORNIA':
        Abbreviation = 'CA'
    elif state == 'COLORADO':
        Abbreviation = 'CO'
    elif state == 'CONNECTICUT':
        Abbreviation = 'CT'
    elif state == 'DELAWARE':
        Abbreviation = 'DE'
    elif state == 'FLORIDA':
        Abbreviation = 'FL'
    elif state == 'GEORGIA':
        Abbreviation = 'GA'
    elif state == 'HAWAII':
        Abbreviation = 'HI'
    elif state == 'IDAHO':
        Abbreviation = 'ID'
    elif state == 'ILLINOIS':
        Abbreviation = 'IL'
    elif state == 'INDIANA':
        Abbreviation = 'IN'
    elif state == 'IOWA':
        Abbreviation = 'IA'
    elif state == 'KANSAS':
        Abbreviation = 'KS'
    elif state == 'KENTUCKY':
        Abbreviation = 'KY'
    elif state == 'LOUISIANA':
        Abbreviation = 'LA'
    elif state == 'MAINE':
        Abbreviation = 'ME'
    elif state == 'MARYLAND':
        Abbreviation = 'MD'
    elif state == 'MASSACHUSETTS':
        Abbreviation = 'MA'
    elif state == 'MICHIGAN':
        Abbreviation = 'MI'
    elif state == 'MINNESOTA':
        Abbreviation = 'MN'
    elif state == 'MISSISSIPPI':
        Abbreviation = 'MS'
    elif state == 'MISSOURI':
        Abbreviation = 'MO'
    elif state == 'MONTANA':
        Abbreviation = 'MT'
    elif state == 'NEBRASKA':
        Abbreviation = 'NE'
    elif state == 'NEVADA':
        Abbreviation = 'NV'
    elif state == 'NEW HAMPSHIRE':
        Abbreviation = 'NH'
    elif state == 'NEW JERSEY':
        Abbreviation = 'NJ'
    elif state == 'NEW MEXICO':
        Abbreviation = 'NM'
    elif state == 'NEW YORK':
        Abbreviation = 'NY'
    elif state == 'NORTH CAROLINA':
        Abbreviation = 'NC'
    elif state == 'NORTH DAKOTA':
        Abbreviation = 'ND'
    elif state == 'OHIO':
        Abbreviation = 'OH'
    elif state == 'OKLAHOMA':
        Abbreviation = 'OK'
    elif state == 'OREGON':
        Abbreviation = 'OR'
    elif state == 'PENNSYLVANIA':
        Abbreviation = 'PA'
    elif state == 'RHODE ISLAND':
        Abbreviation = 'RI'
    elif state == 'SOUTH CAROLINA':
        Abbreviation = 'SC'
    elif state == 'SOUTH DAKOTA':
        Abbreviation = 'SD'
    elif state == 'TENNESSEE':
        Abbreviation = 'TN'
    elif state == 'TEXAS':
        Abbreviation = 'TX'
    elif state == 'UTAH':
        Abbreviation = 'UT'
    elif state == 'VERMONT':
        Abbreviation = 'VT'
    elif state == 'VIRGINIA':
        Abbreviation = 'VA'
    elif state == 'WASHINGTON':
        Abbreviation = 'WA'
    elif state == 'WEST VIRGINIA':
        Abbreviation = 'WV'
    elif state == 'WISCONSIN':
        Abbreviation = 'WI'
    elif state == 'WYOMING':
        Abbreviation = 'WY'
    else:
        Abbreviation = 'NA'

    return Abbreviation