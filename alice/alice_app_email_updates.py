"""
@author: Alex Hyer
https://github.com/alexhyer
"""
import bitget.mix.account_api as accounts
import bitget.mix.order_api as order
from alice_app_funcs import btc_price_return
from alice_app_funcs import time_return
from trycourier import Courier
from bs4 import BeautifulSoup
import requests
import pickle
import math
import time

email = ""
client = Courier(auth_token="")

prices_url = "https://github.com/alexhyer/alice/blob/main/BTC_Data.txt"
symbol = "BTCUSDT_UMCBL"

long_message = {
    "to": {
        "email": email
    },
    "content": {
        "title": "Long Alert!",
        "body": "Long at current price"
    },
}
short_message = {
    "to": {
        "email": email
    },
    "content": {
        "title": "Short Alert!",
        "body": "Short at current price"
    },
}
close_message = {
    "to": {
        "email": email
    },
    "content": {
        "title": "Close Trade!",
        "body": "Close at current price"
    },
}
error_message = {
    "to": {
        "email": email
    },
    "content": {
        "title": "Timing error!",
        "body": "Bruh moment"
    },
}

api_key = ""
secret_key = ""
passphrase = ""

restart = 0 #read price data from github

be_tolerance = 0.05 #0.05
trade_fee = 0.06 #0.06

lev = 0 #1=minimum risk - 10=max risk recomended - choose at your own risk
trade_alerts = 0  #If 0 only error alerts will send, no trade updates

take_profit_toggle = 0 #1 to turn on tp level
take_profit_level = 1.85 #1.85
take_profit_amount = 20 #20

ma_1 = 232 #232
ma_2 = 116 #116
derive_rate = 9 #9
slope_1_open_threshold = 2.19 #2.19
slope_2_open_threshold = 3.02 #3.02
z0_1 = 0 #0
z0_2 = 2.98 #2.98
z1_1 = -1 #-1
z1_2 = -1.3 #-1.3
z2_1 = 0 #0
z2_2 = 0 #0
z3_1 = -2 #-2
z3_2 = -3.7 #-3.7
z4_1 = -3 #-3
z4_2 = -3.35 #-3.35
z_1 = 0.16 #0.16
z_2 = 1.47 #1.47
z_3 = 2.26 #2.26
z_4 = 2.94 #2.94
win_wait_time = 3770 #3770 #In sec not mins
be_wait_time = 5030 #5030
lose_wait_time = 4490 #4490
stop_loss = 0.16 #0.16
trailing_stop = 5 #5
percent_in_profit = 1.8 #1.8
move_stop = 1.17 #1.17


with open("alice/alice_app_data.pickle", "rb") as f:
    state = pickle.load(f)
    current_time = state["current_time"]
    current_price = state["current_price"]
    major_error = state["major_error"]
    timing_error = state["timing_error"]
    open_trade = state["open_trade"]
    last_check = state["last_check"]
    price_list = state["price_list"]
    slow_ma = state["slow_ma"]
    fast_ma = state["fast_ma"]
    long = state["long"]
    short = state["short"]
    tp_price = state["tp_price"]
    position_size = state["position_size"]
    tp_position_size = state["tp_position_size"]
    rest_position_size = state["rest_position_size"]
    open_price = state["open_price"]
    max_trade_price = state["max_trade_price"]
    secure_profit_price = state["secure_profit_price"]
    max_percent = state["max_percent"]
    time_check = state["time_check"]
    be_secured = state["be_secured"]
    profit_secured = state["profit_secured"]
    last_win_time = state["last_win_time"]
    last_be_time = state["last_be_time"]
    last_lose_time = state["last_lose_time"]
    open_time = state["open_time"]
  

while major_error == 0:
    current_time = time_return()
    current_price = btc_price_return(current_price)

    if restart==1 or timing_error==1:
        req = requests.get(prices_url)
        soup = BeautifulSoup(req.text, "html.parser")
        data = soup.find_all("td", class_="blob-code blob-code-inner js-file-line")
        unix_sheet = []
        open_price_sheet = []
        time_diff = []

        for x in range(ma_1+derive_rate):
            string = data[x].text
            row = list(string.split("\t"))
            unix_sheet.append(int(row[1]))
            open_price_sheet.append(float(row[3]))#Running on close rn
            last_time = unix_sheet[-1]
            if x>0:
                time_diff.append(abs(unix_sheet[-2]-last_time-60))
        open_price_sheet.reverse()
        if sum(time_diff)>360 or current_time-unix_sheet[0]>69:
            print(sum(time_diff), current_time-unix_sheet[0])
            major_error=1
            resp = client.send_message(error_message)
            state.update(major_error=major_error)
            with open("alice/alice_app_data.pickle", "wb") as f:
                pickle.dump(state, f)
            break
        else:
            restart = 0
            timing_error = 0

        slow_ma = []
        fast_ma = []
        cut_at_1 = int(ma_1 / 2)
        cut_at_2 = int(ma_2 / 2)
        price_list = open_price_sheet[-int(ma_1):]
        last_check = math.ceil(current_time/60)*60-60
        for x in range(derive_rate):
            first_half_1 = open_price_sheet[x:cut_at_1+x]
            second_half_1 = open_price_sheet[cut_at_1+x:ma_1+x]
            first_half_2 = open_price_sheet[(ma_1-ma_2)+x:(ma_1-ma_2)+cut_at_2+x]
            second_half_2 = open_price_sheet[(ma_1-ma_2)+cut_at_2+x:ma_1+x]
            slow_ma.append(((sum(first_half_1) / 1.5) + (sum(second_half_1) / 0.75)) / ma_1)
            fast_ma.append(((sum(first_half_2) / 1.5) + (sum(second_half_2) / 0.75)) / ma_2)

    if current_time - last_check >= 60:
        accountApi = accounts.AccountApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
        orderApi = order.OrderApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
        time_check = current_time - last_check
        print(time_check, flush=True)
        if (time_check > 73) or (time_check < 58):
            timing_error = 1
            state.update(timing_error=timing_error)
            with open("alice/alice_app_data.pickle", "wb") as f:
                pickle.dump(state, f)
            break
        last_check = last_check + 60
        price_list.append(current_price)
        price_list.pop(0)
        cut_at_1 = int(ma_1 / 2)
        cut_at_2 = int(ma_2 / 2)
        first_half_1 = price_list[:cut_at_1]
        second_half_1 = price_list[cut_at_1:]
        first_half_2 = price_list[ma_1-ma_2:ma_1-cut_at_2]
        second_half_2 = price_list[ma_1-cut_at_2:]

        slow_ma.append(((sum(first_half_1) / 1.5) + (sum(second_half_1) / 0.75)) / ma_1)
        fast_ma.append(((sum(first_half_2) / 1.5) + (sum(second_half_2) / 0.75)) / ma_2)
        slow_ma.pop(0)
        fast_ma.pop(0)

        slow_slope = (slow_ma[-1] - slow_ma[0]) / derive_rate
        fast_slope = (fast_ma[-1] - fast_ma[0]) / derive_rate

        if open_trade == 0:
            print("Open at +/-", slope_1_open_threshold, ":", round(slow_slope, 3), flush=True)
            print("Open at +/-", slope_2_open_threshold, ":", round(fast_slope, 3), flush=True)

            if (fast_slope>=slope_2_open_threshold)and(slow_slope>=slope_1_open_threshold)and(last_win_time+win_wait_time<=current_time)and(last_be_time+be_wait_time<=current_time)and (last_lose_time+lose_wait_time<=current_time):  #Open long
                accountApi.leverage(symbol, marginCoin='USDT', leverage=lev)
                open_price = current_price
                hard_stop_price = math.floor(open_price*(1 - (stop_loss / 100)))
                account_data = accountApi.account(symbol, marginCoin='USDT')
                raw_pos_size = float(account_data['data']['btcEquity'])
                temp_pos_size = (raw_pos_size*lev)-(raw_pos_size*lev*0.042)
                position_size = float(f'{temp_pos_size:.4f}')
                tp_position_size = (position_size/100)*take_profit_amount
                rest_position_size = position_size-tp_position_size
                orderApi.place_order(symbol, marginCoin='USDT', size=position_size, side='open_long', orderType='market', timeInForceValue='normal', presetStopLossPrice=hard_stop_price)
                open_trade = 1
                long = 1
                open_time = current_time
                max_trade_price = open_price
                max_percent = 0
                secure_profit_price = open_price/2
                if trade_alerts==1:
                    resp = client.send_message(long_message)

            elif (fast_slope<=-slope_2_open_threshold)and(slow_slope<=-slope_1_open_threshold)and(last_win_time+win_wait_time<=current_time)and(last_be_time+be_wait_time<=current_time)and (last_lose_time+lose_wait_time<=current_time):  #Open short
                accountApi.leverage(symbol, marginCoin='USDT', leverage=lev)
                open_price = current_price
                hard_stop_price = math.ceil(open_price*(1 - (stop_loss / -100)))
                account_data = accountApi.account(symbol, marginCoin='USDT')
                raw_pos_size = float(account_data['data']['btcEquity'])
                temp_pos_size = (raw_pos_size*lev)-(raw_pos_size*lev*0.042)
                position_size = float(f'{temp_pos_size:.4f}')
                tp_position_size = (position_size/100)*take_profit_amount
                rest_position_size = position_size-tp_position_size
                orderApi.place_order(symbol, marginCoin='USDT', size=position_size, side='open_short', orderType='market', timeInForceValue='normal', presetStopLossPrice=hard_stop_price)
                open_trade = 1
                short = 1
                open_time = current_time
                max_trade_price = open_price
                max_percent = 0
                secure_profit_price = open_price*2
                if trade_alerts==1:
                    resp = client.send_message(short_message)

        if open_trade == 1:  #When trade is open
            if long==1:
                perc = ((current_price - open_price)/current_price)*100
            elif short==1:
                perc = ((current_price - open_price)/current_price)*-100
            if perc < z_1:
                slope_1_close_threshold = z0_1
                slope_2_close_threshold = z0_2
            elif z_1 <= perc < z_2:
                slope_1_close_threshold = z1_1
                slope_2_close_threshold = z1_2
            elif z_2 <= perc < z_3:
                slope_1_close_threshold = z2_1
                slope_2_close_threshold = z2_2
            elif z_3 <= perc < z_4:
                slope_1_close_threshold = z3_1
                slope_2_close_threshold = z3_2
            elif z_4 <= perc:
                slope_1_close_threshold = z4_1
                slope_2_close_threshold = z4_2
      
            if perc<=2:
                account_data = accountApi.account(symbol, marginCoin='USDT')  #Check if stop was hit
                risk_data = float(account_data['data']['crossRiskRate'])
                risk = round(risk_data, 5)
                print("\n", flush=True)
                if risk == 0:
                    open_trade = 0
                    close_trade = 1
                else:
                    open_trade = 1
                    close_trade = 0
      
            if long == 1:
                if current_price > max_trade_price:  #Update trailing stop
                    max_trade_price = current_price
                    max_percent = abs(((open_price-max_trade_price)/open_price)*100)
                    if max_percent >= percent_in_profit:
                        secure_profit_price = (1+(move_stop/100))*open_price
                        be_secured = 1
                if max_percent>=take_profit_level and profit_secured==0 and take_profit_toggle==1:
                    profit_secured = 1
                    tp_price = current_price
                    orderApi.place_order(symbol, marginCoin='USDT', size=tp_position_size, side='close_long', orderType='market', timeInForceValue='normal')
                print("Close at", slope_2_close_threshold, ":", round(fast_slope, 3), flush=True)
                print("Close at", slope_1_close_threshold, ":", round(slow_slope, 3), flush=True)
                print("\n", flush=True)
                print("Profit secured:", ":", be_secured, flush=True)
                print("Perc:", ":", round(perc,3), flush=True)
                print("\n", flush=True)

                if (slow_slope <= slope_1_close_threshold) or (fast_slope <= slope_2_close_threshold)or(current_price<=max_trade_price*(1-trailing_stop/100))or(current_price<=secure_profit_price):#Long close conditions
                    close_trade = 1
                    if profit_secured==0 and open_trade == 1:
                        orderApi.place_order(symbol, marginCoin='USDT', size=position_size, side='close_long', orderType='market', timeInForceValue='normal')
                    elif open_trade == 1:
                        orderApi.place_order(symbol, marginCoin='USDT', size=rest_position_size, side='close_long', orderType='market', timeInForceValue='normal')

            elif short == 1:
                if current_price < max_trade_price:  #Update trailing stop
                    max_trade_price = current_price
                    max_percent = abs(((open_price-max_trade_price)/open_price)*100)
                    if max_percent >= percent_in_profit:
                        secure_profit_price = (1+(move_stop/-100))*open_price
                        be_secured = 1
                if max_percent>=take_profit_level and profit_secured==0 and take_profit_toggle==1:
                    profit_secured = 1
                    tp_price = current_price
                    orderApi.place_order(symbol, marginCoin='USDT', size=tp_position_size, side='close_short', orderType='market', timeInForceValue='normal')
                print("Close at", -slope_2_close_threshold, ":", round(fast_slope, 3), flush=True)
                print("Close at", -slope_1_close_threshold, ":", round(slow_slope, 3), flush=True)
                print("\n", flush=True)
                print("Profit secured:", ":", be_secured, flush=True)
                print("Perc:", ":", round(perc,3), flush=True)
                print("\n", flush=True)

                if (slow_slope >= -slope_1_close_threshold) or (fast_slope >= -slope_2_close_threshold) or (current_price >= max_trade_price *(1-trailing_stop/-100))or(current_price>=secure_profit_price):  #Short close conditions
                    close_trade = 1
                    if profit_secured==0 and open_trade == 1:
                        orderApi.place_order(symbol, marginCoin='USDT', size=position_size, side='close_short', orderType='market', timeInForceValue='normal')
                    elif open_trade == 1:
                        orderApi.place_order(symbol, marginCoin='USDT', size=rest_position_size, side='close_short', orderType='market', timeInForceValue='normal')
                        
            if close_trade==1:
                close_trade = 0
                be_secured = 0
                open_trade = 0
                if profit_secured==0:
                    close_price = current_price
                else:
                    close_price = (current_price*(1-(take_profit_amount/100)))+((take_profit_amount/100)*tp_price)
                if long==1:
                    trade_return = (((close_price - open_price)/close_price)*100)-trade_fee
                elif short==1:
                    trade_return = (((close_price - open_price)/close_price)*-100)-trade_fee
                profit_secured = 0
                long = 0
                short = 0
                if trade_return>be_tolerance:
                    last_win_time = current_time
                elif trade_return<-be_tolerance:
                    last_lose_time = current_time
                else:
                    last_be_time = current_time
                if trade_alerts==1:
                    resp = client.send_message(close_message)
            
        state = {
            "current_time": current_time,
            "current_price": current_price,
            "major_error": major_error,
            "timing_error": timing_error,
            "open_trade": open_trade,
            "last_check": last_check,
            "price_list": price_list,
            "slow_ma": slow_ma,
            "fast_ma": fast_ma,
            "long": long,
            "short": short,
            "tp_price": tp_price,
            "position_size": position_size,
            "tp_position_size": tp_position_size,
            "rest_position_size": rest_position_size,
            "open_price": open_price,
            "max_trade_price": max_trade_price,
            "secure_profit_price": secure_profit_price,
            "max_percent": max_percent,
            "time_check": time_check,
            "be_secured": be_secured,
            "profit_secured": profit_secured,
            "last_win_time": last_win_time,
            "last_be_time": last_be_time,
            "last_lose_time": last_lose_time,
            "open_time": open_time
        }
        with open("alice/alice_app_data.pickle", "wb") as f:
            pickle.dump(state, f)

    time.sleep(0.5)

while major_error == 1: 
    current_time = time_return()
    req = requests.get(prices_url)
    soup = BeautifulSoup(req.text, "html.parser")
    data = soup.find_all("td", class_="blob-code blob-code-inner js-file-line")
    unix_sheet = []
    open_price_sheet = []
    time_diff = []
  
    for x in range(ma_1+derive_rate):
        string = data[x].text
        row = list(string.split("\t"))
        unix_sheet.append(int(row[1]))
        open_price_sheet.append(float(row[3]))#Running on close rn
        last_time = unix_sheet[-1]
        if x>0:
            time_diff.append(abs(unix_sheet[-2]-last_time-60))
    open_price_sheet.reverse()
    if sum(time_diff)>360 or current_time-unix_sheet[0]>69:
        print(sum(time_diff), current_time-unix_sheet[0], flush=True)
    else:
        major_error = 0
        state.update(major_error=major_error)
        with open("alice/alice_app_data.pickle", "wb") as f:
            pickle.dump(state, f)
        break
    time.sleep(2)

    
    
    
    
    
    
    
