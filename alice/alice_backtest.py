# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:13:41 2022

@author: Alex Hyer
https://github.com/alexhyer
"""
from alice_backtest_funcs import open_conditions
from alice_backtest_funcs import close_conditions
from alice_backtest_funcs import plot
import random
import math

best_score = 0
winning = 0
losing = 0

win_count = []
lose_count = []

with open("price_logging/btc_price_data.txt") as f:
    contents = f.read()
bruh1 = contents.replace("\n", "\t")
bruh2 = bruh1.split("\t")
minutes = bruh2[::6]
epoch = bruh2[1::6]
candle_open = bruh2[2::6]
candle_low = bruh2[4::6]
candle_high = bruh2[5::6]
length = len(minutes)

minutes.reverse()
epoch.reverse()
candle_open.reverse()
candle_low.reverse()
candle_high.reverse()
minutes = list(map(float, minutes))
epoch = list(map(float, epoch))
candle_open = list(map(float, candle_open))
candle_low = list(map(float, candle_low))
candle_high = list(map(float, candle_high))

randomizer_testing = 0 #If 1 loops backtesting looking for best scored trading plan
tuning_ratio = 2 #Percent worst downtrend worth giving up for percent per day
min_trades_per_day = 0.6 #Min average trades per day to be counted as best score

be_tolerance = 0.05 #0.05
trade_fee = 0.06 #0.06
compound_interest = 0 #If 1 profits used in next trade
lev = 1

plot_mode = 2 #0-3
plot_trades = 1
plot_indicators = 1

#Plot mode 3
print_win = 1
print_be = 1
print_lose = 1

# Current settings:
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
win_wait_time = 63 #63
be_wait_time = 84 #84
lose_wait_time = 75 #75
stop_loss = 0.16 #0.16
trailing_stop = 2.3 #2.3
percent_in_profit = 1.8 #1.8
move_stop = 1.17 #1.17

tp_level = 1.85 #1.85
tp_amount = 0 #0

while 1:
    if randomizer_testing==1:
        ma_1 = round(random.uniform(40, 300))
        ma_2 = round(random.uniform(10, ma_1))
        derive_rate = round(random.uniform(4, 20))
        slope_1_open_threshold = round(random.uniform(0.5, 5),2)
        slope_2_open_threshold = round(random.uniform(0.5, 5),2)
        win_wait_time = round(random.uniform(5, 100))
        be_wait_time = round(random.uniform(5, 100))
        lose_wait_time = round(random.uniform(5, 100))
        stop_loss = round(random.uniform(0, 0.8),2)
        trailing_stop = round(random.uniform(0.5, 3),2)
        percent_in_profit = round(random.uniform(0.1, 2.5),2)
        move_stop = round(random.uniform(stop_loss, percent_in_profit),2)
        
        z0_1 = round(random.uniform(-4, slope_1_open_threshold),2)
        z0_2 = round(random.uniform(-4, slope_2_open_threshold),2)
        z1_1 = round(random.uniform(-4, slope_1_open_threshold),2)
        z1_2 = round(random.uniform(-4, slope_2_open_threshold),2)
        z2_1 = round(random.uniform(-4, 4),2)
        z2_2 = round(random.uniform(-4, 4),2)
        z3_1 = round(random.uniform(-4, 4),2)
        z3_2 = round(random.uniform(-4, 4),2)
        z4_1 = round(random.uniform(-4, 4),2)
        z4_2 = round(random.uniform(-4, 4),2)
        
        z_1 = round(random.uniform(-stop_loss, -stop_loss+2),2)
        z_2 = round(random.uniform(z_1, z_1+2),2)
        z_3 = round(random.uniform(z_2, z_2+2),2)
        z_4 = round(random.uniform(z_3, z_3+2),2)
        
    if ma_1%2==1: #MA's must be even
        ma_1=ma_1+1
    if ma_2%2==1:
        ma_2=ma_2+1
    
    open_trade=short=long=max_return=max_downtrend=tp=tp_price=close_trade_price=0
    
    slope_1=[]
    slope_2=[]
    average_1=[]
    average_2=[]
    open_price=[]
    close_price=[]
    open_time=[]
    trade_length=[]
    trade_return=[]
    breakeven_return=[]
    return_perc=[]
    long_short=[]
    win_be_lose=[]
    open_x=[]
    close_x=[]
    lose_return=[]
    win_return=[]
    close_time=[]
    win_close_time=[]
    be_close_time=[]
    lose_close_time=[]
    historical_price=[]
    historical_time=[]
    historical_average_1=[]
    historical_average_2=[]
    historical_return_perc=[]

    win_close_time.append(0)
    be_close_time.append(0)
    lose_close_time.append(0)
    return_perc.append(100)
    
    settings = {
      "ma_1": ma_1,
      "ma_2": ma_2,
      "derive_rate": derive_rate,
      "slope_1_open_threshold": slope_1_open_threshold,
      "slope_2_open_threshold": slope_2_open_threshold,
      "stop_loss": stop_loss,
      "trailing_stop": trailing_stop,
      "percent_in_profit": percent_in_profit,
      "move_stop": move_stop,
      "win_wait_time": win_wait_time,
      "be_wait_time": be_wait_time,
      "lose_wait_time": lose_wait_time,
      "z_1": z_1,
      "z_2": z_2,
      "z_3": z_3,
      "z_4": z_4,
      "z0_1": z0_1,
      "z0_2": z0_2,
      "z1_1": z1_1,
      "z1_2": z1_2,
      "z2_1": z2_1,
      "z2_2": z2_2,
      "z3_1": z3_1,
      "z3_2": z3_2,
      "z4_1": z4_1,
      "z4_2": z4_2,
      "plot_mode": plot_mode,
      "plot_trades": plot_trades,
      "plot_indicators": plot_indicators,
      "print_win": print_win,
      "print_be": print_be,
      "print_lose": print_lose,
      "tp_level": tp_level,
      "tp_amount": tp_amount
    }
        
    cut_at_1 = int(ma_1 / 2)
    cut_at_2 = int(ma_2 / 2)
    price_list = candle_open[derive_rate:ma_1+derive_rate]
    
    for x in range(derive_rate): #Initialize variables
        first_half_1 = candle_open[x:cut_at_1+x]
        second_half_1 = candle_open[cut_at_1+x:ma_1+x]
        first_half_2 = candle_open[(ma_1-ma_2)+x:(ma_1-ma_2)+cut_at_2+x]
        second_half_2 = candle_open[(ma_1-ma_2)+cut_at_2+x:ma_1+x]
        average_1.append(((sum(first_half_1) / 1.5) + (sum(second_half_1) / 0.75)) / ma_1)
        average_2.append(((sum(first_half_2) / 1.5) + (sum(second_half_2) / 0.75)) / ma_2)
    
    for x in range(ma_1+derive_rate,length): #Main backtesting loop
        time = minutes[x]
        current_price = candle_open[x]
        price_list.append(current_price)
        price_list.pop(0)
        first_half_1 = price_list[:cut_at_1]
        second_half_1 = price_list[cut_at_1:]
        first_half_2 = price_list[ma_1-ma_2:ma_1-cut_at_2]
        second_half_2 = price_list[ma_1-cut_at_2:]
        average_1.append(((sum(first_half_1) / 1.5) + (sum(second_half_1) / 0.75)) / ma_1)
        average_2.append(((sum(first_half_2) / 1.5) + (sum(second_half_2) / 0.75)) / ma_2)
        average_1.pop(0)
        average_2.pop(0)
        slope_1 = (average_1[-1] - average_1[0]) / derive_rate
        slope_2 = (average_2[-1] - average_2[0]) / derive_rate
    
        historical_price.append(current_price)
        historical_time.append(time)
        historical_average_1.append(average_1[-1])
        historical_average_2.append(average_2[-1])
        historical_return_perc.append(return_perc[-1])
        
        state = {
          "time": time,
          "current_price": current_price,
          "open_trade": open_trade, 
          "long": long, 
          "short": short, 
          "slope_1": slope_1,
          "slope_2": slope_2,
          "close_trade_price": close_trade_price,
          "win_close_time": win_close_time[-1],
          "be_close_time": be_close_time[-1],
          "lose_close_time": lose_close_time[-1],
          "candle_low": candle_low[x],
          "candle_high": candle_high[x]
        }
        
        (long_open_conditions_met, short_open_conditions_met) = open_conditions(settings, state)
    
        if long_open_conditions_met==1:
            open_trade = 1
            long = 1
            open_time.append(time)
            open_price.append(current_price)
            open_x.append(x)
            trailing_stop_price, secure_be_price = open_price[-1]*0.1, open_price[-1]*0.1
            max_trade_price = open_price[-1]
            long_short.append(0)
            max_percent = 0
                    
        elif short_open_conditions_met==1:
            open_trade = 1
            short = 1
            open_time.append(time)
            open_price.append(current_price)
            open_x.append(x)
            trailing_stop_price, secure_be_price = open_price[-1]*10, open_price[-1]*10
            max_trade_price = open_price[-1]
            long_short.append(1)
            max_percent = 0
        
        
        if open_trade == 1:
            state.update({"open_price":open_price[-1]})
            state.update({"open_time":open_time[-1]})
            state.update(long=long, short=short, open_trade=open_trade)
            if long == 1:
                if current_price>max_trade_price:  #Update tailing stop
                    max_trade_price = current_price
                    max_percent = abs(((open_price[-1]-max_trade_price)/open_price[-1])*100)
                    trailing_stop_price = max_trade_price*(1-trailing_stop/100)
                    if max_percent >= percent_in_profit:
                        secure_be_price = (1+(move_stop/100))*open_price[-1]
                if max_percent >= tp_level and tp==0:
                    tp = 1
                    tp_price = current_price
                close_trade_prices = [trailing_stop_price, secure_be_price]
                close_trade_price = max(close_trade_prices)
                        
            elif short == 1:
                if current_price<max_trade_price:  #Update tailing stop
                    max_trade_price = current_price
                    max_percent = abs(((open_price[-1]-max_trade_price)/open_price[-1])*100)
                    if max_percent >= percent_in_profit:
                        secure_be_price = (1+(move_stop/-100))*open_price[-1]
                if max_percent >= tp_level and tp==0:
                    tp = 1
                    tp_price = current_price
                close_trade_prices = [trailing_stop_price, secure_be_price]
                close_trade_price = min(close_trade_prices)
    
            state.update(close_trade_price=close_trade_price)
    
            (long_close_conditions_met, short_close_conditions_met) = close_conditions(settings, state)
    
            if long_close_conditions_met==1:
                if candle_low[x]<=math.floor(open_price[-1]*(1-stop_loss/100)):
                    close_price.append(math.floor(open_price[-1]*(1-stop_loss/100)))
                else:
                    if tp==0:
                        close_price.append(current_price)
                    elif tp==1:
                        close_price.append((current_price*(1-(tp_amount/100)))+((tp_amount/100)*tp_price))
                            
                trade_return.append((((close_price[-1] - open_price[-1])/close_price[-1])*100*lev)-(lev*trade_fee))
                if compound_interest==1:
                    return_perc.append(return_perc[-1]*(1+(trade_return[-1]/100)))
                else:
                    return_perc.append(return_perc[-1]+trade_return[-1])
                close_time.append(time)
                trade_length.append(time-open_time[-1])
                close_x.append(x)
                open_trade = 0
                tp = 0
                long = 0
                if trade_return[-1]>be_tolerance:
                    win_return.append(trade_return[-1])
                    win_close_time.append(time)
                    win_be_lose.append(0)
                elif trade_return[-1]<-be_tolerance:
                    lose_return.append(trade_return[-1])
                    lose_close_time.append(time)
                    win_be_lose.append(2)
                else:
                    breakeven_return.append(trade_return[-1])
                    be_close_time.append(time)
                    win_be_lose.append(1)
                    
            if short_close_conditions_met==1:
                if candle_high[x]>=math.ceil(open_price[-1]*(1-stop_loss/-100)):
                    close_price.append(math.ceil(open_price[-1]*(1-stop_loss/-100)))
                else:
                    if tp==0:
                        close_price.append(current_price)
                    elif tp==1:
                        close_price.append((current_price*(1-(tp_amount/100)))+((tp_amount/100)*tp_price))  
                        
                trade_return.append((((close_price[-1] - open_price[-1])/close_price[-1])*-100*lev)-(lev*trade_fee))
                if compound_interest==1:
                    return_perc.append(return_perc[-1]*(1+(trade_return[-1]/100)))
                else:
                    return_perc.append(return_perc[-1]+trade_return[-1])
                close_time.append(time)
                trade_length.append(time-open_time[-1])
                close_x.append(x)
                open_trade = 0
                tp = 0
                short = 0
                if trade_return[-1]>be_tolerance:
                    win_return.append(trade_return[-1])
                    win_close_time.append(time)
                    win_be_lose.append(0)
                elif trade_return[-1]<-be_tolerance:
                    lose_return.append(trade_return[-1])
                    lose_close_time.append(time)
                    win_be_lose.append(2)
                else:
                    breakeven_return.append(trade_return[-1])
                    be_close_time.append(time)
                    win_be_lose.append(1)
    
    win_perc = (len(win_return)/len(trade_return))*100
    breakeven_perc = (len(breakeven_return)/len(trade_return))*100
    lose_perc = (len(lose_return)/len(trade_return))*100
    return_rate = (return_perc[-1]-100)/(minutes[-1]/1440)
    trade_per_day = len(trade_return)/(minutes[-1]/1440)
    
    for x in return_perc: #Calculate max downtrend
        if x>max_return:
            max_return=x
        trend = max_return-x
        if trend>max_downtrend:
            max_downtrend = trend
            
    if max_downtrend==0:
        max_downtrend=0.01
    score = return_rate/(max_downtrend/tuning_ratio)
    
    if randomizer_testing==0:
        break
    else:
        if score>best_score and trade_per_day>min_trades_per_day:
            best_score=score
            print("ma_1 =",ma_1,"\n"+"ma_2 =",ma_2,"\n"+"derive_rate =",derive_rate)
            print("slope_1_open_threshold =",slope_1_open_threshold,"\n"+"slope_2_open_threshold =",slope_2_open_threshold)
            print("z0_1 =",z0_1,"\n"+"z0_2 =",z0_2,"\n"+"z1_1 =",z1_1,"\n"+"z1_2 =",z1_2,"\n"+"z2_1 =",z2_1,"\n"+"z2_2 =",z2_2)
            print("z3_1 =",z3_1,"\n"+"z3_2 =",z3_2,"\n"+"z4_1 =",z4_1,"\n"+"z4_2 =",z4_2)
            print("z_1 =",z_1,"\n"+"z_2 =",z_2,"\n"+"z_3 =",z_3,"\n"+"z_4 =",z_4)
            print("win_wait_time =",win_wait_time,"\n"+"be_wait_time =",be_wait_time,"\n"+"lose_wait_time =",lose_wait_time)
            print("stop_loss =",stop_loss)
            print("trailing_stop =",trailing_stop,"\n"+"percent_in_profit =",percent_in_profit,"\n"+"move_stop =",move_stop,"\n")
            print("Trades/day:", round(trade_per_day,3),"\n"+"%/day:", round(return_rate,3))
            print("Max down:", round(max_downtrend,3),"\n"+"Score:", round(best_score,3),"\n")


results = {
    "historical_time": historical_time,
    "historical_price": historical_price,
    "historical_average_1": historical_average_1,
    "historical_average_2": historical_average_2,
    "historical_return_perc": historical_return_perc,
    "open_time": open_time,
    "open_price": open_price,
    "close_time": close_time,
    "close_price": close_price,
    "long_short": long_short,
    "candle_open": candle_open,
    "open_x": open_x,
    "close_x": close_x,
    "win_be_lose": win_be_lose,
    "trade_length": trade_length
}
    
plot(settings, results)
        
for x in trade_return: #Calculate winning and losing streaks
    if x>be_tolerance:
        if winning == 0:
            win_count.append(0)
        win_count[-1]=win_count[-1]+1
        winning = 1
        losing = 0
    elif x<-be_tolerance:
        if losing == 0:
            lose_count.append(0)
        lose_count[-1]=lose_count[-1]+1
        losing = 1
        winning = 0

print("Dataset length(days):", round((minutes[-1]/1440),2))
print("Number of trades:",len(trade_return))
print("Number of wins:",len(win_return))
print("Number of loses:",len(lose_return))
print("Number of breakevens:",len(breakeven_return))
print("Avg trade length(min)", round(sum(trade_length)/len(trade_length),2))
print("Longest trade(min)", round(max(trade_length),2))
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
print("Breakeven rate(%):",round(breakeven_perc,2))
print("Lose rate(%):",round(lose_perc,2))
print("W/L ratio:",round((len(win_return)/(len(win_return)+len(lose_return)))*100,1))
print("R/R ratio:",round((sum(win_return)/len(win_return))/(sum(lose_return)/-len(lose_return)),1))
print("Average # of trades per day:",round(trade_per_day,3))
print("Average return per day(%):",round(return_rate,3))
print("Score:", round(score,3))


    
    
    
    
    
    
    
    
