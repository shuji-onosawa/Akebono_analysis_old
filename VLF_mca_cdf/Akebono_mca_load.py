import os as IMos
import sys as IMsys
import cdflib as IMcdflib
import urllib.request as IMurllibreq
import pytplot
#Imported as above to avoid multiple imports, but not sure if this is necessary

class Akebono_mca_load:
    
    def __init__(self,date):
        self.input_date = date
    
    def attach_date(self,date):
        self.input_date = date
        
    def mca(self,dirname = 'Akebono_MCA_data'):
        url_former_text = 'https://akebono-vlf.db.kanazawa-u.ac.jp/permalink.php?keyword=ak_h1_mca_'
        url_later_text = '_v02.cdf'

        url=url_former_text+self.input_date+url_later_text

        pathname = './'+dirname+'/'

        try:
            IMos.mkdir(pathname)
        except:
            pass
        
        
        save_name=pathname+'ak_h1_mca_'+self.input_date+'_v02.cdf'
                  
        if(IMos.path.isfile(save_name)==False):
            
            get_data = IMurllibreq.urlopen(url).read()

            with open(save_name, mode="wb") as f:
                f.write(get_data)

        try:
            cdf_file = IMcdflib.CDF(save_name)
        except:
            print('///////////////////////////ERROR/////////////////////////')
            print("You can not get file or you can not open file \n")
            IMsys.exit(1)
        
        tvars = pytplot.cdf_to_tplot(save_name)
        return tvars