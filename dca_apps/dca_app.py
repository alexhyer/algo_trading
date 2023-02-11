"""
@author: Alex Hyer
https://github.com/alexhyer
"""
import bitget.mix.account_api as accounts
import bitget.mix.order_api as order
import bitget.mix.plan_api as plan
from dca_app_funcs import btc_price_return
from dca_app_funcs import time_return
from dca_app_funcs import define_messages
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
    data = pickle.load(f)[1]
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
   
with open("alice/bots/dca_apps/dca_app_"+str(app_number)+"_data.pickle", "rb") as f:
    values = pickle.load(f)
startup_error,api_error,partial_error = values["startup_error"],values["api_error"],values["partial_error"]
state,last_state,try_again = values["state"],values["last_state"],values["try_again"]
open_price,price = values["open_price"],values["price"]
sl_price,tp_price = values["sl_price"],values["tp_price"]
entry_id_1,entry_id_2,entry_id_3 = values["entry_id_1"],values["entry_id_2"],values["entry_id_3"]
sl_id_1,sl_id_2,sl_id_3 = values["sl_id_1"],values["sl_id_2"],values["sl_id_3"]
tp_id_1,tp_id_2,tp_id_3 = values["tp_id_1"],values["tp_id_2"],values["tp_id_3"]
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
average_fee=0.05
trigger_offset=0.5
hsl_offset=2
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
        if 1<=bt_state<=4:
            if price>=bt_tp:
                if bt_state!=1:
                    last_win_time=time
                print("Activated", flush=True)
                bt_state=0
            if price<=bt_sl:
                last_lose_time=time
                print("Activated", flush=True)
                bt_state=0
        if 5<=bt_state<=8:
            if price<=bt_tp:
                if bt_state!=5:
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
            with open("alice/bots/dca_apps/dca_app_"+str(app_number)+"_data.pickle", "wb") as f:
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
        position_size_1 = float(f'{(total_position_size*(dca_amount_1/100)):.3f}')
        position_size_2 = float(f'{(total_position_size*(dca_amount_2/100)):.3f}')
        position_size_3 = round(total_position_size-(position_size_1+position_size_2),3)
        
        exec(indicator_calc_string)
        
        last_state = state
    
        if 1<=state<=4:
            perc=((price-open_price)/price)*100
            print("Perc:", round(perc,2), flush=True)
            print("Open price:", open_price, flush=True)
        elif 5<=state<=8:
            perc=((price-open_price)/price)*-100
            print("Perc:", round(perc,2), flush=True)
            print("Open price:", open_price, flush=True)
        else:
            perc=0
            
        try:
            if state==1:
                print("0/3 longs opened", flush=True)
                entry_state_1=orderApi.detail(symbol, orderId=entry_id_1)['data']['state']
                if entry_state_1=='filled':
                    state=2
            if state==2:
                print("1/3 longs opened", flush=True)
                entry_state_2=orderApi.detail(symbol, orderId=entry_id_2)['data']['state']
                if entry_state_2=='filled':
                    state=3
            if state==3:
                print("2/3 longs opened", flush=True)
                entry_state_3=orderApi.detail(symbol, orderId=entry_id_3)['data']['state']
                if entry_state_3=='filled':
                    state=4
            if state==4:
                print("3/3 longs opened", flush=True)
            if state==5:
                print("0/3 shorts opened", flush=True)
                entry_state_1=orderApi.detail(symbol, orderId=entry_id_1)['data']['state']
                if entry_state_1=='filled':
                    state=6
            if state==6:
                print("1/3 shorts opened", flush=True)
                entry_state_2=orderApi.detail(symbol, orderId=entry_id_2)['data']['state']
                if entry_state_2=='filled':
                    state=7
            if state==7:
                print("2/3 shorts opened", flush=True)
                entry_state_3=orderApi.detail(symbol, orderId=entry_id_3)['data']['state']
                if entry_state_3=='filled':
                    state=8
            if state==8:
                print("3/3 shorts opened", flush=True)
            if perc<=2 and state!=0 and state!=1 and state!=5:
                trigger_state = planApi.current_plan(symbol, isPlan='plan')['data']
        except Exception as e:
            print(e, flush=True)
            print("Error on 1", flush=True)
            api_error=1
            break
            
        if ((state==1 or state==5)and entry_state_1=='partially_filled')or((state==2 or state==6)and entry_state_2=='partially_filled')or((state==3 or state==7)and entry_state_3=='partially_filled'):
            partial_error=1
            print("Partial fill on entry", flush=True)
            resp = client.send_message(partial_error_message)
            values.update(partial_error=partial_error)
            with open("alice/bots/dca_apps/dca_app_"+str(app_number)+"_data.pickle", "wb") as f:
                pickle.dump(values, f)
                
                
        if perc<=2 and state!=0 and state!=1 and state!=5: #Check status of trades
            sl_hit = 0
            if len(trigger_state)==0:
                sl_hit=1
            else:
                trigger_check=0
                for x in range(len(trigger_state)):
                    trigger_id=trigger_state[x]['orderId']
                    if trigger_id==sl_id_1 or trigger_id==sl_id_2 or trigger_id==sl_id_3:
                        trigger_check=1
                if trigger_check==0:
                    sl_hit=1
            if sl_hit==1:
                if 1<=state<=4:
                    last_state=4
                else:
                    last_state=8
                state=tps_placed=sl_hit=0
                last_lose_time=time
                print("SL Hit", flush=True)
                if trade_alerts==1:
                    resp = client.send_message(sl_message)
                    
        if state==0 and last_state==0 and time-last_lose_time>=lose_wait_time and time-last_win_time>=win_wait_time: #Trigger long or short signal
            #Long open conditions:
            if eval(conditions['long']):
                open_price = price
                sl_price = round(open_price*(1-(stop_loss+dca_perc_1+dca_perc_2+dca_perc_3)/100))
                tp_price = round(open_price*(1-take_profit/-100))
                state=1
            #Short open conditions:
            if eval(conditions['short']):
                open_price = price
                sl_price = round(open_price*(1-(stop_loss+dca_perc_1+dca_perc_2+dca_perc_3)/-100))
                tp_price = round(open_price*(1-take_profit/100))
                state=5
        #Check state
        
        
        if last_state==0 and state==1: #Long triggered
            open_price=price
            open_price_1 = round(open_price*(1-dca_perc_1/100))
            open_price_2 = round(open_price*(1-(dca_perc_1+dca_perc_2)/100))
            open_price_3 = round(open_price*(1-(dca_perc_1+dca_perc_2+dca_perc_3)/100))
            sl_price = round(open_price*(1-(stop_loss+dca_perc_1+dca_perc_2+dca_perc_3)/100))
            tp_price = round(open_price*(1-take_profit/-100))
            pos_size = (max_risk/worst_downtrend)/lev
            total_position_size = round((total_account_size/price)*pos_size*lev,4)
            position_size_1 = float(f'{(total_position_size*(dca_amount_1/100)):.3f}')
            position_size_2 = float(f'{(total_position_size*(dca_amount_2/100)):.3f}')
            position_size_3 = round(total_position_size-(position_size_1+position_size_2),3)
            try:
                accountApi.margin_mode(symbol, marginCoin='USDT', marginMode='crossed')
                accountApi.leverage(symbol, marginCoin='USDT', leverage=lev)
                entry_1_data = orderApi.place_order(symbol, marginCoin='USDT',size=position_size_1,side='open_long',orderType='limit',price=open_price_1, timeInForceValue='normal',presetStopLossPrice=sl_price-hsl_offset)
                entry_2_data = orderApi.place_order(symbol, marginCoin='USDT',size=position_size_2,side='open_long',orderType='limit',price=open_price_2, timeInForceValue='normal',presetStopLossPrice=sl_price-hsl_offset)
                entry_3_data = orderApi.place_order(symbol, marginCoin='USDT',size=position_size_3,side='open_long',orderType='limit',price=open_price_3, timeInForceValue='normal',presetStopLossPrice=sl_price-hsl_offset)
                entry_client_id_1,entry_client_id_2,entry_client_id_3 = entry_1_data['data']['clientOid'],entry_2_data['data']['clientOid'],entry_3_data['data']['clientOid']
                sl_1_data = planApi.place_plan(symbol,marginCoin='USDT',size=position_size_1,side='close_long',orderType='limit',triggerPrice=sl_price,executePrice=sl_price+trigger_offset,triggerType='fill_price',clientOrderId=entry_client_id_1,timeInForceValue='post_only')
                sl_2_data = planApi.place_plan(symbol,marginCoin='USDT',size=position_size_2,side='close_long',orderType='limit',triggerPrice=sl_price,executePrice=sl_price+trigger_offset,triggerType='fill_price',clientOrderId=entry_client_id_2,timeInForceValue='post_only')
                sl_3_data = planApi.place_plan(symbol,marginCoin='USDT',size=position_size_3,side='close_long',orderType='limit',triggerPrice=sl_price,executePrice=sl_price+trigger_offset,triggerType='fill_price',clientOrderId=entry_client_id_3,timeInForceValue='post_only')
            except Exception as e:
                print(e, flush=True)
                print("Error on 2", flush=True)
                api_error=1
                break
            entry_id_1,entry_id_2,entry_id_3 = entry_1_data['data']['orderId'],entry_2_data['data']['orderId'],entry_3_data['data']['orderId']
            sl_id_1,sl_id_2,sl_id_3 = sl_1_data['data']['orderId'],sl_2_data['data']['orderId'],sl_3_data['data']['orderId']
            print("\n", flush=True)
            print("Long orders placed", flush=True)
            print("First entry:",dca_amount_1,"% at", open_price_1, flush=True)
            print("Second entry:",dca_amount_2,"% at", open_price_2, flush=True)
            print("Third entry:",dca_amount_3,"% at", open_price_3, flush=True)
            print("Stop loss:", sl_price, flush=True)
            print("TP:", tp_price, flush=True)
            print("\n", flush=True)
            tps_placed=0
            state=1
            if trade_alerts==1:
                resp = client.send_message(long_message)
                
        if last_state==0 and state==5: #Short triggered
            open_price=price
            open_price_1 = round(open_price*(1-dca_perc_1/-100))
            open_price_2 = round(open_price*(1-(dca_perc_1+dca_perc_2)/-100))
            open_price_3 = round(open_price*(1-(dca_perc_1+dca_perc_2+dca_perc_3)/-100))
            sl_price = round(open_price*(1-(stop_loss+dca_perc_1+dca_perc_2+dca_perc_3)/-100))
            tp_price = round(open_price*(1-take_profit/100))
            pos_size = (max_risk/worst_downtrend)/lev
            total_position_size = round((total_account_size/price)*pos_size*lev,4)
            position_size_1 = float(f'{(total_position_size*(dca_amount_1/100)):.3f}')
            position_size_2 = float(f'{(total_position_size*(dca_amount_2/100)):.3f}')
            position_size_3 = round(total_position_size-(position_size_1+position_size_2),3)
            try:
                accountApi.margin_mode(symbol, marginCoin='USDT', marginMode='crossed')
                accountApi.leverage(symbol, marginCoin='USDT', leverage=lev)
                entry_1_data = orderApi.place_order(symbol, marginCoin='USDT',size=position_size_1,side='open_short',orderType='limit',price=open_price_1, timeInForceValue='normal',presetStopLossPrice=sl_price+hsl_offset)
                entry_2_data = orderApi.place_order(symbol, marginCoin='USDT',size=position_size_2,side='open_short',orderType='limit',price=open_price_2, timeInForceValue='normal',presetStopLossPrice=sl_price+hsl_offset)
                entry_3_data = orderApi.place_order(symbol, marginCoin='USDT',size=position_size_3,side='open_short',orderType='limit',price=open_price_3, timeInForceValue='normal',presetStopLossPrice=sl_price+hsl_offset)
                entry_client_id_1,entry_client_id_2,entry_client_id_3 = entry_1_data['data']['clientOid'],entry_2_data['data']['clientOid'],entry_3_data['data']['clientOid']
                sl_1_data = planApi.place_plan(symbol,marginCoin='USDT',size=position_size_1,side='close_short',orderType='limit',triggerPrice=sl_price,executePrice=sl_price-trigger_offset,triggerType='fill_price',clientOrderId=entry_client_id_1,timeInForceValue='post_only')
                sl_2_data = planApi.place_plan(symbol,marginCoin='USDT',size=position_size_2,side='close_short',orderType='limit',triggerPrice=sl_price,executePrice=sl_price-trigger_offset,triggerType='fill_price',clientOrderId=entry_client_id_2,timeInForceValue='post_only')
                sl_3_data = planApi.place_plan(symbol,marginCoin='USDT',size=position_size_3,side='close_short',orderType='limit',triggerPrice=sl_price,executePrice=sl_price-trigger_offset,triggerType='fill_price',clientOrderId=entry_client_id_3,timeInForceValue='post_only')
            except Exception as e:
                print(e, flush=True)
                print("Error on 3", flush=True)
                api_error=1
                break
            entry_id_1,entry_id_2,entry_id_3 = entry_1_data['data']['orderId'],entry_2_data['data']['orderId'],entry_3_data['data']['orderId']
            sl_id_1,sl_id_2,sl_id_3 = sl_1_data['data']['orderId'],sl_2_data['data']['orderId'],sl_3_data['data']['orderId']
            print("\n", flush=True)
            print("Short orders placed", flush=True)
            print("First entry:",dca_amount_1,"% at", open_price_1, flush=True)
            print("Second entry:",dca_amount_2,"% at", open_price_2, flush=True)
            print("Third entry:",dca_amount_3,"% at", open_price_3, flush=True)
            print("Stop loss:", sl_price, flush=True)
            print("TP:", tp_price, flush=True)
            print("\n", flush=True)
            tps_placed=0
            state=5
            if trade_alerts==1:
                resp = client.send_message(short_message)
                
        #Place tp's
        place_tp_1=0
        place_tp_2=0
        place_tp_3=0
        if state==2 and tps_placed==0 and perc>=place_tp_perc:
            tp_side='close_long'
            place_tp_1=1
        if state==3 and tps_placed==0 and perc>=place_tp_perc:
            tp_side='close_long'
            place_tp_1=1
            place_tp_2=1
        if state==4 and tps_placed==0 and perc>=place_tp_perc:
            tp_side='close_long'
            place_tp_1=1
            place_tp_2=1
            place_tp_3=1
        if state==3 and tps_placed==1 and perc>=place_tp_perc:
            tp_side='close_long'
            place_tp_2=1
        if state==4 and tps_placed==1 and perc>=place_tp_perc:
            tp_side='close_long'
            place_tp_2=1
            place_tp_3=1
        if state==4 and tps_placed==2 and perc>=place_tp_perc:
            tp_side='close_long'
            place_tp_3=1

        if state==6 and tps_placed==0 and perc>=place_tp_perc:
            tp_side='close_short'
            place_tp_1=1
        if state==7 and tps_placed==0 and perc>=place_tp_perc:
            tp_side='close_short'
            place_tp_1=1
            place_tp_2=1
        if state==8 and tps_placed==0 and perc>=place_tp_perc:
            tp_side='close_short'
            place_tp_1=1
            place_tp_2=1
            place_tp_3=1
        if state==7 and tps_placed==1 and perc>=place_tp_perc:
            tp_side='close_short'
            place_tp_2=1
        if state==8 and tps_placed==1 and perc>=place_tp_perc:
            tp_side='close_short'
            place_tp_2=1
            place_tp_3=1
        if state==8 and tps_placed==2 and perc>=place_tp_perc:
            tp_side='close_short'
            place_tp_3=1
        
        if place_tp_1==1:
            try:
                tp_1_data = orderApi.place_order(symbol,marginCoin='USDT',size=position_size_1,side=tp_side,orderType='limit',price=tp_price,timeInForceValue='normal')
            except Exception as e:
                print(e, flush=True)
                print("Error on 4", flush=True)
                api_error=1
                break
            tp_id_1 = tp_1_data['data']['orderId']
            place_tp_1=0
            tps_placed=1
        if place_tp_2==1:
            try:
                tp_2_data = orderApi.place_order(symbol,marginCoin='USDT',size=position_size_2,side=tp_side,orderType='limit',price=tp_price,timeInForceValue='normal')
            except Exception as e:
                print(e, flush=True)
                print("Error on 5", flush=True)
                api_error=1
                break
            tp_id_2 = tp_2_data['data']['orderId']
            place_tp_2=0
            tps_placed=2
        if place_tp_3==1:
            try:
                tp_3_data = orderApi.place_order(symbol,marginCoin='USDT',size=position_size_3,side=tp_side,orderType='limit',price=tp_price,timeInForceValue='normal')
            except Exception as e:
                print(e, flush=True)
                print("Error on 6", flush=True)
                api_error=1
                break
            tp_id_3 = tp_3_data['data']['orderId']
            place_tp_3=0
            tps_placed=3
        #Place tp's  
        
        #TP hit, close all orders
        tp_hit=0
        if tps_placed>=1:
            try:
                tp_state_1 = orderApi.detail(symbol, orderId=tp_id_1)['data']['state']   
            except Exception as e:
                print(e, flush=True)
                print("Error on 7", flush=True)
                api_error=1
                break
        if tps_placed>=2:
            try:
                tp_state_2 = orderApi.detail(symbol, orderId=tp_id_2)['data']['state']   
            except Exception as e:
                print(e, flush=True)
                print("Error on 8", flush=True)
                api_error=1
                break
        if tps_placed==3:
            try:
                tp_state_3 = orderApi.detail(symbol, orderId=tp_id_3)['data']['state']   
            except Exception as e:
                print(e, flush=True)
                print("Error on 9", flush=True)
                api_error=1
                break
        if (tps_placed>=1 and tp_state_1=='partially_filled')or(tps_placed>=2 and tp_state_2=='partially_filled')or(tps_placed>=3 and tp_state_3=='partially_filled'):
            partial_error=1
            print("Partial fill on tp", flush=True)
            resp = client.send_message(partial_error_message)
            values.update(partial_error=partial_error)
            with open("alice/bots/dca_apps/dca_app_"+str(app_number)+"_data.pickle", "wb") as f:
                pickle.dump(values, f)
            
        if tps_placed==1:
            print("1st TP placed", flush=True)
        if tps_placed==2:
            print("2nd TP placed", flush=True)
        if tps_placed==3:
            print("3rd TP placed", flush=True)
            
        if (state==1 and price>=tp_price)or(state==5 and price<=tp_price):
            try:
                orderApi.cancel_orders(symbol , marginCoin='USDT', orderId=entry_id_1)
                orderApi.cancel_orders(symbol , marginCoin='USDT', orderId=entry_id_2)
                orderApi.cancel_orders(symbol , marginCoin='USDT', orderId=entry_id_3)
                planApi.cancel_plan(symbol, marginCoin='USDT', orderId=sl_id_1, planType='normal_plan')
                planApi.cancel_plan(symbol, marginCoin='USDT', orderId=sl_id_2, planType='normal_plan')
                planApi.cancel_plan(symbol, marginCoin='USDT', orderId=sl_id_3, planType='normal_plan')
            except Exception as e:
                print(e, flush=True)
                print("Error on 10", flush=True)
                api_error=1
                break
            tps_placed=0
            tp_hit=1
            state=0
            print("TP hit, 0 entries opened", flush=True)
        if tps_placed==1 and tp_state_1=='filled':
            try:
                orderApi.cancel_orders(symbol , marginCoin='USDT', orderId=entry_id_2)
                orderApi.cancel_orders(symbol , marginCoin='USDT', orderId=entry_id_3)
                planApi.cancel_plan(symbol, marginCoin='USDT', orderId=sl_id_1, planType='normal_plan')
                planApi.cancel_plan(symbol, marginCoin='USDT', orderId=sl_id_2, planType='normal_plan')
                planApi.cancel_plan(symbol, marginCoin='USDT', orderId=sl_id_3, planType='normal_plan')
            except Exception as e:
                print(e, flush=True)
                print("Error on 11", flush=True)
                api_error=1
                break
            tps_placed=0
            tp_hit=1
            state=0
            print("TP hit, 1 entries opened", flush=True)
        if tps_placed==2 and tp_state_1=='filled':
            try:
                orderApi.cancel_orders(symbol , marginCoin='USDT', orderId=entry_id_3)
                planApi.cancel_plan(symbol, marginCoin='USDT', orderId=sl_id_1, planType='normal_plan')
                planApi.cancel_plan(symbol, marginCoin='USDT', orderId=sl_id_2, planType='normal_plan')
                planApi.cancel_plan(symbol, marginCoin='USDT', orderId=sl_id_3, planType='normal_plan')
            except Exception as e:
                print(e, flush=True)
                print("Error on 12", flush=True)
                api_error=1
                break
            tps_placed=0
            tp_hit=1
            state=0
            print("TP hit, 2 entries opened", flush=True)
        if tps_placed==3 and tp_state_1=='filled':
            try:
                planApi.cancel_plan(symbol, marginCoin='USDT', orderId=sl_id_1, planType='normal_plan')
                planApi.cancel_plan(symbol, marginCoin='USDT', orderId=sl_id_2, planType='normal_plan')
                planApi.cancel_plan(symbol, marginCoin='USDT', orderId=sl_id_3, planType='normal_plan')
            except Exception as e:
                print(e, flush=True)
                print("Error on 13", flush=True)
                api_error=1
                break
            tps_placed=0
            tp_hit=1
            state=0
            print("TP hit, 3 entries opened", flush=True)

        if tp_hit==1:
            tp_hit=0
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
            "entry_id_1": entry_id_1,"entry_id_2": entry_id_2,"entry_id_3": entry_id_3,
            "sl_id_1": sl_id_1,"sl_id_2": sl_id_2,"sl_id_3": sl_id_3,
            "tp_id_1": tp_id_1,"tp_id_2": tp_id_2,"tp_id_3": tp_id_3,
            "last_check": last_check,"last_lose_time": last_lose_time,"last_win_time": last_win_time,
            "total_position_size": total_position_size,"tps_placed": tps_placed,
            "indicator_1": indicator_1,"indicator_2": indicator_2,"indicator_3": indicator_3,
            "indicator_4": indicator_4,"indicator_5": indicator_5
        }
        with open("alice/bots/dca_apps/dca_app_"+str(app_number)+"_data.pickle", "wb") as f:
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
    
    
    
    
    
    
    
