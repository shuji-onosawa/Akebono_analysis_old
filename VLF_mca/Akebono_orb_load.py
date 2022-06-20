import os as IMos
import sys as IMsys
import urllib.request as IMurllibreq
import urllib
import pytplot
#Imported as above to avoid multiple imports, but not sure if this is necessary

class Akebono_orb_load:
    
    def __init__(self,date):
        self.input_date = date
    #input_date = yyyymmdd
    def attach_date(self,date):
        self.input_date = date
        
    def orb(self,dirname = 'Akebono_orb_data'):
        url_former_text = 'https://darts.isas.jaxa.jp/stp/data/exosd/orbit/daily/'
        year_month = self.input_date[:6]
        year_month_day = self.input_date[2:]
        url_later_text = '.txt'

        url=url_former_text+'/'+year_month+'/ED'+year_month_day+url_later_text
        #https://darts.isas.jaxa.jp/stp/data/exosd/orbit/daily/201401/ED140101.txt
        pathname = './'+dirname+'/'

        try:
            IMos.mkdir(pathname)
        except:
            pass
        
        
        save_name=pathname+self.input_date+'.orb'
                  
        if(IMos.path.isfile(save_name)==False):
            
            get_data = IMurllibreq.urlopen(url).read()
            try:
                with open(save_name, mode="wb") as f:
                    f.write(get_data)
                   
            except urllib.error.URLError as e:
                    print(e)
                    IMsys.exit(1)
        
        with open(save_name) as f:
            datalist = f.readlines()
            for i in range(len(datalist)):
                datalist[i] = datalist[i].split()
        
        datalist = datalist.T
        return datalist