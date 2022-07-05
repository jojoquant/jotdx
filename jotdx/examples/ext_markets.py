from jotdx.quotes import Quotes


def mootdx_method():
    quotes = Quotes.factory(market='ext')

    df = quotes.markets()

    quotes.close()
    print(1)


def pytdx_method():
    from jotdx.exhq import TdxExHq_API
    from jotdx.utils.best_ip_async import select_best_ip_async

    ip_port_dict = select_best_ip_async(_type="future")
    ip = ip_port_dict['ip']
    port = ip_port_dict['port']

    api = TdxExHq_API()
    with api.connect(ip=ip, port=port):

        df5 = api.to_df(
            api.get_markets()
        )

        print(1)


def ext_markets_test():


    mootdx_method()
    pytdx_method()


if __name__ == '__main__':
    ext_markets_test()
