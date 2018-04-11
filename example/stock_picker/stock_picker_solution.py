import requests


class StockPicker:
    GOOD_BUY_THRESHOLD_PCT = 10.0

    def __init__(self):
        pass

    @classmethod
    def _is_good_buy(cls, current_price: float, one_yr_avg_price: float) -> bool:
        """Return True if `current_price` is less than a percentage of `one_yr_avg_price`.

        >>> StockPicker._is_good_buy(89.99, 100.0)
        True
        >>> StockPicker._is_good_buy(90.00, 100.0)
        False
        """
        return current_price < (one_yr_avg_price * (1 - (cls.GOOD_BUY_THRESHOLD_PCT / 100)))

    def is_good_buy(self, ticker: str) -> bool:
        """"Return True if the stock is a good buy.

        A stock is a good buy if its current price is less than 10% of its 1 year average price.
        """
        # TODO: wire in the API calls to fetch prices
        pass


class StockPricesAPI:
    URL_BASE = "https://api.iextrading.com/1.0/stock/"

    def get_1_yr_avg_price(self, ticker):
        one_yr_prices = self.get_1_yr_price_data(ticker)
        average = sum([d['close'] for d in one_yr_prices]) / len(one_yr_prices)
        return average

    def get_1_yr_price_data(self, ticker):
        url = self.URL_BASE + '{}/chart/1y'.format(ticker)
        response = requests.get(url)
        return response.json()

    def get_current_price(self, ticker):
        url = self.URL_BASE + '{}/price'.format(ticker)
        response = requests.get(url)
        return response.json()


if __name__ == "__main__":
    s = StockPricesAPI()
    print(s.get_1_yr_avg_price('aapl'))
    print(s.get_current_price('aapl'))
