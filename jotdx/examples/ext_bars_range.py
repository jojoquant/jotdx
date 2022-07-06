from joconst.maps import INTERVAL_TDX_MAP
from joconst.object import Interval
from joconst.constant import TdxMarket


##############################################################
# 暂时没有太高的实用价值
# 根据日期区间返回期货数据, 但是数据会缺失, 只能返回1500条 1min bar,
# 而且不能选择数据周期
##############################################################

def pytdx_method(symbol, market, start, end):
    from jotdx.exhq import TdxExHq_API
    from jotdx.utils.best_ip_async import select_best_ip_async

    ip_port_dict = select_best_ip_async(_type="future")
    ip = ip_port_dict['ip']
    port = ip_port_dict['port']

    api = TdxExHq_API()
    with api.connect(ip=ip, port=port):

        df5 = api.to_df(
            api.get_history_instrument_bars_range(
                market=market, code=symbol, start=start, end=end
            )
        )
        print(1)


def ext_bars_test():
    # 也可以使用
    # frequency = TDXParams.KLINE_TYPE_15MIN
    frequency = INTERVAL_TDX_MAP[Interval.MINUTE]

    symbol = "RBL8"
    market = TdxMarket.SHFE

    start = 20220303
    end = 20220705

    pytdx_method(symbol=symbol, market=market, start=start, end=end)


if __name__ == '__main__':
    ext_bars_test()
