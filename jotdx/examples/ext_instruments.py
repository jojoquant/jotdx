from joconst.maps import INTERVAL_TDX_MAP
from joconst.object import Interval
from joconst.constant import TdxMarket
from jotdx.quotes import Quotes


def mootdx_method(symbol, frequency, offset, start, market):
    quotes = Quotes.factory(market='ext')

    # 根据 get_instrument_count 获取所有产品的数量 大概 87000 多条
    # 根据全品种数量进行遍历 get_instrument_info(start=0, offset=100)
    # 感觉实用性不如 get_instrument_quote_list
    # 耗时太长, 注释掉
    # instruments = quotes.instruments()

    # 底层相当于在调用 tdx client 的 get_instrument_info(start=0, offset=100)
    # 通过测试可知, max offset 大约为 1021
    instrument = quotes.instrument(start=start, offset=offset)
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
        df2 = api.to_df(api.get_instrument_info(start=start, count=offset))
        print(1)


def ext_bars_test():
    # 也可以使用
    # frequency = TDXParams.KLINE_TYPE_15MIN
    frequency = INTERVAL_TDX_MAP[Interval.MINUTE]

    symbol = "RBL8"
    market = TdxMarket.SHFE

    start = 0
    offset = 10000  # max offset 大约为 1021

    mootdx_method(symbol=symbol, frequency=frequency, offset=offset, start=start, market=market)
    pytdx_method(symbol=symbol, frequency=frequency, offset=offset, start=start, market=market)


if __name__ == '__main__':
    ext_bars_test()
