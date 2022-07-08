import pyspedas
import pytplot
from pytplot import options, tplot, tlimit, tplot_options, get_data, store_data
import Akebono_mca_load
import Akebono_orb_load
import numpy as np
from load import mca, orb

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


pyspedas.tinterpol('akb_ILAT', interp_to='Emax_Amp', newname = 'ILAT')
pyspedas.tinterpol('akb_MLAT', interp_to='Emax_Amp', newname = 'MLAT')
pyspedas.tinterpol('akb_Pass', interp_to='Emax_Amp', newname = 'Pass')

Emax = get_data('Emax_Amp')
time, Emax = Emax.times, Emax.y
ILAT = get_data('ILAT')
ILAT = ILAT.y
MLAT = get_data('MLAT')
MLAT = MLAT.y

plus_index_tuple = np.where((MLAT>0) & (ILAT>65))
minus_index_tuple = np.where((MLAT<0) & (ILAT>65))

plus_index = plus_index_tuple[0]
minus_index = minus_index_tuple[0]

#make start_time list, end_time list
plus_start_time_index = [plus_index[0]]
plus_end_time_index = []
for i in range(plus_index.size-1):
    if plus_index[i+1] - plus_index[i] > 1:
        plus_end_time_index.append(plus_index[i])
        plus_start_time_index.append(plus_index[i+1])
        
plus_end_time_index.append(plus_index[-1])

plus_start_time_index = np.array(plus_start_time_index)
plus_end_time_index = np.array(plus_end_time_index)

plus_start_time_list = pyspedas.time_string(time[plus_start_time_index], fmt='%Y-%m-%d %H:%M:%S')
plus_end_time_list = pyspedas.time_string(time[plus_end_time_index], fmt='%Y-%m-%d %H:%M:%S')

start_time = plus_start_time_list[0]
end_time = plus_end_time_list[0]

tlimit([start_time, end_time])
options(['Emax_amplitude', 'Bmax_amplitude'], 'spec', 1)
options(['Emax_amplitude', 'Bmax_amplitude'], 'ylog', 1)
options(['Emax_amplitude', 'Bmax_amplitude'], 'zlog', 1)
options(['Emax_amplitude', 'Bmax_amplitude'], 'zrange', [1e-5, 100])
options(['Emax_amplitude', 'Bmax_amplitude'], 'yrange', [1, 2e4])
options('Emax_amplitude', 'ztitle', '[mV/m/Hz^1/2]')
options('Bmax_amplitude', 'ztitle', '[pT/Hz^1/2]')
options('akb_ALT', 'xlabel', 'ALT [km]')
options('akb_MLT', 'xlabel', 'MLT [h]')
options('akb_ILAT', 'ylabel', 'ILAT [deg]')
options('akb_ILAT', 'panel_size', 0.2)
tplot_options('title', str(Pass.y[pass_number_index]) + 'MCA data')
tplot(['Emax_amplitude', 'Bmax_amplitude', 'akb_ILAT'], var_label = ['akb_ALT', 'akb_MLT', 'akb_ILAT'], save_png = 'akb'+ '-pass_number_test')

