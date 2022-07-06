from joconst.maps import INTERVAL_TDX_MAP
from joconst.object import Interval
from joconst.constant import TdxMarket

from jotdx.utils import to_data, get_stock_market
from jotdx.params import TDXParams
from jotdx.quotes import Quotes


########################################################
#  tdx中对指定日期的方式获取数据支持的不好
#  个人观点: 还是使用time换算length的方式, 数据稍微多些, 然后做日期截取
#
#  get_k_data 底层还是调用的 get_security_bar_data
#  循环10次返回8000条数据, 然后用日期 index 去截取
#  还有一种方法是通过交易日历去获取length, 然后循环拼接
########################################################


def mootdx_method(symbol, frequency, offset, start, market):
    '''
    mootdx 这里没有完善
    '''

    # quotes = Quotes.factory(market='std')
    #
    # df = quotes.get_k_data(
    #     code, start_date, end_date
    # )
    #
    # quotes.close()
    print(1)


def pytdx_method(symbol, start_date, end_date):
    from jotdx.hq import TdxHq_API
    from jotdx.utils.best_ip_async import select_best_ip_async

    ip_port_dict = select_best_ip_async(_type="stock")
    ip = ip_port_dict['ip']
    port = ip_port_dict['port']

    api = TdxHq_API()
    with api.connect(ip=ip, port=port):
        df5 = api.to_df(
            api.get_k_data(
                code=symbol, start_date=start_date, end_date=end_date
            )
        )

        print(1)


def std_bars_test():
    # 也可以使用
    # frequency = TDXParams.KLINE_TYPE_15MIN
    frequency = INTERVAL_TDX_MAP[Interval.MINUTE_15]

    symbol = "123075"
    market = get_stock_market(symbol=symbol)

    start_date = "2022-06-03"
    end_date = "2022-07-05"

    pytdx_method(symbol=symbol, start_date=start_date, end_date=end_date)


if __name__ == '__main__':
    std_bars_test()
