# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import bspline
import bspline.splinelab as splinelab
from numpy import *
class Order:
   #'Common class for all order'
    
    def __init__(self, curOrder):
        if(curOrder[1] == 0):
            self.stable = True
        else:
            self.stable = False        
        self.time = curOrder[2]
        self.size = curOrder[3]
        self.price = curOrder[4]
        
    def getTime(self):
        return self.time
    
    def isStable(self):
        return self.stable
    
    def getSize(self):
        return self.size
    
    def getPrice(self):
        return self.price
class OrderBook:
   #'Common class for all orderbook'
   
    def __init__(self, symbol):
        self.symbol = symbol
        self.buyOB = dict()
        self.sellOB = dict()
    
    def addOrder(self, df, orderNumber):
        curOrder = (df.values)[orderNumber]
        if(curOrder[0]=='B'):
            self.buyOB[str(curOrder[4])] = (Order(curOrder))
        else:
            self.sellOB[str(curOrder[4])] = (Order(curOrder))

    def printOrderBook(self):
        self.buyslist = list(self.buyOB.keys())
        self.buyslist.sort(key=float,reverse=True)
        print("Bid")
        for i in range(0,len(self.buyslist)):
            if(self.buyOB[self.buyslist[i]].getSize() != 0):
                print("%8.2f %8.2f" % (self.buyOB[self.buyslist[i]].getPrice(), self.buyOB[self.buyslist[i]].getSize()))
        
        self.sellslist = list(self.sellOB.keys())
        self.sellslist.sort(key=float)
        print("Ask")
        for i in range(0,len(self.sellslist)):
            if(self.sellOB[self.sellslist[i]].getSize() != 0):
                print("%8.2f %8.2f" % (self.sellOB[self.sellslist[i]].getPrice(), self.sellOB[self.sellslist[i]].getSize()))
                
    def bids(self):
        self.buyslist = list(self.buyOB.keys())
        self.buyslist.sort(key=float ,reverse=True)
        self.cleanedBuyOB = dict()
        for i in range(0,len(self.buyslist)):
            if(self.buyOB[self.buyslist[i]].getSize() != 0):
                 self.cleanedBuyOB[self.buyslist[i]] = self.buyOB[self.buyslist[i]]
        return self.cleanedBuyOB
    
    def asks(self):
        self.sellslist = list(self.sellOB.keys())
        self.sellslist.sort(key=float)
        self.cleanedSellOB = dict()
        for i in range(0,len(self.sellslist)):
            if(self.sellOB[self.sellslist[i]].getSize() != 0):
                 self.cleanedSellOB[self.sellslist[i]] = self.sellOB[self.sellslist[i]]
        return self.cleanedSellOB
def orderBookProcessing(OBdf, symbol, time): #time in nanoseconds
    ob = OrderBook(symbol)
    OBdfv = OBdf.values
    for index in range(0,OBdfv.shape[0]):
        if (OBdfv[index][2] >= time):
            break
        ob.addOrder(OBdf, index)
    return ob
def dateNum(y, m, d):
    m = (m + 9) % 12
    y = y - int(m / 10)
    return 365 * y + int(y / 4) - int(y / 100) + int(y / 400) + int((m * 306 + 5) / 10) + (d - 1)

def dateFromEpoch(tdays):
    epochyear = 1970;
    epochmonth = 1;
    epochday = 1
    tdays = tdays + dateNum(epochyear, epochmonth, epochday)
    y = int((10000 * tdays + 14780) / 3652425)
    ddd = tdays - (365 * y + int(y / 4) - int(y / 100) + int(y / 400))
    if (ddd < 0):
        y = y - 1
        ddd = tdays - (365 * y + int(y / 4) - int(y / 100) + int(y / 400))
    mi = int((100 * ddd + 52) / 3060)
    mm = (mi + 2) % 12 + 1
    y = y + int((mi + 2) / 12)
    dd = ddd - int((mi * 306 + 5) / 10) + 1
    dateV = list()
    dateV.append(int(y))
    dateV.append(int(mm))
    dateV.append(int(dd))
    return dateV

def getHumanTime(t):
    tseconds = int(t / 1000000000);
    ns = t % 1000000000;
    tminutes = int(tseconds / 60);
    s = tseconds % 60;
    thour = int(tminutes / 60);
    mins = tminutes % 60;
    tday = int(thour / 24);
    h = thour % 24;
    hdate = dateFromEpoch(tday)
    hdate.append(int(h))
    hdate.append(int(mins))
    hdate.append(int(s))
    hdate.append(int(ns))
    return hdate

def printHumanTimeFull(hdate):
    print(str(hdate[0]) + " Year")
    print(str(hdate[1]) + " Month")
    print(str(hdate[2]) + " Day")
    print(str(hdate[3]) + " Hour")
    print(str(hdate[4]) + " Minute")
    print(str(hdate[5]) + " Second")
    print(str(hdate[6]) + " Nanosecond")
    
def printHumanTime(hdate):
    result = "%04d/%02d/%02d %02d:%02d:%02d.%d " % (hdate[0], hdate[1], hdate[2], hdate[3], hdate[4], hdate[5], hdate[6])
    return(result)

def changetohumantime(df):
    newlist = df['Timestamp'].tolist()
    Humantime_list = []
    for each in newlist:
        a = printHumanTime(getHumanTime(each))
        Humantime_list.append(a)
    df['Timestamp']=pd.Series(Humantime_list)

#orderbook testing
JPdf = pd.read_csv("JPM_2018_2_16.csv")
changetohumantime(JPdf)

#sorting orders according to buy or sell side
JPdf_sell = JPdf.loc[JPdf['Side'] == 'S']    
JPdf_buy = JPdf.loc[JPdf['Side'] == 'B']
#always remember to reset indes
JPdf_sell = JPdf_sell.reset_index(drop = True)
JPdf_buy = JPdf_buy.reset_index(drop = True)

#add order volume in every 5-min time interval,then in one day we'll have 72 data
#choose data in regular market session, which is 10:00am - 4:00pm in all 
ndata = 72
#aggre_sell = [0]*ndata     
#create aggregated volume list at sell side of 390 data,initial value =0 
for i in range(len(JPdf_sell['Timestamp'])):
    ntime = JPdf_sell['Timestamp'][i].split(" ")[1]
    time_list = ntime.split(":")
    if int(time_list[0])==20:
        nend = i
        break
#remove data after 4:00pm
JPdf_sellclean = JPdf_sell[2:nend].reset_index(drop = True)
#REINDEX
JPdf_sellclean1 = JPdf_sellclean.pivot(index = 'Timestamp',columns = 'Price',values = 'Size')
JPdf_sellclean2 = JPdf_sellclean1.fillna(0)
#differentiate to calculate net volume update
JPdf_sellclean3 = JPdf_sellclean2.diff()
#ensure the first line is not nan
#subtract the negative values
JPdf_sellclean3.iloc[0] = JPdf_sellclean2.iloc[0]
JPdf_sellclean3[JPdf_sellclean3<0]=0
import datetime
#time processing 
JPdf_sellclean3.index = pd.to_datetime(JPdf_sellclean3.index)
#calculate aggregated sell volume every 5 minute 
JPdf_sellclean4 = JPdf_sellclean3.resample('5T').sum()
JPdf_sellclean4 = JPdf_sellclean4.fillna(0)
JPdf_sellclean5 = JPdf_sellclean4.shift(1,freq = '5T')   #shift and add the missing two time
df2 = pd.DataFrame(index = ['2018-02-16 14:05:00','2018-02-16 14:10:00'],columns
                   = JPdf_sellclean5.columns)
JPdf_sellclean6 = pd.concat([df2,JPdf_sellclean5],axis = 0)
JPdf_sellclean6.iloc[[0,1],:]=0

#constructing data
best_ask = []    #best ask price list 
spread_list = []   
volume_list = [] #store order update for all 72 t
inv_list = []    #interval list
J  = 50 
#contructing {Y_t,j}t:1-72,j:0-J-1 -- a (T*J) matrix
volume_matrix = np.zeros((72,J))   
#constructing input value: relative price matrix,(72*J)
relativep_matrix = np.zeros((72,J)) 
for i in range(len(JPdf_sellclean6)):
    #for all 72 timepoint
    dict = {}
    for each in JPdf_sellclean6.iloc[i,:].keys():
        #see whether there is any update at any price level
        if JPdf_sellclean6.iloc[i,:].get(each) != 0:
            dict[each]=JPdf_sellclean6.iloc[i,:].get(each)
    volume_list.append(dict)
    
    if dict:
        max_v = max(list(dict.keys()))
        min_v = min(list(dict.keys()))
        best_ask.append(min_v)
        spread = round(max_v-min_v,2)
        spread_list.append(spread)
        inv = round(spread/J,5)  
        inv_list.append(inv)
        for j in range(J):
            relativep_matrix[i,j]= round((j*inv),5)
            for each in dict.keys():
                if (each>= min_v+j*inv) and (each < min_v+(j+1)*inv):
                    volume_matrix[i,j] =  volume_matrix[i,j] + dict[each]                
    else:
        best_ask.append(0)
        spread_list.append(0)
        
#add timestamp as index column
dff = JPdf_sellclean6.reset_index()     
dff = dff.rename(columns = {'index':'Timestamp'})       
df_volumematrix = pd.DataFrame(volume_matrix)
df_volumematrix['Timestamp']=dff['Timestamp']
# {Y},explained variable matrix is df_volumematrix2 
df_volumematrix2 = df_volumematrix.set_index(['Timestamp'])  
df_relativepricematrix = pd.DataFrame(relativep_matrix)
df_relativepricematrix['Timestamp']=dff['Timestamp']
#input {X},explanatory variable matrix is df_relativepricematrix2
df_relativepricematrix2 = df_relativepricematrix.set_index(['Timestamp'])

#import scikits.statsmodels.api as sm
#statsmodels.regression.linear_model.OLS
import scipy
from scipy import *
from patsy import bs
#knots(K) = 20
K = 20
#degree of freedom = knots -1 = 19
#fai = patsy.bs(x,degree = 1,df = 19,include_intercept = True), this is a (Kx1)matrix
#numpy.kron -- kronecker product
#fai_matrix_t = np.zeros((K,J))
#fai_matrix_6 = np.zeros((K,J))   #t = 6
fai_list = []

print(relativep_matrix)

for i in range(72):
    a = np.transpose(bs(relativep_matrix[i,:],knots=np.linspace(0,30,16),include_intercept = True,upper_bound=30,lower_bound=0))
    #a is (20 * 50) 
    fai_list.append(a)
# fai_product = []
# for i in range(72):
#     b = np.dot(fai_list[i],np.transpose(fai_list[i]))
#     fai_product.append(b)
#calculate F10,F20,F01,F11,F02




    

    
    
   

                
                
            
    
        
        
        
        
        
        