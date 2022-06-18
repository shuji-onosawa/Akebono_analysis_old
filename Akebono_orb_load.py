import os as IMos
import sys as IMsys
import zipfile
import urllib.request as IMurllibreq
import urllib
import pytplot
#Imported as above to avoid multiple imports, but not sure if this is necessary

class Akebono_orb_load:
    
    def __init__(self,date):
        self.input_date = date
    
    def attach_date(self,date):
        self.input_date = date
        
    def mca(self,dirname = 'Akebono_orb_data'):
        url_former_text = 'https://www.darts.isas.jaxa.jp/stp/akebono/ORBIT/'
        year = self.input_date[:4]
        year_month = self.input_date[:6]
        url_later_text = 'orb.zip'

        url=url_former_text+'/'+year+'/'+year_month+url_later_text
        #https://www.darts.isas.jaxa.jp/stp/akebono/ORBIT/1989/198905orb.zip
        pathname = './'+dirname+'/'

        try:
            IMos.mkdir(pathname)
        except:
            pass
        
        
        save_name=pathname+self.input_date+'orb.zip'
                  
        if(IMos.path.isfile(save_name)==False):
            
            get_data = IMurllibreq.urlopen(url).read()
            try:
                with open(save_name, mode="wb") as f:
                    f.write(get_data)
            
                with zipfile.ZipFile(save_name) as obj_zip:
                    obj_zip.extractall(pathname)
        
            
            except urllib.error.URLError as e:
                    print(e)
                    IMsys.exit(1)
        
        tvars = pytplot.cdf_to_tplot(save_name)
        return tvars