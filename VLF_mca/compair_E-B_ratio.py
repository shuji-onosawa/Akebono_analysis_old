from pytplot import cdf_to_tplot, tplot_names, tlimit, tplot, get_data, store_data, options
from load import mca_h1cdf_dB_to_absolute
import calc_dispersion_in_cold_plasma as calc_dr

# read cdf
cdf_name = 'Akebono_MCA_data/H1CDF_ave1s/ak_h1_mca_19900217_v02.cdf'
cdf_to_tplot(cdf_name)
mca_h1cdf_dB_to_absolute(spec_type='pwr')
center_freq = 
# get E/cB
n_R, n_L, S, D, P = calc_dr.calc_dispersion_relation()
_, _, _, _, _, E_to_cB = calc_dr.calc_amp_ratio()
tlimit(['1990-2-17 03:45:00', '1990-2-17 03:55:00'])
options(['Emax_pwr', 'Bmax_pwr'], 'spec', 0)

tplot(['Emax_pwr', 'Bmax_pwr'], xsize=10, ysize=10)
