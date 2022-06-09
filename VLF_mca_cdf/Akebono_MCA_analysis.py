import AkebonoMCAImporter
import matplotlib.pyplot as plt
importer = AkebonoMCAImporter.AkebonoMCAimporter('19890607')
Eave = importer.output_mca_data('Eave', 'Eave')
epoch = importer.output_mca_data('Epoch', 'Epoch')



x = [0, 1, 2]
y = [0, 4, 9]

plt.figure()
plt.plot(x,y)
plt.show()
#importer.attach_date('19950304')
#t = importer.output_mca_data('channel','Adata')
#print(t)