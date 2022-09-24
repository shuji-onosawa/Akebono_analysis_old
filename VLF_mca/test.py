import load
from pytplot import tplot, tplot_options
import os
def test_func():
    load.mca(['1990-04-01', '1990-04-02'])
    try:
        north_save_dir = './akb_mca_monthly_plot/south_alpha/test'
        os.mkdir(north_save_dir)
    except Exception as e:
        print(e)
        pass
    try:
        south_save_dir = './akb_mca_monthly_plot/north_alpha/test'
        os.mkdir(south_save_dir)
    except Exception as e:
        print(e)
        pass

    tplot_options('wsize', [1000, 1000])
    tplot(['Emax', 'Bmax'], display=True)

test_func()