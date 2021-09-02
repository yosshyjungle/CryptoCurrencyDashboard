#conda install -c plotly plotly=4.8.2
#pip install mplfinance

import streamlit as st
import pandas as pd
import datetime as datetime
import pandas_datareader
import plotly.graph_objects as go
from PIL import Image

st.write("""
# Crypto Currency Dashboard Application
Visually show data on crypto (BTC-JPY, DOGE-JPY, & ETH-JPY) 
""")

image = Image.open('crypto_image3.PNG')
st.image(image, use_column_width=True)

st.sidebar.header("User Input")

def get_input():
    start_date = st.sidebar.text_input("Strat Date", "2021-01-01")
    end_date = st.sidebar.text_input("End Date", "2021-09-01")
    crypto_symbol = st.sidebar.text_input("Crypto Symbol", "BTC")
    return start_date, end_date, crypto_symbol

def get_crypto_name(symbol):
    symbol = symbol.upper()
    if symbol == "BTC":
        return "Bitcoin"
    elif symbol == "ETH":
        return "Etherium"
    elif symbol == "DOGE":
        return "Dogecoin"
    else:
        return "None"

def get_data(symbol, start, end):
    symbol = symbol.upper()
    if symbol == "BTC":
        df = pd.read_csv("BTC.csv")
        # df = pandas_datareader.data.DataReader('BTC', 'yahoo')

    elif symbol == "ETH":
        df = pd.read_csv("ETH.csv")
        # df = pandas_datareader.data.DataReader('ETH', 'yahoo')
    elif symbol == "DOGE":
        df = pd.read_csv("DOGE.csv")
        # df = pandas_datareader.data.DataReader('DOGE', 'yahoo')
    else:
        df = pd.DataFrame(columns=['Date', 'Close', 'Open', 'Volume', 'Adj Close'])

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index("Date")

    return df.loc[start:end]

start, end, symbol = get_input()
df = get_data(symbol, start, end)
crypto_name = get_crypto_name(symbol)

# Candle Stick用の設定
fig = go.Figure(
    data = [go.Candlestick(
        x = df.index,
        open = df['Open'],
        high = df['High'],
        low = df['Low'],
        close = df['Close'],
        increasing_line_color = 'green',
        decreasing_line_color = 'red',
        )
    ]
)

st.header(crypto_name + " Data")

st.write(df)

st.header(crypto_name + " Data Statistics")
st.write(df.describe())

st.header(crypto_name + " Close Price")
st.line_chart(df['Close'])

st.header(crypto_name + " Volume")
st.bar_chart(df['Volume'])

st.header(crypto_name + " Candle Stick")
st.plotly_chart(fig)




