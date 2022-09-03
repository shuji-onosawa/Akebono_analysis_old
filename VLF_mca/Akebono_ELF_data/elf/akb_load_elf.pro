PRO akb_load_elf

fn=dialog_pickfile(path='C:\Users\石ヶ谷\data\exosd\elf\', filter=['*.cdf'])

;----- Print PI info and rules of the road -----;
if(file_test(fn[0])) then begin
  gatt = cdf_var_atts(fn[0])
  print, '**************************************************************************************'
  ;print, gatt.project
  print, gatt.Logical_source_description
  print, ''
  print, 'PI: ', gatt.PI_name
  print, 'Affiliations: ', gatt.PI_affiliation
  print, ''
  print_str_maxlet, gatt.TEXT
  print, '**************************************************************************************'
endif

cdf2tplot, file=fn

options, "E", spec=1
options, "B", spec=1
options, "By_narrow", spec=1
options, "Bz_narrow", spec=1

ylim, "E", 0, 64, 0
ylim, "B", 0, 64, 0
ylim, "By_narrow", 0, 64, 0
ylim, "Bz_narrow", 0, 64, 0
zlim, "B", 0, 200, 0
zlim, "By_narrow", 0, 200, 0
zlim, "Bz_narrow", 0, 200, 0
options, "E", 'ytitle', 'E-field'
options, "E", 'ysubtitle', '[Hz]'
options, "E", 'ztitle', '[dB]'
options, "B", 'ytitle', 'B-field'
options, "B", 'ysubtitle', '[Hz]'
options, "B", 'ztitle', '[dB]'
options, "By_narrow", 'ytitle', 'By_narrow'
options, "By_narrow", 'ysubtitle', '[Hz]'
options, "By_narrow", 'ztitle', '[dB]'
options, "Bz_narrow", 'ytitle', 'Bz_narrow'
options, "Bz_narrow", 'ysubtitle', '[Hz]'
options, "Bz_narrow", 'ztitle', '[dB]'

window, 0, xsize=1000, ysize=600 & erase
end