import matplotlib.pyplot as plt 
import numpy as np 
import talib 
import requests 
from time import sleep

from make_order import order 
from macd import macd, check_macd
from ema import ema, check_ema

API_KEY = '#####################'
SECRET_KEY = '###################################'

TRADE_SYMBOL = 'BTCUSD'
BUY_QUANTITY = 1 
SELL_QUANTITY = 0.997499998

url = f'https://api.binance.us/api/v3/ticker?symbol={TRADE_SYMBOL}'

closes = []
in_position = False 

counter = 0 
completed_trades = 0
buyprice = 0
sellprice = 0 
winners = 0
losers = 0 
profit = 0 

take_profit = 0 
minimum = 0

while True: 
    counter += 1
    
    response = requests.get(url)
    response = response.json()

    close = response['lastPrice']
    closes.append(float(close))
    
    closes_np = np.array(closes)

    print(f'candle closed at {close}')
    
    if counter > 3:
        last_macd = macd(closes_np)[0]
        last_signal = macd(closes_np)[1]
        last_histogram = macd(closes_np)[2]
        second_last_macd = macd(closes_np)[3]
        second_last_signal = macd(closes_np)[4]
        third_last_macd = macd(closes_np)[5]
        third_last_signal = macd(closes_np)[6]
        last_ema = ema(closes_np)[0]
        second_last_ema = ema(closes_np)[1]
        third_last_ema = ema(closes_np)[2]

        last_close = closes_np[-1]
        second_last_close = closes_np[-2]
        third_last_close = closes_np[-3]         

    if counter > 30:
        macd_output = check_macd(last_macd, last_signal, second_last_macd, second_last_signal)
        ema_output = check_ema(last_ema, second_last_ema, third_last_ema, last_close, second_last_close, third_last_close)
        
    if counter > 100:
        if macd_output and ema_output and not(in_position): 
            order(TRADE_SYMBOL, BUY_QUANTITY, 'buy', 'market', 'gtc', API_KEY, SECRET_KEY)
            in_position = True 
            buyprice = last_close

            pasts = closes[-50:]
            lowests = min(pasts)
            diff = buyprice - lowests 
            take_profit = buyprice + (diff * 1.5)

        elif (last_close >= take_profit and in_position) or (last_close <= minimum and in_position):
            order(TRADE_SYMBOL, SELL_QUANTITY, 'sell', 'market', 'gtc', API_KEY, SECRET_KEY)
            completed_trades += 1
            sellprice = last_close
            in_position = False

            if sellprice * SELL_QUANTITY > buyprice * BUY_QUANTITY:
                winners += 1 
            elif sellprice * SELL_QUANTITY < buyprice * BUY_QUANTITY:
                losers += 1
            profit += (sellprice * SELL_QUANTITY) - (buyprice * BUY_QUANTITY)

            buyprice = 0
            sellprice = 0 

    print(f'Currently Holding : {in_position}')
    print(f'# : {counter}')
    print('===========================================================================================')
    print('TRADE PROFITABILITY TABLE:')
    print(f'Number of Trades Taken: {completed_trades}')
    print(f'Winners : Losers Ratio = | {winners}:{losers} |')
    print(f'Total Profit = ${profit}')
    print('===========================================================================================')
   
    sleep(15)
