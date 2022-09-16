from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pyspedas import time_double
from pytplot import cdf_to_tplot, store_data, get_data

import os
import urllib.request
import numpy as np
import time
from calendar import timegm
from datetime import datetime, timedelta

#mca
def mca(trange = ['2014-01-01', '2014-01-02'],
        downloadonly = False):

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
        
        save_name = pathname + remote_name 
        save_name = save_name.replace(remote_name_prefix, '')

        if(os.path.isfile(save_name)==False):
            
            get_data = urllib.request.urlopen(remote_name).read()
        
            with open(save_name, mode="wb") as f:
                f.write(get_data)
        
        out_files.append(save_name)

    if downloadonly:
        return 
    
    out_files = sorted(out_files)
    
    try:
        tvars = cdf_to_tplot(out_files)
    except:
        print('///////////////////////////ERROR/////////////////////////')
        os.remove(save_name)
        return
    '''
    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')
    '''

    return tvars

#orbit
def orb(trange = ['2013-01-01', '2013-01-02'], downloadonly = False):
    
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

        save_name = pathname + remote_name[-12:]
        
        if(os.path.isfile(save_name)==False):
            
            try:
                get_data = urllib.request.urlopen(remote_name).read()
            except:
                print('///////////////////////////ERROR/////////////////////////')
                print("You can not get orbit file or you can not open orbit file \n")
                continue
            
            with open(save_name, mode="wb") as f:
                f.write(get_data)
        
        out_files.append(save_name)
    # save_name = './Akebono_orb_data/ED%y%m%d.txt'

    if downloadonly:
        return 
    
    out_files = sorted(out_files)
    # out_files = list of './Akebono_orb_data/ED%y%m%d.txt'
    
    Pass = []
    UT_time_double = []
    ILAT = []
    MLAT = []
    MLT = []
    ALT = []
    Bmdl_X = []
    Bmdl_Y = []
    Bmdl_Z = []

    for out_file in out_files:
        datalines = []
        with open(out_file) as f:
            datalines = f.readlines()
            for i in range(len(datalines)):
                datalines[i] = datalines[i].split()

        del datalines[0]
        
        data_array = np.array(datalines, dtype=str).T
        
        #decide %Y from %y in file name, 'ED%y%m%d.txt'

        UT = data_array[1].tolist()
        
        year_suffix = UT[0][:2]
        
        if int(year_suffix) < 16:
            year = '20' + year_suffix
        else:
            year = '19' + year_suffix
            
        for time_index in range(len(UT)):
            Time = UT[time_index]
            month, day, hour, minute, second = Time[2:4], Time[4:6], Time[6:8], Time[8:10], Time[10:12]
            time_string = year + '/' + month + '/' + day + '/' + hour + ':' + minute + ':' + second

            utc_time_tuple = time.strptime(time_string, "%Y/%m/%d/%H:%M:%S")
            dt = datetime(1970, 1, 1) + timedelta(seconds=timegm(utc_time_tuple))
            time_string = dt.strftime("%Y/%m/%d/%H:%M:%S")
            #yyyymmdd.orb has UT data in the format of 'yymmddhhmmss'.
            #To use pyspedas.time_double, change format from 'yymmddhhmmss' to 'yyyy/mm/dd/hh:mm:ss'
            time_time_double = time_double(time_string)
            UT_time_double.append(time_time_double)
        Pass = Pass + data_array[0].tolist()
        ILAT = ILAT + data_array[20].tolist()
        MLAT = MLAT + data_array[22].tolist()
        MLT = MLT + data_array[23].tolist()
        ALT = ALT + data_array[29].tolist()
        Bmdl_X = Bmdl_X + data_array[24].tolist()
        Bmdl_Y = Bmdl_Y + data_array[25].tolist()
        Bmdl_Z = Bmdl_Z + data_array[26].tolist()

    Pass = [float(n) for n in Pass]
    ILAT = [float(n) for n in ILAT]
    MLAT = [float(n) for n in MLAT]
    MLT = [float(n) for n in MLT]
    ALT = [float(n) for n in ALT]

    Bmdl_X = [float(n) for n in Bmdl_X]
    Bmdl_Y = [float(n) for n in Bmdl_Y]
    Bmdl_Z = [float(n) for n in Bmdl_Z]


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
                        'Bmdl_X', 'Bmdl_Y', 'Bmdl_Z', :X, Y, AND Z COMPONENTS OF THE IGRF 2005 MAGNETIC FIELD (nT)   
                        'GCLON_S/C(deg)', 'GCLAT_S/C(deg)',  
                        'ALT(km)', 
                        'LSUN', 
                        's_Direc_x','s_Direc_y', 's_Direc_z', 
                        's/c_pos_x', 's/c_pos_y', 's/c_pos_z', 
                        's/c_vel(km/s)_x', 's/c_vel(km/s)_y','s/c_vel(km/s)_z' ]
    '''
    if int((time_double(trange[1])-time_double(trange[0]))/30) > len(UT_time_double):
        start_to_end_time_double = np.arange(time_double(trange[0]), time_double(trange[1]), 30)
        Pass_array = ILAT_array = MLAT_array = MLT_array = ALT_array = Bmdl_X_array = Bmdl_Y_array = Bmdl_Z_array = np.empty(start_to_end_time_double.size)*np.nan

        for i in range(len(UT_time_double)):
            time_index = np.where(start_to_end_time_double == UT_time_double[i])
            Pass_array[time_index] = Pass[i]
            ILAT_array[time_index] = ILAT[i]
            MLAT_array[time_index] = MLAT[i]
            MLT_array[time_index] = MLT[i]
            ALT_array[time_index] = ALT[i]
            Bmdl_X_array[time_index] = Bmdl_X[i]
            Bmdl_Y_array[time_index] = Bmdl_Y[i]
            Bmdl_Z_array[time_index] = Bmdl_Z[i]

        UT_time_double = start_to_end_time_double
        Pass = Pass_array
        ILAT = ILAT_array
        MLAT = MLAT_array
        MLT = MLT_array
        ALT = ALT_array
        Bmdl_X = Bmdl_X_array
        Bmdl_Y = Bmdl_Y_array
        Bmdl_Z = Bmdl_Z_array
        
    prefix = 'akb_'
    store_data(prefix+'Pass', data={'x': UT_time_double, 'y': Pass})
    store_data(prefix+'ILAT', data={'x': UT_time_double, 'y': ILAT})
    store_data(prefix+'MLAT', data={'x': UT_time_double, 'y': MLAT})
    store_data(prefix+'MLT', data={'x': UT_time_double, 'y': MLT})
    store_data(prefix+'ALT', data={'x': UT_time_double, 'y': ALT})
    store_data(prefix+'Bmdl_X', data={'x': UT_time_double, 'y': Bmdl_X})
    store_data(prefix+'Bmdl_Y', data={'x': UT_time_double, 'y': Bmdl_Y})
    store_data(prefix+'Bmdl_Z', data={'x': UT_time_double, 'y': Bmdl_Z})

    return 

