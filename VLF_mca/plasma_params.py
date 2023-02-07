import numpy as np

# constant
Q = 1.6e-19  # [C]
EPS = 8.9e-12  # [F m*-1]
MYU = 1.3e-6  # [N A**-2]
ME = 9.1e-31  # [kg]
MH = 1.7e-27  # [kg]
MHE = 6.7e-27  # [kg]
MO = 2.7e-26  # [kg]
C = 2.97e8  # [m s**-1]
B0 = 6e-6  # [T]

# plasma parameter
NE = 100e6  # [m**-3]
ion_ratio = np.array([0.5, 0, 0.5])
nh = ion_ratio[0]*NE
nhe = ion_ratio[1]*NE
no = ion_ratio[2]*NE

RHO = sum(ion_ratio*np.array([MH, MHE, MO]))

pi_e = (NE*Q**2/(EPS*ME))**0.5
pi_h = (nh*Q**2/(EPS*MH))**0.5
pi_he = (nhe*Q**2/(EPS*MHE))**0.5
pi_o = (no*Q**2/(EPS*MO))**0.5

omega_h = 2*np.pi*100
omega_e = -Q*B0/ME
omega_o = Q*B0/MO
omega_he = Q*B0/MHE
wlh = np.sqrt((omega_h**2+pi_h**2)/(1+(pi_e/omega_e)**2))
wuh = (omega_e**2 + pi_e**2)**0.5
Va = B0/(MYU*RHO)**0.5

print(pi_e/6)