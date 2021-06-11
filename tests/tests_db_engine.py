import re
import unittest
import db_engine as de


class TestStandardPortfolioData(unittest.TestCase):
    def test_correct_input(self):
        """Test if user input the correct data"""
        ticker, date, price, quantity = de.validate_user_input('/save aapl 2021-06-01 100.12 2')
        self.assertEqual('AAPL', ticker, "Ticker is not in correct format")
        self.assertEqual('2021-06-01', date, 'Date not is in correct format')
        self.assertEqual(100.12, price, 'Price is not in correct format')
        self.assertEqual(2, quantity, 'Quantity is not in correct format')

    def test_incorrect_ticker_input_short_name(self):
        """Test if too short ticker will be filtered"""
        none_obj = de.validate_user_input('/save a 2021-06-01 100.12 2')
        self.assertEqual(None, none_obj, 'Ticker is too short')

    def test_incorrect_ticker_input_long_name(self):
        """Test if too long ticker will be filtered"""
        none_obj = de.validate_user_input('/save apple 2021-06-01 100.12 2')
        self.assertEqual(None, none_obj, 'Ticker is too long')

    def test_incorrect_ticker_input_not_letters(self):
        """Test if wrong ticker will be filtered"""
        none_obj = de.validate_user_input('/save ap1 2021-06-01 100.12 2')
        self.assertEqual(None, none_obj, 'Ticker is not in correct format')


if __name__ == '__main__':
    unittest.main()
