import numpy as np
import pandas as pd

date_list = pd.date_range(start='1990-1-1', end='1990-2-1', freq='D')
date_list = np.datetime_as_string(date_list, unit='D')
date_list = date_list.astype(object)

date_array = np.zeros(len(date_list))
