import pytplot, load
from collections import OrderedDict
load.mca(['1990-01-01', '1990-01-02'])

a = pytplot.get_data('Emax')
od = OrderedDict()

od['k1'] = 1
od['k2'] = 2
od['k3'] = 3

print(od)

print('test')