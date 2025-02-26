import Data_source as ds
from statsmodels.tsa.api import ARIMA
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error
import warnings
import datetime as dt
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
import yfinance as yf
from sklearn.svm import SVR


#testing git
def smape_kun(y_true, y_pred):
    return np.mean((np.abs(y_pred - y_true) * 200/ (np.abs(y_pred) + np.abs(y_true))))

def inverse_difference(history, yhat, interval=1):
	return yhat + history[-interval]

'''https://randerson112358.medium.com/predict-stock-prices-using-python-machine-learning-53aa024da20a'''
def linear_regression():
    warnings.filterwarnings("ignore")
    #symbol='amzn'
    data,symbol = ds.download_data()
    file_name = symbol +'.csv'
    data_complete = pd.read_csv(file_name)
    data = pd.DataFrame({'Close' : data_complete['Close']})
    days_to_predict = int(input('Enter number of days to predict the data for : '))
    data['prediction'] = data[['Close']].shift(-days_to_predict) #Create prediction column in data with values of close column
    forecast_time = int(days_to_predict)
    X = np.array(data.drop(['prediction'], 1))
    Y = np.array(data['prediction'])
    X_prediction = X[:-forecast_time]
    Y_prediction = Y[:-forecast_time]
    X_train, X_test, Y_train, Y_test = train_test_split(X_prediction, Y_prediction, test_size=0.4) #Separating test and train data 60-40
    #Linear regression
    lr = LinearRegression()
    lr.fit(X_train, Y_train)
    lr_confidence = lr.score(X_test, Y_test)
    print("linear Regression confidence: ", lr_confidence)
    x_forecast = np.array(data.drop(['prediction'],1))
    lr_prediction = lr.predict(x_forecast)

    #Forecast
    print('------------------Forecast----------------\n')
    dates = []
    last_date = len(data) -1
    Last_data_date = data_complete['Date'][last_date]
    date = dt.datetime.strptime(str(Last_data_date),'%Y-%m-%d')
    for i in range(days_to_predict):
        dates.append(date.strftime('%Y-%m-%d'))
        print(date.strftime('%Y-%m-%d')," ",round(lr_prediction[-i],2))
        date += dt.timedelta(days=1)  
    plt.figure(figsize=(12,7))
    plt.plot(lr_prediction, color='green', marker='o', linestyle='dashed', label='Predicted Price')
    plt.plot(data['Close'], color='red', label='Actual Price')
    plt.title('Prices Prediction')
    plt.xlabel('Dates')
    plt.ylabel('Prices')
    plt.xticks(np.arange(0,len(data), 150), data_complete['Date'][0:len(data):150])
    plt.legend()
    plt.show()

    #Create and plot the Predicted data
    next_prediction = lr_prediction[-days_to_predict:]
    plt.plot(next_prediction, label='Predicted Values')
    plt.xticks(np.arange(0,len(dates), 2), dates)
    plt.xticks(rotation=45)
    plt.show()

'''	https://machinelearningmastery.com/make-sample-forecasts-arima-python/
    https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/
	https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/
    https://www.analyticsvidhya.com/blog/2020/10/how-to-create-an-arima-model-for-time-series-forecasting-in-python/
    https://www.kdnuggets.com/2020/01/stock-market-forecasting-time-series-analysis.html'''
def Arima_Prediction_model():
    warnings.filterwarnings("ignore")
    data,symbol = ds.download_data()
    format = "%Y-%m-%d"
    file_name = symbol +'.csv'
    data_frame = pd.read_csv(file_name)
    training_data, testing_data = data_frame[0:int(len(data_frame)*0.8)], data_frame[int(len(data_frame)*0.8):]
    train_array = training_data['Open'].values
    test_array = testing_data['Open'].values
    current_data = [x for x in train_array]
    forecast = list()

    #Model train for Forecasting
    for t in range(len(test_array)):
        model = ARIMA(current_data, order=(5,1,0))
        model_fit = model.fit(disp=0)
        model_output = model_fit.forecast()
        Result = model_output[0]
        forecast.append(Result)
        current_data.append(test_array[t])
    error_percentage = mean_squared_error(test_array, forecast)
    print('Testing the Mean Squared Error: %.3f' % error_percentage)
    error_percentage_2 = smape_kun(test_array, forecast)
    print('Symmetric mean absolute percentage error: %.3f' % error_percentage_2)
    
    #Forecast Plot
    plt.figure(figsize=(12,7))
    plt.plot(data_frame['Open'], 'green', color='blue', label='Training Data')
    plt.plot(testing_data.index, forecast, color='green', marker='o', linestyle='dashed', 
            label='Predicted Price')
    plt.plot(testing_data['Open'], color='red', label='Actual Price')
    plt.title('Prices Prediction')
    plt.xlabel('Dates')
    plt.ylabel('Prices')
    plt.xticks(np.arange(0,len(data_frame), 150), data_frame['Date'][0:len(data_frame):150])
    plt.legend()
    plt.show()

    #Plot Actual vs Forecast
    plt.figure(figsize=(12,7))
    plt.plot(testing_data.index, forecast, color='green', marker='o', linestyle='dashed', 
            label='Predicted Price')
    plt.plot(testing_data.index, testing_data['Open'], color='red', label='Actual Price')
    data_till_date = len(data_frame)*0.30
    no_dates = int(len(data_frame)*0.10)
    plt.xticks(np.arange(len(data_frame)-data_till_date,len(data_frame), no_dates), data_frame['Date'][len(test_array):len(data_frame):no_dates])
    plt.title('Prices Prediction')
    plt.xlabel('Dates')
    plt.ylabel('Prices')
    plt.legend()
    plt.show()

    #User Requested prediction frame
    user_predictions = list()
    dates = []
    values = list()
    last_date = len(data_frame) -1
    Last_data_date = data_frame['Date'][last_date]
    print(data.shape)
    days_to_predict = input('Enter number of days to predict the data for : ')
    predict_start_count = len(current_data)
    predict_end_count = predict_start_count + int(days_to_predict)
    pred = model_fit.predict(start= predict_start_count,end= predict_end_count)
    date = dt.datetime.strptime(str(Last_data_date),'%Y-%m-%d')
    print_format = "{:20}{:<10}"
    print(print_format.format('Date','Predicted Open Price'))
    for yhat in pred:
        inverted = yhat + current_data[-1]
        print(print_format.format(date.strftime('%Y-%m-%d'), int(inverted)))
        dates.append(date.strftime('%Y-%m-%d'))
        values.append(int(inverted))
        user_predictions.append(yhat)
        date += dt.timedelta(days=1)   
        current_data.append(inverted)
    #Plot User Requested frame
    plt.plot(values, label='Predicted Values')
    plt.xticks(np.arange(0,len(dates), 2), dates)
    plt.xticks(rotation=45)
    plt.show()