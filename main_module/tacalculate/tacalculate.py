import talib as ta
import os
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import numpy as np
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
data_pairs = pd.read_pickle("data_pairs2.pkl")
pairs = pd.read_pickle("pairs2.pkl")


idex= [*range(0, len(data_pairs), 1)]
ADX_positions  =  pd.DataFrame(index=idex,columns = ['trending_bullish','trending_bearish','best_positions','non_trending'])
WMA_positions  =  pd.DataFrame(index=idex,columns = ['Buy_WMA20','SELL_WMA20','Buy_WMA60','SELL_WMA60','Buy_WMA100','SELL_WMA100','Buy_WMA200','SELL_WMA200'])
MACD_positions =  pd.DataFrame(index=idex,columns = ['trending_bearish_Buy_weak','trending_bullish_sell_weak','trending_bearish_sell_strong','trending_bullish_Buy_strong','Buy_cross_signal','sell_cross_signal'])
RSI_positions  =  pd.DataFrame(index=idex,columns = ['overbought','oversold'])
BB_positions   =  pd.DataFrame(index=idex,columns = ['Buy_BB','sell_BB'])
OBV_positions  =  pd.DataFrame(index=idex,columns = ['Buy_OBV','sell_OBV'])

class calculate_ta :


            def __init__(self,data_pairs=data_pairs,pairs=pairs):
                self.data_pairs=data_pairs
                self.pairs=pairs

            def ADX(self):
                    print('\n \n ADX ')
                    # creat dataframes for positions


                    for j in range(len(self.data_pairs)):

                            if (type(self.data_pairs.at[j,'pair'])==str) | (len(self.data_pairs.at[j,'pair'])== 0):
                                continue
                            print(j,end="-")
                            test=self.data_pairs.at[j,'pair'].copy()
                    #ADX

                            test['ADX'] = ta.ADX(test['high'], test['low'], test['close'], timeperiod=14)
                            DIplus = ta.PLUS_DI(test['high'], test['low'], test['close'], timeperiod=14)
                            DIminus=ta.MINUS_DI(test['high'], test['low'], test['close'], timeperiod=14)

                    #positions

                            trending_bullish = (test['ADX'].iloc[-1]>20) & (DIplus.iloc[-1] > DIminus.iloc[-1]) & (DIplus.iloc[-2] >= DIminus.iloc[-2])
                            trending_bearish = (test['ADX'].iloc[-1]>20) & (DIplus.iloc[-1] < DIminus.iloc[-1]) & (DIplus.iloc[-2] <= DIminus.iloc[-2])
                            best_positions = ((test['ADX'].iloc[-1]>25) & (test['ADX'].iloc[-1] < DIminus.iloc[-1]) & (test['ADX'].iloc[-1] >= DIminus.iloc[-1])) or ((test['ADX'].iloc[-1]>25) & (test['ADX'].iloc[-1] > DIminus.iloc[-1]) & (test['ADX'].iloc[-1] < DIminus.iloc[-1]))
                            non_trending = test['ADX'].iloc[-1]<20


                            positions_ADX = [trending_bullish,trending_bearish,best_positions,non_trending]

                            n=0
                            for i in positions_ADX:

                                if i==True:
                                    ADX_positions.iat[j,n]=i
                                    n+=1
                                if i==False:
                                    n+=1
                    return ADX_positions

                    #---------------------------------------------------------------------------------------------------------------------#

            def WMA(self):
                    print('\n \n WMA ')
                    for j in range(len(self.data_pairs)):

                            if (type(self.data_pairs.at[j,'pair'])==str) | (len(self.data_pairs.at[j,'pair'])== 0):
                                continue
                            print(j,end="-")
                            test=self.data_pairs.at[j,'pair']
                    #WMA

                            WMA20 = ta.WMA(test['close'], timeperiod=20)
                            WMA60 = ta.WMA(test['close'], timeperiod=60)
                            WMA100 = ta.WMA(test['close'], timeperiod=100)
                            WMA200 = ta.WMA(test['close'], timeperiod=200)


                    #positions

                    # WMA20
                            Buy_WMA20 =  (test['close'] > WMA20) & (test['close'].shift(1) <= WMA20)
                            SELL_WMA20 = (test['close'] < WMA20) & (test['close'].shift(1) >= WMA20)

                    # WMA60
                            Buy_WMA60 =  (test['close'] > WMA60) & (test['close'].shift(1) <= WMA60)
                            SELL_WMA60 = (test['close'] < WMA60) & (test['close'].shift(1) >= WMA60)

                    # WMA100
                            Buy_WMA100 =  (test['close'] > WMA100) & (test['close'].shift(1) <= WMA100)
                            SELL_WMA100 = (test['close'] < WMA100) & (test['close'].shift(1) >= WMA100)

                    # WMA200
                            Buy_WMA200 =  (test['close'] > WMA200) & (test['close'].shift(1) <= WMA200)
                            SELL_WMA200 = (test['close'] < WMA200) & (test['close'].shift(1) >= WMA200)

                    #reset index for idmax
                            list_dataframes = [Buy_WMA20,SELL_WMA20, Buy_WMA60,SELL_WMA60, Buy_WMA100,SELL_WMA100, Buy_WMA200,SELL_WMA200]

                            for i in list_dataframes:
                                i.reset_index(drop=True,inplace=True)


                            positions_WMA = [Buy_WMA20,SELL_WMA20, Buy_WMA60,SELL_WMA60, Buy_WMA100,SELL_WMA100, Buy_WMA200,SELL_WMA200]

                            n=0
                            for i in positions_WMA:
                                g=np.where(i == True)   #find true value that place in a tuple

                                if pd.DataFrame(g).empty==False:
                                    h=np.max(g)-((len(test)-1))>=0
                                    if h==False:
                                        n+=1
                                    if h==True: # if latest three item wase true we can chose it

                                        WMA_positions.iat[j,n]=np.max(g)
                                        n+=1

                                if pd.DataFrame(g).empty==True:
                                    n+=1
                    return WMA_positions

                    #---------------------------------------------------------------------------------------------------------------------#
                    #MACD   

            def MACD(self):
                    print('\n \n MACD ')
                    for j in range(len(self.data_pairs)):

                            if (type(self.data_pairs.at[j,'pair'])==str) | (len(self.data_pairs.at[j,'pair'])== 0):
                                continue
                            print(j,end="-")
                            test=self.data_pairs.at[j,'pair']

                            EMA12 = ta.EMA(test['close'], timeperiod=12)
                            EMA26 = ta.EMA(test['close'], timeperiod=26)
                            macd, signal, histogram = ta.MACD(test['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)

                            macd = pd.DataFrame(macd)
                            signal = pd.DataFrame(signal)
                            histogram = pd.DataFrame(histogram)

                    #positions

                    #weak signal buy and sell
                            trending_bearish_Buy_weak =  (macd > signal) & (macd.shift(1) <= signal)&(macd <= 0)
                            trending_bullish_sell_weak = (macd < signal) & (macd.shift(1) >= signal)&(macd >= 0)

                    #strong signal buy and sell
                            trending_bearish_sell_strong =  (macd < signal) & (macd.shift(1) >= signal)&(macd <= 0)
                            trending_bullish_Buy_strong = (macd > signal) & (macd.shift(1) <= signal)&(macd >= 0)


                    #cross with zero line
                            Buy_cross_signal = (signal > 0) & (signal.shift(1) <= 0) #| (signal<=signal.shift()*0.05)
                            sell_cross_signal = (signal < 0) & (signal.shift(1) >= 0)


                    #reset index for idmax
                            list_dataframes = [trending_bearish_Buy_weak,trending_bullish_sell_weak,trending_bearish_sell_strong,trending_bullish_Buy_strong,Buy_cross_signal,sell_cross_signal]

                            for i in list_dataframes:
                                i.reset_index(drop=True,inplace=True)


                            positions_MACD = [trending_bearish_Buy_weak,trending_bullish_sell_weak,trending_bearish_sell_strong,trending_bullish_Buy_strong,Buy_cross_signal,sell_cross_signal]

                            n=0
                            for i in positions_MACD:
                                g=np.where(i == True)

                                if pd.DataFrame(g).empty==False:
                                    h=np.max(g)-((len(test)-1))>=0
                                    if h==False:
                                        n+=1
                                    if h==True:
                                        MACD_positions.iloc[j,n]=np.max(g)
                                        n+=1

                                if pd.DataFrame(g).empty==True:
                                    n+=1

                    return  MACD_positions

                    #---------------------------------------------------------------------------------------------------------------------#

            def RSI(self):
                    print('\n \n RSI ')
                    for j in range(len(self.data_pairs)):

                            if (type(self.data_pairs.at[j,'pair'])==str) | (len(self.data_pairs.at[j,'pair'])== 0):
                                continue
                            print(j,end="-")
                            test=self.data_pairs.at[j,'pair']
                    #RSI

                            RSI = ta.RSI(test['close'], timeperiod=14)

                    #positions

                            overbought = (RSI < 70) & (RSI.shift(1) >= 70) | (RSI>=70*0.95)
                            oversold =   (RSI > 30) & (RSI.shift(1) <= 30) | (RSI<=30*1.05)

                    #reset index for idmax
                            list_dataframes = [overbought,oversold]

                            for i in list_dataframes:
                                i.reset_index(drop=True,inplace=True)


                            positions_RSI = [overbought,oversold]

                            n=0
                            for i in positions_RSI:
                                g=np.where(i == True)

                                if pd.DataFrame(g).empty==False:
                                    h=np.max(g)-((len(test)-1))>=0
                                    if h==False:
                                        n+=1
                                    if h==True:
                                        RSI_positions.iloc[j,n]=np.max(g)
                                        n+=1
                                if pd.DataFrame(g).empty==True:
                                    n+=1

                    return  RSI_positions
    
                    #----------------------------------------------------------------------------------------------------------------#

            def BBANDS(self):
                    print('\n \n BBANDS ')
                    for j in range(len(self.data_pairs)):

                            if (type(self.data_pairs.at[j,'pair'])==str) | (len(self.data_pairs.at[j,'pair'])== 0):
                                continue
                            print(j,end="-")
                            test=self.data_pairs.at[j,'pair']
                    #Bollinger Bands


                            upper, mid, lower = ta.BBANDS(test['close'], nbdevup=2, nbdevdn=2, timeperiod=20)

                            upper = pd.Series(upper)
                            mid = pd.Series(mid)
                            lower = pd.Series(lower)

                            Percent_B = ((test['close']-lower)/(upper-lower))*100

                    #positions

                            Buy_BB =  Percent_B <= 0
                            sell_BB = Percent_B >= 100

                    #reset index for idmax
                            list_dataframes = [Buy_BB,sell_BB]

                            for i in list_dataframes:
                                i.reset_index(drop=True,inplace=True)


                            positions_BB = [Buy_BB,sell_BB]

                            n=0
                            for i in positions_BB:
                                g=np.where(i == True)

                                if pd.DataFrame(g).empty==False:
                                    h=np.max(g)-((len(test)-1))>=0
                                    if h==False:
                                        n+=1
                                    if h==True:
                                        BB_positions.iloc[j,n]=np.max(g)
                                        n+=1 
                                if pd.DataFrame(g).empty==True:
                                    n+=1
                    return  BB_positions

                    #----------------------------------------------------------------------------------------------------------------#            

            def OBV(self):
                    print('\n \n OBV ')
                    for j in range(len(self.data_pairs)):

                            if (type(self.data_pairs.at[j,'pair'])==str) | (len(self.data_pairs.at[j,'pair'])== 0):
                                continue
                            print(j,end="-")
                            test=self.data_pairs.at[j,'pair']
                    # On Balance Volume           
                            OBV = ta.OBV(test['close'], test['volume'])    
                            EMA60 = ta.EMA(OBV, timeperiod=60)    
                            Buy_OBV  = (OBV > EMA60) & (OBV.shift(1) <= EMA60)
                            sell_OBV = (OBV < EMA60) & (OBV.shift(1) >= EMA60)

                    #reset index for idmax
                            list_dataframes = [Buy_OBV,sell_OBV]

                            for i in list_dataframes:
                                i.reset_index(drop=True,inplace=True)


                            positions_OBV = [Buy_OBV,sell_OBV]

                            n=0
                            for i in positions_OBV:
                                g=np.where(i == True)

                                if pd.DataFrame(g).empty==False:
                                    h=np.max(g)-((len(test)-1))>=0
                                    if h==False:
                                        n+=1
                                    if h==True:
                                        OBV_positions.iloc[j,n]=np.max(g)
                                        n+=1 
                                if pd.DataFrame(g).empty==True:
                                    n+=1
                    return OBV_positions


class tacal(calculate_ta):
        item = {'adx':'ADX', 'wma':'WMA', 'macd':'MACD', 'rsi':'RSI', 'bbands':'BBANDS', 'obv':'OBV'}
        All = ['adx', 'wma', 'macd', 'rsi', 'bbands', 'obv']
        def get_ta(self, namepositions=All):
            index=[]
            for i in namepositions:
                index .append(f'{i}')
            tadata = pd.DataFrame(columns = ['data'],index=index)    
            for i in namepositions:
                tadata.at[i,'data'] =eval(f'self.{self.item[i]}()') # eval >>>> 'ADX'  ---> ADX  =  'ADX'  ---> ADX()
            return tadata

       # def item_list(self, namepositions=All):
          # item=["ADX", "WMA", "MACD", "RSI", "BBANDS", "OBV"]
            #index=[]
            #for i in namepositions:
               # index .append(f'{i}')
            #pos = pd.DataFrame(columns = ['data'],index=index)    
            #for i in namepositions:
              #  pos.at[i,'data'] =eval(f'self.{self.item[i]}()') # eval >>>> 'ADX'  ---> ADX  =  'ADX'  ---> ADX()
           # return pos

                

#p=tacal()
#d=['adx']
#h=p.positions()
#h
