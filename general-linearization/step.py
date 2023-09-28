#! usr/bin/env python3

""" valve characterization module -- version 1.0.0"""

import pandas as pd
import numpy as np

__counter = 0


def file(
    title,
    sheet_name,
    usecols,
    bottom_row,
    header = 0
    ):
    
    df_exc = pd.read_excel('title', sheet_name = 'sheet_name', usecols = '',header = int'header')
    df_np = df_exc.values[:int(bottom_row)]

    #check if the data is normal without any NAN value or the length is different
    ...
    return df_exc, df_np

def valve(df_np):
    t = df_np[:,0]
    OP = df_np[:,1]
    PV = df_np[:,2]

    #detect if a change in valve opening is classified as step test:
    #criteria:
    #           Loop
    # 1. Time <2 seconds
    # 2. OP change > 1%
    # 3. PV before the OP change is steady
    # 4. Extract Kp, taup, and DT using foptd model
    # 5. Checker whether PV before OP change is steady state criteria
    # 6. Pull back as far as 2*taup, if the gradient is fulfilled the requirement provided from
    #    Kp, the it's OK
    #           Verification
    # 1. Obtained all step test from the loop
    # 2. Check if all the obtained Kp, taup, and DT distribution is normal
    # 3. If the distribution is far from normal, then detect the valve character --> inform the user 
    # 4. Reccomend to input valve design data
    # 5. Use soptd model

    
    max_OP = max(OP)
    min_OP = min(OP)
    max_PV = max(OP)
    min_PV = min(OP)
    scale_OP = max_OP - min_OP
    scale_OP = max_OP - min_OP
    
    for i in range(len(valve_OP)):
        delta_OP = OP[i+1] - OP[i]
        delta_PV = PV[i+1] - PV[i]
        
    return valve_OP, valve_PV

def graphic(Valve_OP, valve_PV)
    return graph
