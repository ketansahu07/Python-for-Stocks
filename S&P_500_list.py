import bs4 as bs
import datetime as dt
import os
import pandas as pd
# import pandas_datareader.data as web
from pandas_datareader import data as pdr
import pickle 
import requests
import fix_yahoo_finance as yf

yf.pdr_override

# Fucntion to get top 500 tickers from wikipedia
def save_sp500_tickers():
    
    # getting the whole HTML page from the link
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    
    # creating an object and parsing the resp file that contain the HTML page
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    
    # finding the table and with class as mentioned
    table = soup.find('table', {'class':'wikitable sortable'})
    
    # storing all the tickers from 0th column from 1 row and onwards in an empty list
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        
    # dumping the list in a sp500tickers using pickle
    # so that it can be converted to objects again if needed
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
        
    # print(tickers)
        
    return tickers

# save_sp500_tickers()
    
def get_data_from_yahoo(reload_sp500=False):
    
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
            
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
        
    start = dt.datetime(2017, 1, 1)
    end = dt.datetime(2019, 12, 31)

    for ticker in tickers[:25]:
        print(ticker)
        if not os.path.exists(f"stock_dfs/{ticker}.csv"):
            # df = web.DataReader(ticker, 'yahoo', start, end)
            df = pdr.get_data_yahoo(ticker, start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df.to_csv(f"stock_dfs/{ticker}.csv")
        else:
            print('Already have {ticker}')
    
get_data_from_yahoo()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    