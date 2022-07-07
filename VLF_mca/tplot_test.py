import pyspedas
import pytplot
from pytplot import options
from pytplot import tplot
from pytplot import tlimit
from pytplot import tplot_options
import Akebono_mca_load
import Akebono_orb_load
import numpy as np
from load import mca, orb
date = '19910711'
#importer1 = Akebono_mca_load.Akebono_mca_load(date)
#importer2 = Akebono_orb_load.Akebono_orb_load(date)
#importer1.mca()
mca(trange= ['1991-07-11', '1991-07-13'])
orb(trange= ['1991-07-11', '1991-07-13'])

tplot_names = pytplot.tplot_names(True)

#dB to amplitude
for i in range(4):
    tplot_variable = pytplot.get_data(tplot_names[i])
    tplot_variable_0dB = 1e-6 #mV or pT
    bandwidth = tplot_variable.v * 0.3
    tplot_variable_amplitude = (10**(tplot_variable.y/20)) * (tplot_variable_0dB)  / np.sqrt(bandwidth)
    pytplot.store_data(tplot_names[i] +'_amplitude', data={'x': tplot_variable.times, 'y': tplot_variable_amplitude, 'v': tplot_variable.v})
    
    
pytplot.tplot_names()

Pass = pytplot.get_data('akb_orb_Pass')
start_pass_number = Pass.y[3]
pass_start_time = Pass.times[3]
for i in range(0, Pass.y.size):
    if start_pass_number < Pass.y[i+1]:
        pass_end_time = Pass.times[i]
        pass_number_index = i
        break
pass_start_time = pyspedas.time_string(pass_start_time, fmt = '%Y-%m-%d %H:%M:%S')
pass_end_time = pyspedas.time_string(pass_end_time, fmt = '%Y-%m-%d %H:%M:%S')

trange = [pass_start_time, pass_end_time]
print(trange)

tlimit(trange)
options(['Emax_amplitude', 'Bmax_amplitude'], 'spec', 1)
options(['Emax_amplitude', 'Bmax_amplitude'], 'ylog', 1)
options(['Emax_amplitude', 'Bmax_amplitude'], 'zlog', 1)
options(['Emax_amplitude', 'Bmax_amplitude'], 'zrange', [1e-5, 100])
options(['Emax_amplitude', 'Bmax_amplitude'], 'yrange', [1, 2e4])
options('Emax_amplitude', 'ztitle', '[mV/m/Hz^1/2]')
options('Bmax_amplitude', 'ztitle', '[pT/Hz^1/2]')
options('akb_orb_ALT', 'xlabel', 'ALT [km]')
options('akb_orb_MLT', 'xlabel', 'MLT [h]')
options('akb_orb_ILAT', 'ylabel', 'ILAT [deg]')
options('akb_orb_ILAT', 'panel_size', 0.3)
tplot_options('title', str(Pass.y[pass_number_index]) + 'MCA data' + date)
tplot(['Emax_amplitude', 'Bmax_amplitude', 'akb_orb_ILAT'], var_label = ['akb_orb_ALT', 'akb_orb_MLT', 'akb_orb_ILAT'], save_png = 'akb'+ date + '-pass_number_test')

