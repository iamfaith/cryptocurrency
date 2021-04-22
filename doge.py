import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import numpy as np

# get market info for bitcoin from the start of 2016 to the current day
# bitcoin_market_info = pd.read_html("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end="+time.strftime("%Y%m%d"))[2]


dogecoin_market_info = pd.read_html("https://coinmarketcap.com/currencies/dogecoin/historical-data/?start=20130428&end="+time.strftime("%Y%m%d"))[2]
print(dogecoin_market_info)
