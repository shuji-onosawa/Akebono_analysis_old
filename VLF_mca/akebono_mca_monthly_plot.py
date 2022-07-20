import pyspedas
from pytplot import get_data, store_data, tplot_names, tplot
from pyspedas import time_clip, time_double, time_string, tinterpol
import numpy as np
from load import mca, orb

day = 31
unit_time_width = 3600 #1h
lat_array = np.arange(55, 90)

matrix = []

start_time = time_double('1990-01-20 00:00:00')
end_time = start_time+day*24*unit_time_width

days = np.arange(start_time, end_time + 24*unit_time_width, 24*unit_time_width, float)
days_string = time_string(days, fmt= '%Y-%m-%d %H:%M:%S')

for i in range(days_string.size):
    trange = [days_string[i], days_string[i+1]]
    mca(trange)
    orb(trange)
    tplot_name = ['Emax', 'Eave', 'Bmax', 'Bave']
    for i in range(4):
            tplot_variable = get_data(tplot_name[i])
            tplot_variable_float = (tplot_variable.y).astype(float)
            np.place(tplot_variable_float, tplot_variable_float == 254, np.nan)
            tplot_variable_0dB = 1e-6 #mV or pT
            bandwidth = tplot_variable.v * 0.3
            tplot_variable_amplitude = (10**(tplot_variable_float/20)) * (tplot_variable_0dB)  / np.sqrt(bandwidth)
            tplot_variable_power = (10**(tplot_variable_float/10)) * ((tplot_variable_0dB)**2)  / bandwidth
            store_data(tplot_name[i] +'_Amp', data={'x': tplot_variable.times, 'y': tplot_variable_amplitude, 'v': tplot_variable.v})
            store_data(tplot_name[i] +'_Pwr', data={'x': tplot_variable.times, 'y': tplot_variable_power, 'v': tplot_variable.v})
            
    tinterpol('akb_ILAT', interp_to='Emax', newname = 'ILAT')
    tinterpol('akb_MLAT', interp_to='Emax', newname = 'MLAT')
    tinterpol('akb_MLT', interp_to='Emax', newname = 'MLT', method = 'nearest')

    start_time_hour = time_double(days_string[i])
    hours = time_string(np.arange(start_time_hour, start_time_hour + 25*unit_time_width, unit_time_width))
    for j in range(hours.size):
        time_clip('Emax_Pwr', time_start=hours[j], time_end=hours[j+1], new_names='Emax_Pwr_cliped')
        time_clip('ILAT', time_start=hours[j], time_end=hours[j+1], new_names='ILAT_cliped')
        time_clip('MLT', time_start=hours[j], time_end=hours[j+1], new_names='MLT_cliped')
        time_clip('MLAT', time_start=hours[j], time_end=hours[j+1], new_names='MLAT_cliped')
        print(hours[j])
        Emax_pwr = get_data('Emax_Pwr_cliped')
        Emax_pwr = Emax_pwr.y.T[0] #3.16Hz
        ILAT = get_data('ILAT_cliped')
        ILAT = ILAT.y
        MLAT = get_data('MLAT_cliped')
        MLAT = MLAT.y
        MLT_t = get_data('MLT_cliped')
        MLT = MLT_t.y
        Emax = get_data('Emax_Pwr_cliped')

        pwr_list_per_hour = []
        for lat in lat_array:
            index_tuple = np.where((MLAT>0) & (ILAT<lat+1) & (ILAT>lat)) 
            index = index_tuple[0]
            try:
                ILAT_a = ILAT[index[0]]
                ILAT_b = ILAT[index[-1]]
                Emax_1deg = Emax_pwr[index[0]:index[-1]]
                print('pwr:', np.nanmax(Emax_1deg))
                pwr_list_per_hour.append(np.nanmean(Emax_1deg))
            except Exception as e:
                print(e)
                north_pwr_list_per_hour.append(np.nan)
    len(north_pwr_list_per_hour)