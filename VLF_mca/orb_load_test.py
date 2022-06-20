import Akebono_orb_load
import numpy as np

importer = Akebono_orb_load.Akebono_orb_load('20140101')
dataline = importer.orb()
dataline = np.array(dataline).T
print(dataline[:4])