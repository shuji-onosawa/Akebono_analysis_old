import numpy as np


def get_num_ion_species():
    import plasma_params as pp
    num_ion_species = sum(pp.ion_ratio != 0)
    return num_ion_species


def get_crossover_freq_idx(array, value):
    num_ion_species = get_num_ion_species()
    print(num_ion_species)
    array_ = np.copy(array)
    idx = np.empty(num_ion_species, dtype=int)
    for i in range(num_ion_species):
        idx[i] = int(np.nanargmin(np.abs(array_ - value)))
        array_[idx[i]] = np.nan

    return idx


def calc_dispersion_relation(w, theta):
    """
    theta: int, wave normal angle, 0 - 90 [deg]

    return: n_L, n_R, S, D, P
    """
    import plasma_params as pp

    Theta = np.deg2rad(theta)

    Xe = (pp.pi_e/w)**2
    Xh = (pp.pi_h/w)**2
    Xhe = (pp.pi_he/w)**2
    Xo = (pp.pi_o/w)**2
    Ye = pp.omega_e/w
    Yh = pp.omega_h/w
    Yhe = pp.omega_he/w
    Yo = pp.omega_o/w

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

    n_L = np.nan*np.arange(w.size)
    n_R = np.nan*np.arange(w.size)

    polarization_plus = - D / (S - n_plus)
    polarization_minus = - D / (S - n_minus)

    L_mode_plus_idx = np.where(polarization_plus < 0)
    L_mode_minus_idx = np.where(polarization_minus < 0)
    R_mode_plus_idx = np.where(polarization_plus > 0)
    R_mode_minus_idx = np.where(polarization_minus > 0)

    n_L[L_mode_plus_idx[0]], n_L[L_mode_minus_idx[0]] = \
        n_plus[L_mode_plus_idx[0]], n_minus[L_mode_minus_idx[0]]
    n_R[R_mode_plus_idx[0]], n_R[R_mode_minus_idx[0]] = \
        n_plus[R_mode_plus_idx[0]], n_minus[R_mode_minus_idx[0]]

    return n_L, n_R, S, D, P
