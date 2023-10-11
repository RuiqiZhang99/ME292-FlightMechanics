# Calculate the power required curves of Boeing 737 Max 8 twin

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set(style='darkgrid', font='Times New Roman')
x_axis = np.arange(10, 350)
power_required = 0.001*(2.4892*(x_axis**3) + 2.5694484e8/x_axis)
jet_engine_power = 260*x_axis


plt.plot(x_axis, power_required, color=sns.xkcd_rgb['amber'], label='Power required')
plt.plot(x_axis, jet_engine_power, color=sns.xkcd_rgb['windows blue'], label='Engine Power')
plt.yticks([0, 20000, 40000, 60000, 80000, 100000], ['0', '20k', '40k', '60k', '80k', '100k'])
plt.xlabel('Velocity (m/s)')
plt.ylabel('Power (kW)')
plt.title('The Power Required Curve (Boeing-737 Max)')
plt.show()

for i in range(len(x_axis.tolist())+1):
    if power_required.tolist()[i-1] < jet_engine_power.tolist()[i-1] and power_required.tolist()[i] >= jet_engine_power.tolist()[i]:
        print(x_axis[i])