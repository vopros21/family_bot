import unittest
import portfolio_engine as pe


class TestAveragePrice(unittest.TestCase):
    def test_stock_not_in_portfolio(self):
        """Test if someone tries to get a stock which is not presented in the portfolio"""
        query_result = pe.average_price('BUG')
        self.assertEqual((0, 0), query_result, 'Stock BUG was found in the portfolio.')

    def test_stock_in_portfolio(self):
        """Test if average_price function returns the correct values for only bought"""
        stock_price = 20
        quantity = 5
        expected_result = (stock_price, quantity)
        query_result = pe.average_price('TEST')
        self.assertEqual(expected_result, query_result, 'Wrong price for stock in portfolio')

    def test_multiple_stock_in_portfolio(self):
        """Test if average_price function returns the correct value for multiple lines"""
        stock_price = 20
        quantity = 6
        expected_result = (stock_price, quantity)
        query_result = pe.average_price('TEST2')
        self.assertEqual(expected_result, query_result, 'Wrong price for stock in portfolio')


if __name__ == '__main__':
    unittest.main()