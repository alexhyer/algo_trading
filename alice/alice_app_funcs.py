"""
@author: Alex Hyer
https://github.com/alexhyer
"""
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
import time

session = requests.Session()
retry = Retry(connect=4, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def time_return():
  current_time = round(time.time())
  return current_time

def btc_price_return(last_price):
    btc_current_price_url = "https://capi.bitget.com/api/mix/v1/market/ticker?symbol=BTCUSDT_UMCBL"
    current_price_res = session.get(btc_current_price_url)  
    status = current_price_res.status_code
    if status == 200:
        current_price_data=current_price_res.json()
        btc_current_price = float(current_price_data['data']['last'])
        return btc_current_price
    else:
        return last_price