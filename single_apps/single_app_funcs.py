"""
@author: Alex Hyer
https://github.com/alexhyer
"""
import requests
import time

def time_return():
    current_time = round(time.time())
    return current_time

def btc_price_return(last_price):
    btc_current_price_url = "https://capi.bitget.com/api/mix/v1/market/ticker?symbol=BTCUSDT_UMCBL"
    try:
        current_price_res = requests.get(btc_current_price_url)
    except:
        return last_price
    else:
        status = current_price_res.status_code
        if status == 200:
            current_price_data=current_price_res.json()
            btc_current_price = float(current_price_data['data']['last'])
            return btc_current_price
        else:
            return last_price
    
def define_messages(email,app_number,backtest_number):
    long_message = {
        "to": {
            "email": email
        },
        "content": {
            "title": "Single entry long alert",
            "body": "App number: "+str(app_number)+" Backtest number: "+str(backtest_number)
        },
    }
    short_message = {
        "to": {
            "email": email
        },
        "content": {
            "title": "Single entry short alert",
            "body": "App number: "+str(app_number)+" Backtest number: "+str(backtest_number)
        },
    }
    tp_message = {
        "to": {
            "email": email
        },
        "content": {
            "title": "Single entry TP hit",
            "body": "App number: "+str(app_number)+" Backtest number: "+str(backtest_number)
        },
    }
    sl_message = {
        "to": {
            "email": email
        },
        "content": {
            "title": "Single entry SL hit",
            "body": "App number: "+str(app_number)+" Backtest number: "+str(backtest_number)
        },
    }
    startup_error_message = {
        "to": {
            "email": email
        },
        "content": {
            "title": "Single entry startup error",
            "body": "App number: "+str(app_number)+" Backtest number: "+str(backtest_number)
        },
    }
    api_error_message = {
        "to": {
            "email": email
        },
        "content": {
            "title": "Single entry API error",
            "body": "App number: "+str(app_number)+" Backtest number: "+str(backtest_number)
        },
    }
    partial_error_message = {
        "to": {
            "email": email
        },
        "content": {
            "title": "Single entry partial entry error",
            "body": "App number: "+str(app_number)+" Backtest number: "+str(backtest_number)
        },
    }
    return long_message,short_message,tp_message,sl_message,startup_error_message,api_error_message,partial_error_message