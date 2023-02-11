"""
@author: Alex Hyer
https://github.com/alexhyer
"""
import bitget.mix.account_api as accounts
import bitget.mix.order_api as order
import bitget.mix.plan_api as plan
from single_app_funcs import btc_price_return
from single_app_funcs import time_return
from single_app_funcs import define_messages
from trycourier import Courier
from bs4 import BeautifulSoup
import time as pause
import requests
import pickle
import math

app_number = 0
email = ""
client = Courier(auth_token="")

api_key = ""
secret_key = ""
passphrase = ""

trade_alerts = 1  #If 1 alerts will send when trades are triggered
lev = 50

with open("alice/alice_data.pickle", "rb") as f:
    data = pickle.load(f)[0]
backtest_number = data["number_data"][app_number-1]
worst_downtrend = data["worst_downtrend_data"][app_number-1]
max_risk = data["max_risk_data"][app_number-1]
settings_string = data["settings_string_data"][app_number-1]
indicator_type_string = data["type_string_data"][app_number-1]
indicator_calc_string = data["calc_string_data"][app_number-1]
conditions = data["conditions_data"][app_number-1]
total_account_size = data["balance"]
exec(indicator_type_string)

print("App number:",app_number, flush=True)
print("Backtest number:",backtest_number, flush=True)
print(worst_downtrend, flush=True)
print(max_risk, flush=True)
print(settings_string, flush=True)
print(indicator_type_string, flush=True)
print(indicator_calc_string, flush=True)
print(conditions, flush=True)
   
with open("alice/bots/single_apps/single_app_"+str(app_number)+"_data.pickle", "rb") as f:
    values = pickle.load(f)
startup_error,api_error,partial_error = values["startup_error"],values["api_error"],values["partial_error"]
state,last_state,try_again = values["state"],values["last_state"],values["try_again"]
open_price,price = values["open_price"],values["price"]
sl_price,tp_price = values["sl_price"],values["tp_price"]
entry_id,tp_id = values["entry_id"],values["tp_id"]
last_check,last_lose_time,last_win_time = values["last_check"],values["last_lose_time"],values["last_win_time"]
total_position_size,tps_placed = values["total_position_size"],values["tps_placed"]
indicator_1,indicator_2,indicator_3 = values["indicator_1"],values["indicator_2"],values["indicator_3"]
indicator_4,indicator_5 = values["indicator_4"],values["indicator_5"]
bt_state,bt_sl,bt_tp = values["bt_state"],values["bt_sl"],values["bt_tp"]
print(values, flush=True)
if bt_state!=0:
    print("Waiting for previous trade to finish", flush=True)

exec(settings_string)

prices_url="https://github.com/alexhyer/algo_trading/blob/main/price_logging/btc_price_data.txt"
symbol="BTCUSDT_UMCBL"
long_message,short_message,tp_message,sl_message,startup_error_message,api_error_message,partial_error_message=define_messages(email,app_number,backtest_number)
accountApi = accounts.AccountApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
orderApi = order.OrderApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
planApi = plan.PlanApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
restart=1
limit_offset=1
maker_fee = 0.04 #0.02+0.02
taker_fee = 0.08 #0.02+0.06
data_length=1000

if ma_1%2==1: #MA's must be even
    ma_1=ma_1+1
if ma_2%2==1:
    ma_2=ma_2+1
if ma_3%2==1:
    ma_3=ma_3+1
    
while startup_error==0 and api_error==0:
    time = time_return()
    while bt_state!=0:
        price = btc_price_return(price)
        if 1<=bt_state<=2:
            if price>=bt_tp:
                if bt_state!=1:
                    last_win_time=time
                print("Activated", flush=True)
                bt_state=0
            if price<=bt_sl:
                last_lose_time=time
                print("Activated", flush=True)
                bt_state=0
        if 3<=bt_state<=4:
            if price<=bt_tp:
                if bt_state!=3:
                    last_win_time=time
                print("Activated", flush=True)
                bt_state=0
            if price>=bt_sl:
                last_lose_time=time
                print("Activated", flush=True)
                bt_state=0
        pause.sleep(3)
        
    if restart==1:
        req = requests.get(prices_url)
        soup = BeautifulSoup(req.text, "html.parser")
        data = soup.find_all("td", class_="blob-code blob-code-inner js-file-line")
        unix_sheet,price_list,time_diff,average_1,average_2,average_3=([] for i in range(6))
        for x in range(data_length):
            string = data[x].text
            row = list(string.split("\t"))
            unix_sheet.append(int(row[1]))
            price_list.append(float(row[3]))
            last_time = unix_sheet[-1]
            if x>0:
                time_diff.append(abs(unix_sheet[-2]-last_time-60))
        price_list.reverse()
        if sum(time_diff)>420 or time-unix_sheet[0]>142:
            startup_error=1
            resp = client.send_message(startup_error_message)
            values.update(startup_error=startup_error)
            with open("alice/bots/single_apps/single_app_"+str(app_number)+"_data.pickle", "wb") as f:
                pickle.dump(values, f)
            break
        else:
            restart = 0

        cut_at_1,cut_at_2,cut_at_3 = int(ma_1/2),int(ma_2/2),int(ma_3/2)
        place_tp_perc = round(take_profit/10,2)
        last_check = math.ceil(time/60)*60-60
        for x in range(derive_rate):
            first_half_1 = price_list[data_length-ma_1-derive_rate+x:data_length-cut_at_1-derive_rate+x]
            second_half_1 = price_list[data_length-cut_at_1-derive_rate+x:data_length-derive_rate+x]
            first_half_2 = price_list[data_length-ma_2-derive_rate+x:data_length-cut_at_2-derive_rate+x]
            second_half_2 = price_list[data_length-cut_at_2-derive_rate+x:data_length-derive_rate+x]
            first_half_3 = price_list[data_length-ma_3-derive_rate+x:data_length-cut_at_3-derive_rate+x]
            second_half_3 = price_list[data_length-cut_at_3-derive_rate+x:data_length-derive_rate+x]
            average_1.append(((sum(first_half_1) / 1.5) + (sum(second_half_1) / 0.75)) / ma_1)
            average_2.append(((sum(first_half_2) / 1.5) + (sum(second_half_2) / 0.75)) / ma_2)
            average_3.append(((sum(first_half_3) / 1.5) + (sum(second_half_3) / 0.75)) / ma_3)

    if time-last_check>=60:
        price = btc_price_return(price)
        time_check = time - last_check
        if (time_check > 73) or (time_check < 58):
            restart=1
            break
        last_check = last_check + 60
        price_list.append(price)
        price_list.pop(0)
        first_half_1,second_half_1 = price_list[data_length-ma_1:data_length-cut_at_1],price_list[data_length-cut_at_1:data_length]
        first_half_2,second_half_2 = price_list[data_length-ma_2:data_length-cut_at_2],price_list[data_length-cut_at_2:data_length]
        first_half_3,second_half_3 = price_list[data_length-ma_3:data_length-cut_at_3],price_list[data_length-cut_at_3:data_length]
        average_1.append(((sum(first_half_1) / 1.5) + (sum(second_half_1) / 0.75)) / ma_1)
        average_2.append(((sum(first_half_2) / 1.5) + (sum(second_half_2) / 0.75)) / ma_2)
        average_3.append(((sum(first_half_3) / 1.5) + (sum(second_half_3) / 0.75)) / ma_3)
        average_1.pop(0)
        average_2.pop(0)
        average_3.pop(0)
        slope_1 = (average_1[-1] - average_1[0]) / derive_rate
        slope_2 = (average_2[-1] - average_2[0]) / derive_rate
        slope_3 = (average_3[-1] - average_3[0]) / derive_rate
        
        exec(indicator_calc_string)
        
        last_state = state
    
        if 1<=state<=2:
            perc=((price-open_price)/price)*100
            print("Perc:", round(perc,2), flush=True)
            print("Open price:", open_price, flush=True)
        elif 3<=state<=4:
            perc=((price-open_price)/price)*-100
            print("Perc:", round(perc,2), flush=True)
            print("Open price:", open_price, flush=True)
        else:
            perc=0
    
        try:
            if state==1:
                print("Long not opened", flush=True)
                entry_state=orderApi.detail(symbol, orderId=entry_id)['data']['state']
                if entry_state=='filled':
                    state=2
            if state==2:
                print("Long opened", flush=True)
            if state==3:
                print("Short not opened", flush=True)
                entry_state=orderApi.detail(symbol, orderId=entry_id)['data']['state']
                if entry_state=='filled':
                    state=4
            if state==4:
                print("Short opened", flush=True)
            if perc<=2 and state!=0 and state!=1 and state!=3:
                sl_data = planApi.current_plan(symbol, isPlan='profit_loss')['data']
        except Exception as e:
            print(e, flush=True)
            print("Error on 1", flush=True)
            api_error=1
            break
            
        if (state==1 or state==3) and entry_state=='partially_filled':
            partial_error=1
            print("Partial fill on entry", flush=True)
            resp = client.send_message(partial_error_message)
            values.update(partial_error=partial_error)
            with open("alice/bots/single_apps/single_app_"+str(app_number)+"_data.pickle", "wb") as f:
                pickle.dump(values, f)
                    
        if perc<=2 and state!=0 and state!=1 and state!=3: #Check status of trades
            for x in range(len(sl_data)):
                if sl_data[x]['size']==str(total_position_size) and sl_data[x]['triggerPrice']==str(int(sl_price)) and sl_data[x]['status']=='triggered':
                    if 1<=state<=2:
                        last_state=2
                    else:
                        last_state=4
                    state=tps_placed=0
                    last_lose_time=time
                    print("SL Hit", flush=True)
                    if trade_alerts==1:
                        resp = client.send_message(sl_message)
                    
        if state==0 and last_state==0 and time-last_lose_time>=lose_wait_time and time-last_win_time>=win_wait_time: #Trigger long or short signal
            #Long open conditions:
            if eval(conditions['long']):
                open_price = price
                sl_price = round(open_price*(1-stop_loss/100))
                tp_price = round(open_price*(1-take_profit/-100))
                state=1
            #Short open conditions:
            if eval(conditions['short']):
                open_price = price
                sl_price = round(open_price*(1-stop_loss/-100))
                tp_price = round(open_price*(1-take_profit/100))
                state=3
        #Check state
        
        
        if last_state==0 and state==1: #Long triggered
            open_price=price-limit_offset
            sl_price = round(open_price*(1-stop_loss/100))
            tp_price = round(open_price*(1-take_profit/-100))
            pos_size = (max_risk/worst_downtrend)/lev
            total_position_size = str(round((total_account_size/price)*pos_size*lev,3))
            try:
                accountApi.margin_mode(symbol, marginCoin='USDT', marginMode='crossed')
                accountApi.leverage(symbol, marginCoin='USDT', leverage=lev)
                entry_data = orderApi.place_order(symbol, marginCoin='USDT',size=total_position_size,side='open_long',orderType='limit',price=open_price, timeInForceValue='normal',presetStopLossPrice=sl_price)
            except Exception as e:
                print(e, flush=True)
                print("Error on 2", flush=True)
                api_error=1
                break
            entry_id = entry_data['data']['orderId']
            print("\n", flush=True)
            print("Long orders placed", flush=True)
            print("Entry:",open_price, flush=True)
            print("Stop loss:", sl_price, flush=True)
            print("TP:", tp_price, flush=True)
            print("\n", flush=True)
            tps_placed=0
            state=1
            if trade_alerts==1:
                resp = client.send_message(long_message)
                
        if last_state==0 and state==3: #Short triggered
            open_price=price+limit_offset
            sl_price = round(open_price*(1-stop_loss/-100))
            tp_price = round(open_price*(1-take_profit/100))
            pos_size = (max_risk/worst_downtrend)/lev
            total_position_size = str(round((total_account_size/price)*pos_size*lev,3))
            try:
                accountApi.margin_mode(symbol, marginCoin='USDT', marginMode='crossed')
                accountApi.leverage(symbol, marginCoin='USDT', leverage=lev)
                entry_data = orderApi.place_order(symbol, marginCoin='USDT',size=total_position_size,side='open_short',orderType='limit',price=open_price, timeInForceValue='normal',presetStopLossPrice=sl_price)
            except Exception as e:
                print(e, flush=True)
                print("Error on 3", flush=True)
                api_error=1
                break
            entry_id = entry_data['data']['orderId']
            print("\n", flush=True)
            print("Short orders placed", flush=True)
            print("Entry:",open_price, flush=True)
            print("Stop loss:", sl_price, flush=True)
            print("TP:", tp_price, flush=True)
            print("\n", flush=True)
            tps_placed=0
            state=3
            if trade_alerts==1:
                resp = client.send_message(short_message)
                
        #Place tp's
        place_tp=0
        if state==2 and tps_placed==0 and perc>=place_tp_perc:
            tp_side='close_long'
            place_tp=1
        if state==4 and tps_placed==0 and perc>=place_tp_perc:
            tp_side = 'close_short'
            place_tp=1
        if place_tp==1:
            try:
                tp_data = orderApi.place_order(symbol,marginCoin='USDT',size=total_position_size,side=tp_side,orderType='limit',price=tp_price,timeInForceValue='normal')
            except Exception as e:
                print(e, flush=True)
                print("Error on 4", flush=True)
                api_error=1
                break
            tp_id = tp_data['data']['orderId']
            place_tp=0
            tps_placed=1
        #Place tp's
                
        #TP hit, close all orders 
        if tps_placed==1:
            print("TP is placed", flush=True)
            try:
                tp_state = orderApi.detail(symbol, orderId=tp_id)['data']['state']
            except Exception as e:
                print(e, flush=True)
                print("Error on 5", flush=True)
                api_error=1
                break
            if tp_state=='partially_filled':
                partial_error=1
                print("Partial fill on tp", flush=True)
                resp = client.send_message(partial_error_message)
                values.update(partial_error=partial_error)
                with open("alice/bots/single_apps/single_app_"+str(app_number)+"_data.pickle", "wb") as f:
                    pickle.dump(values, f)
        if (state==1 and price>=tp_price) or (state==3 and price<=tp_price):
            try:
                orderApi.cancel_orders(symbol , marginCoin='USDT', orderId=entry_id)
            except Exception as e:
                print(e, flush=True)
                print("Error on 6", flush=True)
                api_error=1
                break
            tps_placed=0
            state=0
            print("TP hit with no entry", flush=True)
            last_win_time=time
            if trade_alerts==1:
                resp = client.send_message(tp_message)
        if tps_placed==1 and tp_state=='filled':
            tps_placed=0
            state=0
            print("TP hit", flush=True)
            last_win_time=time
            if trade_alerts==1:
                resp = client.send_message(tp_message)
        #TP hit, close all orders

        try_again=0
        values = {
            "startup_error": startup_error,"api_error": api_error,"partial_error": partial_error,
            "state": state,"last_state": last_state,"try_again": try_again,
            "bt_state": bt_state,"bt_sl": bt_sl,"bt_tp": bt_tp,
            "open_price": open_price,"price": price,
            "sl_price": sl_price,"tp_price": tp_price,
            "entry_id": entry_id,"tp_id": tp_id,
            "last_check": last_check,"last_lose_time": last_lose_time,"last_win_time": last_win_time,
            "total_position_size": total_position_size,"tps_placed": tps_placed,
            "indicator_1": indicator_1,"indicator_2": indicator_2,"indicator_3": indicator_3,
            "indicator_4": indicator_4,"indicator_5": indicator_5
        }
        with open("alice/bots/single_apps/single_app_"+str(app_number)+"_data.pickle", "wb") as f:
            pickle.dump(values, f)

    pause.sleep(0.5)

if api_error==1 and try_again==0:
    api_error=0
    try_again=1
    resp = client.send_message(api_error_message)
    values.update(api_error=api_error)
    values.update(try_again=try_again)
    print("Trying again", flush=True)
    with open("alice/bots/single_apps/single_app_"+str(app_number)+"_data.pickle", "wb") as f:
        pickle.dump(values, f)
    pause.sleep(20)
elif api_error==1 and try_again==1:
    values.update(api_error=api_error)
    values.update(try_again=try_again)
    print("Try again failed", flush=True)
    with open("alice/bots/single_apps/single_app_"+str(app_number)+"_data.pickle", "wb") as f:
        pickle.dump(values, f)
    pause.sleep(100)
    
    
    
    
    
    
    
