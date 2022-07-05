from joconst.constant import TdxMarket, TdxCategory

from jotdx.quotes import Quotes

##########################################################################
# 该函数主要用于给 instruments 或者 get_instrument_info 的 for 循环一个总的范围 #
##########################################################################

def mootdx_method():
    quotes = Quotes.factory(market='ext')
    total_count = quotes.instrument_count()


def pytdx_method(market_name, category, market):

    # 结果为 int 87134, 总的 instrument 数目, 貌似基本没啥用
    total_count = api.get_instrument_count()

    print("=" * 100)


def ext_bars_test():
    # 只支持测试用例这里的交易所

    market_name = "SHFE"
    market = getattr(TdxMarket, market_name)  # TdxMarket.SHFE
    category = getattr(TdxCategory, market_name)  # TdxCategory.SHFE
    pytdx_method(market_name=market_name, category=category, market=market)


if __name__ == '__main__':
    from jotdx.exhq import TdxExHq_API
    from jotdx.utils.best_ip_async import select_best_ip_async

    ip_port_dict = select_best_ip_async(_type="future")
    ip = ip_port_dict['ip']
    port = ip_port_dict['port']

    api = TdxExHq_API()
    api.connect(ip=ip, port=port)
    ext_bars_test()
    api.close()
