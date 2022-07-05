from joconst.maps import INTERVAL_TDX_MAP
from joconst.object import Interval
from joconst.constant import TdxMarket
from jotdx.quotes import Quotes


def mootdx_method(symbol, frequency, offset, start, market):
    quotes = Quotes.factory(market='ext')

    df = quotes.bars(
        symbol=symbol, frequency=frequency, offset=offset, start=start, market=market
    )

    quotes.close()
    print(1)


def pytdx_method(symbol, frequency, offset, start, market):
    from jotdx.exhq import TdxExHq_API
    from jotdx.utils.best_ip_async import select_best_ip_async

    ip_port_dict = select_best_ip_async(_type="future")
    ip = ip_port_dict['ip']
    port = ip_port_dict['port']

    api = TdxExHq_API()
    with api.connect(ip=ip, port=port):

        # df1 = api.to_df(api.get_security_list(market=market))
        # df2 = api.to_df(api.get_instrument_info(0, 10000))
        # df3 = api.to_df(api.get_instrument_quote_list(30, 3, count=800))  # count max is 100
        # df4 = api.to_df(api.get_instrument_quote_list(30, 3, start=100, count=800))  # count max is 100

        df5 = api.to_df(
            api.get_instrument_bars(
                category=frequency, market=market, code=symbol, start=start, count=offset
            )
        )
        # list6 = api.get_transaction_data(
        #     category=frequency, market=market, code=symbol, start=0, count=700
        # )
        print(1)


def ext_bars_test():
    # 也可以使用
    # frequency = TDXParams.KLINE_TYPE_15MIN
    frequency = INTERVAL_TDX_MAP[Interval.MINUTE]

    symbol = "RBL8"
    market = TdxMarket.SHFE

    start = 0
    offset = 1000

    mootdx_method(symbol=symbol, frequency=frequency, offset=offset, start=start, market=market)
    pytdx_method(symbol=symbol, frequency=frequency, offset=offset, start=start, market=market)


if __name__ == '__main__':
    ext_bars_test()
