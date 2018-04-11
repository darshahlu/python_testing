"""

Task:
    - build a stock picker; it identifies good stocks to buy.
    - first part of stock picking is to determine if a given stock is a good buy.
    - we define a stock is a good buy if its current price is less than 10% of its 1 year average price.
    - price data is given by the following APIs:
        - 1 year average obtained from: https://api.iextrading.com/1.0/stock/aapl/chart/1y
        - current price: https://api.iextrading.com/1.0/stock/aapl/price
    - to make this simpler, the following template is already implemented.
"""


class StockPicker:

    def __init__(self):
        pass

    def is_good_buy(self, ticker: str) -> bool:
        """"Return True if the stock is a good buy.

        A stock is a good buy if its current price is less than 10% of its 1 year average price.
        """
        pass

