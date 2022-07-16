from joconst.maps import INTERVAL_TDX_MAP
from joconst.object import Interval
from joconst.constant import TdxMarket

from jotdx.utils import to_data, get_stock_market
from jotdx.params import TDXParams
from jotdx.quotes import Quotes


def mootdx_method(symbol, frequency, offset, start, market):
    quotes = Quotes.factory(market='std')

    df = quotes.transaction(
        symbol=symbol, frequency=frequency, offset=offset, start=start
    )

    quotes.close()
    return df


def pytdx_method(symbol, frequency, offset, start, market):
    from jotdx.hq import TdxHq_API
    from jotdx.utils.best_ip_async import select_best_ip_async
    from jotdx.params import TDXParams

    ip_port_dict = select_best_ip_async(_type="stock")
    ip = ip_port_dict['ip']
    port = ip_port_dict['port']

    api = TdxHq_API()
    with api.connect(ip=ip, port=port):
        df5 = api.to_df(
            api.get_transaction_data(
                market=market, code=symbol, start=start, count=offset
            )
        )

        list6 = api.get_transaction_data(
            market=market, code=symbol, start=start, count=offset
        )
        return df5, list6


def std_bars_test():
    # 也可以使用
    # frequency = TDXParams.KLINE_TYPE_15MIN
    frequency = INTERVAL_TDX_MAP[Interval.MINUTE_15]

    symbol = "123075"
    market = get_stock_market(symbol=symbol)

    start = 0
    offset = 800

    df1 = mootdx_method(symbol=symbol, frequency=frequency, offset=offset, start=start, market=market)
    df2, list1 = pytdx_method(symbol=symbol, frequency=frequency, offset=offset, start=start, market=market)
    print(1)


if __name__ == '__main__':
    std_bars_test()
