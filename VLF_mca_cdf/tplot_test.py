import pyspedas
import pytplot
from pytplot import options
from pytplot import tplot
from pytplot import tlimit
import matplotlib.pyplot as plt

pytplot.cdf_to_tplot('ak_h1_mca_19890607_v02.cdf')
tplot_names = pytplot.tplot_names(True)

for i in range(4):
    tplot_variable = pytplot.get_data(tplot_names[i])
    tplot_variable_0dB = 1e-6 #mV or pT
    bandwidth = tplot_variable.v * 0.3
    tplot_variable_power = (10**(tplot_variable.y/10)) * (tplot_variable_0dB**2) / bandwidth 
    pytplot.store_data(tplot_names[i] +'_power', 
                       data={'x': tplot_variable.times, 
                             'y': tplot_variable_power, 
                             'v': tplot_variable.v})