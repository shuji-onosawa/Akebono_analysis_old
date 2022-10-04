import load
from pytplot import get_data
from pyspedas import tinterpol
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

start_date = '1989-03-05'
end_date = '1989-03-10'

date_list = pd.date_range(start=start_date, end=end_date, freq='D')
date_list = np.datetime_as_string(date_list, unit='D')
date_list = date_list.astype(object)

matrix = np.zeros((16, 254))
for i in range(date_list.size-1):
    load.mca([date_list[i], date_list[i+1]], del_invalid_data=False)
    
    #load.orb([date_list[i], date_list[i+1]])
    #tinterpol('akb_ILAT', interp_to = 'Emax', newname = 'ILAT')
    #tinterpol('akb_MLAT', interp_to = 'Emax', newname = 'MLAT')
    #tinterpol('akb_MLT', interp_to = 'Emax', newname = 'MLT', method = 'nearest')
    #tinterpol('akb_ALT', interp_to = 'Emax', newname = 'ALT')
    
    Emax_tvar = get_data('Emax')
    Emax_array = Emax_tvar.y
    Emax_array_T = Emax_array.T
    Emax_list = Emax_array_T.tolist()

    freq_array = np.array([3.16, 5.62, 10.0, 17.8,
                           31.6, 56.2, 100,  178,
                           316,  562,  1000, 1780,
                           3160, 5620, 10000,17800])
    intensity_array = np.arange(1,255)

    matrix_per_day = np.empty((freq_array.size, intensity_array.size), dtype = int)

    for ch in range(freq_array.size):
        for intensity in range(intensity_array.size):
            matrix_per_day[ch][intensity] = Emax_list[ch].count(intensity)

    matrix = matrix + matrix_per_day

fig = plt.figure(figsize=(15, 6))
ax = fig.add_subplot(1,1,1)
for i in range(16):
    ax.plot(intensity_array, matrix[i], label = 'ch'+str(i+1))

ax.set_xlabel('Intensity [dB]')
ax.set_ylabel('Count')    
plt.legend(loc='center left', bbox_to_anchor=(1, 0.2, 0.5, 0.5))
plt.savefig('./plots/mca_intensity_distribution/test')
plt.show()

