"""
@author: Alex Hyer
https://github.com/alexhyer
"""
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button

def plot(results):
    ma_1 = results["ma_1"]
    derive_rate = results["derive_rate"]
    plot_mode = results["plot_mode"]
    historical_time = results["historical_time"]
    historical_price_low = results["historical_price_low"]
    historical_price_high = results["historical_price_high"]
    historical_average_1 = results["historical_average_1"]
    historical_average_2 = results["historical_average_2"]
    historical_average_3 = results["historical_average_3"]
    historical_indicator_1 = results["historical_indicator_1"]
    historical_indicator_2 = results["historical_indicator_2"]
    historical_return_perc = results["historical_return_perc"]
    open_long_time = results["open_long_time"]
    open_short_time = results["open_short_time"]
    open_long_price = results["open_long_price"]
    open_short_price = results["open_short_price"]
    close_time = results["close_time"]
    close_price = results["close_price"]
    candle_open = results["candle_open"]
    
    if plot_mode==1:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.subplots_adjust(right=0.88)
        ax.plot(historical_time, historical_price_low, linewidth=0.3, color="black")
        ax.plot(historical_time, historical_price_high, linewidth=0.3, color="black")
        ax.set_title("Price Action")
        ax.set_xlabel("Time(m)")
        ax.set_ylabel("Price($)")
        ax.grid(visible=True)
        ax.plot(historical_time, historical_average_1, linewidth=0.4, color="purple")
        ax.plot(historical_time, historical_average_2, linewidth=0.4, color="purple")
        ax.plot(historical_time, historical_indicator_1, linewidth=0.4, color="red")
        ax.plot(historical_time, historical_indicator_2, linewidth=0.4, color="green")
        
        for x in range(len(open_long_time)):
            ax.plot(open_long_time[x], open_long_price[x], marker="o", markersize=3, markeredgecolor="green", markerfacecolor="green")
        for x in range(len(open_short_time)):
            ax.plot(open_short_time[x], open_short_price[x], marker="o", markersize=3, markeredgecolor="red", markerfacecolor="red")
        for x in range(len(close_time)):
            ax.plot(close_time[x], close_price[x], marker="o", markersize=3, markeredgecolor="blue", markerfacecolor="blue")
             
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
            ymin = min(candle_open[min_x-offset:end_time])
            ymax = max(candle_open[min_x-offset:end_time])
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
        ax1.plot(historical_time, historical_price_low, linewidth=0.3, color="black")
        ax1.plot(historical_time, historical_price_high, linewidth=0.3, color="black")
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
        
        ax1.plot(historical_time, historical_average_1, linewidth=0.4, color="black")
        ax1.plot(historical_time, historical_average_2, linewidth=0.4, color="purple")
        ax1.plot(historical_time, historical_average_3, linewidth=0.4, color="blue")
        ax1.plot(historical_time, historical_indicator_1, linewidth=0.4, color="red")
        ax1.plot(historical_time, historical_indicator_2, linewidth=0.4, color="green")
        
        for x in range(len(open_long_time)):
            ax1.plot(open_long_time[x], open_long_price[x], marker="o", markersize=3, markeredgecolor="green", markerfacecolor="green")
        for x in range(len(open_short_time)):
            ax1.plot(open_short_time[x], open_short_price[x], marker="o", markersize=3, markeredgecolor="red", markerfacecolor="red")
        for x in range(len(close_time)):
            ax1.plot(close_time[x], close_price[x], marker="o", markersize=3, markeredgecolor="blue", markerfacecolor="blue")
                    
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
            ymin1 = min(historical_price_low[min_x-offset:end_time-offset])
            ymax1 = max(historical_price_high[min_x-offset:end_time-offset])
            ymin2 = min(historical_return_perc[min_x-offset:end_time-offset])
            ymax2 = max(historical_return_perc[min_x-offset:end_time-offset])
            ax1.set_ylim(ymin1-100, ymax1+100)
            ax2.set_ylim(ymin2-1, ymax2+1)
            fig.canvas.draw_idle()
        
        update2(0)
        end_time_slider.on_changed(update2)
        width_slider.on_changed(update2)




