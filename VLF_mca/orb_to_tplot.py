import string
import numpy as np
from pyspedas import time_double
from pytplot import cdf_to_tplot
#remot path = 'http://darts.isas.jaxa.jp/stp/data/exosd/orbit/daily/'
path = './Akebono_orb_data/20140101.orb'

with open(path) as f:
    datalist = f.readlines()
    for i in range(len(datalist)):
        datalist[i] = datalist[i].split() 

datalist_header = [  'PASS',
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


for data_list_index in range(1, len(datalist[1:])):
    for data_index in range(len(datalist[data_list_index])):
        datalist[data_list_index][data_index] = float(datalist[data_list_index][data_index])

del datalist[0]

data_array = np.array(datalist, dtype=float).T

YY = '20'

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

mlt = data_array[23]




