# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 20:14:02 2023

@author: mrm
"""
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy import interpolate


class model(object):
    """
    System parameter
    ---------------
    system must be in the form of 'first order plus time delay or FOPTD'
    Kp      : process gain
    taup    : process time
    thetap  : process time delay
    
    """
    num_index = 100
    Kp = 2
    taup = 200
    thetap = 0
    init_val = 0
    lift = 2
    
class pid(object):
    """
    Controller Input
    ----------------
    Kc = controller gain
    tauI = integral time
    tauD = derivative timw
    sp = setpoint
    op_hi = anti-reset windup high limit
    op_lo = anti-reset windup low limit

    """
    Kc = 2
    tauI = 10
    tauD = 0
    sp = []
    op_hi = 100
    op_lo = 20
    
def process(y,t,u,Kp,taup):
    """
    Parameters
    ----------
    y : PROCESS VARIABLE / PV
        Representing a control variable of a system
    t : TIME
        Time duration is in second by default of this program
    u : MANIPULATED VARIABLE
        Representing a manipulated variable of a system
    Kp : PROCESS GAIN
        Ratio of the change in process variable/ in manipulated variable
        => deltaPV/deltaMV
    taup : PROCESS TIME
        Time needed for process variable to move

    Returns
    -------
    dydt : TYPE
        DESCRIPTION.
    """
    dydt = -y/taup + Kp/taup*u
    return dydt


def calc_response(t,xm,xc,mode=False,arwnet =False,valvechar = False):
    """
    Parameters
    ----------
    t    : refer to the time duration input
    mode : auto or manual controller mode, auto = 1, manual = 0
    xm   : refer to the class of model system constants Kp, taup, thetap
    xc   : refer to the class of pid controller constants Kc, tauI, tauD
    
    """
    global pv_itplt,op_itplt
    Kp = xm.Kp
    taup = xm.taup
    thetap = xm.thetap
    init_val = xm.init_val
    num_index = xm.num_index
    
    Kc = xc.Kc
    tauI = xc.tauI
    tauD = xc.tauD
    op_hi = xc.op_hi
    op_lo = xc.op_lo
    sp = xc.sp
    
    delta_t = t[1] - t[0]

    pv = np.zeros(num_index+1)
    pv[0] = init_val
    error = np.zeros(num_index+1) 
    ioe = np.zeros(num_index+1)
    dpv = np.zeros(num_index+1)
    P = np.zeros(num_index+1)
    I = np.zeros(num_index+1)
    D = np.zeros(num_index+1)
    op = np.zeros(num_index+1)
    op_tr = np.zeros(num_index+1)
    op_out = np.zeros(num_index+1)
    

    # Manual for single step test
    if mode == True:
        op[100:] = 100
    
    # Manual for interpolate valve characteristic
    if valvechar == True:
        t_interpolate = [100,250,400,550]
        op[t_interpolate[0]:] = 25
        op[t_interpolate[1]:] = 50
        op[t_interpolate[2]:] = 75
        op[t_interpolate[3]:] = 100
        
    for i in range(0,num_index):
        # PID engine
        error[i] = sp[i] - pv[i]
        if i >= 1:
            dpv[i] = (pv[i] - pv[i-1])/delta_t
            ioe[i] = ioe[i-1] + error[i]*delta_t
        P[i] = Kc*error[i]
        I[i] = Kc/tauI*ioe[i]
        D[i] = -Kc*tauD*dpv[i]
        # Apply PID engine output onlye when mode is auto
        if mode == False:
            op[i] = op[0] + P[i] + I[i] + D[i]
        
        # Anti-reset windup
        if arwnet == True:
            if op[i] > 100:
                op[i] = op_hi
                ioe[i] = ioe[i-1] - error[i]*delta_t
            if op[i] < 0:
                op[i] = op_lo
                ioe[i] = ioe[i-1] - error[i]*delta_t
        # simulate system with time delay as long as thetap
        # thetap is time delay of the process system, for instance it is 2.32 seconds then my
        # simulation duration is as long as num_index which is 2 menit or 120 seconds. I then apply
        # linspace to step with evenly spaced from start time to end time 0 - 120-th seconds. Let's say
        # my total step is 150. Then interval between one step to another step is 120/150 which is 4/5 or
        # 0.8 second. Then, the order of the time delay in the indices is 2.32/0.8 ~ 2.9-th.
        # So let's say 0, 0.8, 1.6, 2.4, 3.2. The exact time delay happens between 1.6 --> 2.4 or 2-th --> 3--th indices
        # Using numpy.ceil that 2.9-th index will turn to the ceil of that scalar which is smallest integer i where i > 2.9 
        # and it is 3.
        # in some cases, the method will experience deviation from reality. Consider the case where i have simulation duration
        # for 120 seconds, then i apply linspace of just 10 elements. Then the space between one step to the next step is 12 seconds
        # . The order of the time delay will be 2.32/12 = 0.1934 and by numpy.ceil function the time delay index will be 1-st index
        # which is 12 seconds after the error sample send to the controller. Not quite accurate of actual representation.
        
        # simulate imperfect valve characteristic
        if valvechar == True:
            lift_char = xm.lift
            op_tr[i] = op[i]/100*10
            op_out[i] = op_tr[i]**(lift_char)
        else:
            op_out[i] = op[i]
        
        # simulate time delay
        ndelay = int(np.ceil(thetap/delta_t))
        iop = max(0,i-ndelay)
        
        # simulate system response
        y = odeint(process,pv[i],[0,delta_t],args=(op_out[iop],Kp,taup))
        pv[i+1] = y[-1]
    
    # normalize end point    
    error[num_index] = error[num_index-1] 
    ioe[num_index] = ioe[num_index-1]
    dpv[num_index] = dpv[num_index-1]
    P[num_index] = P[num_index-1]
    I[num_index] = I[num_index-1]
    D[num_index] = D[num_index-1]
    op[num_index] = op[num_index-1]
    
    # special imperfect valve identification
    if valvechar == True:
        pv_itplt = [pv[0],pv[t_interpolate[1]-5],pv[t_interpolate[2]-5],pv[t_interpolate[3]-5],pv[num_index-10]]
        op_itplt = [op[0],op[t_interpolate[1]-5],op[t_interpolate[2]-5],op[t_interpolate[3]-5],op[num_index-10]]
        #op_itplt = [op_out[0],op[t_interpolate[1]-5],op_out[t_interpolate[2]-5],op_out[t_interpolate[3]-5],op_out[num_index-10]]
    return (pv,op)

def auto():
    model.num_index = 1000
    model.Kp = 1.3
    model.taup = 15
    model.thetap = 7
    model.init_val = 0

    t = np.linspace(0,model.num_index,model.num_index+1)

    sp = np.zeros(model.num_index+1)*30  # set point
    sp[50:600] = 70
    sp[600:] = 30
    pid.sp = sp

    pid.Kc = 2
    pid.tauI = 30
    pid.tauD = 0
    pid.op_hi = 100
    pid.op_lo = 0
    
    (pv,op) = calc_response(t,model,pid)

    # plotting
    plt.figure()
    plt.subplot(2,1,1)
    plt.title('PID Response')
    plt.plot(t,pv,'b',linewidth=2, label='PV')
    plt.plot(t,sp,'k--',linewidth=2, label='SP')
    plt.xlabel('Time')
    plt.ylabel('Response')
    plt.legend()
    plt.subplot(2,1,2)
    plt.plot(t,op,'r',linewidth=2, label='OP')
    plt.xlabel('Time')
    plt.ylabel('Response')
    plt.legend()


def valve_generated():
    model.num_index = 1000
    model.Kp = 1.3
    model.taup = 15
    model.thetap = 7
    model.init_val = 0

    t = np.linspace(0,model.num_index,model.num_index+1)

    sp = np.zeros(model.num_index+1)*30  # set point
    sp[50:600] = 70
    sp[600:] = 30
    pid.sp = sp

    pid.Kc = 2
    pid.tauI = 30
    pid.tauD = 0
    pid.op_hi = 100
    pid.op_lo = 0
    
    (pv,op)=(pv,op) = calc_response(t,model,pid, mode = True, valvechar = True)
    # interpolate
    intplt = interpolate.interp1d(op_itplt,pv_itplt)
    opnew = np.linspace(0,100,11)
    pvnew = intplt(opnew)

    plt.figure()
    pic = plt.plot(opnew,pvnew,label='Valve Characteristic')
    plt.ylabel('OP')
    plt.xlabel('PV')
    plt.legend()
    return pic 

auto()
valve_generated()
