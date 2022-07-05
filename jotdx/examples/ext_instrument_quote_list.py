from joconst.constant import TdxMarket, TdxCategory


def mootdx_method():
    pass


def pytdx_method(market_name, category, market):
    quote_list = []
    start = 0
    count = 100
    while True:
        temp_list = api.get_instrument_quote_list(
            market=market, category=category, start=start, count=count
        )  # count max is 100

        if not temp_list:
            break

        quote_list += temp_list
        start += count
        print(f"[{market_name}] get_instrument_quote_list length: {len(quote_list)}", flush=True)

    df3 = api.to_df(quote_list)

    print("=" * 100)


def ext_bars_test():
    # 只支持测试用例这里的交易所

    market_name = "SHFE"
    market = getattr(TdxMarket, market_name)  # TdxMarket.SHFE
    category = getattr(TdxCategory, market_name)  # TdxCategory.SHFE
    pytdx_method(market_name=market_name, category=category, market=market)

    market_name = "DCE"
    market = getattr(TdxMarket, market_name)
    category = getattr(TdxCategory, market_name)
    pytdx_method(market_name=market_name, category=category, market=market)

    market_name = "CZCE"
    market = getattr(TdxMarket, market_name)
    category = getattr(TdxCategory, market_name)
    pytdx_method(market_name=market_name, category=category, market=market)

    market_name = "CFFEX"
    market = getattr(TdxMarket, market_name)
    category = getattr(TdxCategory, market_name)
    pytdx_method(market_name=market_name, category=category, market=market)

    market_name = "HKSE"
    market = getattr(TdxMarket, market_name)
    category = getattr(TdxCategory, market_name)
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
