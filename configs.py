import argparse

parser = argparse.ArgumentParser()

# Conditions
parser.add_argument('--rho_air', type=float, default=1.225) # Air Desity
parser.add_argument('--T', type=float, default=288.15) # Temperatrue
parser.add_argument('--P', type=float, default=101325) # Air Pressure
parser.add_argument('--v_air', type=float, default=1.789e-5) # Viscocity of Air
parser.add_argument('--g', type=float, default=9.81) # Gravity

# Airpot Information
parser.add_argument('--len_runway', type=float, default=3618)
parser.add_argument('--mu_normal', type=float, default=0.02) # Normal coefficient of rolling friction
parser.add_argument('--mu_brake', type=float, default=0.067) # Coefficient of rolling friction while braking

# Aircraft Information
parser.add_argument('--weight_max', type=float, default=575000*9.81)
parser.add_argument('--thrust_max', type=float, default=979968)
parser.add_argument('--thrust_revs', type=float, default=0.15*979968)
parser.add_argument('--wingtip_h', type=float, default=7.8)
parser.add_argument('--wingspan', type=float, default=79.75)
parser.add_argument('--wingarea', type=float, default=845)
parser.add_argument('--efficiency', type=float, default=0.9)

# Aircraft Properties
parser.add_argument('--CL_takeoff', type=float, default=1.423)
parser.add_argument('--CL_landing', type=float, default=1.203)
parser.add_argument('--CD0_takeoff', type=float, default=0.013)
parser.add_argument('--CD0_landing', type=float, default=0.0143)

# Simulation Settings
parser.add_argument('--tEnd', type=float, default=1000)
parser.add_argument('--time_gap', type=float, default=0.1)
parser.add_argument('--condition', type=str, default='takeoff')


args = parser.parse_args()