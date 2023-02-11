# algo_trading
Backtest and apply trading strategies on BTC using python

Single entry:
Each trade has only a single entry level with a set offset from where the trade triggers

DCA entry:
Each trade has three entry levels, each a defined amount and percentage from where the trade triggers 

In the backtests files are the following scripts:

Single/DCA_backtest:
This is the main backtest file which outputs the needed pickle files to run the apps.

Single/DCA_bots:
Here the settings, indicators, and open conditions are defined for each strategy.

Single/DCA_lightning_backtest:
This is where new strategies can be developed as the backtest is looped to find the best possible settings.

Single/DCA_plotting_backtest:
This script outputs an interactive plot where the historical trades and performance can be visualized

These algos define their risk by looking at their worst historical performance. This can be scaled to whatever level is desired via leverage and position sizing. No matter how you use this you bear all financial responsibility.
