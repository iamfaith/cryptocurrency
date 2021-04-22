import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import numpy as np
import json
from http_request import HttpRequest
import time
from links import DogeLinks


# # get market info for bitcoin from the start of 2016 to the current day
# # bitcoin_market_info = pd.read_html("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end="+time.strftime("%Y%m%d"))[2]

# link = "https://coinmarketcap.com/currencies/dogecoin/historical-data/?start=20130428&end="+time.strftime("%Y%m%d")

# driver.get(link)

# df=pd.read_html(driver.find_element_by_tagname("history_table").get_attribute('outerHTML'))[0]

# print(link)
# dogecoin_market_info = pd.read_html(link)
# print(dogecoin_market_info)


# url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id=74&convert=USD&time_start=1000732800&time_end=1619049600"

# url = f"https://web-api.coinmarketcap.com/v1.1/cryptocurrency/quotes/historical?convert=USD,BTC&format=chart_crypto_details&id=74&interval=5m&time_end={int(time.time())}&time_start=1618991900"


dogeLink = DogeLinks.day_by_5_min

data_json = dogeLink.get_json()

# print(data_json)
df = pd.read_json(json.dumps(data_json))
# print(r.text)
# df.sort_values(by=['Date'])
print(df.shape)
df.to_pickle(dogeLink.get_pklename())