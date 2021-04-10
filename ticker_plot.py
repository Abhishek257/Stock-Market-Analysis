import tkinter as tk
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
import plotly.graph_objects as plots
import plotly.express as px
from datetime import datetime
from scipy.stats import linregress
import matplotlib.dates as mpdates
import datetime as dt
import warnings


'''https://pandas.pydata.org/pandas-docs/version/0.10.0/visualization.html
https://matplotlib.org/2.1.1/api/_as_gen/matplotlib.pyplot.plot.html'''

def get_choice(data,symbol):
    warnings.filterwarnings("ignore")
    print('-'*60)
    choice = input("Please Enter your choice : ")
    print('-'*60)
    file_name = symbol +'.csv'
    if choice == "1":
        raw_data_plot(data)
    elif choice == "2":
        Moving_Average(data)
    elif choice == "3":
        Daily_return(data)
    elif choice == "4":
        Risk(data,symbol)
    elif choice == "5":
        OHLC_plotlyy(data,file_name)
    elif choice == "6":
        MACD(data)
    elif choice == "7":
        signal_buy_sell(data)
    elif choice == "8":
        weighted_moving_average(data)
    elif choice == "9":
        linear_tread_line(data)
    elif choice == "10":
        return False
    else:
        print("Wrong choice, please try again.")
    return True
        
def get_ticker_data(data,symbol):
    #Data Plot Menu
    flag = True
    while (flag):
        print('-'*60)
        print("Choose from the list of below plotting options:\
    \n\t1. Raw Data Plot\n\t2. Moving Averages\n\t3. Daily Return\n\t4. Variation in Daily Return\
    \n\t5. OHLC\n\t6. MACD\n\t7. Buy Sell Signals\n\t8. Weighted Moving Average\n\t9. Linear Trend Line\n\t10. To back to previous menu")
        print('-'*60)
        flag = get_choice(data,symbol)


def linear_tread_line(data):
    x = [dt.datetime.strptime(date, '%Y-%m-%d').date() for date in data['Date']]
    x = mpdates.date2num(x)
    y = data['Close']
    plt.plot(x,y,label='Close')
    p = np.poly1d(np.polyfit(x, y, 1))
    trend = np.linspace(x.min(),x.max(),100)
    date_trend = mpdates.num2date(trend)
    plt.plot(date_trend,p(trend),"r--")
    plt.xticks(rotation=45)
    plt.show()

def raw_data_plot(data):
    fig, axes = plt.subplots(nrows=3, ncols=2)
    fig.set_figheight(8)
    fig.set_figwidth(15)
    # plot the data itself

    data.plot(x='Date', y='Open',ax=axes[0,0])
    axes[0,0].set_title('Open Price')

    data.plot(x='Date', y='High',ax=axes[0,1])
    axes[0,1].set_title('High Price')

    data.plot(x='Date', y='Low',ax=axes[1,0])
    axes[1,0].set_title('Low Price')

    data.plot(x='Date', y='Volume',ax=axes[1,1])
    axes[1,1].set_title('Volume')

    data.plot(x='Date', y='Close',ax=axes[2,0])
    axes[2,0].set_title('Close')

    data.plot(x='Date', y='Adj Close',ax=axes[2,1])
    axes[2,1].set_title('Adj Close')

    fig.tight_layout()
    plt.show()

def Moving_Average(data):
    num_days = input("Moving Average for how many days : ")
    column_list = ['Open','High','Low','Volume','Close','Adj Close']
    for item in column_list:
        strr = f"{item}"
        column_name = f"{item} MA for {num_days} days"
        data[column_name] = data[strr].rolling(int(num_days)).mean()
    fig, axes = plt.subplots(nrows=3, ncols=2)
    fig.set_figheight(25)
    fig.set_figwidth(30)
    data.plot(x='Date',y=['Open',f"Open MA for {num_days} days"],ax=axes[0,0])    

    data.plot(x='Date',y=['Close',f"Close MA for {num_days} days"],ax=axes[0,1])

    data.plot(x='Date',y=['Low',f"Low MA for {num_days} days"],ax=axes[1,0])

    data.plot(x='Date',y=['High',f"High MA for {num_days} days"],ax=axes[1,1])

    data.plot(x='Date',y=['Adj Close',f"Adj Close MA for {num_days} days"],ax=axes[2,0])

    data.plot(x='Date',y=['Volume',f"Volume MA for {num_days} days"],ax=axes[2,1])
    plt.show()


#https://quant.stackexchange.com/questions/57729/calculating-a-linear-weighted-moving-average-in-python
def weighted_moving_average(data):
    column='Close'
    n=20
    add_col = False
    moving_weights = np.arange(1, n + 1)
    wt_mv_avg_list = data[column].rolling(n).apply(lambda x: np.dot(x, moving_weights) /moving_weights.sum(), raw=True).to_list()
    data[f'{column}_WMA_{n}'] = wt_mv_avg_list
    plt.plot(data['Date'],data[['Close',f"{column}_WMA_{n}"]])
    plt.xticks(np.arange(0,len(data), 120), data['Date'][0:len(data):120])
    plt.xticks(rotation=45)
    plt.title("Weighted Moving Average")
    plt.show()

def Daily_return(data):
    color = {'boxes': 'DarkGreen', 'whiskers': 'DarkOrange','medians': 'DarkBlue', 'caps': 'Gray'}
    data['Daily Close Return'] = data['Close'].pct_change()
    data.plot.box(x='Date',y=['Daily Close Return'],color=color, sym='r+')
    plt.show()

#http://srutisj.in/2017-09-03-Stock-Market-Analysis/
def Risk(data, symbol):
    msft = yf.Ticker(symbol)
    closing_df = msft.dividends
    returns = closing_df.pct_change().dropna()
    area_plot = np.pi*20
    plt.figure(figsize=(12, 10))
    plt.scatter(returns.mean(), returns.std(), s=area_plot)
    plt.xlabel('Expected return')
    plt.ylabel('Risk')
    plt.title('Stock Risk')
    x = returns.mean()
    y = returns.std()
    label= symbol
    plt.annotate(label, xy=(x, y), xytext=(50, 50), textcoords='offset points', ha='right', va='bottom', 
                 arrowprops=dict(arrowstyle='-', color='blue', connectionstyle='arc3,rad=-0.3')) 
    plt.show()

#OHLC - Open High Low CLose
def OHLC_plotlyy(data,file_name):
    df = pd.read_csv(file_name)
    fig = plots.Figure(data=[plots.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
    fig.update_layout(xaxis_rangeslider_visible=False,title="Open_High_Low_Close")
    fig.show()

#https://randerson112358.medium.com/determine-when-to-buy-sell-stock-edeeac03f9fb
def MACD(data):
    data.plot(x='Date',y= ['MACD','Signal'])
    plt.xticks(rotation=45)
    plt.show()

def signal_buy_sell(data): 
    sig_PriceBuy = []
    sig_PriceSell = []
    flag = -1
    for i in range(0,len(data)):
        if data['MACD'][i] > data['Signal'][i]:
            if flag != 1:
                sig_PriceBuy.append(data['Close'][i])
                sig_PriceSell.append(np.nan)
                flag = 1
            else:
                sig_PriceBuy.append(np.nan)
                sig_PriceSell.append(np.nan)
        elif data['MACD'][i] < data['Signal'][i]: 
            if flag != 0:
                sig_PriceSell.append(data['Close'][i])
                sig_PriceBuy.append(np.nan)
                flag = 0
            else:
                sig_PriceBuy.append(np.nan)
                sig_PriceSell.append(np.nan)
        else: 
            sig_PriceBuy.append(np.nan)
            sig_PriceSell.append(np.nan)  
    data['Buy_Signal_Value'] = sig_PriceBuy
    data['Sell_Signal_Value'] = sig_PriceSell

    #Visualise
    title = 'Close Price History Buy and  Sell Signals'
    my_stocks_data = data
    plt.figure(figsize=(13,5)) 
    plt.scatter(my_stocks_data.index, my_stocks_data['Buy_Signal_Value'], color = 'green', label='Buy Signal', marker = '^', alpha = 1)
    plt.scatter(my_stocks_data.index, my_stocks_data['Sell_Signal_Value'], color = 'red', label='Sell Signal', marker = 'v', alpha = 1)
    plt.plot(my_stocks_data['Date'],my_stocks_data['Close'],  label='Close Price', alpha = 0.35)
    plt.xticks(np.arange(0,len(data), 100), data['Date'][0:len(data):100])
    plt.xticks(rotation=45)
    plt.title(title)
    plt.xlabel('Date',fontsize=18)
    plt.ylabel('Close Price',fontsize=18)
    plt.legend( loc='upper left')
    plt.show()
