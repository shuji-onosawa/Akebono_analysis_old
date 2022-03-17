set pm3d map
set palette rgbformulae 22,13,-31
set size 0.9,0.5
set xr[0:100]
set xtics 20
set mxtics 5
set yr[-180:180]
set ytics 90
set yl "spin angle"
set zr[1:10000]
set zl "[counts/sec]"
set logscale z
set logscale cb
splot "smsploto.txt" using 1:2:3