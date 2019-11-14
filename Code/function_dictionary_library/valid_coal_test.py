def valid_coal_test(coal):
    class BadCoalError(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)

    #Test that the coal the user has inputted is a valid coal that we have data for.
    if type(coal) == str:
        if (coal == 'Appalachian Low Sulfur') | (coal == 'Appalachian Med Sulfur') | (coal == 'Beulah-Zap') | \
                (coal == 'Illinois #6') | (coal == 'ND Lignite') | (coal == 'Pocahontas #3') | \
                (coal == 'Upper Freeport') | (coal == 'WPC Utah') | (coal == 'Wyodak') | (coal == 'Wyodak Anderson') | \
                (coal == 'Wyoming PRB') | (coal == 'Bituminous') | (coal == 'Subbituminous') | (coal == 'Lignite') | \
                (coal == 'QGESS Bituminous') | (coal == 'QGESS Subbituminous'):
            print("The coal you've selected, %s, is a valid coal." % coal)

        else:
            print("The coal you've selected, %s, 'is not a valid coal." % coal)
            raise BadCoalError("Not a valid coal!")

    else:
        print('That is not a string.')
        raise BadCoalError("Not a valid coal!")

