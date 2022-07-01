import pyspedas
import pytplot
from pytplot import options
from pytplot import tplot
from pytplot import tlimit
from pytplot import tplot_options
import Akebono_mca_load
import Akebono_orb_load
import numpy as np

date = '19910711'
importer1 = Akebono_mca_load.Akebono_mca_load(date)
importer2 = Akebono_orb_load.Akebono_orb_load(date)
importer1.mca()
importer2.orb()

tplot_names = pytplot.tplot_names()

#dB to amplitude
for i in range(4):
    tplot_variable = pytplot.get_data(tplot_names[i])
    tplot_variable_0dB = 1e-6 #mV or pT
    bandwidth = tplot_variable.v * 0.3
    tplot_variable_amplitude = (10**(tplot_variable.y/20)) * (tplot_variable_0dB)  / np.sqrt(bandwidth)
    pytplot.store_data(tplot_names[i] +'_power', data={'x': tplot_variable.times, 'y': tplot_variable_amplitude, 'v': tplot_variable.v})

tplot_options('wsize', [500,10000])
tlimit(['1991-07-11 00:00:00', '1991-07-11 23:59:00'])
options(['Eave_power', 'Emax_power'], 'spec', 1)
options(['Eave_power', 'Emax_power'], 'ylog', 1)
options(['Eave_power', 'Emax_power'], 'zlog', 1)
options(['Eave_power', 'Emax_power'], 'zrange', [1e-5, 1])
options(['Eave_power', 'Emax_power'], 'yrange', [1, 2e4])
options(['Eave_power', 'Emax_power'], 'ztitle', '[mV/m/Hz^1/2]')
options('akb_orb_ALT', 'ylabel', 'ALT [km]')
options('akb_orb_MLT', 'ylabel', 'MLT [h]')
options('akb_orb_ILAT', 'ylabel', 'ILAT [deg]')
tplot_options('title', 'MCA data ' + date)
tplot(['Eave_power', 'Emax_power'], var_label = ['akb_orb_ALT', 'akb_orb_MLT', 'akb_orb_ILAT'], save_png = 'akb'+ date + '053300_wsize500-10000')
