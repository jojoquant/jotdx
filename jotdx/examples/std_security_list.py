from joconst.maps import INTERVAL_TDX_MAP
from joconst.object import Interval
from joconst.constant import TdxMarket

from jotdx.utils import to_data, get_stock_market
from jotdx.params import TDXParams
from jotdx.quotes import Quotes


def mootdx_method():
    quotes = Quotes.factory(market='std')

    # Header 为 [code, volunit, decimal_point, name, pre_close]
    # 上海 15549 条记录, 包含股票, 指数, 基金, 板块概念, 债券
    sse_stocks = quotes.stocks(market=0)
    # 深圳 20123 条记录, 包含股票, 指数, 基金, 板块概念, 债券
    szse_stocks = quotes.stocks(market=1)

    # empty
    # bse_stocks = quotes.stocks(market=2)

    quotes.close()
    print(1)
    return sse_stocks


def pytdx_method():
    from jotdx.hq import TdxHq_API
    from jotdx.utils.best_ip_async import select_best_ip_async

    ip_port_dict = select_best_ip_async(_type="stock")
    ip = ip_port_dict['ip']
    port = ip_port_dict['port']

    api = TdxHq_API()
    with api.connect(ip=ip, port=port):

        # 参数 start 为整张大表 ( 15000~20000 多条数据 ) 的起点, 每次返回 1000 条数据
        df1 = api.to_df(api.get_security_list(market=0, start=1000))
        df2 = api.to_df(api.get_security_list(market=1, start=10000))

        # df2 = api.to_df(api.get_instrument_info(0, 10000))
        # df3 = api.to_df(api.get_instrument_quote_list(30, 3, count=800))  # count max is 100
        # df4 = api.to_df(api.get_instrument_quote_list(30, 3, start=100, count=800))  # count max is 100

        print(1)
    return df1


def std_bars_test():

    dd1 = mootdx_method()
    dd2 = pytdx_method()
    print(1)


if __name__ == '__main__':
    std_bars_test()
