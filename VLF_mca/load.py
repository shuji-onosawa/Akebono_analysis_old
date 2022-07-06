from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pyspedas import time_double
from pytplot import cdf_to_tplot
from pytplot import store_data
import os
import urllib.request
import numpy as np


#mca
def mca(trange = ['2014-01-01', '2014-01-03'],
        time_clip = True):

    remote_name_prefix = 'https://akebono-vlf.db.kanazawa-u.ac.jp/permalink.php?keyword='
    pathformat = 'https://akebono-vlf.db.kanazawa-u.ac.jp/permalink.php?keyword=ak_h1_mca_%Y%m%d_v02.cdf'

    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    pathname = './Akebono_MCA_data/'


    try:
        os.mkdir(pathname)
    except:
        pass

    for remote_name in remote_names:                           
        get_data = urllib.request.urlopen(remote_name).read()

        save_name = pathname + remote_name 
        save_name = save_name.replace(remote_name_prefix, '')

        with open(save_name, mode="wb") as f:
            f.write(get_data)
        
        out_files.append(save_name)

    out_files = sorted(out_files)

    tvars = cdf_to_tplot(out_files)

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')
    
    return tvars

#orbit
def orb(trange = ['2014-01-01', '2014-01-03']):
    
    remote_name_prefix = 'https://darts.isas.jaxa.jp/stp/data/exosd/orbit/daily/%Y%m/'
    pathformat = 'https://darts.isas.jaxa.jp/stp/data/exosd/orbit/daily/%Y%m/ED%y%m%d.txt'
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    pathname = './Akebono_orb_data/'

    try:
        os.mkdir(pathname)
    except:
        pass

    for remote_name in remote_names:  
    # remote_name = 'https://darts.isas.jaxa.jp/stp/data/exosd/orbit/daily/%Y%m/ED%y%m%d.txt'
        get_data = urllib.request.urlopen(remote_name).read()

        save_name = pathname + remote_name[-12:]

        with open(save_name, mode="wb") as f:
            f.write(get_data)
        
        out_files.append(save_name)
    # save_name = './Akebono_orb_data/ED%y%m%d.txt'

    out_files = sorted(out_files)
    # out_files = list of './Akebono_orb_data/ED%y%m%d.txt'

    UT_time_double = []
    ILAT = []
    MLAT = []
    MLT = []
    ALT = []

    for out_file in out_files:
        datalines = []
        with open(out_file) as f:
            datalines = f.readlines()
            for i in range(len(datalines)):
                datalines[i] = datalines[i].split()

        for data_list_index in range(1, len(datalines[1:])):
                for data_index in range(len(datalines[data_list_index])):
                    datalines[data_list_index][data_index] = float(datalines[data_list_index][data_index])
        del datalines[0]

        data_array = np.array(datalines, dtype=float).T

        year = out_file[-10:-8]
        #decide %Y from %y in file name, 'ED%y%m%d.txt'
        if float(year) < 20: 
            year = '20' + year
        else:
            year = '19' + year

        UT = data_array[1].tolist()
        UT = [int(n) for n in UT]
        UT = [str(n) for n in UT]
        for time_index in range(len(UT)):
            time = UT[time_index]
            month, day, hour, minute, second = time[2:4], time[4:6], time[6:8], time[8:10], time[10:12]
            time_string = year + '/' + month + '/' + day + '/' + hour + ':' + minute + ':' + second
            #yyyymmdd.orb has UT data in the format of 'yymmddhhmmss'.
            #To use pyspedas.time_double, change format from 'yymmddhhmmss' to 'yyyy/mm/dd/hh:mm:ss'
            time_time_double = time_double(time_string)
            UT_time_double.append(time_time_double)
        ILAT = ILAT + data_array[20].tolist()
        MLAT = MLAT + data_array[22].tolist()
        MLT = MLT + data_array[23].tolist()
        ALT = ALT + data_array[29].tolist()

    '''
    datalist_header = [ 'PASS',
                        'UT', 
                        'ksc_azm(deg)', 'ksc_elv(deg)', 'ksc_dis(km)', 'ksc_ang(deg)', 
                        'syo_azm(deg)', 'syo_elv(deg)', 'syo_dis(km)', 'syo_ang(deg)', 
                        'pra_azm(deg)', 'pra_elv(deg)', 'pra_dis(km)', 'pra_ang(deg)', 
                        'esr_azm(deg)', 'esr_elv(deg)', 'esr_dis(km)', 'esr_ang(deg)', 
                        'GCLAT(deg)', 'GCLON(deg)', 
                        'INV(deg)', 
                        'FMLAT(deg)', 
                        'MLAT(deg)', 
                        'MLT(h)', 
                        'Bmdl_X', 'Bmdl_Y', 'Bmdl_Z', 
                        'GCLON_S/C(deg)', 'GCLAT_S/C(deg)',  
                        'ALT(km)', 
                        'LSUN', 
                        's_Direc_x','s_Direc_y', 's_Direc_z', 
                        's/c_pos_x', 's/c_pos_y', 's/c_pos_z', 
                        's/c_vel(km/s)_x', 's/c_vel(km/s)_y','s/c_vel(km/s)_z' ]
    '''
    prefix = 'akb_orb_'
    print(len(UT_time_double))
    print(len(ILAT))
    print(len(MLAT))
    store_data(prefix+'ILAT', data={'x': UT_time_double, 'y': ILAT})
    store_data(prefix+'MLAT', data={'x': UT_time_double, 'y': MLAT})
    store_data(prefix+'MLT', data={'x': UT_time_double, 'y': MLT})
    store_data(prefix+'ALT', data={'x': UT_time_double, 'y': ALT})
    
    return 