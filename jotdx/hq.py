# coding=utf-8

#
# Just for practising
#


import datetime
import os
import random
import socket
import sys
import threading

import pandas as pd
from jotdx.base_socket_client import BaseSocketClient, update_last_ack_time
from jotdx.heartbeat import HqHeartBeatThread
from jotdx.log import DEBUG, log
from jotdx.params import TDXParams
from jotdx.parser.get_block_info import (GetBlockInfo, GetBlockInfoMeta,
                                         get_block_dat_ver_up, get_and_parse_block_info)
from jotdx.parser.get_company_info_category import GetCompanyInfoCategory
from jotdx.parser.get_company_info_content import GetCompanyInfoContent
from jotdx.parser.get_finance_info import GetFinanceInfo
from jotdx.parser.get_history_minute_time_data import GetHistoryMinuteTimeData
from jotdx.parser.get_history_transaction_data import GetHistoryTransactionData
from jotdx.parser.get_index_bars import GetIndexBarsCmd
from jotdx.parser.get_minute_time_data import GetMinuteTimeData
from jotdx.parser.get_security_bars import GetSecurityBarsCmd, GetSecurityBarDataCmd
from jotdx.parser.get_security_count import GetSecurityCountCmd
from jotdx.parser.get_security_list import GetSecurityList
from jotdx.parser.get_security_quotes import GetSecurityQuotesCmd, GetSecurityTickDataCmd
from jotdx.parser.get_transaction_data import GetTransactionData
from jotdx.parser.get_xdxr_info import GetXdXrInfo
from jotdx.parser.setup_commands import SetupCmd1, SetupCmd2, SetupCmd3

if __name__ == '__main__':
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))


class TdxHq_API(BaseSocketClient):

    def setup(self):
        SetupCmd1(self.client).call_api()
        SetupCmd2(self.client).call_api()
        SetupCmd3(self.client).call_api()

    # API List

    # Notice：，如果一个股票当天停牌，那天的K线还是能取到，成交量为0
    @update_last_ack_time
    def get_security_bars(self, category, market, code, start, count):
        '''
        count max is 800, beyond it will get none
        '''
        cmd = GetSecurityBarsCmd(self.client, lock=self.lock)
        cmd.setParams(category, market, code, start, count)
        return cmd.call_api()

    @update_last_ack_time
    def get_security_bar_data(self, category, market, code, start, count):
        ''' fangyang
        获取 veighna 中的 BarData 类型的 list
        count max is 800, beyond it will get none
        '''
        cmd = GetSecurityBarDataCmd(self.client, lock=self.lock)
        cmd.setParams(category, market, code, start, count)
        return cmd.call_api()

    @update_last_ack_time
    def get_index_bars(self, category, market, code, start, count):
        cmd = GetIndexBarsCmd(self.client, lock=self.lock)
        cmd.setParams(category, market, code, start, count)
        return cmd.call_api()

    @update_last_ack_time
    def get_security_quotes(self, all_stock):
        cmd = GetSecurityQuotesCmd(self.client, lock=self.lock)
        cmd.setParams(all_stock)
        return cmd.call_api()

    @update_last_ack_time
    def get_security_tick_data(self, all_stock):
        cmd = GetSecurityTickDataCmd(self.client, lock=self.lock)
        cmd.setParams(all_stock)
        return cmd.call_api()

    @update_last_ack_time
    def get_security_count(self, market):
        cmd = GetSecurityCountCmd(self.client, lock=self.lock)
        cmd.setParams(market)
        return cmd.call_api()

    @update_last_ack_time
    def get_security_list(self, market, start):
        cmd = GetSecurityList(self.client, lock=self.lock)
        cmd.setParams(market, start)
        return cmd.call_api()

    @update_last_ack_time
    def get_minute_time_data(self, market, code):
        cmd = GetMinuteTimeData(self.client, lock=self.lock)
        cmd.setParams(market, code)
        return cmd.call_api()

    @update_last_ack_time
    def get_history_minute_time_data(self, market, code, date):
        cmd = GetHistoryMinuteTimeData(self.client, lock=self.lock)
        cmd.setParams(market, code, date)
        return cmd.call_api()

    @update_last_ack_time
    def get_transaction_data(self, market, code, start, count):
        cmd = GetTransactionData(self.client, lock=self.lock)
        cmd.setParams(market, code, start, count)
        return cmd.call_api()

    @update_last_ack_time
    def get_history_transaction_data(self, market, code, start, count, date):
        cmd = GetHistoryTransactionData(self.client, lock=self.lock)
        cmd.setParams(market, code, start, count, date)
        return cmd.call_api()

    @update_last_ack_time
    def get_company_info_category(self, market, code):
        cmd = GetCompanyInfoCategory(self.client, lock=self.lock)
        cmd.setParams(market, code)
        return cmd.call_api()

    @update_last_ack_time
    def get_company_info_content(self, market, code, filename, start, length):
        cmd = GetCompanyInfoContent(self.client, lock=self.lock)
        cmd.setParams(market, code, filename, start, length)
        return cmd.call_api()

    @update_last_ack_time
    def get_xdxr_info(self, market, code):
        cmd = GetXdXrInfo(self.client, lock=self.lock)
        cmd.setParams(market, code)
        return cmd.call_api()

    @update_last_ack_time
    def get_finance_info(self, market, code):
        cmd = GetFinanceInfo(self.client, lock=self.lock)
        cmd.setParams(market, code)
        return cmd.call_api()

    @update_last_ack_time
    def get_block_info_meta(self, blockfile):
        cmd = GetBlockInfoMeta(self.client, lock=self.lock)
        cmd.setParams(blockfile)
        return cmd.call_api()

    @update_last_ack_time
    def get_block_info(self, blockfile, start, size):
        cmd = GetBlockInfo(self.client, lock=self.lock)
        cmd.setParams(blockfile, start, size)
        return cmd.call_api()

    def get_block_dat_ver_up(self, blockfile):
        return get_block_dat_ver_up(self, blockfile)

    def get_and_parse_block_info(self, blockfile):
        return get_and_parse_block_info(self, blockfile)

    def do_heartbeat(self):
        self.get_security_count(random.randint(0, 1))

    def get_k_data(self, code, start_date, end_date):
        # 具体详情参见 https://github.com/rainx/pytdx/issues/5
        # 具体详情参见 https://github.com/rainx/pytdx/issues/21
        def __select_market_code(code):
            code = str(code)
            if code[0] in ['5', '6', '9'] or code[:3] in ["009", "126", "110", "201", "202", "203", "204"]:
                return 1
            return 0

        # 新版一劳永逸偷懒写法zzz
        market_code = 1 if str(code)[0] == '6' else 0
        # https://github.com/rainx/pytdx/issues/33
        # 0 - 深圳， 1 - 上海

        data = pd.concat([self.to_df(self.get_security_bars(9, __select_market_code(
            code), code, (9 - i) * 800, 800)) for i in range(10)], axis=0)

        data = data.assign(date=data['datetime'].apply(lambda x: str(x)[0:10])).assign(code=str(code)) \
                   .set_index('date', drop=False, inplace=False) \
                   .drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1)[start_date:end_date]
        return data.assign(date=data['date'].apply(lambda x: str(x)[0:10]))


if __name__ == '__main__':
    import pprint

    api = TdxHq_API()
    if api.connect('101.227.73.20', 7709):
        log.info("获取股票行情")
        #         stocks = api.get_security_quotes([(0, "000001"), (1, "600300")])
        #         stocks = api.to_df(stocks)
        #         pprint.pprint(stocks)
        #         log.info("获取k线")
        #         data = api.get_security_bars(9, 0, '000001', 4, 3)
        #         pprint.pprint(data)
        #         log.info("获取 深市 股票数量")
        #         pprint.pprint(api.get_security_count(0))
        #         log.info("获取股票列表")
        #         stocks = api.get_security_list(1, 255)
        #         pprint.pprint(stocks)
        #         log.info("获取指数k线")
        #         data = api.get_index_bars(9, 1, '000001', 1, 2)
        #         pprint.pprint(data)
        #         log.info("查询分时行情")
        #         data = api.get_minute_time_data(TDXParams.MARKET_SH, '600300')
        #         pprint.pprint(api.to_df(data))
        #         log.info("查询历史分时行情")
        #         data = api.get_history_minute_time_data(
        #             TDXParams.MARKET_SH, '600300', 20161209)
        #         pprint.pprint(data)
        #         log.info("查询分时成交")
        data = api.get_transaction_data(TDXParams.MARKET_SZ, '000001', 0, 300)
        pprint.pprint(data)
        #         log.info("查询历史分时成交")
        #         data = api.get_history_transaction_data(
        #             TDXParams.MARKET_SZ, '000001', 0, 10, 20170209)
        #         pprint.pprint(data)
        #         log.info("查询公司信息目录")
        #         data = api.get_company_info_category(TDXParams.MARKET_SZ, '000001')
        #         pprint.pprint(data)
        #         log.info("读取公司信息-最新提示")
        #         data = api.get_company_info_content(0, '000001', '000001.txt', 0, 9441)
        #         pprint.pprint(data)
        #         log.info("读取除权除息信息")
        #         data = api.get_xdxr_info(1, '600300')
        #         pprint.pprint(data)
        #         log.info("读取财务信息")
        #         data = api.get_finance_info(0, '000001')
        #         data = api.to_df(data)
        #         pprint.pprint(data)
        #         log.info("日线级别k线获取函数")
        #         data = api.get_k_data('000001', '2017-07-01', '2017-07-10')
        #         pprint.pprint(data)

        api.disconnect()
