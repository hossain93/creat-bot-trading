#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import ccxt
def symbols():
      binance = ccxt.binance()

      pairs=pd.DataFrame(binance.load_markets())

      pairs=pairs.T


      pairs.drop(pairs.loc[pairs['margin']!=True].index, inplace=True)

      pairs.drop(pairs.loc[pairs['quote']!='USDT'].index, inplace=True)

      pairs=pairs['symbol']

      pairs=pd.DataFrame(pairs)

      pairs.reset_index(drop=True, inplace=True)

      pd.set_option('display.max_row', pairs.shape[0]+1)

      return pairs
