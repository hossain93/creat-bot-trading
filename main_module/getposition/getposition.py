import pandas as pd
import numpy as np
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
data_pairs = pd.read_pickle("data_pairs2.pkl")
pairs = pd.read_pickle("pairs2.pkl")
class positions:

    strategy=['SELL_WMA20','Buy_WMA60']
    All = ['adx', 'wma', 'macd', 'rsi', 'bbands', 'obv']

    def strategy_just(self,tadata,Allpositions=All,strategy=strategy):
        lis=()
        b=0
        new=0
        pairx=[]
        for j in Allpositions:
            b = tadata.at[j,'data']
            new = lis + (b,)
            lis=new
        w=pd.concat(lis, axis=1)
        s=[]
        for i in strategy:
            for j in range (len(w)):
                if w.at[j,i]>0 or w.at[j,i]==True:
                       w.at[j,i]=1
        
        for i in strategy:
            for j in range (len(w)):
                if w.at[j,i]==1 :
                        s.append(j)
        x=list({i for i in s if s.count(i)==len (strategy)})
        pairx=pd.DataFrame(columns=strategy,index=x)
        for j in x:
            for i in strategy:
                pairx.at[j,i]=pairs.at[j,'pair']

        pd.set_option('display.max_rows', w.shape[0]+1)
        pd.set_option('display.max_columns', w.shape[0]+1)
        
        
        return w.iloc[x] , x ,pairx
    
    
    def strategy_any(self,tadata,Allpositions=All,strategy=strategy):
        
        lis=()
        b=0
        new=0
        

        for j in Allpositions:
            
            b = tadata.at[j,'data']
            new = lis + (b,)
            lis=new
            
        w=pd.concat(lis, axis=1)
        y=[]
        
        for i in strategy:
            
            for j in range (len(w)):
                if w.at[j,i]>0 or w.at[j,i]==True:
                       w.at[j,i]=1
        
        
        for i in strategy:
            for j in range (len(w)):
                if w.at[j,i]==1 :
                    y.append(j)
                    
                    
        pairy=pd.DataFrame(columns=strategy,index=y)
        for i in strategy:
            for j in range (len(w)):
                if w.at[j,i]==1 :
                    pairy.at[j,i]=pairs.at[j,'pair']
                        
        pd.set_option('display.max_rows', w.shape[0]+1)
        pd.set_option('display.max_columns', w.shape[0]+1)
        
        
        return w.iloc[y] , y , pairy
    
    
    
    
# ADX_positions  = ['trending_bullish','trending_bearish','best_positions','non_trending']
# WMA_positions  = ['Buy_WMA20','SELL_WMA20','Buy_WMA60','SELL_WMA60','Buy_WMA100','SELL_WMA100','Buy_WMA200','SELL_WMA200']
# MACD_positions=['trending_bearish_Buy_weak','trending_bullish_sell_weak','trending_bearish_sell_strong','trending_bullish_Buy_strong','Buy_cross_signal','sell_cross_signal']
# RSI_positions  = ['overbought','oversold']
# BB_positions   = ['Buy_BB','sell_BB']
# OBV_positions  = ['Buy_OBV','sell_OBV']
