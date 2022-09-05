import cdflib, pytplot

cdf_file = cdflib.CDF('ak_h1_elf_19900206_v03.cdf')
pytplot.cdf_to_tplot('ak_h1_elf_19900206_v03.cdf')
print(pytplot.tplot_names())
cdf_file.cdf_info()