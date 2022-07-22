from cmath import nan
import pyspedas
from pytplot import get_data, store_data, tplot_names, tplot, options, tlimit
from pyspedas import time_clip, time_double, time_string, tinterpol
import numpy as np
from load import mca, orb

day = 1
seconds_per_day = 86400
unit_time_hour = 1
unit_time_width = 3600 * unit_time_hour
unit_per_day = seconds_per_day/(unit_time_width)
lat_array = np.arange(55, 90)

freq_channel_index = 0

matrix = []

start_time = time_double('1989-03-10 00:00:00')
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
            
    tinterpol('akb_ILAT', interp_to='Emax', newname = 'ILAT')
    tinterpol('akb_MLAT', interp_to='Emax', newname = 'MLAT')
    tinterpol('akb_MLT', interp_to='Emax', newname = 'MLT', method = 'nearest')

    start_time_hour = time_double(days_string[i])
    hours = np.arange(start_time_hour, start_time_hour + (unit_per_day + 1)*unit_time_width, unit_time_width)
    
    Emax_pwr = get_data('Emax_pwr')
    ILAT = get_data('ILAT')
    MLAT = get_data('MLAT')
    MLT = get_data('MLT')
    
    #in north hemisphere
    for j in range(2):
        pwr_list_per_hour = []
        for lat in lat_array:
            index_tuple = np.where((hours[j] <= Emax_pwr.times) & (Emax_pwr.times < hours[j+1]) & (ILAT.y > lat) & (ILAT.y < lat+1) & (MLAT.y<0))
            index = index_tuple[0] 
            ilat = ILAT.y[index]
            mlat = MLAT.y[index]
            mlt = MLT.y[index]
            if len(index) == 0:
                pwr_list_per_hour.append(np.nan)
            else:
                Emax_pwr_1deg = Emax_pwr.y.T[0][index]
            
                pwr_list_per_hour.append(np.nanmax(Emax_pwr_1deg))
                print(np.nanmax(Emax_pwr_1deg))
            
        matrix.append(pwr_list_per_hour)
    print(matrix)
    
            




'''
    for j in range(len(hours)-1):
        pwr_list_per_hour = []
        for lat in lat_array:
            index_tuple = np.where((hours[j] <= Emax_pwr.times) & (hours[j+1] > Emax_pwr.times))
            index = index_tuple[0] 
            print(index)
            Emax_pwr_1h = Emax_pwr.y.T[0][index]
            ilat = ILAT.y[index]
            mlat = MLAT.y[index]
            mlt = MLT.y[index]
            
            try:
                Emax_1deg = Emax_pwr.y.T[freq_channel_index][index]               
                pwr_list_per_hour.append(np.nanmax(Emax_1deg))
            except Exception as e:
                print(e)
                pwr_list_per_hour.append(np.nan)
        matrix.append(pwr_list_per_hour)
    

times = np.arange(start_time, end_time, unit_time_width, dtype=float)
print(np.array(matrix).shape)
print(times.size)
print(lat_array.size)

store_data('Epwr_monthly', data={'x':times, 'y':matrix, 'v':lat_array})

pyspedas.omni.data([start_time, end_time], datatype='1min', level='hro', no_update=True)
#options('Epwr_monthly', 'zrange',[1e-4, 1] )
options('Epwr_monthly', 'spec', 1)
options('Epwr_monthly', 'zlog', 1)
options('MLAT', 'yrange', [-90, 0])
#omni_var_name = ['BZ_GSM', 'flow_speed', 'proton_density', 'Pressure', 'SYM_H']
#options(omni_var_name, 'panel_size', 0.5)
tplot(['Epwr_monthly', 'MLAT'], xsize=16, ysize = 18, save_png='north_mca_monthly_2h_omni_max_test2')
'''