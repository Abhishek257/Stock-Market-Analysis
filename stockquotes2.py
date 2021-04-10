import Data_source as ds
from Desc_Ans import descriptive_analysis
from Prediction import Arima_Prediction_model,linear_regression
import warnings
from Unit_testing import unittest

'''https://www.kaggle.com/samansiadati/stock-market-analysis
	https://www.kaggle.com/pierpaolo28/stock-market-analysis-and-time-series-prediction'''

def t_and_c():
    """Display terms and conditions from 'terms.txt'"""
    for line in open('terms.txt'):
        print(line, end = "")

def Login():
    print('-'*60)
    print('Welcome to the Stock Quote Application')
    print('-'*60)
    print("\t1. Export Data\n\t2. Descriptive Analysis\n\t3. Predictive Analysis\n\t4. Unit Testing\n\t5. Read T&C\n\t6. Quit")
    print('-'*60)
    return input("Please choose option: ")
    
def process_choice(choice):
    while choice != "6":
        if choice == "1":
            ds.download_data()
        elif choice == "2":
            descriptive_analysis()
        elif choice == "3":
            print('-'*60)
            choice_prediction = input("Please choose among the model options:\n\t1. Linear Regression\n\t2. ARIMA\n")
            print('-'*60)
            if choice_prediction=='1':
                linear_regression()
            elif choice_prediction=='2':
                Arima_Prediction_model()
            else:
                print('Enter a valid choice')
        elif choice == "4":
            print('-'*60)
            print("The below listed tests were performed during the unit testing:\n1. Data length for user defined dates\n\
            2. Wrong Ticker Symbol- Output - AMZNNN: No data found, symbol may be delisted\n\
            3. Data Compare for a Period\n\
            4. No period\n\
            5. Empty Period\n\
            6. Wrong Period\n\
            7. Downloaded CSV\n\
            8. Downloaded CSV column length\n\
            9. Start date greater than end date\n\
            10. Wrong date used\n\
            11. Blank date used\n\
            12. Wrong input ticker\n\
            13. Length of saved description data frsamse4\n\
            14. Checked descriptive_analysis() for wrong csv file name - Output - No Such file or Directory found")
            print('-'*60)
            print('-'*60)
            print("Python file with name Unit_testing.py can be execute to check the unit testing model")
        elif choice == '5':
            t_and_c()
        else:
            print("Wrong choice, please try again.")
        choice = Login()

def main():
    warnings.filterwarnings("ignore")
    choice = Login()
    process_choice(choice)

if __name__ == '__main__':
    main()