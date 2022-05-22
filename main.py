from binance_service import DataColumns, getData
import numpy as np
import talib
from triangles import Triangles

if __name__ == '__main__':
    df = getData()
    np_opens = np.array(df[DataColumns.OPEN.value])
    np_highs = np.array(df[DataColumns.HIGH.value])
    np_lows = np.array(df[DataColumns.LOW.value])
    np_closes = np.array(df[DataColumns.CLOSE.value])
    np_volume = np.array(df[DataColumns.VOLUME.value])
    np_open_time = np.array(df[DataColumns.OPEN_TIME.value])
    ema_5 = talib.EMA(np_closes, timeperiod=5)
    ema_21 = talib.EMA(np_closes, timeperiod=21)
    ema_55 = talib.EMA(np_closes, timeperiod=55)
    triangles = Triangles(np_opens[55:], np_highs[55:], np_lows[55:], np_closes[55:], np_volume[55:], np_open_time[55:], ema_5[55:], ema_21[55:], ema_55[55:])