from jotdx.quotes import Quotes
from mock_params import Interval_to_frequency_dict, Interval
from jotdx.utils import to_data

if __name__ == '__main__':
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
