from huobi.client.market import MarketClient
from huobi.utils import *
market_client = MarketClient()
list_obj = market_client.get_history_trade("btcusdt", 1000)
LogInfo.output_list(list_obj)