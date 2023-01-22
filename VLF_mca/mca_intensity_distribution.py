import load
from pytplot import get_data
from pyspedas import tinterpol
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker



def mca_intensity_distribution_plot(start_date, end_date, del_inst_interference, alt_range = [0, 11000], suffix = ''):

    date_list = pd.date_range(start=start_date, end=end_date, freq='D')
    date_list = np.datetime_as_string(date_list, unit='D')
    date_list = date_list.astype(object)

    del_invalid_data = del_inst_interference
    E_matrix = np.zeros((16, 255))
    E_sms_matrix = np.zeros((16, 255))
    B_matrix = np.zeros((16, 255))
    B_sms_matrix = np.zeros((16, 255))
    
    freq_array = np.array([3.16, 5.62, 10.0, 17.8,
                           31.6, 56.2, 100,  178,
                           316,  562,  1000, 1780,
                           3160, 5620, 10000,17800])
    intensity_array = np.arange(0,255) #0 - 254 dB
    
    for i in range(date_list.size-1):
        print(date_list[i])
        load.mca([date_list[i], date_list[i+1]], del_invalid_data=del_invalid_data)
        try:
            load.orb([date_list[i], date_list[i+1]])
        except:
            continue
        
        try:
            tinterpol('akb_ILAT', 'Emax')
        except:
            print('data lack in orbit data')
            continue
        tinterpol('akb_MLAT', 'Emax')
        tinterpol('akb_MLT', 'Emax')
        tinterpol('akb_ALT', 'Emax')

        postgap = get_data('PostGap')
        sms_flag_array = np.empty([postgap.y.size])
        for flag_index in range(postgap.y.size):
            postgap_str = format(postgap.y[flag_index], '08b')
            sms_flag_array[flag_index] = int(postgap_str[2])

        sms_on_tuple = np.where(sms_flag_array==1)
        sms_on_indices = sms_on_tuple[0]
        if sms_on_indices.size == 0:
            continue
        sms_start_indices = [sms_on_indices[0]]
        sms_end_indices = []
        
        for sms_index in range(sms_on_indices.size-1):
            if sms_on_indices[sms_index+1]-sms_on_indices[sms_index] > 15:
                sms_end_indices.append(sms_on_indices[sms_index])
                sms_start_indices.append(sms_on_indices[sms_index+1])
        sms_end_indices.append(sms_on_indices[-1])
    
        E_tvar = get_data('Emax')
        E_array = E_tvar.y
        #E_sms_array = np.copy(E_tvar.y)
        B_tvar = get_data('Bmax')
        B_array = B_tvar.y
        #B_sms_array = np.copy(B_tvar.y)
        
        ilat = get_data('akb_ILAT-itrp')
        mlt = get_data('akb_MLT-itrp')
        alt = get_data('akb_ALT-itrp')
        
        index_of_data_in_target_region = np.where((ilat.y >= 60)&(10 <= mlt.y)&(mlt.y <= 14)&(alt.y >= alt_range[0])&(alt.y <= alt_range[1]))
        index_of_data_in_target_region = index_of_data_in_target_region[0]
        '''
        for sms_time_index in range(len(sms_start_indices)):
            E_array[sms_start_indices[sms_time_index]:sms_end_indices[sms_time_index] + 1] = np.nan
            B_array[sms_start_indices[sms_time_index]:sms_end_indices[sms_time_index] + 1] = np.nan
        '''
        E_array_in_target_region = E_array[index_of_data_in_target_region]
        E_array_in_target_region_T = E_array_in_target_region.T
        E_list = E_array_in_target_region_T.tolist()
        #E_sms_list = E_sms_array.T[].tolist()
        
        B_array_in_target_region = B_array[index_of_data_in_target_region]
        B_array_in_target_region_T = B_array_in_target_region.T
        B_list = B_array_in_target_region_T.tolist()
        #B_sms_list = B_sms_array.T.tolist()
        
        E_matrix_per_day = np.empty((freq_array.size, intensity_array.size), dtype = int)
        B_matrix_per_day = np.empty((freq_array.size, intensity_array.size), dtype = int)
        
        #E_sms_matrix_per_day = np.empty((freq_array.size, intensity_array.size), dtype = int)
        #B_sms_matrix_per_day = np.empty((freq_array.size, intensity_array.size), dtype = int)
        

        for ch in range(freq_array.size):
            for intensity in intensity_array:
                E_matrix_per_day[ch][intensity] = E_list[ch].count(intensity)
                B_matrix_per_day[ch][intensity] = B_list[ch].count(intensity)
                #for j in range(len(sms_start_indices)):
                #    E_sms_matrix_per_day[ch][intensity] = E_sms_list[ch][sms_start_indices[j]:sms_end_indices[j]+1].count(intensity)
                #    B_sms_matrix_per_day[ch][intensity] = B_sms_list[ch][sms_start_indices[j]:sms_end_indices[j]+1].count(intensity)

        E_matrix = E_matrix + E_matrix_per_day
        B_matrix = B_matrix + B_matrix_per_day
        #E_sms_matrix = E_sms_matrix + E_sms_matrix_per_day
        #B_sms_matrix = B_sms_matrix + B_sms_matrix_per_day
        
    bottom = 0.8
    #xlim = [1e-15, 10]
    ylim = [0.8, 5e5]
    marker = '.'
    #Efield_plot_save_name = './plots/mca_intensity_distribution/test/mca_' + 'Efield_' + start_date+'_'+end_date+suffix
    Efield_plot_save_name = './plots/mca_intensity_distributio_per_alt_plot/mca_' + 'Efield_' + start_date+'_'+end_date+'_'+'alt'+str(alt_range[0])+'_'+str(alt_range[1])+suffix
    Efield_plot_sms_on_save_name = './plots/mca_intensity_distribution/test/mca_' + 'Efield_' + start_date+'_'+end_date+'_sms-only'+suffix
    #Mfield_plot_save_name = './plots/mca_intensity_distribution/test/mca_' + 'Mfield_' + start_date+'_'+end_date+suffix
    Mfield_plot_save_name = './plots/mca_intensity_distributio_per_alt_plot/mca_' + 'Mfield_' + start_date+'_'+end_date+'_'+'alt'+str(alt_range[0])+'_'+str(alt_range[1])+suffix
    Mfield_plot_sms_on_save_name = './plots/mca_intensity_distribution/test/mca_' + 'Mfield_' + start_date+'_'+end_date+'_sms-only'+suffix
    
    def distribution_plot(x, matrix, title, save_name):
        
        fig = plt.figure(figsize=(16, 8))
        ax1 = fig.add_subplot(3,1,1)
        for i in range(6):
            ax1.plot(x, matrix[i], label = str(freq_array[i]) +' Hz', marker = marker)
        
            #ax1.plot(10**(intensity_array/10 -12)/(freq_array[i]*0.3), matrix[i], label = str(freq_array[i])+' Hz', marker = marker)
        #ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_ylabel('Count')
        #ax1.set_xlim(xlim)
        #ax1.set_ylim(ylim)
        ax1.legend()
        ax1.set_title(title)
        
        ax2 = fig.add_subplot(3,1,2)
        for i in range(5):
            ax2.plot(x, matrix[i+6], label = str(freq_array[i+6]) +' Hz', marker = marker)

            #ax2.plot(10**(intensity_array/10 -12)/(freq_array[i+6]*0.3), E_matrix[i+6], label = str(freq_array[i+6])+' Hz', marker = marker)
        #ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.set_ylabel('Count')
        #ax2.set_xlim(xlim)
        #ax2.set_ylim(ylim)
        ax2.legend()

        ax3 = fig.add_subplot(3,1,3)
        for i in range(5):
            ax3.plot(x, matrix[i+11], label = str(freq_array[i+11]) + ' Hz', marker = marker)
        
            #ax3.plot(10**(intensity_array/10 -12)/(freq_array[i+11]*0.3), E_matrix[i+11], label = str(freq_array[i+11]) + ' Hz', marker = marker)
        #ax3.set_xscale('log')
        ax3.set_yscale('log')
        ax3.set_ylabel('Count')
        #ax3.set_xlim(xlim)
        #ax3.set_ylim(ylim)
        #ax3.set_xlabel('PSD [(mV/m)^2/Hz]')
        ax3.set_xlabel('Count')
        ax3.legend()
        

        plt.savefig(save_name)
        plt.clf()
        plt.close()
    
    distribution_plot(x = intensity_array, matrix = E_matrix, title = 'E field intensity distribution dB' + start_date + '_' + end_date, save_name = Efield_plot_save_name)
    distribution_plot(x = intensity_array, matrix = B_matrix, title = 'M field intensity distribution dB' + start_date + '_' + end_date, save_name = Mfield_plot_save_name)
    with open('mca_intensity_distribution.txt', 'w') as f:
        for ch_idx in range(freq_array.size):
            print(freq_array[ch_idx], ' Hz', file=f)
            for intensity in intensity_array:
                print(str(intensity) + ': ' ,E_matrix[ch_idx][intensity], file=f)
    '''
    xlim = [1e-10, 1e8]
    fig = plt.figure(figsize=(10, 8))
    ax1 = fig.add_subplot(3,1,1)
    for i in range(6):
        ax1.plot(10**(intensity_array/10 -12)/(freq_array[i]*0.3), B_matrix[i], label = str(freq_array[i])+' Hz', marker = marker)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_ylabel('Count')
    ax1.set_xlim(xlim)
    ax1.set_ylim(ylim)
    ax1.legend()
    subtitle = ''
    for i in range(len(del_invalid_data)):
        subtitle = subtitle + ' ' + del_invalid_data[i]
    ax1.set_title('Akebono VLF/MCA ' + 'Mfield in cusp '+start_date + ' ' + end_date + '\n' + subtitle)
    
    ax2 = fig.add_subplot(3,1,2)
    for i in range(5):
        ax2.plot(10**(intensity_array/10 -12)/(freq_array[i+6]*0.3), B_matrix[i+6], label = str(freq_array[i+6])+' Hz', marker = marker)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_ylabel('Count')
    ax2.set_xlim(xlim)
    ax2.set_ylim(ylim)
    ax2.legend()
                                    
    ax3 = fig.add_subplot(3,1,3)
    for i in range(5):
        ax3.plot(10**(intensity_array/10 -12)/(freq_array[i+11]*0.3), B_matrix[i+11], label = str(freq_array[i+11]) + ' Hz', marker = marker)
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlim(xlim)
    ax3.set_ylim(ylim)
    ax3.set_ylabel('Count')
    ax3.set_xlabel('PSD [pT^2/Hz]')
    ax3.legend()
    
    plt.savefig(Mfield_plot_save_name)
    plt.clf()
    plt.close()
    '''
mca_intensity_distribution_plot('1989-4-1', '2003-12-1', del_inst_interference=['off', 'noisy', 'sms', 'bit rate m', 'bdr', 'pws'])