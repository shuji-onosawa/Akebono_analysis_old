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
    pytplot.store_data(tplot_names[i] +'_Amp', data={'x': tplot_variable.times, 'y': tplot_variable_amplitude, 'v': tplot_variable.v})
    
    
pytplot.tplot_names()

#Time interpolate
pyspedas.tinterpol('akb_ILAT', interp_to='Emax_Amp', newname = 'ILAT')
pyspedas.tinterpol('akb_MLAT', interp_to='Emax_Amp', newname = 'MLAT')
pyspedas.tinterpol('akb_Pass', interp_to='Emax_Amp', newname = 'Pass', method = 'nearest')

#Limit ILAT range
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

#make Passname list corresponding with start(end) time list
Passname = get_data('Pass')
Passname = Passname.y
Passname_list = Passname[plus_start_time_index]

#make tplot vars of Electric field Amplitude at 3.16 - 100 Hz
Emax = get_data('Emax_Amp')

Emax_channel1 = Emax.y.T[0] #3.16 Hz
Emax_channel2 = Emax.y.T[1] #5.62 Hz
Emax_channel3 = Emax.y.T[2] #10 Hz
Emax_channel4 = Emax.y.T[3] #17.8 Hz
Emax_channel5 = Emax.y.T[4] #31.6 Hz
Emax_channel6 = Emax.y.T[5] #56.2 Hz
Emax_channel7 = Emax.y.T[6] #100 Hz

store_data(name = 'Emax_channel1', data={'x':time, 'y':Emax_channel1})

#store data: Line spectrum
Emax = get_data('Emax_Amp')
Emax.v, Emax.y.T[0].size
Emax_channel1 = Emax.y.T[0]
Emax_channel2 = Emax.y.T[1]
Emax_channel3 = Emax.y.T[2]
Emax_channel4 = Emax.y.T[3]
Emax_channel5 = Emax.y.T[4]
Emax_channel6 = Emax.y.T[5]
Emax_channel7 = Emax.y.T[6]

store_data(name = 'Emax_channel1', data={'x':time, 'y':Emax_channel1})
store_data(name = 'Emax_channel2', data={'x':time, 'y':Emax_channel2})
store_data(name = 'Emax_channel3', data={'x':time, 'y':Emax_channel3})
store_data(name = 'Emax_channel4', data={'x':time, 'y':Emax_channel4})
store_data(name = 'Emax_channel5', data={'x':time, 'y':Emax_channel5})
store_data(name = 'Emax_channel6', data={'x':time, 'y':Emax_channel6})
store_data(name = 'Emax_channel7', data={'x':time, 'y':Emax_channel7})

colorlist = ["r", "g", "b", "c", "m", "y", "k", "w"]

options('Emax_channel1', 'color', colorlist[1])
options('Emax_channel2', 'color', colorlist[1])
options('Emax_channel3', 'color', colorlist[2])
options('Emax_channel4', 'color', colorlist[3])
options('Emax_channel5', 'color', colorlist[4])
options('Emax_channel6', 'color', colorlist[5])
options('Emax_channel7', 'color', colorlist[6])

store_data(name = 'Amplitude at 3.16-100 Hz', 
           data=['Emax_channel1', 
                 'Emax_channel2', 
                 'Emax_channel3', 
                 'Emax_channel4', 
                 'Emax_channel5',
                 'Emax_channel6',
                 'Emax_channel7'])

#designate start, end time and Passname 
start_time = plus_start_time_list[0]
end_time = plus_end_time_list[0]
Passname = Passname_list[0]

tlimit([start_time, end_time])
options(['Emax_Amp', 'Bmax_Amp'], 'spec', 1)
options(['Emax_Amp', 'Bmax_Amp'], 'ylog', 1)
options(['Emax_Amp', 'Bmax_Amp'], 'zlog', 1)
options('Emax_Amp', 'zrange', [1e-5, 10])
options('Bmax_Amp', 'zrange', [1e-5, 100])
options(['Emax_Amp', 'Bmax_Amp'], 'yrange', [1, 2e4])
options('Emax_Amp', 'ztitle', '[mV/m/Hz^1/2]')
options('Bmax_Amp', 'ztitle', '[pT/Hz^1/2]')
options('Amplitude at 3.16-100 Hz', 'ylog', 1)
options('Amplitude at 3.16-100 Hz', 'yrange', [1e-5, 10])
options('akb_ALT', 'xlabel', 'ALT [km]')
options('akb_MLT', 'xlabel', 'MLT [h]')
options('akb_ILAT', 'ylabel', 'ILAT [deg]')
tplot_options('title', str(int(Passname)) + 'MCA data')
tplot(['Emax_Amp', 'Amplitude at 3.16-100 Hz'], 
      var_label = ['akb_ALT', 'akb_MLT', 'akb_ILAT'], 
      save_png = 'akb'+str(int(Passname))+'-line_plot_test')

