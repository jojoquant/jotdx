# coding=utf-8
import datetime

from jotdx.parser.base import BaseParser
from jotdx.helper import get_datetime
from collections import OrderedDict
import six
import struct

from joconst import TdxMarket
from joconst.object import BarData
from joconst.maps import TDX_JONPY_MARKET_MAP, TDX_INTERVAL_MAP

from jotdx.parser.gateway import GATEWAY_NAME


def gen_datetime(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    datetime_value = datetime.datetime(year, month, day, hour, minute)
    # datetime_value.weekday() , 0 代表 星期一 ... 6 代表星期日
    # if datetime_value.weekday() == 0:
    #     datetime_value -= datetime.timedelta(days=3)

    pm = 18
    if datetime_value.weekday() == 0:
        if 0 <= hour <= 8:
            datetime_value -= datetime.timedelta(days=2)
        elif pm < hour:
            datetime_value -= datetime.timedelta(days=3)
    else:
        if pm < hour:
            datetime_value -= datetime.timedelta(days=1)

    return datetime_value


class GetInstrumentBars(BaseParser):
    # ﻿ff232f49464c30007401a9130400010000000000f000
    """

    first：

    ﻿0000   01 01 08 6a 01 01 16 00 16 00                    ...j......


    second：
    ﻿0000   ff 23 2f 49 46 4c 30 00 74 01 a9 13 04 00 01 00  .#/IFL0.t.......
    0010   00 00 00 00 f0 00                                ......

    ﻿0000   ff 23 28 42 41 42 41 00 00 00 a9 13 04 00 01 00  .#(BABA.........
    0010   00 00 00 00 f0 00                                ......

    ﻿0000   ff 23 28 42 41 42 41 00 00 00 a9 13 03 00 01 00  .#(BABA.........
    0010   00 00 00 00 f0 00                                ......

    ﻿0000   ff 23 08 31 30 30 30 30 38 34 33 13 04 00 01 00  .#.10000843.....
    0010   00 00 00 00 f0 00                                ......
    """

    def setup(self):
        pass
        # self.client.send(bytearray.fromhex('01 01 08 6a 01 01 16 00 16 00'))

    def setParams(self, category, market, code, start, count):

        self.category = category
        self.market = market
        self.code = code

        if type(code) is six.text_type:
            code = code.encode("utf-8")

        pkg = bytearray.fromhex('01 01 08 6a 01 01 16 00 16 00')
        pkg.extend(bytearray.fromhex("ff 23"))

        # pkg = bytearray.fromhex("ff 23")

        # count
        last_value = 0x00f00000
        pkg.extend(struct.pack('<B9sHHIH', market, code, category, 1, start, count))
        # 这个1还不确定是什么作用，疑似和是否复权有关
        self.send_pkg = pkg

    def parseResponse(self, body_buf):
        pos = 0

        # 算了，前面不解析了，没太大用
        # (market, code) = struct.unpack("<B9s", body_buf[0: 10])
        pos += 18
        (ret_count,) = struct.unpack('<H', body_buf[pos: pos + 2])
        pos += 2

        klines = []

        for i in range(ret_count):
            year, month, day, hour, minute, pos = get_datetime(self.category, body_buf, pos)
            (open_price, high, low, close, position, trade, price) = struct.unpack("<ffffIIf", body_buf[pos: pos + 28])
            (amount,) = struct.unpack("f", body_buf[pos + 16: pos + 16 + 4])

            pos += 28

            datetime_value = gen_datetime(year, month, day, hour, minute)
            if trade > 0:
                kline = OrderedDict([
                    ("open", open_price),
                    ("high", high),
                    ("low", low),
                    ("close", close),
                    ("position", position),
                    ("trade", trade),
                    ("price", price),
                    ("year", year),
                    ("month", month),
                    ("day", day),
                    ("hour", hour),
                    ("minute", minute),
                    ("datetime", datetime_value),
                    ("amount", amount),
                ])
            else:
                continue

            klines.append(kline)

        return klines


class GetInstrumentBarData(GetInstrumentBars):
    def parseResponse(self, body_buf):
        pos = 0

        # 算了，前面不解析了，没太大用
        # (market, code) = struct.unpack("<B9s", body_buf[0: 10])
        pos += 18
        (ret_count,) = struct.unpack('<H', body_buf[pos: pos + 2])
        pos += 2

        klines = []

        for i in range(ret_count):
            year, month, day, hour, minute, pos = get_datetime(self.category, body_buf, pos)
            (open_price, high, low, close, position, trade, price) = struct.unpack("<ffffIIf", body_buf[pos: pos + 28])
            # (amount,) = struct.unpack("f", body_buf[pos + 16: pos + 16 + 4])

            pos += 28

            datetime_value = gen_datetime(year, month, day, hour, minute)

            # 清理 volume 为 0 的 bar
            if trade > 0:
                bar_data = BarData(
                    gateway_name=GATEWAY_NAME,
                    symbol=self.code,
                    interval=TDX_INTERVAL_MAP[self.category],
                    exchange=TDX_JONPY_MARKET_MAP[self.market],
                    open_price=open_price, high_price=high, low_price=low, close_price=close,
                    volume=trade, open_interest=position,
                    datetime=datetime_value
                )
            else:
                continue

            klines.append(bar_data)

        return klines


if __name__ == '__main__':
    from jotdx.exhq import TdxExHq_API
    from jotdx.params import TDXParams

    api = TdxExHq_API()
    # cmd = GetInstrumentBars(api)
    # cmd.setParams(4, 7, "10000843", 0, 10)
    # print(cmd.send_pkg)
    with api.connect('59.175.238.38', 7727):
        # r1 = api.to_df(api.get_instrument_bars(TDXParams.KLINE_TYPE_EXHQ_1MIN, 74, 'BABA')).tail()
        # r2 = api.to_df(api.get_instrument_bars(TDXParams.KLINE_TYPE_DAILY, 31, '00001')).tail()
        # r3 = api.to_df(api.get_instrument_bars(TDXParams.KLINE_TYPE_5MIN, 30, 'AUL8'))

        r3 = api.get_instrument_bar_data(TDXParams.KLINE_TYPE_5MIN, 30, 'AUL8')
        r4 = api.get_instrument_bar_data(TDXParams.KLINE_TYPE_DAILY, 30, 'AUL8')
        print(1)
