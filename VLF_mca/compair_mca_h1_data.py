import cdflib

created_h1_data = cdflib.cdf_to_xarray('/home/onosawa/Document/Make_mca_cdf/onosawa/CDF-H1/1990/ak_h1_mca_19900201_v02.cdf')
existing_h1_data = cdflib.cdf_to_xarray('/home/onosawa/Document/Akebono_analysis/VLF_mca/Akebono_MCA_data/ak_h1_mca_19900201_v02.cdf')

print(created_h1_data._dims)
print(existing_h1_data)
