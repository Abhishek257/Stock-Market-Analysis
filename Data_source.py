import yfinance as yf
import datetime
import pandas as pd
import os
##testing a change 2s

'''https://pypi.org/project/yfinance/
	https://algotrading101.com/learn/yfinance-guide/
	https://towardsdatascience.com/free-stock-data-for-python-using-yahoo-finance-api-9dafd96cad2'''

def export_data(symbol, start, end, period):
    """Searches for the ticker using yfinance library for a given time range and stores it to an object.
    Adds some extra columns to the object for plots basis and saves it to a csv
    """
    data_df = pd.DataFrame()
    try:
        if(period != '0' and len(period) > 1 and len(period)< 4):
            data_df = yf.download(symbol, period=period)
        elif(start !='0' and end!='0'):
            data_df = yf.download(symbol, start=start, end=end)
        else:
            print('Enter a valid period')
        if(len(data_df)>1 ):
            data_df['dividends'] = yf.Ticker(symbol).dividends
            SExpWM = data_df.Close.ewm(span=12, adjust=False).mean() #Short Exponencial Weighted Mean
            LExpWM = data_df.Close.ewm(span=26, adjust=False).mean() #Long Exponencial Weighted Mean
            MovAvgCD = SExpWM - LExpWM
            signal = MovAvgCD.ewm(span=9, adjust=False).mean()
            data_df['MACD'] = MovAvgCD
            data_df['Signal'] = signal
            data_df.to_csv(symbol.lower() + '.csv')
            return data_df
        else:
            return None
    except ValueError:
        print('Wrong data input')


def validate_date_format(start,end):
    """Validates the date format of user input"""
    format = "%Y-%m-%d"
    try:
        start_date = datetime.datetime.strptime(start, format)
        end_date = datetime.datetime.strptime(end, format)
        if start_date>end_date:
            print('Start Date should be smaller than end date')
            return False
    except ValueError:
        print("\nWrong data format used.\nTry again with valid period format (YYYY-MM-DD)\n")
        return False
    return True

def get_stock_history():
    data = None
    while data is None:
        print('-'*60)
        symbol = input("Please choose ticker symbol: ")
        print('-'*60)
        print('Would you like to get data for :\n','-'*60,'\n\t1. User defined date range(start & end date) \n\t2. Pre-defined periods (1d, 5d, etc.) ')
        print('-'*60)
        choice = input("Enter your Choice : ")
        if(choice == '1'):
            start = input("Please choose start period (YYYY-MM-DD) : ")
            end = input("Please choose end period (YYYY-MM-DD) : ")
            print('-'*60)
            if (validate_date_format(start,end)): 
                data = export_data(symbol, start, end, '0')
        elif(choice == '2'):
            print('-'*60)
            period = input("Please choose period: (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max) : ")
            print('-'*60)
            data = export_data(symbol, '0', '0', period)
        else:
            print('Enter a valid choice')
    return data,symbol

def download_data():
    data = None
    while data is None:
        data,symbol = get_stock_history()
        print("The requested data has been downloaded\nLocation - ",os.getcwd()+symbol+'.csv')
        print('-'*60)
        choice = input('Would you like to see the data info(Y/N) : ')
        if(choice=='Y' or choice =='y'):
            print('\n-------Data Info------\n')
            print(data.info())
            print('\n-------Data(First 10 rows)-----------\n')
            print(data.head())
            print('-------END---------')
    return data,symbol

