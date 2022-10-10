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

st.set_page_config(page_title="Virtual Market Analyst", page_icon="📈", layout="centered")
st.header('Virtual Market Analyst')
df = pd.read_csv('c_ticker_list.csv')

company = st.selectbox( 'Company', (df['Company_Ticker_list']))
st.write(company)
ticker=re.search('\(([^)]+)', company).group(1)
st.write(str(ticker))
  
# df_c.plot(xlabel = 'Time', ylabel='Adj Close', marker='o', legend = False, figsize = (20, 5))
# plt.show()
#dfp = yf.Ticker("DEEPAKFERT.NS")
dfc = yf.Ticker(str(ticker))
# get stock info
#msft.info

# get historical market data
#hist_dfp = dfp.history(period='120mo', interval='1d', auto_adjust = False)
# hist_dfc = dfc.history(period=str(months2)+'mo', interval='3mo', auto_adjust = False)
hist_dfc = dfc.history(period=str(months2)+'mo', interval='1d', auto_adjust = False)
