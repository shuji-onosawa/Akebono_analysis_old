from cmath import nan
import pyspedas
from pytplot import get_data, store_data, tplot_names, tplot, options, tplot_options
from pyspedas import time_clip, time_double, time_string, tinterpol
import numpy as np
from load import mca, orb

day = 30
freq_channel_index = 2
channels = ["3.16 Hz", "5.62 Hz", "10 Hz", "17.6 Hz",
            "31.6 Hz", "56.2 Hz", "100 Hz", "176 Hz",
            "316 Hz", "562 Hz", "1 kHz", '1.76 kHz']
unit_time_hour = 2
hemisphere = 'south'


seconds_per_day = 86400
unit_time_width = 3600 * unit_time_hour
unit_per_day = seconds_per_day/(unit_time_width)
lat_array = np.arange(55, 90)

matrix = []
start_time_string = '1989-03-6 00:00:00'
start_time = time_double(start_time_string)
end_time = start_time+day*seconds_per_day

days = np.arange(start_time, end_time + seconds_per_day, seconds_per_day, float)
days_string = time_string(days, fmt= '%Y-%m-%d %H:%M:%S')

for i in range(len(days_string)-1):
    trange = [days_string[i], days_string[i+1]]
    mca(trange)
    orb(trange)
    tplot_name = ['Emax', 'Eave', 'Bmax', 'Bave']
    for k in range(4):
            tplot_variable = get_data(tplot_name[k])
            tplot_variable_float = (tplot_variable.y).astype(float)
            np.place(tplot_variable_float, tplot_variable_float == 254, np.nan)
            tplot_variable_0dB = 1e-6 #mV or pT
            bandwidth = tplot_variable.v * 0.3
            tplot_variable_amplitude = (10**(tplot_variable_float/20)) * (tplot_variable_0dB)  / np.sqrt(bandwidth)
            tplot_variable_power = (10**(tplot_variable_float/10)) * ((tplot_variable_0dB)**2)  / bandwidth
            store_data(tplot_name[k] +'_amp', data={'x': tplot_variable.times, 'y': tplot_variable_amplitude, 'v': tplot_variable.v})
            store_data(tplot_name[k] +'_pwr', data={'x': tplot_variable.times, 'y': tplot_variable_power, 'v': tplot_variable.v})
            
    tinterpol('akb_ILAT', interp_to='Emax', newname = 'ILAT', )
    tinterpol('akb_MLAT', interp_to='Emax', newname = 'MLAT')
    tinterpol('akb_MLT', interp_to='Emax', newname = 'MLT', method = 'nearest')

    start_time_hour = time_double(days_string[i])
    hours = np.arange(start_time_hour, start_time_hour + (unit_per_day + 1)*unit_time_width, unit_time_width)
    
    Emax_pwr = get_data('Emax_pwr')
    ILAT = get_data('ILAT')
    MLAT = get_data('MLAT')
    MLT = get_data('MLT')
    
    #in north hemisphere
    for j in range(hours.size-1):
        pwr_list_per_hour = []
        for lat in lat_array:
            if hemisphere == 'north':
                index_tuple = np.where((hours[j] <= Emax_pwr.times) & (Emax_pwr.times < hours[j+1]) 
                                       & (ILAT.y > lat) & (ILAT.y < lat+1) 
                                       #& (10 <= MLT.y) & (MLT.y <= 14)
                                       & (MLAT.y>0))
                                       
            elif hemisphere == 'south':
                index_tuple = np.where((hours[j] <= Emax_pwr.times) & (Emax_pwr.times < hours[j+1]) 
                                       & (ILAT.y > lat) & (ILAT.y < lat+1) 
                                       #& (10 <= MLT.y) & (MLT.y <= 14)
                                       & (MLAT.y<0))
            index = index_tuple[0] 
            if len(index) == 0:
                pwr_list_per_hour.append(np.nan)
            else:
                Emax_pwr_1deg = Emax_pwr.y.T[freq_channel_index][index]
            
                pwr_list_per_hour.append(np.nanmax(Emax_pwr_1deg))
           
        matrix.append(pwr_list_per_hour)
    
times = np.arange(start_time, end_time, unit_time_width, dtype=float)

store_data('Epwr_monthly', data={'x':times, 'y':matrix, 'v':lat_array})

pyspedas.omni.data([start_time, end_time], datatype='1min', level='hro', no_update=True)
options('Epwr_monthly', 'spec', 1)
options('Epwr_monthly', 'zlog', 1)
options('Epwr_monthly', 'zrange', [1e-10, 1])
options('Epwr_monthly', 'ztitle', 'PSD \n [(mV/m)^2/Hz]')
options('Epwr_monthly', 'ytitle', 'ILAT \n [deg]')

omni_var_name = ['BZ_GSM', 'flow_speed', 'proton_density', 'Pressure', 'SYM_H']
options(omni_var_name, 'panel_size', 0.5)

tplot_options('title','AKEBONO/MCA Ew Power Spectral Density @' + hemisphere + channels[freq_channel_index]
              + '\n' + start_time_string)
tplot(['SYM_H', 'Epwr_monthly'], save_png=hemisphere + '_mca_monthly_2h_omni_test')


