import AkebonoMCAImporter

importer = AkebonoMCAImporter.AkebonoMCAimporter('19940103')

t = importer.output_mca_data('channel','Adata')
print(t)

importer.attach_date('19950304')
t = importer.output_mca_data('channel','Adata')
print(t)