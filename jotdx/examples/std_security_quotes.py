from joconst.maps import INTERVAL_TDX_MAP
from joconst.object import Interval
from joconst.constant import TdxMarket

from jotdx.utils import to_data, get_stock_market, get_stock_markets
from jotdx.params import TDXParams
from jotdx.quotes import Quotes


def mootdx_method(symbol_list):
    quotes = Quotes.factory(market='std')

    df = quotes.quotes(
        symbol=symbol_list
    )

    quotes.close()
    return df


def pytdx_method(market_symbol_list):
    from jotdx.hq import TdxHq_API
    from jotdx.utils.best_ip_async import select_best_ip_async

    ip_port_dict = select_best_ip_async(_type="stock")
    ip = ip_port_dict['ip']
    port = ip_port_dict['port']

    api = TdxHq_API()
    with api.connect(ip=ip, port=port):
        df5 = api.get_security_quotes(market_symbol_list)
        tickdata_list = api.get_security_tick_data(market_symbol_list)
        return df5, tickdata_list


def std_bars_test():
    # 也可以使用
    # frequency = TDXParams.KLINE_TYPE_15MIN
    frequency = INTERVAL_TDX_MAP[Interval.MINUTE_15]

    symbol = ["000001","000550","600300", "123121"]
    # 注意! 是两个不同的函数
    # market = get_stock_market(symbol=symbol)
    market_symbol_list = get_stock_markets(symbols=symbol)

    start = 0
    offset = 800

    df1 = mootdx_method(symbol_list=symbol)
    df2, ticks = pytdx_method(market_symbol_list=market_symbol_list)
    print(1)


if __name__ == '__main__':
    std_bars_test()
