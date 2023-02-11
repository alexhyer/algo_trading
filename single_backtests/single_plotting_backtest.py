"""
@author: Alex Hyer
https://github.com/alexhyer
"""
from single_plotting_backtest_funcs import plot
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
import random
import pickle
import os

number = 1
plot_mode = 2

cur_path = os.path.dirname(os.path.realpath(__file__)).split('single_backtest_structure')[0]
with open(cur_path+'\single_bots_data.pickle', "rb") as f:
    single_bots_data = pickle.load(f)
    
settings_string = single_bots_data[number-1][0]
indicator_type_string = single_bots_data[number-1][1]
indicator_calc_string = single_bots_data[number-1][2]
conditions = single_bots_data[number-1][3]

exec(settings_string)
    
if ma_1%2==1: #MA's must be even
    ma_1=ma_1+1
if ma_2%2==1:
    ma_2=ma_2+1
if ma_3%2==1:
    ma_3=ma_3+1
        
with open(os.path.dirname(__file__).split("alice",1)[0]+'alice\\price_logging\\btc_logging\\btc_price_data.txt') as f:
    contents = f.read()
price_data=contents.replace("\n", "\t")
price_data=price_data.split("\t")
minutes,unix=price_data[::6],price_data[1::6]
minutes.reverse()
unix.reverse()
minutes,unix=list(map(float, minutes)),list(map(float, unix)) 
candle_open,candle_low,candle_high=price_data[2::6],price_data[4::6],price_data[5::6]
candle_open.reverse()
candle_low.reverse()
candle_high.reverse()
candle_open,candle_low,candle_high = list(map(float, candle_open)),list(map(float, candle_low)),list(map(float, candle_high))
    
maker_fee = 0.04 #0.02+0.02
taker_fee = 0.08 #0.02+0.06
limit_offset = 1
trigger_offset = 0.5 #0.5
hsl_offset = 2 #2
trigger_success_rate = 40 #40
try:
    best_recover_rate
except NameError:
    best_recover_rate=100

max_return=max_downtrend=state=open_price=sl_price=tp_price=last_lose_time=last_win_time=winning=losing=indicators=0

exec(indicator_type_string)
indicator_1,indicator_2,indicator_3,indicator_4,indicator_5 = indicators[0],indicators[1],indicators[2],indicators[3],indicators[4]

win_count,lose_count,average_1,average_2,average_3,win_return,lose_return,close_time,close_price,open_long_time,open_short_time=([] for i in range(11))
historical_price_low,historical_price_high,historical_time,historical_average_1,historical_average_2,historical_average_3=([] for i in range(6))
historical_indicator_1,historical_indicator_2,historical_return_perc,open_long_price,open_short_price,return_perc,trade_return=([] for i in range(7))
return_perc.append(100)

data_length = 1000
cut_at_1,cut_at_2,cut_at_3 = int(ma_1/2),int(ma_2/2),int(ma_3/2)
price_list = candle_open[0:data_length]
length = len(minutes)

for x in range(derive_rate): #Initialize variables
    first_half_1 = price_list[data_length-ma_1-derive_rate+x:data_length-cut_at_1-derive_rate+x]
    second_half_1 = price_list[data_length-cut_at_1-derive_rate+x:data_length-derive_rate+x]
    first_half_2 = price_list[data_length-ma_2-derive_rate+x:data_length-cut_at_2-derive_rate+x]
    second_half_2 = price_list[data_length-cut_at_2-derive_rate+x:data_length-derive_rate+x]
    first_half_3 = price_list[data_length-ma_3-derive_rate+x:data_length-cut_at_3-derive_rate+x]
    second_half_3 = price_list[data_length-cut_at_3-derive_rate+x:data_length-derive_rate+x]
    average_1.append(((sum(first_half_1) / 1.5) + (sum(second_half_1) / 0.75)) / ma_1)
    average_2.append(((sum(first_half_2) / 1.5) + (sum(second_half_2) / 0.75)) / ma_2)
    average_3.append(((sum(first_half_3) / 1.5) + (sum(second_half_3) / 0.75)) / ma_3)
    
for x in range(1000,length): #Main backtesting loop
    time,time_min,price = unix[x],minutes[x],candle_open[x]
    high_price,low_price = candle_high[x],candle_low[x]
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
    
    historical_indicator_1.append(indicator_1),historical_indicator_2.append(indicator_2) #Choose what to plot
    
    historical_price_low.append(low_price),historical_price_high.append(high_price),historical_time.append(time_min)
    historical_average_1.append(average_1[-1]),historical_average_2.append(average_2[-1]),historical_average_3.append(average_3[-1])
    historical_return_perc.append(return_perc[-1])
    
    last_state = state
    
    if 1<=state<=2: #Close longs
        if high_price>=tp_price or low_price<=sl_price:
            state=0
    if 3<=state<=4: #Close shorts
        if low_price<=tp_price or high_price>=sl_price:
            state=0
    
    if state==1 and low_price<=open_price-limit_offset: #Open long
        state=2
    if state==3 and high_price>=open_price+limit_offset: #Open short
        state=4

    if state==0 and last_state==0 and time-last_lose_time>=lose_wait_time and time-last_win_time>=win_wait_time: #Trigger long or short signal
        #Long open conditions:
        if eval(conditions['long']):
            open_price = price-limit_offset
            sl_price = round(open_price*(1-stop_loss/100))
            tp_price = round(open_price*(1-take_profit/-100))
            state=1
        #Short open conditions:
        if eval(conditions['short']):
            open_price = price+limit_offset
            sl_price = round(open_price*(1-stop_loss/-100))
            tp_price = round(open_price*(1-take_profit/100))
            state=3
    
    if last_state==0 and state==1: #Long triggered
        open_price = price-limit_offset
        open_time = time
        sl_price = round(open_price*(1-stop_loss/100))
        tp_price = round(open_price*(1-take_profit/-100))
    if last_state==1 and state==2: #0 to 1 longs open
        open_long_time.append(time_min)
        open_long_price.append(open_price)
            
    if last_state==0 and state==3: #Short triggered
        open_price = price+limit_offset
        open_time = time
        sl_price = round(open_price*(1-stop_loss/-100))
        tp_price = round(open_price*(1-take_profit/100))
    if last_state==3 and state==4: #0 to 1 shorts open
        open_short_time.append(time_min)
        open_short_price.append(open_price)
            
    
    if 1<=last_state<=2 and state==0: #Longs closed
        close_time.append(time_min)
        if low_price<=sl_price:
            last_state=2 #If stop hit all orders had to open
            if round(random.uniform(0, 100))>=trigger_success_rate:
                trade_fee = taker_fee
                close_price.append(sl_price-hsl_offset)
            else:
                trade_fee = maker_fee
                close_price.append(sl_price+trigger_offset)
        else:
            close_price.append(tp_price)
            trade_fee = maker_fee
        if last_state==1 and state==0: #0 long closed
            trade_return.append(0)
        if last_state==2 and state==0: #1 long closed
            trade_return.append((((close_price[-1]-open_price)/close_price[-1])*100)-trade_fee)
        return_perc.append(return_perc[-1]+trade_return[-1])
        if trade_return[-1]>0:
            win_return.append(trade_return[-1])
            last_win_time = time
        elif trade_return[-1]<0:
            lose_return.append(trade_return[-1])
            last_lose_time = time


    if 3<=last_state<=4 and state==0: #Shorts closed
        close_time.append(time_min)
        if high_price>=sl_price:
            last_state=4 #If stop hit all orders had to open
            if round(random.uniform(0, 100))>=trigger_success_rate:
                trade_fee = taker_fee
                close_price.append(sl_price+hsl_offset)
            else:
                trade_fee = maker_fee
                close_price.append(sl_price-trigger_offset)
        else:
            close_price.append(tp_price)
            trade_fee = maker_fee
        if last_state==3 and state==0: #0 short closed
            trade_return.append(0)
        if last_state==4 and state==0: #1 short closed
            trade_return.append((((close_price[-1]-open_price)/close_price[-1])*-100)-trade_fee)
        return_perc.append(return_perc[-1]+trade_return[-1])
        if trade_return[-1]>0:
            win_return.append(trade_return[-1])
            last_win_time = time
        elif trade_return[-1]<0:
            lose_return.append(trade_return[-1])
            last_lose_time = time


for x in return_perc: #Calculate max downtrend
    if x>max_return:
        max_return=x
    trend = max_return-x
    if trend>max_downtrend:
        max_downtrend = trend

if max_downtrend==0: #prevent /0 errors
    max_downtrend=0.01
if len(trade_return)==0:
    trade_return.append(0)
        
return_rate = (return_perc[-1]-100)/(minutes[-1]/1440)
win_perc = (len(win_return)/len(trade_return))*100
lose_perc = (len(lose_return)/len(trade_return))*100
trade_per_day = len(trade_return)/(minutes[-1]/1440)
recover_rate = max_downtrend/(return_rate+0.0001)
    

for x in trade_return: #Calculate winning and losing streaks
    if x>0:
        if winning == 0:
            win_count.append(0)
        win_count[-1]=win_count[-1]+1
        winning = 1
        losing = 0
    elif x<0:
        if losing == 0:
            lose_count.append(0)
        lose_count[-1]=lose_count[-1]+1
        losing = 1
        winning = 0

results = {
    "historical_time": historical_time,"historical_return_perc": historical_return_perc,
    "historical_price_low": historical_price_low,"historical_price_high": historical_price_high,
    "historical_average_1": historical_average_1,"historical_average_2": historical_average_2,"historical_average_3": historical_average_3,
    "historical_indicator_1": historical_indicator_1,"historical_indicator_2": historical_indicator_2,
    "open_long_time": open_long_time,"open_long_price": open_long_price,
    "open_short_time": open_short_time,"open_short_price": open_short_price,
    "open_price": open_price,"close_time": close_time,"close_price": close_price,"candle_open": candle_open,
    "ma_1": ma_1, "derive_rate": derive_rate, "plot_mode": plot_mode
}
plot(results)

print("Dataset length(days):", round((minutes[-1]/1440),2))
print("Number of trades:",len(trade_return))
print("Number of wins:",len(win_return))
print("Number of loses:",len(lose_return))
print("Number unopened:",len(trade_return)-(len(win_return)+len(lose_return)))
print("\n")
print("Average trade return(%):", round(sum(trade_return)/len(trade_return),2))
print("Best win(%):", round(max(win_return),2))
print("Worst loss(%):", round(min(lose_return),2))
print("Average win(%):", round(sum(win_return)/len(win_return),2))
print("Average loss(%):", round(sum(lose_return)/len(lose_return),2))

print("Most wins in row:", max(win_count))
print("Most loses in row:", max(lose_count))
print("Worst downtrend(%):", round(max_downtrend,2))

print("\n")
print("Win rate(%):",round(win_perc,2))
print("Lose rate(%):",round(lose_perc,2))
print("Unopened rate(%):",round(100-win_perc-lose_perc,2))
print("W/L rate(%):",round(win_perc/(win_perc+lose_perc)*100,2))
print("R/R ratio:",round((sum(win_return)/len(win_return))/(sum(lose_return)/-len(lose_return)),2))
print("Average # of trades per day:",round(trade_per_day,2))
print("Average return per day(%):",round(return_rate,3))
print("Recover rate(days):", round(recover_rate,3))
print("Time since last open(days)",round((unix[-1]-open_time)/86400,3))
    
    