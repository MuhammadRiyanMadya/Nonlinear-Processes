#! usr/bin/env python3

"""Module generate: generating process system model responses"""


from scipy import integrate, interpolate
import matplotlib.pyplot as plt
import pandas as pd

class flakes():
    def __init__(self, time = 0, name = 'fopdt'):
        self.time   = time
        self.name   = name
        self.Kp     = None
        self.taup   = None
        self.thetap = None
        self.t      = []
        self.u      = []
        self.pv     = None
        
    def __model(self,y,t,uf,Kp,taup,thetap):

        if self.name == 'fopdt':
            try:
                if (t - thetap) < 0:
                    u = uf(0)
                else:
                    u = uf(t - thetap)
            except:
                u = uf(0)
            dydt = (Kp*u - y)/taup
            return dydt

    def response(self,
                 step       :dict,
                 Kp         :int,
                 taup       :int,
                 thetap     :int = 0,
                 IV         :int = 0,
                 Input0     :int = 0,
                 time0      :int = 0,
                 filename   :str = 'Step_Data_1',
                 save       :bool = False
                 ):
        
        self.Kp = Kp
        self.taup = taup
        self.thetap = thetap

        for i in range(time0, self.time + 1):
                self.t.append(i)    
        
        for i in range(0, self.time + 1):
                self.u.append(Input0)
        for keys,values in step.items():
            for n in range(keys,len(self.u)):
                self.u[n]= values
            
        uf = interpolate.interp1d(self.t,self.u)
        
        self.pv = [IV]
        for i in range(0,self.time + 1):
            if i < 1:
                delta_t = [0,1]
            else:
                delta_t = [self.t[i-1],self.t[i]]
            yt = integrate.odeint(self.__model,self.pv[i],delta_t,args=(uf,self.Kp,self.taup,self.thetap))
            self.pv.append(yt[1,0])

        del self.pv[0]
        dt = [self.t, self.u, self.pv]

        return dt

    def graph(self,data: dict, show = True ):
        for i in range(1, len(data) + 1):
            plt.figure(i)
            for n in data:
                plt.plot(n[0],n[1],label= 'process')
                if show == True:
                    plt.show()
        
