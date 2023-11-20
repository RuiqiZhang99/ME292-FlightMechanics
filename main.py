from configs import args
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

span_ratio = args.wingspan**2 / args.wingarea
time_axis = np.arange(0, args.tEnd, args.time_gap)
acceleration_his, velocity_his, displace_his = np.zeros_like(time_axis), np.zeros_like(time_axis), np.zeros_like(time_axis)
condition = args.condition

def Drag_Calculation(velocity, condition='takeoff', args=args):
    if condition == 'takeoff':
        CD0 = args.CD0_takeoff
        CL = args.CL_takeoff
    elif condition == 'landing':
        CD0 = args.CD0_landing
        CL = args.CL_landing
    else:
        raise Exception('Please correct the condition')

    para_drag = 0.5 * args.rho_air * velocity**2 * args.wingarea * CD0
    indu_drag_factor = (16*args.wingtip_h/args.wingspan)**2 / (1+(16*args.wingtip_h/args.wingspan)**2)
    indu_drag = 0.5 * args.rho_air * velocity**2 * args.wingarea * CL**2/(math.pi*args.efficiency*span_ratio) * indu_drag_factor
    total_drag = para_drag + indu_drag
    return total_drag


def Lift_Calculation(velocity, condition='takeoff', args=args):
    if condition == 'takeoff':
        CD0 = args.CD0_takeoff
        CL = args.CL_takeoff
    elif condition == 'landing':
        CD0 = args.CD0_landing
        CL = args.CL_landing
    else:
        raise Exception('Please correct the condition')

    total_lift = 0.5 * args.rho_air * velocity**2 * args.wingarea * CL
    return total_lift



def Efficient_Force(velocity, condition='takeoff', args=args):
    # When takeoff
    lift = Lift_Calculation(velocity, condition='takeoff', args=args)
    drag = Drag_Calculation(velocity, condition='takeoff', args=args)
    friction = args.mu_normal*(args.weight_max-lift)
    efficient_force = args.thrust_max - (drag + friction)
    return efficient_force, (lift, drag)

if condition == 'takeoff':
    acceleration_min = 0
    acceleration_max = 100
elif condition == 'landing':
    acceleration_min = -100
    acceleration_max = 0
else:
    raise Exception('Please correct the condition')
for i in range(0, time_axis.shape[0]-1):
    velocity = velocity_his[i]
    efficient_force, (lift, drag) = Efficient_Force(velocity, condition='takeoff', args=args)
    if lift >= args.weight_max:
        print('When velocity = {}(m/s), the lift equals to maximum weight'.format(velocity))
        time_axis = time_axis[:i]
        displace_his = displace_his[:i]
        velocity_his = velocity_his[:i]
        acceleration_his = acceleration_his[:i]
        break
    acceleration = max(min(efficient_force / (args.weight_max / args.g), acceleration_max), acceleration_min)
    velocity += acceleration * args.time_gap
    displace_his[i+1] = displace_his[i] + velocity*args.time_gap
    velocity_his[i+1] = velocity
    acceleration_his[i+1] = acceleration

plt.subplot(411)
plt.plot(time_axis, acceleration_his)
plt.subplot(412)
plt.plot(time_axis, velocity_his)
plt.subplot(413)
plt.plot(time_axis, displace_his)
plt.subplot(414)
plt.plot(displace_his, velocity_his)
plt.show()