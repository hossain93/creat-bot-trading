#!/usr/bin/env python
# coding: utf-8


from datetime import timedelta, date, datetime
import time
import pandas as pd
import numpy as np
from pandas import ExcelWriter
import ccxt
#import logging
#logging.basicConfig(level=logging.DEBUG)
pairs = pd.read_pickle("pairs2.pkl")


#--------------------------------------------
timeframe='1d'  
limit=400

data_pairs=pairs.copy()
save_pairs=pairs.copy()
counter=0
msec = 1000
hold = 30

timeframes = (['1m',1,'minutes',limit*1,60*msec],['3m',3,'minutes',limit*3,60*msec],['5m',5,'minutes',limit*5,60*msec],['15m',15,'minutes',limit*15,60*msec],['30m',30,'minutes',limit*30,60*msec],['1h',1,'hours',limit*1,60*60*msec],['2h',2,'hours',limit*2,60*60*msec],['4h',4,'hours',limit*4,60*60*msec],['6h',6,'hours',limit*6,60*60*msec],['8h',8,'hours',limit*8,60*60*msec],['12h',12,'hours',limit*12,60*60*msec],['1d',1,'days',limit*1,60*60*24*msec],['3d',3,'days',limit*3,60*60*24*msec],['1w',1,'weeks',limit*7,60*60*24*7*msec])
timeframes = pd.DataFrame(timeframes,columns=['timeframe' , 'time' , 'name_time' , 'limit' , 'period'])
timeframes.set_index('timeframe', inplace=True)

timeframes['limit']  = timeframes['limit'].astype(np.float64)
timeframes['period'] = timeframes['period'].astype(np.float64)


exchange = ccxt.binance({'enableRateLimit': True})
#exchange.verbose = True
def run(i,timeframe=timeframe):
    now = exchange.milliseconds()
    if timeframes.loc[timeframe, 'name_time'] == 'minutes':
        from_datetime=pd.to_datetime(now, unit='ms') - timedelta(minutes=timeframes.loc[timeframe, 'limit'])

    if timeframes.loc[timeframe, 'name_time'] == 'hours':
        from_datetime=pd.to_datetime(now, unit='ms') - timedelta(hours=timeframes.loc[timeframe, 'limit'])

    if timeframes.loc[timeframe, 'name_time'] == 'days':
        from_datetime=pd.to_datetime(now, unit='ms') - timedelta(days=timeframes.loc[timeframe, 'limit'])



    from_datetime=datetime.strftime(from_datetime, '%Y-%m-%d %H:%M:%S%z')
    from_timestamp = exchange.parse8601(from_datetime)
    data = []

    while from_timestamp < now:
        #writer = ExcelWriter('1min.xlsx')
        try:
            ohlcvs = exchange.fetch_ohlcv(save_pairs.at[i,'pair'], timeframe, from_timestamp)
            #print(candles, from_timestamp)     
            print( 'Fetched', len(ohlcvs), 'candles')
            if len(ohlcvs) > 0:
                first = ohlcvs[0][0]
                last = ohlcvs[-1][0]

                from_timestamp = ohlcvs[-1][0] + timeframes.loc[timeframe, 'period'] * timeframes.loc[timeframe, 'time']
                data += ohlcvs

            df = pd.DataFrame(data, columns=['Timestamp','open','high','low','close', 'volume'])
            df['Timestamp'] = pd.DataFrame(df['Timestamp'].apply(exchange.iso8601))
            #save_excel = df.to_excel(writer, sheet_name='2017_CURRENT')
            #writer.save()

            print('first time:',pd.to_datetime(first, unit='ms'),'\nlast time:',pd.to_datetime(first, unit='ms'))
        except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout, ccxt.BadSymbol) as error:
            counter += 1
            EROREF[counter-1]=save_pairs.at[i,'pair']

            print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
            time.sleep(hold)
    return df


