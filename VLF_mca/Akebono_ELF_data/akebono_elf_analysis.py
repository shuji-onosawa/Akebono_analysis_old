from pytplot import cdf_to_tplot, get_data, store_data, options, tplot, tlimit
import numpy as np

cdf_to_tplot('ak_h1_elf_19900211_v03.cdf')
E = get_data('dE_wav_narrow')

maxE, minE = max(E.y), min(E.y)
time_delta = 1 #s
time_array = np.arange(E.times[0], E.times[0]+int(24*3600/time_delta), time_delta)

saturation_rate = np.empty(time_array.size)

for i in range(time_array.size-1):
    time_index = np.where((E.times >= time_array[i]) & (E.times < time_array[i+1]))
    E_for_time_delta = E.y[time_index]
    
    maxE_index = np.where(E_for_time_delta==maxE)
    minE_index = np.where(E_for_time_delta==minE)
    
    print(time_array[i], maxE_index, minE_index)
    try:
        saturation_rate[i] = (maxE_index[0].size + minE_index[0].size)/time_index[0].size
    except:
        saturation_rate[i] = np.nan

store_data('saturation_rate', data={'x':time_array, 'y':saturation_rate})

Efield = E.y/(30*(-2.15)*20)
store_data('dE_waveform_narrow', data={'x':E.times, 'y':Efield})
options('dE_waveform_narrow', 'yrange', [-1.5, 1.5])
tlimit(['1990-02-11 18:00:00', '1990-02-11 18:15:00'])
tplot(['dE_waveform_narrow','saturation_rate'], save_png='elf_saturation_rate')