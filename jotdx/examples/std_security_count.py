
from joconst.constant import TdxMarket
from jotdx.quotes import Quotes

###############################################################
# 该函数主要用于给 stocks 或者 security_list 的 for 循环一个总的范围 #
###############################################################
#
# bse_count 有的 ip 节点有结果 106, 有的节点显示为 0
#
###############################################################


def mootdx_method():
    quotes = Quotes.factory(market='std')

    szse_count = quotes.stock_count(market=0)  # 15549
    sse_count = quotes.stock_count(market=1)   # 20123
    bse_count = quotes.stock_count(market=2)   # 106

    # 股票 api 请求期货数据, 返回全是 None
    # dce_count = quotes.stock_count(market=TdxMarket.DCE)
    # shfe_count = quotes.stock_count(market=TdxMarket.SHFE)
    # cffex_count = quotes.stock_count(market=TdxMarket.CFFEX)
    # czce_count = quotes.stock_count(market=TdxMarket.CZCE)
    # hkse_count = quotes.stock_count(market=TdxMarket.HKSE)

    quotes.close()
    print(1)


def pytdx_method():
    from jotdx.hq import TdxHq_API
    from jotdx.utils.best_ip_async import select_best_ip_async

    ip_port_dict = select_best_ip_async(_type="stock")
    ip = ip_port_dict['ip']
    port = ip_port_dict['port']

    api = TdxHq_API()
    with api.connect(ip=ip, port=port):

        sse_count = api.get_security_count(market=TdxMarket.SSE)   # 20123
        szse_count = api.get_security_count(market=TdxMarket.SZSE)  # 15549
        bse_count = api.get_security_count(market=TdxMarket.BSE)   # 106
        print(1)


def std_bars_test():

    mootdx_method()
    pytdx_method()


if __name__ == '__main__':
    std_bars_test()
