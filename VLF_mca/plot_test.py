import matplotlib.pyplot as plt

a = [1,2,3,4,5]
b = [1,2,3,4,5]

plt.figure(figsize = [6.4, 6.4])
plt.plot(a,b, label = 'test')
plt.legend(loc = 'center left', bbox_to_anchor=(1., 0.5))
plt.show() 