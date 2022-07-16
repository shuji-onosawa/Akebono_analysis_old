import pyspedas
import pytplot
from pytplot import options, tplot, tlimit, tplot_options, get_data, store_data
import numpy as np
from load import mca, orb

ILAT_min = 55
start_day_string = '1991-01-01'
start_day_time_double = pyspedas.time_double(start_day_string)
seconds_per_day = 86400
day_list = []
for i in range(0, 365):
    time_double = start_day_time_double + i * seconds_per_day
    day_list.append(pyspedas.time_string(time_double, fmt='%Y-%m-%d %H:%M:%S'))

for k in range(len(day_list)-1):
    
    trange = [day_list[k], day_list[k+1]]
    print(trange)
    
    mca(trange= trange)
    orb(trange= trange)
    pyspedas.omni.data(trange = trange, level = 'hro', datatype='1min')
    
    IMFx_tvar = pytplot.get_data('BX_GSE')
    IMFy_tvar = pytplot.get_data('BY_GSM')
    IMFz_tvar = pytplot.get_data('BZ_GSM')

    time = IMFx_tvar.times
    IMFx = IMFx_tvar.y
    IMFy = IMFy_tvar.y
    IMFz = IMFz_tvar.y

    IMF_matrix = [IMFx,
                  IMFy,
                  IMFz]
    IMF_matrix = np.array(IMF_matrix).T
    pytplot.store_data('IMF', data = {'x':time, 'y':IMF_matrix})
    
    tplot_names = pytplot.tplot_names(True)

    #dB to amplitude
    for i in range(4):
        tplot_variable = pytplot.get_data(tplot_names[i])
        tplot_variable_float = (tplot_variable.y).astype(float)
        np.place(tplot_variable_float, tplot_variable_float == 254, np.nan)
        tplot_variable_0dB = 1e-6 #mV or pT
        bandwidth = tplot_variable.v * 0.3
        tplot_variable_amplitude = (10**(tplot_variable_float/20)) * (tplot_variable_0dB)  / np.sqrt(bandwidth)
        tplot_variable_power = (10**(tplot_variable_float/10)) * ((tplot_variable_0dB)**2)  / bandwidth
        pytplot.store_data(tplot_names[i] +'_Amp', data={'x': tplot_variable.times, 'y': tplot_variable_amplitude, 'v': tplot_variable.v})
        pytplot.store_data(tplot_names[i] +'_Pwr', data={'x': tplot_variable.times, 'y': tplot_variable_power, 'v': tplot_variable.v})

    #Time interpolate
    pyspedas.tinterpol('akb_ILAT', interp_to='Emax_Pwr', newname = 'ILAT')
    pyspedas.tinterpol('akb_MLAT', interp_to='Emax_Pwr', newname = 'MLAT')
    pyspedas.tinterpol('akb_Pass', interp_to='Emax_Pwr', newname = 'Pass', method = 'nearest')
    pyspedas.tinterpol('akb_ALT', interp_to='Emax_Pwr', newname = 'ALT')
    #Limit ILAT range
    Emax = get_data('Emax_Pwr')
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

    north_start_time_index = np.array(north_start_time_index)
    north_end_time_index = np.array(north_end_time_index)

    north_start_time_list = pyspedas.time_string(time[north_start_time_index], fmt='%Y-%m-%d %H:%M:%S')
    north_end_time_list = pyspedas.time_string(time[north_end_time_index], fmt='%Y-%m-%d %H:%M:%S')

    south_start_time_index = [south_index[0]]
    south_end_time_index = []
    for i in range(south_index.size-1):
        if south_index[i+1] - south_index[i] > 1:
            south_end_time_index.append(south_index[i])
            south_start_time_index.append(south_index[i+1])
            
    south_end_time_index.append(south_index[-1])

    south_start_time_index = np.array(south_start_time_index)
    south_end_time_index = np.array(south_end_time_index)

    south_start_time_list = pyspedas.time_string(time[south_start_time_index], fmt='%Y-%m-%d %H:%M:%S')
    south_end_time_list = pyspedas.time_string(time[south_end_time_index], fmt='%Y-%m-%d %H:%M:%S')


    start_time_list_list = [north_start_time_list, south_start_time_list]
    end_time_list_list = [north_end_time_list, south_end_time_list]


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
    Emax_channel11 = Emax.y.T[10] #1000 Hz

    Amp_data = [Emax_channel1, 
                Emax_channel2, 
                Emax_channel3, 
                Emax_channel4, 
                Emax_channel5,
                Emax_channel6,
                Emax_channel7,
                Emax_channel8,
                Emax_channel9,
                Emax_channel10,
                Emax_channel11]

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
    Emax_channel11 = Emax.y.T[10] #1000 Hz

    Pwr_data = [Emax_channel1, 
                Emax_channel2, 
                Emax_channel3, 
                Emax_channel4, 
                Emax_channel5,
                Emax_channel6,
                Emax_channel7,
                Emax_channel8,
                Emax_channel9,
                Emax_channel10,
                Emax_channel11]

    store_data(name = 'Emax_lines_Pwr', 
            data={'x': time,
                    'y': np.array(Pwr_data).T})


    #make Passname list corresponding with start(end) time list
    Passname = get_data('Pass')
    Passname = Passname.y
    north_Passname_list = Passname[north_start_time_index]
    south_Passname_list = Passname[south_start_time_index]

    Passname_list_list = [north_Passname_list, south_Passname_list]

    dir_list = ['./akb_North_mca_plot/', './akb_South_mca_plot/']
    hemisphere_list = ['N', 'S']
    surfix = 'Pwr'

    #make color table for line plots
    color_table = ['red', 'yellow', 'blue', 'green',
                'crimson', 'y', 'dodgerblue', 'lime',
                'deeppink', 'orange', 'c']

    #plot
    for i in range(2):
        dir = dir_list[i]
        hemisphere = hemisphere_list[i]
        start_time_list = start_time_list_list[i]
        end_time_list = end_time_list_list[i]
        Passname_list = Passname_list_list[i]

        for j in range(len(start_time_list)):
            start_time = start_time_list[j]
            end_time = end_time_list[j]

            year = start_time[:4]
            Month = start_time[5:7]
            day = start_time[8:10]
            hour = start_time[11:13]
            minute = start_time[14:16]
            second = start_time[17:19]

            Passname = Passname_list[j]
            Passname = str(int(Passname))
            Passname = Passname[-4:]
            
            #dict event case
            pyspedas.time_clip('Emax_Pwr', time_start=start_time, time_end = end_time, new_names='Emax_Pwr_clip')
            Emax_cliped = get_data('Emax_Pwr_clip')
            Emax_10Hz = Emax_cliped.y.T[2]
            event_case=''
            if np.nanmax(Emax_10Hz) >=10:
                event_case = 'super_strong'
            elif np.nanmax(Emax_10Hz) >=1:
                event_case = 'strong'
            
            tlimit([start_time, end_time])
            options(['Emax_' + surfix, 'Bmax_' + surfix], 'spec', 1)
            options(['Emax_' + surfix, 'Bmax_' + surfix], 'ylog', 1)
            options(['Emax_' + surfix, 'Bmax_' + surfix], 'zlog', 1)
            #options(['Emax_' + surfix, 'Bmax_' + surfix], 'Colormap', 'viridis')
            if surfix == 'Amp':
                options('Emax_' + surfix, 'zrange', [1e-5, 10])
                options('Bmax_' + surfix, 'zrange', [1e-5, 10])
                options('Emax_lines_' + surfix, 'yrange', [1e-3, 10])
                options('Emax_' + surfix, 'ztitle', '$[mV/m/Hz^(1/2)]$')
                options('Bmax_' + surfix, 'ztitle', '$[pT/Hz^(1/2)]$')
                options('Emax_lines_' + surfix, 'ysubtitle', '$[mV/m/Hz^(1/2)]$')
            elif surfix == 'Pwr':
                options('Emax_' + surfix, 'zrange', [1e-10, 100])
                options('Bmax_' + surfix, 'zrange', [1e-8, 1e6])
                options('Emax_lines_' + surfix, 'yrange', [1e-6, 100])
                options('Emax_' + surfix, 'ztitle', '$[(mV/m)^2/Hz]$')
                options('Bmax_' + surfix, 'ztitle', '$[pT^2/Hz]$')
                options('Emax_lines_' + surfix, 'ysubtitle', '$[(mV/m)^2/Hz]$')
            options(['Emax_' + surfix, 'Bmax_' + surfix], 'yrange', [1, 2e4])
            options(['Emax_' + surfix, 'Bmax_' + surfix], 'ysubtitle', 'freq [Hz]')
            options('Emax_lines_' + surfix, 'ylog', 1)
            options('Emax_lines_' + surfix, 'legend_names', ["3.16 Hz", "5.62 Hz", "10 Hz", "17.6 Hz",
                                                            "31.6 Hz", "56.2 Hz", "100 Hz", "176 Hz",
                                                            "316 Hz", "562 Hz", "1000 Hz"])
            options('Emax_lines_' + surfix, 'Color', color_table)
            options('ALT', 'ytitle', 'ALT [km]')
            options('akb_MLT', 'ytitle', 'MLT [h]')
            options('ILAT', 'ytitle', 'ILAT [deg]')
            
            omni_data_names = ['SYM_H', 'IMF', 'flow_speed', 'proton_density', 'Pressure', 'E']
            options(omni_data_names, 'panel_size', 0.5)
            options('IMF', 'legend_names', ['IMF x', "IMF y", "IMF z"])
            options('SYM_H', 'ytitle', 'SYM-H')
            options('SYM_H', 'ysubtitle', '[nT]')
            options('flow_speed', 'ytitle', 'flow \n speed')
            options('flow_speed', 'ysubtitle', '[km/s]')
            options('proton_density', 'ytitle', 'proton \n density')
            options('Pressure', 'ytitle', 'flow \n pressure')
            options('E', 'ytitle', 'E_sw')
            options('E', 'ysubtitle', 'mV/m')

            tplot_options('title', Passname + hemisphere + '_' + year+Month+day+ ' MCA ' + surfix)
            tplot_options('var_label', ["3.16 Hz", "5.62 Hz", "10 Hz", "17.6Hz",
                                        "31.6 Hz", "56.2 Hz", "100 Hz", "176 Hz",
                                        "316 Hz", "562 Hz", '1000 Hz'])
            if event_case =='super_strong':
                tplot(['IMF', 'flow_speed', 'proton_density', 'Pressure', 'E','Bmax_' + surfix, 'Emax_' + surfix, 'Emax_lines_' + surfix, 'SYM_H'], 
                var_label = ['ALT', 'akb_MLT', 'ILAT'], 
                save_png = dir + 'super_strong_event/' + 'akb-orbit0'+Passname + hemisphere +'_'+ year + Month + day + '_' + hour + minute + second,
                xsize=14, ysize=16,
                display=False)
            if event_case =='strong':
                tplot(['IMF', 'flow_speed', 'proton_density', 'Pressure', 'E','Bmax_' + surfix, 'Emax_' + surfix, 'Emax_lines_' + surfix, 'SYM_H'], 
                var_label = ['ALT', 'akb_MLT', 'ILAT'], 
                save_png = dir + 'strong_event/' + 'akb-orbit0'+Passname + hemisphere +'_'+ year + Month + day + '_' + hour + minute + second,
                xsize=14, ysize=16,
                display=False)
    tplot_names = pytplot.tplot_names(True)
    pytplot.store_data(tplot_names, delete=True)
    print(pytplot.tplot_names())
