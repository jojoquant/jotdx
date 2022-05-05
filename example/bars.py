from jotdx.params import TDXParams
from jotdx.quotes import Quotes
from mock_params import Interval_to_frequency_dict, Interval
from jotdx.utils import to_data


def std_bars_test():
    frequency = Interval_to_frequency_dict[Interval.MINUTE_15]
    market = 0
    symbol = "123075"
    start = 0
    offset = 100

    quotes = Quotes.factory(market='std')

    df = quotes.bars(
        symbol=symbol, frequency=frequency, offset=offset, start=start
    )

    df2_list = quotes.client.get_security_bars(
        int(frequency), int(market), str(symbol), int(start), int(offset)
    )
    df2 = to_data(df2_list)

    print(1)


def ext_bars_test():
    frequency = Interval_to_frequency_dict[Interval.MINUTE]
    market = 0
    symbol = "RBL8"
    start = 0
    offset = 100

    quotes = Quotes.factory(market='ext')

    df = quotes.bars(
        market=30,
        symbol=symbol, frequency=frequency, offset=offset, start=start
    )
    print(1)


def ext_bars_pytdx_test():
    from jotdx.exhq import TdxExHq_API
    api = TdxExHq_API()
    # 59.175.238.38 : 7727
    with api.connect('59.175.238.38', 7727):
        df1 = api.to_df(api.get_markets())
        df2 = api.to_df(api.get_instrument_info(0, 800))
        df3 = api.to_df(api.get_instrument_quote_list(30, 3, count=800))
        df4 = api.to_df(api.get_instrument_quote_list(30, 3, start=100, count=800))
        print(2)


if __name__ == '__main__':
    # std_bars_test()
    # ext_bars_test()
    ext_bars_pytdx_test()