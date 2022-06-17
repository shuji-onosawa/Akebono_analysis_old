import pyspedas
import pytplot
from pytplot import options
from pytplot import tplot
from pytplot import tlimit
from pytplot import tplot_options
import Akebono_mca_load

importer = Akebono_mca_load.Akebono_mca_load('19890607')
importer.mca()

tplot_names = pytplot.tplot_names(True)

for i in range(4):
    tplot_variable = pytplot.get_data(tplot_names[i])
    tplot_variable_0dB = 1e-6 #mV or pT
    bandwidth = tplot_variable.v * 0.3
    tplot_variable_power = (10**(tplot_variable.y/10)) * (tplot_variable_0dB**2) / bandwidth 
    pytplot.store_data(tplot_names[i] +'_power', data={'x': tplot_variable.times, 'y': tplot_variable_power, 'v': tplot_variable.v})

tlimit(['1989-06-07 00:00:00', '1989-06-07 23:39:00'])
options('Emax', 'spec', 1)
options('Emax', 'ytitle', 'Freq')
options('Emax', 'ysubtitle', '[Hz]')
options('Emax', 'ztitle', '$Emax [dB]$')
options('Emax', 'panel_size', 0.5)
options('Eave', 'spec', 1)
options('Eave', 'ytitle', 'Freq')
options('Eave', 'ysubtitle', '[Hz]')
options('Eave', 'ztitle', '$Emax [dB]$')
tplot(['Emax', 'Eave'])