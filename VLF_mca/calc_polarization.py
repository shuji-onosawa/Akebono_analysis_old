import numpy as np
import matplotlib.pyplot as plt

theta = np.deg2rad(np.linspace(0, 90))

#constant
q = 1.6e-19
eps = 8.9e-12
myu = 1.3e-6
me = 9.1e-31
mh = 1.7e-27
mhe = 6.7e-27
mo = 2.7e-26
c = 2.97e8

#plasma parameter
ne = 100e6
nh = 0.5*ne
nhe = 0*ne
no = 0.5*ne

pi_e = (ne*q**2/(eps*me))**0.5
pi_h = (nh*q**2/(eps*mh))**0.5
pi_he = (nhe*q**2/(eps*mhe))**0.5
pi_o = (no*q**2/(eps*mo))**0.5

omega_h = 2*np.pi*100
B0 = omega_h*mo/q
omega_e = -q*B0/me
omega_o = q*B0/mo
omega_he = q*B0/mhe
wlh = np.sqrt((omega_h**2+pi_h**2)/(1+(pi_e/omega_e)**2))
w = 0.9*omega_o

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

A = S*(np.sin(theta))**2 + P*(np.cos(theta))**2
B = R*L*(np.sin(theta))**2 + P*S*(1+(np.cos(theta))**2)
C = P*R*L
F = np.sqrt(B**2 - 4*A*C)

n1 = np.sqrt((B + F)/(2*A))
n2 = np.sqrt((B - F)/(2*A))

Ey_to_Ex1, Ey_to_Ex2 = - D/(S - n1**2), -D/(S - n2**2)
Ez_to_Ex1, Ez_to_Ex2 = - n1**2*np.cos(theta)*np.sin(theta)/(P - n1**2*np.sin(theta)**2), - n2**2*np.cos(theta)*np.sin(theta)/(P - n2**2*np.sin(theta)**2) 
Bx_to_Ex1, Bx_to_Ex2 = - n1/c*np.cos(theta)*Ey_to_Ex1, - n2/c*np.cos(theta)*Ey_to_Ex2
By_to_Ex1, By_to_Ex2 = n1/c*(np.cos(theta) - Ez_to_Ex1*np.sin(theta)), n2/c*(np.cos(theta) - Ez_to_Ex2*np.sin(theta))
Bz_to_Ex1, Bz_to_Ex2 = n1/c*np.sin(theta)*Ey_to_Ex1, n2/c*np.sin(theta)*Ey_to_Ex2

print(wlh/omega_h)
fig = plt.figure(figsize=(10, 8))

ax1 = fig.add_subplot(2,2,1)
ax1.plot(np.rad2deg(theta), np.ones(theta.size))
ax1.plot(np.rad2deg(theta), Ey_to_Ex1, label='Ey')
ax1.plot(np.rad2deg(theta), Ez_to_Ex1, label='Ez')
ax1.hlines(1, xmin=0, xmax=90, linestyles='dashed', label='Ex')
ax1.set_ylabel('Amplitude ratio')
ax1.legend()
ax1.set_title('Frequency = 0.9*fco')

ax2 = fig.add_subplot(2,2,2)
ax2.plot(np.rad2deg(theta), np.ones(theta.size))
ax2.plot(np.rad2deg(theta), Bx_to_Ex1, label='Bx')
ax2.plot(np.rad2deg(theta), By_to_Ex1, label='By')
ax2.plot(np.rad2deg(theta), Bz_to_Ex1, label='Bz')
ax2.hlines(1, xmin=0, xmax=90, linestyles='dashed', label='Ex')
ax2.legend()

ax3 = fig.add_subplot(2,2,3)
ax3.plot(np.rad2deg(theta), np.ones(theta.size))
ax3.plot(np.rad2deg(theta), Ey_to_Ex2, label='Ey')
ax3.plot(np.rad2deg(theta), Ez_to_Ex2, label='Ez')
ax3.hlines(1, xmin=0, xmax=90, linestyles='dashed', label='Ex')
ax3.set_xlabel('wave normal angle [deg]')
ax3.legend()

ax4 = fig.add_subplot(2,2,4)
ax4.plot(np.rad2deg(theta), np.ones(theta.size))
ax4.plot(np.rad2deg(theta), Bx_to_Ex2, label='Bx')
ax4.plot(np.rad2deg(theta), By_to_Ex2, label='By')
ax4.plot(np.rad2deg(theta), Bz_to_Ex2, label='Bz')
ax4.hlines(1, xmin=0, xmax=90, linestyles='dashed', label='Ex')
ax4.set_xlabel('wave normal angle [deg]')
ax4.legend()

plt.show()
