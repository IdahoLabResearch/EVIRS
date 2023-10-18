# -*- coding: utf-8 -*-
"""
Spyder Editor

"""

import cv2
from matplotlib import pyplot as plt
import os
import numpy as np
import itertools
import json
import random
from vininfo import Vin
import pandas as pd


x = input("Please enter VIN number: ")
#x = '5YJ3GDEF2LFR00942'
EV = Vin(x)   

r_mile = int(input("Please enter the range: "))
    

# x = Vin('JN1AZ0CP7CT024420')
# x = Vin('5YJ3GDEF2LFR00942')
# x = Vin('5YJYGDEE3MF071288')


# print(x.country)                 
print(EV.manufacturer)             
print(EV.wmi)                      
print(EV.vds)
print(EV.vis)
print(EV.region)
print(EV.years)
#print(x.model)
#print(x.details.model)

#datasheet = pd.read_excel (r'C:\Users\ZHANB\OneDrive - Idaho National Laboratory\python3\task2\VehicleBatteryPackConfig_useforcode.xlsx', sheet_name= 'Tesla', na_values='n/a') 
datasheet = pd.read_excel (os.path.expanduser('~/OneDrive - Idaho National Laboratory/python3/task2/VehicleBatteryPackConfig_useforcode.xlsx'), sheet_name= EV.manufacturer, na_values='n/a')
# print (datasheet)

df = pd.DataFrame(datasheet, columns= ['ID','Model','Year', 'Fuel type','EV range (miles)','Nominal pack voltage (V)','kWh rated', 'Current range (miles)'])
# print (df)

EV_model = EV.vds[0]
print("\n")
print('EV model:', EV_model)

EV_bodytype = EV.vds[1]
print('EV bodytype:', EV_bodytype)

EV_fueltype = EV.vds[3]
print('EV fueltype:', EV_fueltype)

print(EV.years[0])
print(df['Model'].dtype)
print(EV_model)

if df['Model'].dtype == int:

    select_EV = df.loc[(df['Model'] == int(EV_model)) & (df['Year'] == EV.years[0]) & (df['EV range (miles)'] == r_mile)]
    select_EV_T = select_EV.transpose()
    print("\n")
    print (select_EV_T)

elif df['Model'].dtype == object:
    
    select_EV = df.loc[(df['Model'].astype(str) == EV_model) & (df['Year'] == EV.years[0]) & (df['EV range (miles)'] == r_mile)]
    select_EV_T = select_EV.transpose()
    print("\n")
    print (select_EV_T)

elif df['Model'].dtype == str:
    
    select_EV = df.loc[(df['Model'] == EV_model) & (df['Year'] == EV.years[0]) & (df['EV range (miles)'] == r_mile)]
    select_EV_T = select_EV.transpose()
    print("\n")
    print (select_EV_T)

else :
    print("error, please check")


SOC = select_EV['Current range (miles)'].values[0]/ select_EV['EV range (miles)'].values[0]
print("\n")
print("EV SOC is:", SOC)

e_stranded = select_EV['kWh rated'].values[0] * SOC

print("EV energy stranded (kWh) is:", e_stranded)



"""



c_mile = int(input("Please enter the current mile: "))

#SOC = select_EV['Current range (miles)'].values[0]/ select_EV['EV range (miles)'].values[0]
#print("\n")
#print("EV SOC is:", SOC)


"""













