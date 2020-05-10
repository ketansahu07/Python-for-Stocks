import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

# Get the data from internet and store it in csv file
'''start = dt.datetime(2000, 1, 1)
end = dt.datetime(2019, 12, 31)
df = web.DataReader('TSLA', 'yahoo', start, end)
# print(df.head(6))
df.to_csv('tsla.csv')'''

# Reading the csv file
df = pd.read_csv('tsla.csv', parse_dates = True, index_col = 0)

# Adding 100 moving average column to the csv file
# df['100ma'] = df['Adj Close'].rolling(window = 100, min_periods = 0).mean()

# Resampling the dataframe for candle sitck graph
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

# Resetting the index to column
df_ohlc.reset_index(inplace=True)

# Converting the dates to mdate format
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

# Making subplots in the graph
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
'''ax1.plot(df.index, df['Adj Close'], linewidth=2, markersize=12)
ax1.plot(df.index, df['100ma'], linewidth=2, markersize=12)
ax2.bar(df.index, df['Volume'])'''
ax1.xaxis_date()
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

