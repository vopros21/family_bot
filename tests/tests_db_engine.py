import unittest
from datetime import datetime

import db_engine as de


class TestValidateUserInput(unittest.TestCase):
    def test_correct_input(self):
        """Test if user inputs the correct data"""
        user_input_1 = '/save aapl 2021-06-01 100.12 2'
        ticker, date, price, quantity = de.validate_user_input(user_input_1)
        date = str(datetime.fromtimestamp(date)).split()[0]
        self.assertEqual('AAPL', ticker, "Ticker is not in correct format")
        self.assertEqual('2021-06-01', date, 'Date not is in correct format')
        self.assertEqual(100.12, price, 'Price is not in correct format')
        self.assertEqual(2, quantity, 'Quantity is not in correct format')

        user_input_2 = '/save aapl 2021-06-30 100.12 2'
        ticker, date, price, quantity = de.validate_user_input(user_input_2)
        date = str(datetime.fromtimestamp(date)).split()[0]
        self.assertEqual('AAPL', ticker, "Ticker is not in correct format")
        self.assertEqual('2021-06-30', date, 'Date not is in correct format')
        self.assertEqual(100.12, price, 'Price is not in correct format')
        self.assertEqual(2, quantity, 'Quantity is not in correct format')

    def test_wrong_argument_quantity(self):
        """Test if there is correct number of arguments in user's input"""
        user_input = ('/save aapl', '/save aapl 2021-06-01 100.12 2 45')
        for text in user_input:
            none_obj = de.validate_user_input(user_text=text)
            self.assertIsNone(none_obj, 'Not enough arguments in user input')

    def test_incorrect_ticker_input_short_name(self):
        """Test if too short ticker will be filtered"""
        none_obj = de.validate_user_input('/save a 2021-06-01 100.12 2')
        self.assertIsNone(none_obj, 'Ticker is too short')

    def test_incorrect_ticker_input_long_name(self):
        """Test if too long ticker will be filtered"""
        none_obj = de.validate_user_input('/save apple 2021-06-01 100.12 2')
        self.assertIsNone(none_obj, 'Ticker is too long')

    def test_incorrect_ticker_input_not_letters(self):
        """Test if wrong ticker will be filtered"""
        none_obj = de.validate_user_input('/save ap1 2021-06-01 100.12 2')
        self.assertIsNone(none_obj, 'Ticker is not in correct format')

    def test_incorrect_date_format_two_digits_year(self):
        """Test if two digits year will be filtered"""
        user_input = '/save aapl 21-06-01 100.12 2'
        none_obj = de.validate_user_input(user_text=user_input)
        self.assertIsNone(none_obj, 'Wrong year format: two digits')

    def test_incorrect_date_format_one_digit_dm(self):
        """Test if one digit day or month will be filtered"""
        user_input = '/save aapl 2021-6-01 100.12 2'
        none_obj = de.validate_user_input(user_text=user_input)
        self.assertIsNone(none_obj, 'Wrong month format: one digit')
        user_input = '/save aapl 2021*06-1 100.12 2'
        none_obj = de.validate_user_input(user_text=user_input)
        self.assertIsNone(none_obj, 'Wrong day format: one digit')

    def test_incorrect_date_wrong_month(self):
        """Test if month number is not greater than 12"""
        user_input = '/save aapl 2021-13-01 100.12 2'
        none_obj = de.validate_user_input(user_text=user_input)
        self.assertIsNone(none_obj, 'Month number is greater than 12')

    def test_incorrect_date_wrong_day(self):
        """Test if day is not greater than in the specified month"""
        user_input = '/save aapl 2021-06-31 100.12 2'
        none_obj = de.validate_user_input(user_text=user_input)
        self.assertIsNone(none_obj, 'Day number is greater than in the specified month')

        user_input_2 = '/save aapl 2021-02-29 100.12 2'
        none_obj = de.validate_user_input(user_text=user_input_2)
        self.assertIsNone(none_obj, 'Day number is greater than in the specified month')

    def test_incorrect_price_format(self):
        """Test if price is in correct format"""
        user_input_1 = '/save aapl 2021-06-01 100,12 2'
        none_obj = de.validate_user_input(user_text=user_input_1)
        self.assertIsNone(none_obj, 'Price is not in correct format')

        user_input_2 = '/save aapl 2021-06-01 10a.12 2'
        none_obj = de.validate_user_input(user_text=user_input_2)
        self.assertIsNone(none_obj, 'Price is not in correct format')

        user_input_3 = '/save aapl 2021-06-01 100 2'
        none_obj = de.validate_user_input(user_text=user_input_3)
        self.assertIsNone(none_obj, 'Price is not in correct format')

        user_input_4 = '/save aapl 2021-06-01 .12 2'
        none_obj = de.validate_user_input(user_text=user_input_4)
        self.assertIsNone(none_obj, 'Price is not in correct format')

    def test_incorrect_quantity_format(self):
        """Test if quantity shares is in correct format"""
        user_input_1 = '/save aapl 2021-06-01 100.12 2.2'
        none_obj = de.validate_user_input(user_text=user_input_1)
        self.assertIsNone(none_obj, 'Quantity is not in correct format')

        user_input_1 = '/save aapl 2021-06-01 100.12 a'
        none_obj = de.validate_user_input(user_text=user_input_1)
        self.assertIsNone(none_obj, 'Quantity is not in correct format')


if __name__ == '__main__':
    unittest.main()
