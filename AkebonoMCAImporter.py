import os as IMos
import sys as IMsys
import cdflib as IMcdflib
import urllib.request as IMurllibreq
#Imported as above to avoid multiple imports, but not sure if this is necessary

class AkebonoMCAimporter:
    
    input_date = '19920101'
    
    def __init__(self,date):
        self.input_date = date
    
    def input_date(self,date):
        self.input_date = date
        
    def output_mca_data(self,type = 'Epoch',dirname = 'Akebono_MCA_data',headname='data'):
        url_former_text = 'https://akebono-vlf.db.kanazawa-u.ac.jp/permalink.php?keyword=ak_h1_mca_'
        url_later_text = '_v02.cdf'

        url=url_former_text+self.input_date+url_later_text

        filename_later_text = '_mca.cdf'

        pathname = './'+dirname+'/'

        try:
            IMos.mkdir(pathname)
        except:
            pass
        
        
        save_name=pathname+headname+self.input_date+type+filename_later_text

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
            
        cdf_data = cdf_file.varget(type)
        if(type == 'Epoch'):
            cdf_data = IMcdflib.cdfepoch.breakdown(cdf_data,False)
        return cdf_data
        
    

