#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import ccxt
def symbols():
        binance = ccxt.binance({'options': { 'defaultType': 'future' , 'contractType': 'PERPETUAL' , 'quote': 'USDT' }})
        pairs=pd.DataFrame(binance.fetchMarkets ())
        pairs
        pairs.drop(pairs.loc[pairs['quote']!='USDT'].index, inplace=True)
        pairs
        pairs=pairs['symbol']
        pairs=pd.DataFrame(pairs)
        pairs = pairs.rename(columns={'symbol': 'pair'})
        pairs.reset_index(drop=True, inplace=True)
        return pairs

