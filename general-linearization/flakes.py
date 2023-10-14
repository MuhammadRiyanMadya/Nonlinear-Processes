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
        self.u      = {}
        self.pv     = None
        
    def model(self,y,t,uf,Kp,taup,thetap):

        if self.name == 'fopdt':
            try:
                if (time - thetap) < 0:
                    u = uf(0)
                else:
                    u = uf(t - thetap)
            except:
                u = uf(0)
            dydt = (Kp*u - y)/taup
            return dydt

    def response(step:dict,
                Kp,
                taup,
                thetap = 0 ,
                filename = 'Step_Data_1', save = False):
        
        self.Kp = Kp
        self.taup = taup
        self.thetap = thetap
        t = []
        for i in range(0, self.time + 1):
                t.append(i)    
        
        self.u = []
        for i in range(0, self.time + 1):
                self.u.append(0)
        for keys,values in step():
            for n in range(keys,len(self.u)):
                self.u[keys]= values
            
        uf = interpolate.interp1d(t,u)
        
        self.pv = [0]
        for i in range(0,self.time + 1):
            if i < 1:
                delta_t = [0,1]
            else:
                delta_t = [t[i-1],t[i]]
            yt = integrate.odeint(self.model(,pv[i],delta_t,args=(uf,self.Kp,self.taup,self.thetap))
            self.pv.append(yt[1,0])

        del self.pv[0]
        dt = [t, self.u, self.pv]
        
        # ------------------- #
        
        if save == True:
            try: 
                df = pd.DataFrame(dt).transpose()
                df.columns = ['Time', 'OP','PV']
                print(df)
                df.to_excel(filename + '.xlsx')
            except:
                "Please input your filename"
        return dt

    def graph(t,op,pv,show = True ):
        if len(t) == len(op) == len(pv) and show == True:
            plt.figure(1)
            plt.subplot(2,1,1)
            plt.plot(t,pv,'b-',linewidth = 3,label='process variable')
            plt.legend()
            plt.ylabel('% pv')
            plt.subplot(2,1,2)
            plt.plot(t,op,'g-',linewidth = 3,label='manipulated variable')
            plt.legend()
            plt.ylabel('% op')
            plt.xlabel('Time')
            plt.show()
        
dt_1 = process(100,[0,30], save = True)

dt_2 = process(100,[0,30], save = True)

graph(dt[0],dt[1],dt[2], show = False)
