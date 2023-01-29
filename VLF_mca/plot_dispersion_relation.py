import numpy as np
import plasma_params as pp
import matplotlib.pyplot as plt
import calc_dispersion_in_cold_plasma as calc_dr
omega_s = np.abs(pp.omega_h)
freq = omega_s*np.arange(1e-2, 2, 1e-4)

n_L, n_R, S, D, P = calc_dr.calc_dispersion_relation(freq, 0)
idx = calc_dr.get_nearest_value_idx(D, 0)

print(pp.B0)
pi_2 = 2*np.pi
char_freq = np.array([pp.omega_h, pp.omega_o, -pp.omega_e, pp.wlh])/omega_s
crossover_freq = np.array([freq[idx]]) / omega_s
fig = plt.figure(figsize=[16, 8])
ax1 = fig.add_subplot(121)
ax1.plot(freq/omega_s, S, label=r'$S$', color='blue')
ax1.plot(freq/omega_s, D, label=r'$D$', color='red')
ax1.plot(freq/omega_s, P, label=r'$F$', color='g')
ax1.vlines(char_freq, 0, 1e7, linestyles='dashed', colors='k')
ax1.vlines(crossover_freq, 0, 1e7, linestyles='dashed', colors='r')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel(r'$\omega / \Omega_O$')
ax1.set_ylabel(r'$Refraction index ^2$')
plt.legend()

ax2 = fig.add_subplot(122)
ax2.plot(freq/omega_s, n_L, label=r'$L mode$', color='r')
ax2.plot(freq/omega_s, n_R, label=r'$R mode$', color='b')
ax2.vlines(char_freq, 0, 1e7, linestyles='dashed', colors='k')
ax2.vlines(crossover_freq, 0, 1e7, linestyles='dashed', colors='r')
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_xlabel(r'$\omega / \Omega_O$')
ax2.set_ylabel(r'$Refraction index ^2$')

plt.legend()
plt.show()
