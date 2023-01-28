import numpy as np
import matplotlib.pyplot as plt

ne = 225e6
nh = 0.5*ne
nhe = 0*ne
no = 0.5*ne
q = 1.6e-19
eps = 8.9e-12
myu = 1.3e-6

me = 9.1e-31
mh = 1.7e-27
mhe = 6.7e-27
mo = 2.7e-26
rho = mo*no + mh*nh + mhe*nhe
c = 2.99792458e+8

pi_e = (ne*q**2/(eps*me))**0.5
pi_h = (nh*q**2/(eps*mh))**0.5
pi_he = (nhe*q**2/(eps*mhe))**0.5
pi_o = (no*q**2/(eps*mo))**0.5

omega_o = 2*np.pi*6
B0 = omega_o*mo/q
omega_e = -q*B0/me
omega_h = q*B0/mh
omega_he = q*B0/mhe

print(B0, omega_h)


def calc_dispersion_relation(w, theta):
    """
    theta: wave normal angle, 0 - 90 [deg]
    """

    Theta = np.deg2rad(theta)

    Xe = (pi_e/w)**2
    Xh = (pi_h/w)**2
    Xhe = (pi_he/w)**2
    Xo = (pi_o/w)**2
    Ye = omega_e/w
    Yh = omega_h/w
    Yhe = omega_he/w
    Yo = omega_o/w

    R = 1 - Xe/(1 + Ye) - Xh/(1 + Yh) - Xhe/(1 + Yhe) - Xo/(1 + Yo)
    L = 1 - Xe/(1 - Ye) - Xh/(1 - Yh) - Xhe/(1 - Yhe) - Xo/(1 - Yo)

    S = (R + L)*0.5
    D = (R - L)*0.5
    P = 1 - Xe - Xh - Xhe - Xo

    A = S*(np.sin(Theta))**2 + P*(np.cos(Theta))**2
    B = R*L*(np.sin(Theta))**2 + P*S*(1+(np.cos(Theta))**2)
    C = P*R*L
    F = np.sqrt(B**2 - 4*A*C)

    n_plus = (B + F)/(2*A)
    n_minus = (B - F)/(2*A)

    return n_plus, n_minus, S, D, P, L, R


def k_energy(w, E, theta, alpha):
    theta = np.deg2rad(theta)
    alpha = np.deg2rad(alpha)
    k_energy = (w - omega_o)/((2*E/mo)*np.cos(theta)*np.cos(alpha))
    return k_energy


va = 1e7
wuh = (omega_e**2 + pi_e**2)**0.5
wlh = ((omega_h**2 + pi_h**2)/(1 + (pi_e/omega_e)**2))**0.5

# dispersion calc
omega_s = np.abs(omega_o)
angler_freq = omega_s*np.arange(1e-2, wlh/omega_o, 1e-4)

n_plus, n_minus, S, D, P, L, R = calc_dispersion_relation(angler_freq, 0)

print(B0)
pi_2 = 2*np.pi
char_freq = np.array([omega_h, omega_o, -omega_e, wlh]) / omega_s

fig = plt.figure(figsize=[16, 8])
ax1 = fig.add_subplot(121)
ax1.plot(angler_freq/omega_s, R, label=r'$n^2 R$', color='blue')
ax1.plot(angler_freq/omega_s, L, label=r'$n^2 L$', color='red')
ax1.vlines(char_freq, 0, 1e7, linestyles='dashed', colors='k')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel(r'$\omega / \Omega_O$')
ax1.set_ylabel(r'$Refraction index ^2$')
plt.legend()

ax2 = fig.add_subplot(122)
ax2.plot(angler_freq/omega_s, n_plus, label=r'$n^2 +$', color='blue')
ax2.plot(angler_freq/omega_s, n_minus, label=r'$n^2 -$', color='red')
ax2.vlines(char_freq, 0, 1e7, linestyles='dashed', colors='k')
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_xlabel(r'$\omega / \Omega_O$')
ax2.set_ylabel(r'$Refraction index ^2$')

plt.legend()
plt.show()
