import yfinance as yf
import Data_source as ds
import Desc_Ans as da
import Prediction as pred
import ticker_plot as tkp
import unittest
import os
import warnings

class Data_source_mod_test(unittest.TestCase):
    def test_export_data(self):
        #1. Data length for user defined dates
        data_df = yf.download('amzn', start='2020-02-01', end='2020-03-02')
        data = ds.export_data('amzn', '2020-02-01', '2020-03-02', '0')
        self.assertEqual(len(data),len(data_df))
        #2. Wrong Ticker Symbol- Output - AMZNNN: No data found, symbol may be delisted
        data = ds.export_data('amznnn', '2020-02-01', '2020-03-02', '0')
        self.assertEqual(data,None)
        #3. Data Compare for a Period
        data = ds.export_data('amzn', '2020-02-01', '2020-03-02', '1y')
        data_df = yf.download('amzn', period='1y')
        self.assertEqual(len(data),len(data_df))
        #4. No period - Output "Not a Valid Period"
        data = ds.export_data('amzn', '0', '0', '')
        self.assertEqual(data,None)
        #5. Empty Period - Output "Not a Valid Period"
        data = ds.export_data('amzn', '0', '0', ' ')
        self.assertEqual(data,None)
        #6. Wrong Period - Output "Not a Valid Period"
        data = ds.export_data('amzn', '0', '0', 'afsgdh')
        self.assertEqual(data,None)
        #7. Downloaded CSV
        yf.download('amzn', start='2020-02-01', end='2020-03-02')
        self.assertTrue(os.path.isfile('amzn.csv'))
        #8. Downloaded CSV column length
        data = ds.export_data('amzn', '2020-02-01', '2020-03-02', '0')
        file = open('amzn.csv')
        self.assertEqual(len(file.readlines())-1,len(data))
        file.close()

    def test_validate_date_format(self):
        #9. Start date greater than end date
        self.assertFalse(ds.validate_date_format('2020-12-02','2020-03-09'))
        #10. Wrong date used
        self.assertFalse(ds.validate_date_format('2020-13-12','202-03-09'))
        #11. Blank date used
        self.assertFalse(ds.validate_date_format('2020-13-12','202-03-09'))


class Desc_Ans_test(unittest.TestCase):
    def test_get_stock_history(self):
        #12. Wrong input ticker - Output = "Data/File is empty"
        symbol = 'amznnn'
        msft = yf.Ticker(symbol)
        data = msft.history(period='1y')
        self.assertEqual(da.data_description(data,symbol),None)
        #13. Length of saved description data frsamse4
        symbol = 'amzn'
        msft = yf.Ticker(symbol)
        data = msft.history(period='1y')
        file = open('amzn_description.csv')
        description_data = data.describe()
        self.assertEqual(len(file.readlines()),len(description_data))
        file.close()
        #14. Checked descriptive_analysis() for wrong csv file name - Output - "No Such file or Directory found"
    
def test_function():
    unittest.main()
