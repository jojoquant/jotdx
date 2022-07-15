import pandas as pd
from joconst.maps import INTERVAL_TDX_MAP
from joconst.object import Interval
from joconst.constant import TdxMarket

from jotdx.utils import to_data, get_stock_market
from jotdx.params import TDXParams
from jotdx.quotes import Quotes


def mootdx_method(symbol, frequency, offset, start, market):
    quotes = Quotes.factory(market='std')

    df = quotes.bars(
        symbol=symbol, frequency=frequency, offset=offset, start=start
    )

    # quotes.bars 中封装的是如下操作,
    # 但是实际调用的时候却是使用期货的函数 get_instrument_bars, 非常奇怪
    # offset 超过 800, get_security_bars 无法获取数据
    df2_list = quotes.client.get_security_bars(
        int(frequency), int(market), str(symbol), int(start), int(offset)
    )
    df2 = to_data(df2_list)

    quotes.close()
    print(1)


def pytdx_method(symbol, frequency, offset, start, market):
    from jotdx.hq import TdxHq_API
    from jotdx.utils.best_ip_async import select_best_ip_async
    from jotdx.params import TDXParams

    ip_port_dict = select_best_ip_async(_type="stock")
    ip = ip_port_dict['ip']
    port = ip_port_dict['port']

    api = TdxHq_API()
    with api.connect(ip=ip, port=port):

        all_df = pd.DataFrame()
        while True:
            df5 = api.to_df(
                api.get_index_bars(
                    category=frequency, market=market, code=symbol, start=start, count=offset
                )
            )

            if df5.empty:
                break

            all_df = pd.concat([df5, all_df])
            start += offset
            print(start)

        bar_data_list = api.get_security_bar_data(
            category=frequency, market=market, code=symbol, start=start, count=offset
        )

        # list6 = api.get_transaction_data(
        #     market=market, code=symbol, start=start, count=offset
        # )
        print(1)


def std_bars_test():
    # 也可以使用
    # frequency = TDXParams.KLINE_TYPE_15MIN
    frequency = INTERVAL_TDX_MAP[Interval.DAILY]

    symbol = "000001"
    market = TdxMarket.SSE

    start = 0
    offset = 800

    # mootdx_method(symbol=symbol, frequency=frequency, offset=offset, start=start, market=market)
    pytdx_method(symbol=symbol, frequency=frequency, offset=offset, start=start, market=market)


if __name__ == '__main__':
    std_bars_test()
