

import re
from huobi.client.market import MarketClient
from huobi.model.market import *
import requests, urllib

upperbound = 0.15
lowerbound = -0.15

# ios: https://api.day.app/nwsrJuWCNoh3XKgogVv8tQ/Customed Notification Content

pushes = ['nwsrJuWCNoh3XKgogVv8tQ', 'gkeS97H7xBtPvraCC46pee']

def callback(obj_event: 'MarketDetailEvent'):
    # obj_event.print_object()
    # obj_event.tick.print_object()
    tick = obj_event.tick
    # from huobi.utils.print_mix_object import PrintBasic
    # format_data=""
    # PrintBasic.print_basic(tick.id, format_data + "ID")
    # PrintBasic.print_basic(tick.open, format_data + "Open")
    # PrintBasic.print_basic(tick.close, format_data + "Close")

    range = (tick.close - tick.open) / tick.open
    
    range_str = '{:.2%}'.format(range)
    msg = f"range:{range_str},open:{tick.open},close:{tick.close}" 
    if range > upperbound or range < lowerbound:
        title = ""
        if range > upperbound:
            title = f"up{range_str}"

        else:
            title = f"down{range_str}"

        for push in pushes:       
            url = f"https://api.day.app/{push}/{title}/{msg}"
            # url = urllib.parse.quote(url)
            url = url.replace('%', '%25')
            print(url)
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
        # requests.get(url)
    print(msg)
    print()

market_client = MarketClient(init_log=True, url="https://api.huobiasia.vip")
market_client.sub_market_detail("filusdt", callback)
