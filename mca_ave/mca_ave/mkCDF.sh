#!/bin/csh
cd /home/staff/kasahara/exos/CDF/MCA/mca_ave
foreach YEAR (2008 2009 2010)
  foreach MONTH (1 2 3 4 5 6 7 8 9 10 11 12)
    foreach DAY (1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31)
      echo $YEAR $MONTH $DAY
      ./bnd $YEAR $MONTH $DAY 8
    end
  end
end
