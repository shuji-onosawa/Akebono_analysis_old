import numpy as np
import matplotlib.pyplot as plt
import calc_dispersion_in_cold_plasma as calc_dr
import plasma_params as pp


def calc_amp_ratio(n, S, D, P, theta):
    theta = np.deg2rad(theta)

    Ey_to_Ex = -D/(S-n)
    Ez_to_Ex = -n*np.cos(theta)*np.sin(theta)/(P-(n**2)*np.sin(theta)**2)
    By_to_Bx = -P*(S-n)/(D*(P-n*(np.sin(theta))**2))
    Bz_to_Bx = -np.tan(theta)*np.ones(n.size)
    E_to_BVa = pp.C/n/pp.Va*np.sqrt((1+((P-n)*(S-n)*(np.sin(theta)))**2/((P*np.cos(theta)*(S-n))**2-D*(P-n*(np.sin(theta))**2)**2)))

    return Ey_to_Ex, Ez_to_Ex, By_to_Bx, Bz_to_Bx, E_to_BVa


theta = 0
omega_s = np.abs(pp.omega_h)
freq = omega_s*np.arange(1e-2, 2, 1e-2)

amp_ratio_L = np.empty((5, freq.size))
amp_ratio_R = np.empty((5, freq.size))

n_L, n_R, S, D, P = calc_dr.calc_dispersion_relation(freq, theta)
amp_ratio_L[0], amp_ratio_L[1], amp_ratio_L[2], amp_ratio_L[3], amp_ratio_L[4] = \
    calc_amp_ratio(n_L, S, D, P, theta)
amp_ratio_R[0], amp_ratio_R[1], amp_ratio_R[2], amp_ratio_R[3], amp_ratio_R[4] = \
    calc_amp_ratio(n_R, S, D, P, theta)

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(18, 8))
fig.suptitle('WNA 0°')

mp1 = axs[0].scatter(x=freq/omega_s, y=n_L, c=amp_ratio_L[0], marker='.',
                     cmap='jet', vmin=-2, vmax=2, label='L')
mp2 = axs[0].scatter(x=freq/omega_s, y=n_R, c=amp_ratio_R[0], marker='.',
                     cmap='jet', vmin=-2, vmax=2, label='R')
cbar = plt.colorbar(mp1, aspect=10)
axs[0].set_ylabel(r'$n^2$')
# ax1.set_xlabel(r'$\omega/\Omega_cO$')
axs[0].set_xscale('log')
axs[0].set_yscale('log')
axs[0].set_ylim(top=1e7)
axs[0].set_title('Ey / Ex')
plt.legend()

axs[1]
mp3 = axs[1].scatter(x=freq/omega_s, y=n_L, c=amp_ratio_L[1], marker='.',
                     cmap='jet', vmin=-2, vmax=2, label='L')
mp4 = axs[1].scatter(x=freq/omega_s, y=n_R, c=amp_ratio_R[1], marker='.',
                     cmap='jet', vmin=-2, vmax=2, label='R')
cbar = plt.colorbar(mp3, aspect=10)
axs[1].set_ylabel(r'$n^2$')
# axs[1].set_xlabel(r'$\omega/\Omega_cO$')
axs[1].set_xscale('log')
axs[1].set_yscale('log')
axs[1].set_ylim(top=1e7)
axs[1].set_title('Ez / Ex ')
plt.legend()
'''
ax3 = fig.add_subplot(223)
mp = ax3.scatter(x=freq/omega_s, y=n_L, c=By_Bx_L, marker='>',
                 cmap='jet', vmin=-2, vmax=2, label='L')
mp = ax3.scatter(x=freq/omega_s, y=n_R, c=By_Bx_R, marker='<',
                 cmap='jet', vmin=-2, vmax=2, label='R')
cbar = plt.colorbar(mp, aspect=10)
ax3.set_ylabel(r'$n^2$')
ax3.set_xlabel(r'$\omega/\Omega_cO$')
ax3.set_xscale('log')
ax3.set_yscale('log')
ax3.set_ylim(top=1e7)
ax3.set_title('By / Bx ')
plt.legend()

ax4 = fig.add_subplot(224)
mp = ax4.scatter(x=freq/omega_s, y=n_L, c=Bz_Bx_L, marker='>',
                 cmap='jet', vmin=-2, vmax=2, label='L')
mp = ax4.scatter(x=freq/omega_s, y=n_R, c=Bz_Bx_R, marker='<',
                 cmap='jet', vmin=-2, vmax=2, label='R')

cbar = plt.colorbar(mp, aspect=10)
ax4.set_ylabel(r'$n^2$')
ax4.set_xlabel(r'$\omega/\Omega_cO$')
ax4.set_xscale('log')
ax4.set_yscale('log')
ax4.set_ylim(top=1e7)
ax4.set_title('Bz / Bx ')
plt.legend()
'''
plt.savefig('plots/polarization/Amp_ratio_test.png')
plt.show()
