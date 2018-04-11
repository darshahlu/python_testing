from example.stock_picker.stock_picker_solution import StockPicker, StockPricesAPI


def test_get_1_yr_avg_price():

    def my_price_data(ticker):
        return [{'date': '2017-04-10',
                 'open': 141.3635,
                 'high': 141.6384,
                 'low': 140.6744,
                 'close': 140.9402,
                 'volume': 18933397,
                 'unadjustedVolume': 18933397,
                 'change': -0.167353,
                 'changePercent': -0.119,
                 'vwap': 141.1334,
                 'label': 'Apr 10, 17',
                 'changeOverTime': 0}]

    s = StockPricesAPI()
    s.get_1_yr_price_data = my_price_data
    assert s.get_1_yr_avg_price('some-ticker') == 140.9402

    s.get_1_yr_price_data = lambda ticker: [{'close': 3}, {'close': 1}]
    assert s.get_1_yr_avg_price('some-ticker') == 2
