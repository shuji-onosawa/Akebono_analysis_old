import numpy as np
import matplotlib.pyplot as plt

theta = np.deg2rad(np.arange(0, 90, 0.01))

# constant
Q = 1.6e-19
EPS = 8.9e-12
MYU = 1.3e-6
ME = 9.1e-31
MH = 1.7e-27
MHE = 6.7e-27
MO = 2.7e-26
C = 2.97e8

# plasma parameter
NE = 100e6
nh = 0.5*NE
nhe = 0*NE
no = 0.5*NE

pi_e = (NE*Q**2/(EPS*ME))**0.5
pi_h = (nh*Q**2/(EPS*MH))**0.5
pi_he = (nhe*Q**2/(EPS*MHE))**0.5
pi_o = (no*Q**2/(EPS*MO))**0.5

omega_h = 2*np.pi*100
B0 = omega_h*MO/Q
omega_e = -Q*B0/ME
omega_o = Q*B0/MO
omega_he = Q*B0/MHE
wlh = np.sqrt((omega_h**2+pi_h**2)/(1+(pi_e/omega_e)**2))
w = 0.5*omega_o

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

n = np.array([np.sqrt((B + F)/(2*A)), np.sqrt((B - F)/(2*A))])

Ey_to_Ex = - D/(S - n**2)
# plus(minus) means Eperp rotate in the same direction as ion(electron) gyro
Ez_to_Ex = - (n**2)*np.cos(theta)*np.sin(theta)/(P - (n**2)*np.sin(theta)**2)

By_to_Bx = -P*(S - n**2)/(D*(P - (n**2)*(np.sin(theta))**2))
Bz_to_Bx = -np.tan(theta)

rho = MO*no + MH*nh + MHE*nhe
Va = B0/(MYU*rho)
E_to_B_Va = C/n/Va*np.sqrt((1+((P-n**2)*(S-n**2)*(np.sin(theta)))**2/((P*np.cos(theta)*(S-n**2))**2-D*(P-(n*np.sin(theta))**2)**2)))

print(Va)
print(wlh/omega_h)
fig = plt.figure(figsize=(10, 10))

ax1 = fig.add_subplot(311)
ax1.plot(np.rad2deg(theta), Ey_to_Ex[0], label='Ey/Ex +')
ax1.plot(np.rad2deg(theta), Ey_to_Ex[1], label='Ey/Ex -')
ax1.plot(np.rad2deg(theta), Ez_to_Ex[0], label='Ez/Ex +')
ax1.plot(np.rad2deg(theta), Ez_to_Ex[1], label='Ez/Ex -')
ax1.set_ylabel('Amplitude ratio')
ax1.set_ylim(-1.1, 1.1)
ax1.legend()
ax1.set_title('Frequency = 0.5*fco')

ax2 = fig.add_subplot(312)
ax2.plot(np.rad2deg(theta), By_to_Bx[0], label='By/Bx +')
ax2.plot(np.rad2deg(theta), By_to_Bx[1], label='By/Bx -')
ax2.plot(np.rad2deg(theta), Bz_to_Bx, label='Bz/Bx')
ax2.set_ylabel('Amplitude ratio')
ax2.set_ylim(-10, 10)
ax2.legend()

ax3 = fig.add_subplot(313)
ax3.plot(np.rad2deg(theta), E_to_B_Va[0], label='E/VaB +')
ax3.plot(np.rad2deg(theta), E_to_B_Va[1], label='E/VaB -')
ax3.set_ylabel('E/B/Va')
plt.show()
plt.savefig('plots/polarization/Amp_ratio_<fci.png')
