import re
import unittest
import db_engine as de


class TestValidateUserInput(unittest.TestCase):
    def test_correct_input(self):
        """Test if user input the correct data"""
        ticker, date, price, quantity = de.validate_user_input('/save aapl 2021-06-01 100.12 2')
        self.assertEqual('AAPL', ticker, "Ticker is not in correct format")
        self.assertEqual('2021-06-01', date, 'Date not is in correct format')
        self.assertEqual(100.12, price, 'Price is not in correct format')
        self.assertEqual(2, quantity, 'Quantity is not in correct format')

    def test_wrong_argument_quantity(self):
        """Test if there is correct number of arguments in user's input"""
        user_input = ('/save aapl', '/save aapl 2021-06-01 100.12 2 45')
        for text in user_input:
            none_obj = de.validate_user_input(user_text=text)
            self.assertEqual(None, none_obj, 'Not enough arguments in user input')

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

    def test_incorrect_date_format_two_digits_year(self):
        """Test if two digits year will be filtered"""
        user_input = '/save aapl 21-06-01 100.12 2'
        none_obj = de.validate_user_input(user_text=user_input)
        self.assertEqual(None, none_obj, 'Wrong year format: two digits')

    def test_incorrect_date_format_one_digit_dm(self):
        """Test if one digit day or month will be filtered"""
        user_input = '/save aapl 2021-6-01 100.12 2'
        none_obj = de.validate_user_input(user_text=user_input)
        self.assertEqual(None, none_obj, 'Wrong month format: one digit')


if __name__ == '__main__':
    unittest.main()
