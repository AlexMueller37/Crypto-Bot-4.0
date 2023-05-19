def ema(closes):
    import numpy as np 
    import talib

    closes = np.array(closes)

    ema = talib.EMA(closes, timeperiod=100)
    
    last_ema = ema[-1]
    second_last_ema = ema[-2]
    third_last_ema = ema[-2]
    
    return last_ema, second_last_ema, third_last_ema

def check_ema(last_ema, second_last_ema, third_last_ema, last_close, second_last_close, third_last_close):
    if third_last_close > third_last_ema and second_last_close > second_last_ema and last_close > last_ema:
        return True
    else:
        return False