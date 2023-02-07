import numpy as np
import plasma_params as pp
import matplotlib.pyplot as plt
import calc_dispersion_in_cold_plasma as calc_dr

theta = 90
omega_s = np.abs(pp.wlh)
freq = omega_s*np.logspace(-4, 1, 10000)

n_L, n_R, S, D, P = calc_dr.calc_dispersion_relation(freq, theta)
# idx = calc_dr.get_crossover_freq_idx(D, theta)

char_freq = np.array([pp.omega_h, pp.omega_o, -pp.omega_e, pp.wlh])/omega_s

# crossover_freq = np.empty(idx.size)
# for i in range(idx.size):
#     crossover_freq[i] = freq[idx[i]] / omega_s

fig, axs = plt.subplots(nrows=1, ncols=1, figsize=[16, 8])
axs.scatter(x=freq/omega_s, y=n_L, label=r'$L mode$', c='r', marker='.')
axs.scatter(x=freq/omega_s, y=n_R, label=r'$R mode$', c='b', marker='.')
axs.vlines(char_freq, 0, 1e7, linestyles='dashed', colors='k')
# axs.vlines(crossover_freq, 0, 1e7, linestyles='dashed', colors='r')
axs.set_xscale('log')
axs.set_yscale('log')
axs.set_xlabel(r'$\omega / \Omega_cH$')
axs.set_ylabel(r'$Refraction index ^2$')

plt.legend()
plt.show()
