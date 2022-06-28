import os as IMos
import sys as IMsys
import urllib.request as IMurllibreq
import urllib
import pytplot
import numpy as np
from pyspedas import time_double
from pytplot import store_data


#Imported as above to avoid multiple imports, but not sure if this is necessary

class Akebono_orb_load:
    
    def __init__(self,date):
        self.input_date = date
    #input_date = yyyymmdd
    def attach_date(self,date):
        self.input_date = date
        
    def orb(self,dirname = 'Akebono_orb_data'):
        url_former_text = 'https://darts.isas.jaxa.jp/stp/data/exosd/orbit/daily/'
        year_month = self.input_date[:6]
        year_month_day = self.input_date[2:]
        url_later_text = '.txt'

        url=url_former_text+'/'+year_month+'/ED'+year_month_day+url_later_text
        #https://darts.isas.jaxa.jp/stp/data/exosd/orbit/daily/201401/ED140101.txt
        pathname = './'+dirname+'/'

        try:
            IMos.mkdir(pathname)
        except:
            pass
        
        
        save_name=pathname+self.input_date+'.orb'
                  
        if(IMos.path.isfile(save_name)==False):
            
            get_data = IMurllibreq.urlopen(url).read()
            try:
                with open(save_name, mode="wb") as f:
                    f.write(get_data)
                   
            except urllib.error.URLError as e:
                    print(e)
                    IMsys.exit(1)
        
        with open(save_name) as f:
            datalist = f.readlines()
            for i in range(len(datalist)):
                datalist[i] = datalist[i].split()
        
        prefix = 'akb_orb_'
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
        for data_list_index in range(1, len(datalist[1:])):
            for data_index in range(len(datalist[data_list_index])):
                datalist[data_list_index][data_index] = float(datalist[data_list_index][data_index])

        del datalist[0]

        data_array = np.array(datalist, dtype=float).T

        YY = self.input_date[:2]

        UT = data_array[1].tolist()
        UT = [int(n) for n in UT]
        UT = [str(n) for n in UT]
        UT_time_double = []
        for time_index in range(len(UT)):
            time = UT[time_index]
            time_string = YY + time[:2] + '/' + time[2:4] + '/' + time[4:6] + '/' + time[6:8] + ':' + time[8:10] + ':' + time[10:12]
            #yyyymmdd.orb has UT data in the format of 'yymmddhhmmss'.
            #To use pyspedas.time_double, change format from 'yymmddhhmmss' to 'yyyy/mm/dd/hh:mm:ss'
            time_time_double = time_double(time_string)
            UT_time_double.append(time_time_double)

        store_data(prefix+'ILAT', data={'x': UT_time_double, 'y': data_array[20]})
        store_data(prefix+'MLT', data={'x': UT_time_double, 'y': data_array[23]})
        store_data(prefix+'ALT', data={'x': UT_time_double, 'y': data_array[29]})

        return 