import Data_source as ds
import ticker_plot as tk
import yfinance as yf
import pandas as pd


def data_description(data,symbol):
    """print the data description in tablular format(mean, std, max, quartiles etc)"""
    if(len(data)>0):
        description_data = data.describe()
        count_cols = description_data.shape[1]
        data_frame = pd.DataFrame({'Mean' : description_data.loc['mean'],\
        'Std' : description_data.loc['std'], 'Min' : description_data.loc['min'],\
        'Max' : description_data.loc['max'],'Range' : description_data.loc['max']-description_data.loc['min']\
        ,'First Quartile' : description_data.loc['25%'],'Second Quartile' : description_data.loc['50%']\
        ,'Third Quartile' : description_data.loc['75%']})
        print('-'*100)
        print(data_frame)
        print('-'*100)
        choice = input("Would you like to save the data description to csv file(Y/N) : ")
        if(choice =='Y' or choice == 'y'):
            file_name = symbol.lower() + '_description.csv'
            data_frame.to_csv(file_name)
            print("Data Description has been saved with file name : ", file_name)
    else:
        print('Data file/source is empty')

def get_choice(choice,data,symbol):
    if choice == "1":
        data_description(data,symbol)
    elif choice == "2":
        tk.get_ticker_data(data,symbol)
    elif choice == "9":
        return False
    else:
        print("Please Enter a valid input")
    return True

def descriptive_analysis():
    """Load the online or offline object as per the user's ask"""
    flag =True
    print('-'*60)
    print("What is the data source you want to use\n",'-'*60,"\n\t1. Online\n\t2. Offline")
    print('-'*60)
    choice = input("Please choose option: ")
    data = None
    while(data is None):
        if choice == "1":
            data_object,symbol = ds.get_stock_history()
            try:
                data = pd.read_csv(symbol+'.csv')
            except OSError:
                print('No such file or directory found')
            print('-------Accessing Live Online------')
        elif choice == "2":
            print('-'*60)
            symbol = input('Please enter the csv File Name(Example- xyz): ')
            try:
                data = pd.read_csv(symbol+'.csv')
            except OSError:
                print('No such file or directory found')
        else:
            print('-'*60)
            print("Enter a valid Choice: ")
            print('-'*60)
            choice = input("What is the data source you want to use \n\t1. Online\n\t2. Offline")
            print('-'*60)
    while(flag):
        print('-'*60)
        choice = input("Descriptive Analysis:\n\t1. Data\n\t2. Plots\n\t9. Back to Previous options \nEnter your Choice : ")
        print('-'*60)
        flag = get_choice(choice,data,symbol)
    
