import AkebonoMCAImporter
importer = AkebonoMCAImporter.AkebonoMCAimporter('19900211')
E_field = importer.output_mca_data('Eave', 'Eave')
t = importer.output_mca_data('Epoch', 'Epoch')
print(t[0:10])
print(type(t[0]))

#importer.attach_date('19950304')
#t = importer.output_mca_data('channel','Adata')
#print(t)