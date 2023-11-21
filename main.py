from configs import args
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

span_ratio = args.wingspan**2 / args.wingarea
time_axis_tf = np.arange(0, args.tEnd_tf, args.time_gap)
time_axis_ld = np.arange(0, args.tEnd_ld, args.time_gap)
time_axis_ld2 = np.arange(0, args.tEnd_ld, args.time_gap)
tf_acc_his, tf_velo_his, tf_dis_his = np.zeros_like(time_axis_tf), np.zeros_like(time_axis_tf), np.zeros_like(time_axis_tf)
ld_acc_his, ld_velo_his, ld_dis_his = np.zeros_like(time_axis_ld), np.zeros_like(time_axis_ld), np.zeros_like(time_axis_ld)
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
    if condition == 'takeoff':
        CD0 = args.CD0_takeoff
        CL = args.CL_takeoff
        mu = args.mu_normal
    elif condition == 'landing':
        CD0 = args.CD0_landing
        CL = args.CL_landing
        mu = args.mu_brake
    else:
        raise Exception('Please correct the condition')
    lift = Lift_Calculation(velocity, condition, args)
    drag = Drag_Calculation(velocity, condition, args)
    friction = mu*(args.weight_max-lift)
    if condition == 'takeoff':
        efficient_force = args.thrust_max - (drag + friction)
    elif condition == 'landing':
        efficient_force = args.thrust_revs + (drag + friction)
    return efficient_force, (lift, drag)

def Efficient_Force_diffu(velocity, mu, condition='takeoff', args=args):
    lift = Lift_Calculation(velocity, condition, args)
    drag = Drag_Calculation(velocity, condition, args)
    friction = mu*(args.weight_max-lift)
    if condition == 'takeoff':
        efficient_force = args.thrust_max - (drag + friction)
    elif condition == 'landing':
        efficient_force = args.thrust_revs + (drag + friction)
    return efficient_force, (lift, drag)


# ============================== Begin the integration ====================================
acceleration_min = 0
acceleration_max = 100
sns.set(style='whitegrid', font='Calibri')


for i in range(0, time_axis_tf.shape[0]-1):
    velocity = tf_velo_his[i]
    efficient_force, (lift, drag) = Efficient_Force(velocity, condition='takeoff', args=args)
    
    if lift >= args.weight_max:
        print('When velocity = {}(m/s), the lift equals to maximum weight'.format(velocity))
        print('It takes {}(m) runway to takeoff'.format(tf_dis_his[i]))
        time_axis_tf = time_axis_tf[:i]
        tf_dis_his = tf_dis_his[:i]
        tf_velo_his = tf_velo_his[:i]
        tf_acc_his = tf_acc_his[:i]
        break
    
    acceleration = max(min(efficient_force / (args.weight_max / args.g), acceleration_max), acceleration_min)
    velocity += acceleration * args.time_gap
    tf_dis_his[i+1] = tf_dis_his[i] + velocity*args.time_gap
    tf_velo_his[i+1] = velocity
    tf_acc_his[i+1] = acceleration

for j in range(0, time_axis_ld.shape[0]-1):
    velocity = ld_velo_his[j]
    efficient_force, (lift, drag) = Efficient_Force(velocity, condition='landing', args=args)
    acceleration = max(min(efficient_force / (args.weight_max / args.g), acceleration_max), acceleration_min)
    velocity += acceleration * args.time_gap
    displacement = ld_dis_his[j] + velocity*args.time_gap
    ld_dis_his[j+1] = displacement
    ld_velo_his[j+1] = velocity
    ld_acc_his[j+1] = acceleration
    if ld_dis_his[j] >= args.len_runway:
        print('Max landing Velocity is {}'.format(velocity))    
        break
    rev_ld_dis_his = args.len_runway - ld_dis_his



eval_velo_acc = 0.01
eval_velo = np.arange(0, 70, eval_velo_acc)
for x in range(0, eval_velo.shape[0]-1):
    sampled_v = eval_velo[x]
    select_lpoint_tf, select_lpoint_ld = 0, 0
    select_vpoint_tf, select_vpoint_ld = 0, 0
    for y in range(0, tf_dis_his.shape[0]-1):
        if tf_velo_his[y] < sampled_v and tf_velo_his[y+1] >= sampled_v:
            select_lpoint_tf = tf_dis_his[y]
            select_vpoint_tf = tf_velo_his[y]
            break
    for z in range(0, rev_ld_dis_his.shape[0]-1):
        if ld_velo_his[z] < sampled_v and ld_velo_his[z+1] >= sampled_v:
            select_lpoint_ld = ld_dis_his[z]
            select_vpoint_ld = ld_velo_his[z]
            break
    if select_lpoint_ld + select_lpoint_tf >= args.len_runway:
        print(
            'The intersection point locates at the {}(m) of the runway, with the velocity = {}m/s'.format(
            min(select_lpoint_tf, select_lpoint_ld), sampled_v))
        break


eval_mu_acc = 0.0001
eval_mu = np.arange(0.1, 0.2, eval_mu_acc)
stored_velo = 9.7222
for q in range(eval_mu.shape[0]-1):
    sampled_u = eval_mu[q]
    ld2_acc_his, ld2_velo_his, ld2_dis_his = np.zeros_like(time_axis_ld2), np.ones_like(time_axis_ld2)*9.7222, np.zeros_like(time_axis_ld2)
    for k in range(0, time_axis_ld.shape[0]-1):
        velocity = ld2_velo_his[k]
        efficient_force, (lift, drag) = Efficient_Force_diffu(velocity, sampled_u, condition='landing', args=args)
        acceleration = max(min(efficient_force / (args.weight_max / args.g), acceleration_max), acceleration_min)
        velocity += acceleration * args.time_gap
        displacement = ld2_dis_his[k] + velocity*args.time_gap
        ld2_dis_his[k+1] = displacement
        ld2_velo_his[k+1] = velocity
        ld2_acc_his[k+1] = acceleration
        if ld2_dis_his[k] >= 2500:
            # print('Max landing Velocity is {}'.format(velocity))    
            break
        rev_ld2_dis_his = 2500 - ld2_dis_his
    if velocity >= 78.956 and stored_velo < 78.956:
        print('The minimum required mu is {}'.format(sampled_u))    
        break
    stored_velo = velocity



plt.plot(tf_dis_his, tf_velo_his, color=sns.xkcd_rgb['windows blue'], label='Max takeoff V with MTOW')
plt.plot(rev_ld_dis_his, ld_velo_his, color=sns.xkcd_rgb['amber'], label="Max landing V with MTOW")
plt.title("Takeoff Rejected Speed")
plt.xlabel("Runway Used (m)")
plt.ylabel("Velocity (m/s)")
plt.legend()
plt.show()
