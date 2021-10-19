# coding=utf-8
from __future__ import unicode_literals, division

import datetime

import pandas as pd
import os

import struct
from jotdx.reader.base_reader import TdxFileNotFoundException
from jotdx.reader.base_reader import BaseReader

"""
读取通达信数据
"""


class TdxExHqDailyBarReader(BaseReader):

    def __init__(self, vipdoc_path=None):
        self.vipdoc_path = vipdoc_path

    def parse_data_by_file(self, fname):
        if not os.path.isfile(fname):
            raise TdxFileNotFoundException('no tdx kline data, pleaes check path %s', fname)

        with open(fname, 'rb') as f:
            content = f.read()
            return self.unpack_records('<hhffffIIf', content)

        return []

    def get_df(self, code_or_file):
        # 只传入了一个参数
        data = [self._df_convert(row) for row in self.parse_data_by_file(code_or_file)]

        df = pd.DataFrame(data=data, columns=(
            'date', 'open', 'high', 'low', 'close', 'amount', 'volume', 'jiesuan', 'hk_stock_amount'))
        # df.index = pd.to_datetime(df.date)
        return df

    def _df_convert(self, row):
        t_date = row[0]
        year = int(t_date / 2048 + 2036)
        month = int(t_date % 2048 / 100)
        day = t_date % 2048 % 100

        t_time = row[1]
        hour = int(t_time / 60)
        min = t_time % 60

        datetimep = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=min)

        offset = 1
        (hk_stock_amount,) = struct.unpack('<f', struct.pack('<I', row[5 + offset]))
        new_row = (
            datetimep,
            row[1 + offset],
            row[2 + offset],
            row[3 + offset],
            row[4 + offset],
            row[5 + offset],
            row[6 + offset],
            row[7 + offset],
            hk_stock_amount
        )

        return new_row


if __name__ == '__main__':
    tdx_reader = TdxExHqDailyBarReader()
    try:
        print(tdx_reader.get_df("/Users/rainx/tmp/vipdoc/ds/29#A1801.day"))
        # print(tdx_reader.get_df("/Volumes/share/transfer/76#AG200.day"))

    except TdxFileNotFoundException as e:
        pass
