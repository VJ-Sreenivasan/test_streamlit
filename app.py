# app.py
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

dfp = yf.Ticker("DEEPAKFERT.NS")
dfc = yf.Ticker("CTSH")
# get stock info
#msft.info

# get historical market data
hist_dfp = dfp.history(period='120mo', interval='1d', auto_adjust = False)
hist_dfc = dfc.history(period='120mo', interval='1d', auto_adjust = False)
dfc.quarterly_financials.T

st.title('Hello Group 8!')

st.write('Welcome to final project!')

st.write(dfc)
st.write(hist_dfc)

df_c = hist_dfc[['Adj Close']]
df_c.plot(xlabel = 'Time', ylabel='Adj Close', marker='o', legend = False, figsize = (20, 5))
plt.show()
