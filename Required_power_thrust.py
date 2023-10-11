import numpy as np


velocity = np.arange(30, 600.005, 0.005)

AR = float(input('AR (ratio) = '))
C_D0 = float(input('C_D0 = '))
e = float(input('Effi = '))
W = float(input('Weight = '))
S = float(input('S (Wing Area) = '))
T = float(input('Thrust = '))
Rho = float(input('Air Desity = '))

T_induced = 2*W**2 / (Rho*S*np.pi*e*AR) * velocity**(-2)
T_para = 0.5*Rho*S*C_D0 * velocity**(2)
T_require = T_induced + T_para

T_require_min = np.min(T_require)
V_atT_require_min = 30 + 0.005*np.where(T_require==T_require_min)[0]
print('T require min = {}, Corresponding Velocity = {}'.format(T_require_min, V_atT_require_min))

P_require = T_require * velocity
P_require_min = np.min(P_require)
V_atP_require_min = 30 + 0.005*np.where(P_require==P_require_min)[0]
print('P require min = {}, Corresponding Velocity = {}'.format(P_require_min, V_atP_require_min))