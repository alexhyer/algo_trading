# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 13:26:54 2022

@author: Alex Hyer
https://github.com/alexhyer
"""
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np
import math

def open_conditions(settings, state):
    current_time = state["time"]
    open_trade = state["open_trade"]
    win_close_time = state["win_close_time"]
    be_close_time = state["be_close_time"]
    lose_close_time = state["lose_close_time"]
    slope_1 = state["slope_1"]
    slope_2 = state["slope_2"]

    if (win_close_time+settings["win_wait_time"]<=current_time) and (be_close_time+settings["be_wait_time"]<=current_time) and (lose_close_time+settings["lose_wait_time"]<=current_time) and (slope_1>=settings["slope_1_open_threshold"]) and (slope_2>=settings["slope_2_open_threshold"]) and (open_trade==0):
        long_open_condition = 1
    else:
        long_open_condition = 0
    if (win_close_time+settings["win_wait_time"]<=current_time) and (be_close_time+settings["be_wait_time"]<=current_time) and (lose_close_time+settings["lose_wait_time"]<=current_time) and (slope_1<=-settings["slope_1_open_threshold"]) and (slope_2<=-settings["slope_2_open_threshold"]) and (open_trade==0):
        short_open_condition = 1
    else:
        short_open_condition = 0
    return (long_open_condition, short_open_condition)
    

def close_conditions(settings, state):
    current_price = state["current_price"]
    open_price = state["open_price"]
    close_trade_price = state["close_trade_price"]
    long = state["long"]
    short = state["short"]
    slope_1 = state["slope_1"]
    slope_2 = state["slope_2"]
    candle_low = state["candle_low"]
    candle_high = state["candle_high"]
    
    if long==1:
        perc = ((current_price-open_price)/current_price)*100
    elif short==1:
        perc = ((current_price-open_price)/current_price)*-100
            
    if perc < settings["z_1"]:
        slope_1_close_threshold = settings["z0_1"]
        slope_2_close_threshold = settings["z0_2"]
    elif settings["z_1"] <= perc < settings["z_2"]:
        slope_1_close_threshold = settings["z1_1"]
        slope_2_close_threshold = settings["z1_2"]
    elif settings["z_2"] <= perc < settings["z_3"]:
        slope_1_close_threshold = settings["z2_1"]
        slope_2_close_threshold = settings["z2_2"]
    elif settings["z_3"] <= perc < settings["z_4"]:
        slope_1_close_threshold = settings["z3_1"]
        slope_2_close_threshold = settings["z3_2"]
    elif settings["z_4"] <= perc:
        slope_1_close_threshold = settings["z4_1"]
        slope_2_close_threshold = settings["z4_2"]
    
    long_close_conditions_met = 0
    short_close_conditions_met = 0
    
    if long==1:
        if (current_price<=close_trade_price) or (slope_2<=slope_2_close_threshold) or (slope_1<=slope_1_close_threshold) or (candle_low<=math.floor(open_price*(1-settings["stop_loss"]/100))):
            long_close_conditions_met = 1
    elif short==1:
        if (current_price>=close_trade_price) or (slope_2>=-slope_2_close_threshold) or (slope_1>=-slope_1_close_threshold) or (candle_high>=math.ceil(open_price*(1-settings["stop_loss"]/-100))):
            short_close_conditions_met = 1
                
    return (long_close_conditions_met, short_close_conditions_met)
    
def plot(settings, results):
    ma_1 = settings["ma_1"]
    derive_rate = settings["derive_rate"]
    plot_mode = settings["plot_mode"]
    plot_indicators = settings["plot_indicators"]
    plot_trades = settings["plot_trades"]
    print_win = settings["print_win"]
    print_be = settings["print_be"]
    print_lose = settings["print_lose"]
    stop_loss = settings["stop_loss"]
    historical_time = results["historical_time"]
    historical_price = results["historical_price"]
    historical_average_1 = results["historical_average_1"]
    historical_average_2 = results["historical_average_2"]
    historical_return_perc = results["historical_return_perc"]
    open_time = results["open_time"]
    open_price = results["open_price"]
    close_time = results["close_time"]
    close_price = results["close_price"]
    long_short = results["long_short"]
    candle_open = results["candle_open"]
    open_x = results["open_x"]
    close_x = results["close_x"]
    win_be_lose = results["win_be_lose"]
    trade_length = results["trade_length"]
    
    if plot_mode==1:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.subplots_adjust(right=0.88)
        ax.plot(historical_time, historical_price, linewidth=0.3, color="black")
        ax.set_title("Price Action")
        ax.set_xlabel("Time(m)")
        ax.set_ylabel("Price($)")
        ax.grid(visible=True)
        if plot_indicators==1:
            ax.plot(historical_time, historical_average_1, linewidth=0.3, color="purple")
            ax.plot(historical_time, historical_average_2, linewidth=0.3, color="orange")
        if plot_trades==1:
            for x in range(len(close_time)):
                ax.plot(close_time[x], close_price[x], marker="o", markersize=3, markeredgecolor="blue", markerfacecolor="blue")
            for x in range(len(open_time)):
                if long_short[x]==0 and plot_mode==1:
                    ax.plot(open_time[x], open_price[x], marker="o", markersize=3, markeredgecolor="green", markerfacecolor="green")
                elif long_short[x]==1 and plot_mode==1:
                    ax.plot(open_time[x], open_price[x], marker="o", markersize=3, markeredgecolor="red", markerfacecolor="red")
        
        axstart = plt.axes([0.96, 0.17, 0.03, 0.65])
        axwidth = plt.axes([0.9, 0.17, 0.03, 0.65])
        end_time_slider = Slider(axstart, 'Move', 0.0, historical_time[-1], historical_time[-1], orientation="vertical")
        width_slider = Slider(axwidth, 'Zoom', 500, historical_time[-1], historical_time[-1], orientation="vertical")
        end_time_slider.valtext.set_visible(False)
        width_slider.valtext.set_visible(False)
    
        def update1(val):
            end_time = round(end_time_slider.val)
            width = round(width_slider.val)
            min_x = end_time-width
            offset = ma_1+derive_rate
            if min_x<offset:
                min_x=offset
            end_time_slider.valmin = width
            width_slider.valmax = end_time
            ax.set_xlim([min_x, end_time])
            ymin = min(historical_price[min_x-offset:end_time])
            ymax = max(historical_price[min_x-offset:end_time])
            ax.set_ylim(ymin-100, ymax+100)
            fig.canvas.draw_idle()
    
        update1(0)
        end_time_slider.on_changed(update1)
        width_slider.on_changed(update1)
             
    elif plot_mode==2:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)  
        fig.subplots_adjust(right=0.88)
        ax1.plot(historical_time, historical_price, linewidth=0.3, color="black")
        ax2.plot(historical_time, historical_return_perc, linewidth=0.8, color="black")
        ax1.set_title("Price action")
        ax2.set_title("Percent return")
        ax.set_xlabel("Time(m)")
        ax1.set_ylabel("Price($)")
        ax2.set_ylabel("Return(%)")
        ax.spines['left'].set_color('none')
        ax.spines['right'].set_color('none')
        ax1.set_xticklabels([])
        ax.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
        ax1.grid(visible=True)
        ax2.grid(visible=True)
        if plot_indicators==1:
            ax1.plot(historical_time, historical_average_1, linewidth=0.3, color="purple")
            ax1.plot(historical_time, historical_average_2, linewidth=0.3, color="orange")
        if plot_trades==1:
            for x in range(len(close_time)):
                ax1.plot(close_time[x], close_price[x], marker="o", markersize=3, markeredgecolor="blue", markerfacecolor="blue")
            for x in range(len(open_time)):
                if long_short[x]==0:
                    ax1.plot(open_time[x], open_price[x], marker="o", markersize=3, markeredgecolor="green", markerfacecolor="green")
                elif long_short[x]==1:
                    ax1.plot(open_time[x], open_price[x], marker="o", markersize=3, markeredgecolor="red", markerfacecolor="red")
                
        axstart = plt.axes([0.96, 0.17, 0.03, 0.65])
        axwidth = plt.axes([0.9, 0.17, 0.03, 0.65])
        end_time_slider = Slider(axstart, 'Move', 0.0, historical_time[-1], historical_time[-1], orientation="vertical")
        width_slider = Slider(axwidth, 'Zoom', 500, historical_time[-1], historical_time[-1], orientation="vertical")
        end_time_slider.valtext.set_visible(False)
        width_slider.valtext.set_visible(False)
    
        def update2(val):
            end_time = round(end_time_slider.val)
            width = round(width_slider.val)
            min_x = end_time-width
            offset = ma_1+derive_rate
            if min_x<offset:
                min_x=offset
            end_time_slider.valmin = width
            width_slider.valmax = end_time
            ax1.set_xlim([min_x, end_time])
            ax2.set_xlim([min_x, end_time])
            ymin1 = min(historical_price[min_x-offset:end_time-offset])
            ymax1 = max(historical_price[min_x-offset:end_time-offset])
            ymin2 = min(historical_return_perc[min_x-offset:end_time-offset])
            ymax2 = max(historical_return_perc[min_x-offset:end_time-offset])
            ax1.set_ylim(ymin1-100, ymax1+100)
            ax2.set_ylim(ymin2-1, ymax2+1)
            fig.canvas.draw_idle()
    
        update2(0)
        end_time_slider.on_changed(update2)
        width_slider.on_changed(update2)
        
        
    elif plot_mode==3:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.subplots_adjust(right=0.88)
        ax.set_title("Trade Performance After Open")
        ax.set_xlabel("Time(m)")
        ax.set_ylabel("Return(%)")
        ax.grid(visible=True)
        perc_history = []
        
        for x in range(len(close_time)):
            prices_list = []
            perc_list = []
            time_list = []
            prices_list = candle_open[int(open_x[x]):int(close_x[x])]
            for i in range(len(prices_list)):
                perc_list.append(((prices_list[i]-open_price[x])/(prices_list[i]))*100)
                if long_short[x]==1:
                    perc_list[i] = -perc_list[i]
            perc_history.append(perc_list)
            p_len = len(perc_list)
            time_list = np.linspace(0, p_len, p_len)
            if win_be_lose[x]==0 and print_win==1:
                ax.plot(time_list, perc_list, linewidth=0.4, color="green")
            if win_be_lose[x]==1 and print_be==1:
                ax.plot(time_list, perc_list, linewidth=0.4, color="black")
            if win_be_lose[x]==2 and print_lose==1:
                ax.plot(time_list, perc_list, linewidth=0.4, color="red")
            
        axstart = plt.axes([0.96, 0.17, 0.03, 0.65])
        axwidth = plt.axes([0.9, 0.17, 0.03, 0.65])
        start_time_slider = Slider(axstart, 'Move', 0, max(trade_length), max(trade_length), orientation="vertical")
        width_slider = Slider(axwidth, 'Zoom', 10, max(trade_length), max(trade_length), orientation="vertical")
        start_time_slider.valtext.set_visible(False)
        width_slider.valtext.set_visible(False)
        
        perc_max = [0]*int(max(trade_length))
        for x in range(len(perc_history)):
            for i in range(len(perc_history[x])):
                if perc_history[x][i]>perc_max[i]:
                    perc_max[i]=perc_history[x][i]
    
        def update3(val):
            start_time = round(start_time_slider.val)
            width = round(width_slider.val)
            min_x = int(max(trade_length)-start_time)
            max_x = int(width+(max(trade_length)-start_time))
            ax.set_xlim([min_x, max_x])
            ymin = -stop_loss-0.2
            ymax = max(perc_max[min_x:max_x])+0.2
            start_time_slider.valmin = width
            width_slider.valmax = start_time
            ax.set_ylim(ymin, ymax)
            fig.canvas.draw_idle()
    
        update3(0)
        start_time_slider.on_changed(update3)
        width_slider.on_changed(update3)









