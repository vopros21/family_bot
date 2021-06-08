import re
import unittest
import db_engine as de


class TestStandardPortfolioData(unittest.TestCase):
    def test_correct_input(self):
        """Test if user input the correct data"""
        ticker, date, price, quantity = de.standard_portfolio_data('/save aapl 2021-06-01 100.12 2')
        self.assertEqual('AAPL', ticker, "Ticker is not in correct format")
        self.assertEqual('2021-06-01', date, 'Date not is in correct format')
        self.assertEqual(100.12, price, 'Price is not in correct format')
        self.assertEqual(2, quantity, 'Quantity is not in correct format')

    def test_incorrect_ticker_input_short_name(self):
        """Test if too short ticker will be filtered"""
        ticker, date, price, quantity = de.standard_portfolio_data('/save a 2021-06-01 100.12 2')
        self.assertEqual(0, ticker, "Returned value of ticker is not correct")
        self.assertNotEqual('A', ticker, "Ticker is not in correct format")
        self.assertEqual(0, date, 'Ticker is not in correct format')
        self.assertEqual(0, price, 'Ticker is not in correct format')
        self.assertEqual(0, quantity, 'Ticker is not in correct format')

    def test_incorrect_ticker_input_long_name(self):
        """Test if too long ticker will be filtered"""
        ticker, date, price, quantity = de.standard_portfolio_data('/save apple 2021-06-01 100.12 2')
        self.assertEqual(0, ticker, "Returned value of ticker is not correct")
        self.assertNotEqual('APPLE', ticker, "Ticker is not in correct format")
        self.assertEqual(0, date, 'Ticker is not in correct format')
        self.assertEqual(0, price, 'Ticker is not in correct format')
        self.assertEqual(0, quantity, 'Ticker is not in correct format')

    def test_incorrect_ticker_input_not_letters(self):
        """Test if wrong ticker will be filtered"""
        ticker, date, price, quantity = de.standard_portfolio_data('/save ap1 2021-06-01 100.12 2')
        self.assertEqual(0, ticker, "Returned value of ticker is not correct")
        self.assertNotEqual('AP1', ticker, "Ticker is not in correct format")
        self.assertEqual(0, date, 'Ticker is not in correct format')
        self.assertEqual(0, price, 'Ticker is not in correct format')
        self.assertEqual(0, quantity, 'Ticker is not in correct format')
