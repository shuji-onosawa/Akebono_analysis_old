import cdflib
import pytplot

for date in ['0201', '0202', '0203', '0204', '0205', '0206', '0207', '0208', '0209', '0210',
             '0211', '0212', '0213', '0214', '0215', '0216', '0217', '0218', '0219', '0220',
             '0221', '0222', '0223', '0224', '0225', '0226', '0227', '0228']:

    cdf_name = '/home/onosawa/Document/Make_mca_cdf/onosawa/CDF-H0/1990/ak_h0_mca_1990' + date + '_v01.cdf'
    x_array = cdflib.cdf_to_xarray(cdf_name)
    print(x_array)
    print('----')
    start_time = '1990' + date + ' 00:00:00'
    end_time = '1990' + date + ' 23:59:00'
    print(start_time)
    pytplot.cdf_to_tplot('/home/onosawa/Document/Akebono_analysis/VLF_mca/Akebono_MCA_data/ak_h1_mca_1990' + date + '_v02.cdf')
    pytplot.options(name='Emax', opt_dict={'spec': 1, 'ylog': 1, 'zlog': 1})
    pytplot.tlimit([start_time, end_time])
    pytplot.tplot('Emax')
