import pyspedas
import pytplot
from pytplot import options, tplot, tlimit, tplot_options, get_data, store_data
import numpy as np
from load import mca, orb

trange = ['1990-02-11', '1990-02-13']
ILAT_min = 55
mca(trange= trange)
orb(trange= trange)

tplot_names = pytplot.tplot_names(True)

#dB to amplitude
for i in range(4):
    tplot_variable = pytplot.get_data(tplot_names[i])
    tplot_variable_0dB = 1e-6 #mV or pT
    bandwidth = tplot_variable.v * 0.3
    tplot_variable_amplitude = (10**(tplot_variable.y/20)) * (tplot_variable_0dB)  / np.sqrt(bandwidth)
    tplot_variable_power = (10**(tplot_variable.y/10)) * ((tplot_variable_0dB)**2)  / bandwidth
    pytplot.store_data(tplot_names[i] +'_Amp', data={'x': tplot_variable.times, 'y': tplot_variable_amplitude, 'v': tplot_variable.v})
    pytplot.store_data(tplot_names[i] +'_Pwr', data={'x': tplot_variable.times, 'y': tplot_variable_power, 'v': tplot_variable.v})
    
    
pytplot.tplot_names()

#Time interpolate
pyspedas.tinterpol('akb_ILAT', interp_to='Emax_Amp', newname = 'ILAT')
pyspedas.tinterpol('akb_MLAT', interp_to='Emax_Amp', newname = 'MLAT')
pyspedas.tinterpol('akb_Pass', interp_to='Emax_Amp', newname = 'Pass', method = 'nearest')

#Limit ILAT range
Emax = get_data('Emax_Amp')
time = Emax.times
ILAT = get_data('ILAT')
ILAT = ILAT.y
MLAT = get_data('MLAT')
MLAT = MLAT.y

north_index_tuple = np.where((MLAT>0) & (ILAT>ILAT_min)) 
south_index_tuple = np.where((MLAT<0) & (ILAT>ILAT_min))

north_index = north_index_tuple[0]
south_index = south_index_tuple[0]

#make start_time list, end_time list
north_start_time_index = [north_index[0]]
north_end_time_index = []
for i in range(north_index.size-1):
    if north_index[i+1] - north_index[i] > 1:
        north_end_time_index.append(north_index[i])
        north_start_time_index.append(north_index[i+1])
        
north_end_time_index.append(north_index[-1])

pnorth_start_time_index = np.array(north_start_time_index)
north_end_time_index = np.array(north_end_time_index)

north_start_time_list = pyspedas.time_string(time[north_start_time_index], fmt='%Y-%m-%d %H:%M:%S')
north_end_time_list = pyspedas.time_string(time[north_end_time_index], fmt='%Y-%m-%d %H:%M:%S')

#make tplot vars of Electric field Amplitude at 3.16 - 100 Hz
Emax = get_data('Emax_Amp')
Emax_channel1 = Emax.y.T[0] #3.16 Hz
Emax_channel2 = Emax.y.T[1] #5.62 Hz
Emax_channel3 = Emax.y.T[2] #10 Hz
Emax_channel4 = Emax.y.T[3] #17.8 Hz
Emax_channel5 = Emax.y.T[4] #31.6 Hz
Emax_channel6 = Emax.y.T[5] #56.2 Hz
Emax_channel7 = Emax.y.T[6] #100 Hz
Emax_channel8 = Emax.y.T[7] #178 Hz
Emax_channel9 = Emax.y.T[8] #316 Hz
Emax_channel10 = Emax.y.T[9] #562 Hz

Amp_data = [Emax_channel1, 
            Emax_channel2, 
            Emax_channel3, 
            Emax_channel4, 
            Emax_channel5,
            Emax_channel6,
            Emax_channel7,
            Emax_channel8,
            Emax_channel9,
            Emax_channel10]

store_data(name = 'Emax_lines_Amp', 
           data={'x': time,
                 'y': np.array(Amp_data).T})

#make tplot vars of Electric field Amplitude at 3.16 - 100 Hz
Emax = get_data('Emax_Pwr')
Emax_channel1 = Emax.y.T[0] #3.16 Hz
Emax_channel2 = Emax.y.T[1] #5.62 Hz
Emax_channel3 = Emax.y.T[2] #10 Hz
Emax_channel4 = Emax.y.T[3] #17.8 Hz
Emax_channel5 = Emax.y.T[4] #31.6 Hz
Emax_channel6 = Emax.y.T[5] #56.2 Hz
Emax_channel7 = Emax.y.T[6] #100 Hz
Emax_channel8 = Emax.y.T[7] #178 Hz
Emax_channel9 = Emax.y.T[8] #316 Hz
Emax_channel10 = Emax.y.T[9] #562 Hz

Pwr_data = [Emax_channel1, 
            Emax_channel2, 
            Emax_channel3, 
            Emax_channel4, 
            Emax_channel5,
            Emax_channel6,
            Emax_channel7,
            Emax_channel8,
            Emax_channel9,
            Emax_channel10]

store_data(name = 'Emax_lines_Pwr', 
           data={'x': time,
                 'y': np.array(Pwr_data).T})

#make Passname list corresponding with start(end) time list
Passname = get_data('Pass')
Passname = Passname.y
north_Passname_list = Passname[north_start_time_index]

#dict start, end time and Passname 
print(north_start_time_list)
input_index_str = input('dict start time index: ')
input_index_int = int(input_index_str)
start_time = north_start_time_list[input_index_int]
end_time = north_end_time_list[input_index_int]
Passname = north_Passname_list[input_index_int]

dir = './akb_north_mca_plot/'
hemisphere = 'north'
surfix = input('Amp or Pwr: ')

#make color table for line plots
color_table = ['red', 'yellow', 'blue', 'green',
               'crimson', 'y', 'c', 'lime',
               'deeppink', 'orange']

#plot
tlimit([start_time, end_time])
options(['Emax_' + surfix, 'Bmax_' + surfix], 'spec', 1)
options(['Emax_' + surfix, 'Bmax_' + surfix], 'ylog', 1)
options(['Emax_' + surfix, 'Bmax_' + surfix], 'zlog', 1)
options(['Emax_' + surfix, 'Bmax_' + surfix], 'Colormap', 'viridis')
if surfix == 'Amp':
    options('Emax_' + surfix, 'zrange', [1e-5, 10])
    options('Bmax_' + surfix, 'zrange', [1e-5, 10])
    options('Emax_lines_' + surfix, 'yrange', [1e-3, 10])
    options('Emax_' + surfix, 'ztitle', '$[mV/m/Hz^(1/2)]$')
    options('Bmax_' + surfix, 'ztitle', '$[pT/Hz^(1/2)]$')
    options('Emax_lines_' + surfix, 'ysubtitle', '$[mV/m/Hz^(1/2)]$')
elif surfix == 'Pwr':
    options('Emax_' + surfix, 'zrange', [1e-10, 100])
    options('Bmax_' + surfix, 'zrange', [1e-10, 100])
    options('Emax_lines_' + surfix, 'yrange', [1e-6, 100])
    options('Emax_' + surfix, 'ztitle', '$[(mV/m)^2/Hz]$')
    options('Bmax_' + surfix, 'ztitle', '$[pT^2/Hz]$')
    options('Emax_lines_' + surfix, 'ysubtitle', '$[(mV/m)^2/Hz]$')
options(['Emax_' + surfix, 'Bmax_' + surfix], 'yrange', [1, 2e4])
options(['Emax_' + surfix, 'Bmax_' + surfix], 'ysubtitle', 'freq [Hz]')
options('Emax_lines_' + surfix, 'ylog', 1)
options('Emax_lines_' + surfix, 'legend_names', ["3.16 Hz", "5.62 Hz", "10 Hz", "17.6 Hz",
                                                 "31.6 Hz", "56.2 Hz", "100 Hz", "176 Hz",
                                                 "316 Hz", "562 Hz"])
options('Emax_lines_' + surfix, 'Color', color_table)
options('akb_ALT', 'ylabel', 'ALT [km]')
options('akb_MLT', 'ylabel', 'MLT [h]')
options('akb_ILAT', 'ylabel', 'ILAT [deg]')
tplot_options('wsize', [500, 100000])
tplot_options('title', hemisphere+str(int(Passname)) + ' MCA ' + surfix)
tplot_options('axis_font_size', 8)
tplot_options('var_label', ["3.16 Hz", "5.62 Hz", "10 Hz", "17.6Hz",
                            "31.6 Hz", "56.2 Hz", "100 Hz", "176 Hz",
                            "316 Hz", "562 Hz"])
tplot(['Bmax_' + surfix, 'Emax_' + surfix, 'Emax_lines_' + surfix], 
      var_label = ['akb_ALT', 'akb_MLT', 'akb_ILAT'], 
      save_png = dir + 'akb-' + hemisphere+str(int(Passname))+'-MCA-'+ surfix + 'wsize_test',
      xsize=16, ysize=10)

