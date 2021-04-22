
import time, json
from http_request import HttpRequest
from enum import Enum
from datetime import date, timedelta

class DogeLinks(Enum):

    all_by_day = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id=74&convert=USD&time_start=1000732800&time_end=1619049600"
    day_by_5_min = f"https://web-api.coinmarketcap.com/v1.1/cryptocurrency/quotes/historical?convert=USD,BTC&format=chart_crypto_details&id=74&interval=5m&time_end={int(time.time())}&time_start={int(time.time()) - 86400}"


    def get_pklename(self):
        date = time.strftime("%Y%m%d")
        if self == DogeLinks.all_by_day:
            return f"doge_all_till_{date}.pkl"
        if self == DogeLinks.day_by_5_min:
            return f"doge_by_5min_day_{date}.pkl"


    def get_json(self):

        http = HttpRequest()
        print(self.value)
        r = http.get(self.value)

        if self == DogeLinks.all_by_day:
            data_json = json.loads(r.text)["data"]["quotes"]
            for price in data_json:
                usd = price["quote"]["USD"]
                for price_detail in usd:
                    price[price_detail] = usd[price_detail]
                    # print('price_detail', price_detail)
                del price["quote"]
            
            return data_json
        if self == DogeLinks.day_by_5_min:
            data_json = json.loads(r.text)["data"]
            usd = None
            dates = []
            for price in data_json:
                # usd = data_json[price]['USD'][0]
                # data_json[price] = [usd]
                temp_list = []
                usd = data_json[price]['USD']
                data_json[price] = usd
                temp_list.append(price)
                temp_list.extend(usd)
                dates.append(temp_list)
            return dates
