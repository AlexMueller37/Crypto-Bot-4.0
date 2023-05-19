def macd(closes):
    import numpy as np 
    import talib

    closes = np.array(closes)
    macd, macdsignal, macdhist = talib.MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
    last_macd = macd[-1]
    last_signal = macdsignal[-1]
    last_histogram = macdhist[-1] 
    second_last_macd = macd[-2]
    second_last_signal = macdsignal[-2] 
    third_last_macd = macd[-3]
    third_last_signal = macdsignal[-3]
    
    return last_macd, last_signal, last_histogram, second_last_macd, second_last_signal, third_last_macd, third_last_signal 

def check_macd(last_macd, last_signal, second_last_macd, second_last_signal):
    if last_macd > last_signal and second_last_macd < second_last_signal:
        return True 
    else: 
        return False 