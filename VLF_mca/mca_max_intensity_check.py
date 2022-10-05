import load
from pytplot import get_data
from pyspedas import tinterpol
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def mca_intensity_distribution_plot(start_date, end_date, field):

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
        
        field_tvar = get_data(field + 'max')
        field_array = field_tvar.y
        field_array_T = field_array.T
        field_list = field_array_T.tolist()

        freq_array = np.array([3.16, 5.62, 10.0, 17.8,
                            31.6, 56.2, 100,  178,
                            316,  562,  1000, 1780,
                            3160, 5620, 10000,17800])
        intensity_array = np.arange(1,255)

        matrix_per_day = np.empty((freq_array.size, intensity_array.size), dtype = int)

        for ch in range(freq_array.size):
            for intensity in range(intensity_array.size):
                matrix_per_day[ch][intensity] = field_list[ch].count(intensity)

        matrix = matrix + matrix_per_day

    fig = plt.figure(figsize=(15, 12))
    ax1 = fig.add_subplot(3,1,1)
    for i in range(6):
        ax1.plot(intensity_array, matrix[i], label = str(freq_array[i])+' Hz')
    ax1.set_ylabel('Count')
    ax1.legend()
    ax1.set_title('Akebono VLF/MCA '+ field + 'field '+start_date + ' ' + end_date)
    
    ax2 = fig.add_subplot(3,1,2)
    for i in range(5):
        ax2.plot(intensity_array, matrix[i+6], label = str(freq_array[i+6])+' Hz')
    ax2.set_ylabel('Count')
    ax2.legend()
    
    ax3 = fig.add_subplot(3,1,3)
    for i in range(5):
        ax3.plot(intensity_array, matrix[i+11], label = str(freq_array[i+11]) + ' Hz')
    ax3.set_ylabel('Count')
    ax3.set_xlabel('Intensity [dB]')
    ax3.legend()

    plt.savefig('./plots/mca_intensity_distribution/mca_' + field + 'field_' + start_date+'_'+end_date)
    plt.clf()
    plt.close()

import pandas as pd

date_list = pd.date_range(start='1989-01-01', end='2014-01-01', freq='YS')
date_list = np.datetime_as_string(date_list, unit='D')
date_list = date_list.astype(object)

for i in range(date_list.size-1):
    mca_intensity_distribution_plot(start_date=date_list[i], end_date=date_list[i+1], field='E')
    mca_intensity_distribution_plot(start_date=date_list[i], end_date=date_list[i+1], field='B')
    
