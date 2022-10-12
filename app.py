# app.py
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from seaborn.relational import lineplot
import plotly.express as px
from PIL import Image
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rc
import utils as ut
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re
import fundamentalanalysis as fa
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import *


fa_api_key = "9528170166318a21f58bf0270843c4f6"
duration='1M'

st.set_page_config(page_title="Virtual Market Analyst", page_icon="📈", layout="centered")
st.header('Virtual Market Analyst')
df = pd.read_csv('c_ticker_list.csv')

company = st.selectbox( 'Company', (df['Company_Ticker_list']))
# st.write(company)
ticker=re.search('\(([^)]+)', company).group(1)
# st.write(str(ticker))
  
# df_c.plot(xlabel = 'Time', ylabel='Adj Close', marker='o', legend = False, figsize = (20, 5))
# plt.show()
#dfp = yf.Ticker("DEEPAKFERT.NS")
ticker_data = yf.Ticker(str(ticker))
# get stock info
#msft.info

# get historical market data
# hist_dfp = dfp.history(period='120mo', interval='1d', auto_adjust = False)
# hist_dfc = dfc.history(period=str(months2)+'mo', interval='3mo', auto_adjust = False)
# st.write(ticker_df.columns)
# hist_dfc.reset_index(inplace = True)

def show_stock_trend(duration='1M'):
  curr_date=datetime.today()
#   st.write('g8_1:',duration, curr_date)
  if duration== '1M':
    st_dt=curr_date.date() - relativedelta(months=1)
    print( st_dt)
  if duration== '6M':
    st_dt = curr_date.date() - relativedelta(months=6)
    print( st_dt)
  if duration== '1Y':
    st_dt = curr_date.date() - relativedelta(months=12)
    print( st_dt)
  if duration== '5Y':
    st_dt = curr_date.date() - relativedelta(months=60)
    print( st_dt)
  else:
    st_dt = '2022-01-01'
  ticker_df = ticker_data.history(period='1d', start=st_dt, end=curr_date.strftime('%Y-%m-%d'))
  st.line_chart(ticker_df.Close)

      
  
# ticker_df = ticker_data.history(period='id', start='2010-1-1', end='2022-9-30')
# st.line_chart(ticker_df.Close)
duration = st.selectbox( 'Company', ('1M', '6M', '1Y', '5Y'), on_change=show_stock_trend)


income_statement_quarterly = fa.income_statement(str(ticker), fa_api_key, period="quarter")
income_statement_quarterly = income_statement_quarterly.T.drop(income_statement_quarterly.T.index[-1])
# income_statement_quarterly = income_statement_quarterly.reindex(index = income_statement_quarterly.index[::-1])
income_statement_quarterly=income_statement_quarterly.query('index>= "2010-01"')
# income_statement_quarterly

st.line_chart(income_statement_quarterly.revenue)

# st.write(income_statement_quarterly.columns)
# st.write(income_statement_quarterly.index.tolist())

finwiz_url = 'https://finviz.com/quote.ashx?t='
news_tables = {}

url = finwiz_url + ticker
req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}) 
response = urlopen(req)    
# Read the contents of the file into 'html'
html = BeautifulSoup(response)
# Find 'news-table' in the Soup and load it into 'news_table'
news_table = html.find(id='news-table')
# Add the table to our dictionary
news_tables[ticker] = news_table
parsed_news = []
# Iterate through the news
for file_name, news_table in news_tables.items():
    # Iterate through all tr tags in 'news_table'
    for x in news_table.findAll('tr'):
        # read the text from each tr tag into text
        # get text from a only
        if x.a is None:
          continue
          
        text = x.a.get_text() 
        # splite text in the td tag into a list 
        date_scrape = x.td.text.split()
        
        # if the length of 'date_scrape' is 1, load 'time' as the only element
        if len(date_scrape) == 1:
            time = date_scrape[0]
            
        # else load 'date' as the 1st element and 'time' as the second
        else:
            date = date_scrape[0]
            time = date_scrape[1]
        # Extract the ticker from the file name, get the string up to the 1st '_'  
        ticker = file_name.split('_')[0]
        
        # Append ticker, date, time and headline as a list to the 'parsed_news' list
        parsed_news.append([ticker, date, time, text])
        
# st.write(parsed_news[:5]) # print first 5 rows of news
