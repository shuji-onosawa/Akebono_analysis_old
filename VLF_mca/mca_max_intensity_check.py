import load
from pytplot import get_data
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def mca_intensity_distribution_plot(start_date, end_date, del_inst_interference):

    date_list = pd.date_range(start=start_date, end=end_date, freq='D')
    date_list = np.datetime_as_string(date_list, unit='D')
    date_list = date_list.astype(object)

    del_invalid_data = del_inst_interference
    E_matrix = np.zeros((16, 254))
    B_matrix = np.zeros((16, 254))
    freq_array = np.array([3.16, 5.62, 10.0, 17.8,
                           31.6, 56.2, 100,  178,
                           316,  562,  1000, 1780,
                           3160, 5620, 10000,17800])
    intensity_array = np.arange(1,255)
    
    for i in range(date_list.size-1):
        
        load.mca([date_list[i], date_list[i+1]], del_invalid_data=del_invalid_data)
        
        #load.orb([date_list[i], date_list[i+1]])
        #tinterpol('akb_ILAT', interp_to = 'Emax', newname = 'ILAT')
        #tinterpol('akb_MLAT', interp_to = 'Emax', newname = 'MLAT')
        #tinterpol('akb_MLT', interp_to = 'Emax', newname = 'MLT', method = 'nearest')
        #tinterpol('akb_ALT', interp_to = 'Emax', newname = 'ALT')
        
        E_tvar = get_data('Emax')
        if E_tvar is None:
            print('cdf of ' + date_list[i] + ' has no data')
            continue
        E_array = E_tvar.y
        E_array_T = E_array.T
        E_list = E_array_T.tolist()

        B_tvar = get_data('Bmax')
        B_array = B_tvar.y
        B_array_T = B_array.T
        B_list = B_array_T.tolist()

        E_matrix_per_day = np.empty((freq_array.size, intensity_array.size), dtype = int)
        B_matrix_per_day = np.empty((freq_array.size, intensity_array.size), dtype = int)
        
        for ch in range(freq_array.size):
            for intensity in range(intensity_array.size):
                E_matrix_per_day[ch][intensity] = E_list[ch].count(intensity)
                B_matrix_per_day[ch][intensity] = B_list[ch].count(intensity)
        
        E_matrix = E_matrix + E_matrix_per_day
        B_matrix = B_matrix + B_matrix_per_day

    fig = plt.figure(figsize=(15, 12))
    ax1 = fig.add_subplot(3,1,1)
    for i in range(6):
        ax1.plot(intensity_array, E_matrix[i], label = str(freq_array[i])+' Hz')
    ax1.set_ylabel('Count')
    ax1.legend()
    ax1.set_title('Akebono VLF/MCA ' + 'Efield '+start_date + ' ' + end_date)
    
    ax2 = fig.add_subplot(3,1,2)
    for i in range(5):
        ax2.plot(intensity_array, E_matrix[i+6], label = str(freq_array[i+6])+' Hz')
    ax2.set_ylabel('Count')
    ax2.legend()
    
    ax3 = fig.add_subplot(3,1,3)
    for i in range(5):
        ax3.plot(intensity_array, E_matrix[i+11], label = str(freq_array[i+11]) + ' Hz')
    ax3.set_ylabel('Count')
    ax3.set_xlabel('Intensity [dB]')
    ax3.legend()

    plt.savefig('./plots/mca_intensity_distribution/mca_' + 'Efield_' + start_date+'_'+end_date)
    plt.clf()
    plt.close()
    
    fig = plt.figure(figsize=(15, 12))
    ax1 = fig.add_subplot(3,1,1)
    for i in range(6):
        ax1.plot(intensity_array, B_matrix[i], label = str(freq_array[i])+' Hz')
    ax1.set_ylabel('Count')
    ax1.legend()
    subtitle = ''
    for i in range(len(del_invalid_data)):
        subtitle = subtitle + ' ' + del_invalid_data[i]
    ax1.set_title('Akebono VLF/MCA ' + 'Bfield '+start_date + ' ' + end_date)
    
    ax2 = fig.add_subplot(3,1,2)
    for i in range(5):
        ax2.plot(intensity_array, B_matrix[i+6], label = str(freq_array[i+6])+' Hz')
    ax2.set_ylabel('Count')
    ax2.legend()
    
    ax3 = fig.add_subplot(3,1,3)
    for i in range(5):
        ax3.plot(intensity_array, B_matrix[i+11], label = str(freq_array[i+11]) + ' Hz')
    ax3.set_ylabel('Count')
    ax3.set_xlabel('Intensity [dB]')
    ax3.legend()

    plt.savefig('./plots/mca_intensity_distribution/mca_' + 'Bfield_' + start_date+'_'+end_date)
    plt.clf()
    plt.close()


mca_intensity_distribution_plot(start_date='1989-03-05', end_date='2015-04-22', del_inst_interference=['off', 'noisy', 'sms', 'bit rate m', 'bdr', 'pws'])    
