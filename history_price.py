from huobi.client.market import MarketClient
from huobi.constant import *
from huobi.exception.huobi_api_exception import HuobiApiException
from datetime import datetime
from huobi.utils.print_mix_object import PrintBasic

def callback(candlestick_req: 'CandlestickReq'):
    # candlestick_req.print_object()
    
    ts = datetime.utcfromtimestamp(int(candlestick_req.id) // 1000).strftime('%Y-%m-%d %H:%M:%S')
    # print('---', datetime.fromtimestamp(int(candlestick_req.id)))
    
    PrintBasic.print_basic(candlestick_req.rep, "Channel")
    PrintBasic.print_basic(ts, "Unix Time")
    print()
    print(len(candlestick_req.data))
    
    
    # last_row = candlestick_req.data[-1]
    if len(candlestick_req.data):
        for last_row in candlestick_req.data:
            ts = datetime.utcfromtimestamp(int(last_row.id)).strftime('%Y-%m-%d %H:%M:%S')
            print(candlestick_req.id, last_row.id)
            PrintBasic.print_basic(ts,  "Id")
            # PrintBasic.print_basic(last_row.timestamp,  "Unix Time")
            PrintBasic.print_basic(last_row.high,  "High")
            PrintBasic.print_basic(last_row.low,  "Low")
            PrintBasic.print_basic(last_row.open, "Open")
            PrintBasic.print_basic(last_row.close, "Close")
            PrintBasic.print_basic(last_row.count, "Count")
            PrintBasic.print_basic(last_row.amount, "Amount")
            PrintBasic.print_basic(last_row.vol, "Volume")
            print()
    
    # if len(candlestick_req.data):
    #     for row in candlestick_req.data:
    #         row.print_object()
    #         print()

def error(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)


# class CandlestickInterval:
#     MIN1 = "1min"
#     MIN5 = "5min"
#     MIN15 = "15min"
#     MIN30 = "30min"
#     MIN60 = "60min"
#     HOUR4 = "4hour"
#     DAY1 = "1day"
#     MON1 = "1mon"
#     WEEK1 = "1week"
#     YEAR1 = "1year"
#     INVALID = None


sub_client = MarketClient(init_log=True, url="https://api.huobiasia.vip")
#sub_client.request_candlestick_event("btcusdt", CandlestickInterval.MIN1, callback, from_ts_second=None, end_ts_second=None, error_handler=None)
#sub_client.request_candlestick_event("btcusdt", CandlestickInterval.MIN1, callback, from_ts_second=1571124360, end_ts_second=1571129820)
#sub_client.request_candlestick_event("btcusdt", CandlestickInterval.MIN1, callback, from_ts_second=1569361140, end_ts_second=0)
#sub_client.request_candlestick_event("btcusdt", CandlestickInterval.MIN1, callback, from_ts_second=1569379980)
list=sub_client.req_candlestick("filusdt", CandlestickInterval.MIN30, callback)


# sub_client.get_market_trade(symbol="filusdt")


# print(list)