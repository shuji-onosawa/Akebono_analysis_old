import load
import numpy as np

start_date = '1989-03-06'
end_date = '1989-03-07'

load.mca(trange=[start_date, end_date], del_invalid_data=True)
load.orb(trange=[start_date, end_date])

altitude_array = np.arange(500, 11000, 1000)
