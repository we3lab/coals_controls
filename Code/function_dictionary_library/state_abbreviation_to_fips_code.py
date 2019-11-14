# COALQUAL reports everything in terms of state names instead of state abbreviations. This code takes a state name and
# returns the respective state abbreviation.

# This function takes one input:  A string containing a state name
# This function returns one output:  A string containing the abbreviation for the state.

# This function is used in the following codes:  coal_data_processing_functions.py

def state_abbreviation_to_fips_code(state):
    state = state.upper()
    if state == 'AL':
        fips_code = '01'
    elif state == 'AK':
        fips_code = '02'
    elif state == 'AZ':
        fips_code = '04'
    elif state == 'AR':
        fips_code = '05'
    elif state == 'CA':
        fips_code = '06'
    elif state == 'CO':
        fips_code = '08'
    elif state == 'CT':
        fips_code = '09'
    elif state == 'DE':
        fips_code = '10'
    elif state == 'FL':
        fips_code = '12'
    elif state == 'GA':
        fips_code = '13'
    elif state == 'HI':
        fips_code = '15'
    elif state == 'ID':
        fips_code = '16'
    elif state == 'IL':
        fips_code = '17'
    elif state == 'IN':
        fips_code = '18'
    elif state == 'IA':
        fips_code = '19'
    elif state == 'KS':
        fips_code = '20'
    elif state == 'KY':
        fips_code = '21'
    elif state == 'LA':
        fips_code = '22'
    elif state == 'ME':
        fips_code = '23'
    elif state == 'MD':
        fips_code = '24'
    elif state == 'MA':
        fips_code = '25'
    elif state == 'MI':
        fips_code = '26'
    elif state == 'MN':
        fips_code = '27'
    elif state == 'MS':
        fips_code = '28'
    elif state == 'MO':
        fips_code = '29'
    elif state == 'MT':
        fips_code = '30'
    elif state == 'NE':
        fips_code = '31'
    elif state == 'NV':
        fips_code = '32'
    elif state == 'NH':
        fips_code = 'NH'
    elif state == 'NJ':
        fips_code = '34'
    elif state == 'NM':
        fips_code = '35'
    elif state == 'NY':
        fips_code = '36'
    elif state == 'NC':
        fips_code = '37'
    elif state == 'ND':
        fips_code = '38'
    elif state == 'OH':
        fips_code = '39'
    elif state == 'OK':
        fips_code = '40'
    elif state == 'OR':
        fips_code = '41'
    elif state == 'PA':
        fips_code = '42'
    elif state == 'RI':
        fips_code = '44'
    elif state == 'SC':
        fips_code = '45'
    elif state == 'SD':
        fips_code = '46'
    elif state == 'TN':
        fips_code = '47'
    elif state == 'TX':
        fips_code = '48'
    elif state == 'UT':
        fips_code = '49'
    elif state == 'VT':
        fips_code = '50'
    elif state == 'VA':
        fips_code = '51'
    elif state == 'WA':
        fips_code = '53'
    elif state == 'WV':
        fips_code = '54'
    elif state == 'WI':
        fips_code = '55'
    elif state == 'WY':
        fips_code = '56'
    else:
        fips_code = 'NA'

    return fips_code

