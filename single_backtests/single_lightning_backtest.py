"""
@author: Alex Hyer
https://github.com/alexhyer
"""
import random
import pickle
import decimal
import os

startup=0

name = "single_lightning"

min_trades_day = 0.3
variance_var = 0.05 #High=0.2, low=0.01

ma_1 = 400
ma_2 = 100
ma_3 = 40
derive_rate = 10
stop_loss = 0.5 
take_profit = 1
lose_wait_time = 30000
win_wait_time = 1000

var_1 = 0
var_2 = 0
var_3 = 0
var_4 = 0
var_5 = 0
var_6 = 0
var_7 = 0
var_8 = 0
var_9 = 0 
var_10 = 0 

best_settings = {
    "ma_1": ma_1,"ma_2": ma_2,"ma_3": ma_3,"derive_rate": derive_rate,
    "stop_loss": stop_loss,"take_profit": take_profit,
    "lose_wait_time": lose_wait_time,"win_wait_time": win_wait_time,
    "var_1": var_1,"var_2": var_2,"var_3": var_3,"var_4": var_4,"var_5": var_5,
    "var_6": var_6,"var_7": var_7,"var_8": var_8,"var_9": var_9,"var_10": var_10
}

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
data_length = 1000
length = len(minutes)

while 1:
    ma_1 = best_settings['ma_1'] 
    ma_2 = best_settings['ma_2']  
    ma_3 = best_settings['ma_3']  
    derive_rate = best_settings['derive_rate'] 
    stop_loss = best_settings['stop_loss']  
    take_profit = best_settings['take_profit'] 
    lose_wait_time = best_settings['lose_wait_time']  
    win_wait_time = best_settings['win_wait_time']  
    var_1 = best_settings['var_1']  
    var_2 = best_settings['var_2'] 
    var_3 = best_settings['var_3']  
    var_4 = best_settings['var_4']  
    var_5 = best_settings['var_5'] 
    var_6 = best_settings['var_6']  
    var_7 = best_settings['var_7']  
    var_8 = best_settings['var_8']  
    var_9 = best_settings['var_9']  
    var_10 = best_settings['var_10']  
    
    if startup==1:
        ma_1 = round(random.uniform(ma_1*(1-variance_var), ma_1*(1+variance_var)))
        ma_2 = round(random.uniform(ma_2*(1-variance_var), ma_2*(1+variance_var)))
        ma_3 = round(random.uniform(ma_3*(1-variance_var), ma_3*(1+variance_var)))
        derive_rate = round(random.uniform(derive_rate*(1-variance_var), derive_rate*(1+variance_var)))
        stop_loss = round(random.uniform(stop_loss*(1-variance_var), stop_loss*(1+variance_var)),2)
        take_profit = round(random.uniform(take_profit*(1-variance_var), take_profit*(1+variance_var)),2)
        lose_wait_time = round(random.uniform(lose_wait_time*(1-variance_var), lose_wait_time*(1+variance_var)))
        win_wait_time = round(random.uniform(win_wait_time*(1-variance_var), win_wait_time*(1+variance_var)))
                
        var_1 = round(random.uniform(var_1*(1-variance_var), var_1*(1+variance_var)),abs(decimal.Decimal(str(var_1)).as_tuple().exponent))
        var_2 = round(random.uniform(var_2*(1-variance_var), var_2*(1+variance_var)),abs(decimal.Decimal(str(var_2)).as_tuple().exponent))
        var_3 = round(random.uniform(var_3*(1-variance_var), var_3*(1+variance_var)),abs(decimal.Decimal(str(var_3)).as_tuple().exponent))
        var_4 = round(random.uniform(var_4*(1-variance_var), var_4*(1+variance_var)),abs(decimal.Decimal(str(var_4)).as_tuple().exponent))
        var_5 = round(random.uniform(var_5*(1-variance_var), var_5*(1+variance_var)),abs(decimal.Decimal(str(var_5)).as_tuple().exponent))
        var_6 = round(random.uniform(var_6*(1-variance_var), var_6*(1+variance_var)),abs(decimal.Decimal(str(var_6)).as_tuple().exponent))
        var_7 = round(random.uniform(var_7*(1-variance_var), var_7*(1+variance_var)),abs(decimal.Decimal(str(var_7)).as_tuple().exponent))
        var_8 = round(random.uniform(var_8*(1-variance_var), var_8*(1+variance_var)),abs(decimal.Decimal(str(var_8)).as_tuple().exponent))
        var_9 = round(random.uniform(var_9*(1-variance_var), var_9*(1+variance_var)),abs(decimal.Decimal(str(var_9)).as_tuple().exponent))
        var_10 = round(random.uniform(var_10*(1-variance_var), var_10*(1+variance_var)),abs(decimal.Decimal(str(var_10)).as_tuple().exponent))
        
        lv = [var_1,var_2,var_3,var_4,var_5,var_6,var_7,var_8,var_9,var_10]
        for x in range(len(lv)):
            if lv[x].is_integer():
                lv[x] = round(lv[x])
        var_1,var_2,var_3,var_4,var_5,var_6,var_7,var_8,var_9,var_10 = lv[0],lv[1],lv[2],lv[3],lv[4],lv[5],lv[6],lv[7],lv[8],lv[9]
    
    if ma_1%2==1: #MA's must be even
        ma_1=ma_1+1
    if ma_2%2==1:
        ma_2=ma_2+1
    if ma_3%2==1:
        ma_3=ma_3+1
            
    try:
        best_recover_rate
    except NameError:
        best_recover_rate=100
    
    max_return=max_downtrend=state=open_price=sl_price=tp_price=last_lose_time=last_win_time=winning=losing=0
    #Indicator definition
    indicators = [0,0,0,0,0]
    #Indicator definition
    indicator_1,indicator_2,indicator_3,indicator_4,indicator_5 = indicators[0],indicators[1],indicators[2],indicators[3],indicators[4]

    win_count,lose_count,average_1,average_2,average_3,close_price=([] for i in range(6))
    open_long_price,open_short_price,return_perc,trade_return=([] for i in range(4))
    return_perc.append(100)
    
    cut_at_1,cut_at_2,cut_at_3 = int(ma_1/2),int(ma_2/2),int(ma_3/2)
    price_list = candle_open[0:data_length]
    
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
        
        #Indicators
        indicator_1 = 0
        indicator_2 = 0
        indicator_3 = 0
        indicator_4 = 0
        indicator_5 = 0
        #Indicators
        
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
            if 0==1:
                open_price = price-limit_offset
                sl_price = round(open_price*(1-stop_loss/100))
                tp_price = round(open_price*(1-take_profit/-100))
                state=1
            #Short open conditions:
            if 0==1:
                open_price = price+limit_offset
                sl_price = round(open_price*(1-stop_loss/-100))
                tp_price = round(open_price*(1-take_profit/100))
                state=3
        
        if last_state==0 and state==1: #Long triggered
            open_price = price-limit_offset
            open_time = time
            sl_price = round(open_price*(1-stop_loss/100))
            tp_price = round(open_price*(1-take_profit/-100))
                
        if last_state==0 and state==3: #Short triggered
            open_price = price+limit_offset
            open_time = time
            sl_price = round(open_price*(1-stop_loss/-100))
            tp_price = round(open_price*(1-take_profit/100))
        
        if 1<=last_state<=2 and state==0: #Longs closed
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
                last_win_time = time
            elif trade_return[-1]<0:
                last_lose_time = time


        if 3<=last_state<=4 and state==0: #Shorts closed
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
                last_win_time = time
            elif trade_return[-1]<0:
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
    trade_per_day = len(trade_return)/(minutes[-1]/1440)
    recover_rate = max_downtrend/(return_rate+0.0001)
    
    if 0<recover_rate<best_recover_rate and min_trades_day<=trade_per_day:
        best_recover_rate=recover_rate
        startup=1
        print("ma_1 =",ma_1,"\n"+"ma_2 =",ma_2,"\n"+"ma_3 =",ma_3,"\n"+"derive_rate =",derive_rate)
        print("stop_loss =",stop_loss,"\n"+"take_profit =",take_profit,"\n"+"lose_wait_time =",lose_wait_time,"\n"+"win_wait_time =",win_wait_time,"\n")
        print("var_1 =",var_1,"\n"+"var_2 =",var_2,"\n"+"var_3 =",var_3,"\n"+"var_4 =",var_4,"\n"+"var_5 =",var_5)
        print("var_6 =",var_6,"\n"+"var_7 =",var_7,"\n"+"var_8 =",var_8,"\n"+"var_9 =",var_9,"\n"+"var_10 =",var_10,"\n")
        print("Trades/day:", round(trade_per_day,3),"\n"+"%/day:", round(return_rate,3))
        print("Max down:", round(max_downtrend,3),"\n"+"Recover rate(days):", round(best_recover_rate,3),"\n")
        best_settings = {
            "ma_1": ma_1,"ma_2": ma_2,"ma_3": ma_3,"derive_rate": derive_rate,
            "stop_loss": stop_loss,"take_profit": take_profit,
            "lose_wait_time": lose_wait_time,"win_wait_time": win_wait_time,
            "var_1": var_1,"var_2": var_2,"var_3": var_3,"var_4": var_4,"var_5": var_5,
            "var_6": var_6,"var_7": var_7,"var_8": var_8,"var_9": var_9,"var_10": var_10
        }

    
    