import pyspedas
import pytplot
from pytplot import options
from pytplot import tplot
from pytplot import tlimit
from pytplot import tplot_options
import Akebono_mca_load
import Akebono_orb_load
import numpy as np

importer1 = Akebono_mca_load.Akebono_mca_load('19900211')
importer2 = Akebono_orb_load.Akebono_orb_load('19900211')
importer1.mca()
importer2.orb()

tplot_names = pytplot.tplot_names()

for i in range(4):
    tplot_variable = pytplot.get_data(tplot_names[i])
    tplot_variable_0dB = 1e-6 #mV or pT
    bandwidth = tplot_variable.v * 0.3
    tplot_variable_power = (10**(tplot_variable.y/10)) * (tplot_variable_0dB**2) / bandwidth 
    pytplot.store_data(tplot_names[i] +'_power', data={'x': tplot_variable.times, 'y': tplot_variable_power, 'v': tplot_variable.v})

tlimit(['1990-02-11 01:00:00', '1990-02-11 03:00:00'])
options('Emax', 'spec', 1)
options('Emax', 'ylog', 1)
options('Emax', 'zrange', [40, 120])
tplot_options('title', 'MCA data on Feb 11, 1990')
tplot('Emax', var_label = ['akb_orb_ILAT', 'akb_orb_MLT', 'akb_orb_ALT'], save_png = 'savefig_test2')