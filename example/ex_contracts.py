from joconst.constant import TdxMarket, TdxCategory

def ext_contracts_pytdx_test():
    from jotdx.exhq import TdxExHq_API
    api = TdxExHq_API()
    # 59.175.238.38 : 7727
    with api.connect('59.175.238.38', 7727):
        df1 = api.to_df(api.get_markets())
        # df2 = api.to_df(api.get_instrument_info(0, 800))
        df3 = api.to_df(api.get_instrument_quote_list(TdxMarket.SHFE, TdxCategory.SHFE, count=100))
        df4 = api.to_df(api.get_instrument_quote_list(30, 3, start=100, count=100))
        df5 = api.to_df(api.get_instrument_quote_list(31, 2, start=0, count=100))
        print(2)


if __name__ == '__main__':
    ext_contracts_pytdx_test()