import pyspedas, pytplot, load
a = load.mca(['1990-02-01', '1990-02-02'])
b =pytplot.data_quants['Emax'].CDF['VATT']

print('test')