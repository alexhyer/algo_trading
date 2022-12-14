# alice
A trend following trading algorithm

Designed to run via the Bitget trading api found here:
https://github.com/BitgetLimited/v3-bitget-api-sdk

There are two main scripts labeled as alice_app and alice_backtest.
Alice backtesting is for testing and analysing trading plans on historical data.
Alice app is where that plan is applied to live data.

The trading plan currently provided is tuned for bitcoin price action only but could run on any coin supported by bitget futures if retuned. 

It's designed to boot off the btc_price_data.txt file when it detects a timing error or is told to do so manually. The txt should be automatically kept up to date. If it's not updated or the data has incorrect timing it will stop running until it detects correct timing.

If you decide to setup and run alice_app_email_updates it will send you an email if a timing error is detected. You can also get updates when trades are opened and closed using the trade_alerts variable. 

Emails come from courier's email service which can be found here:
https://www.courier.com/

For a cloud hosting service I have found PythonAnywhere to be a good option as it's easy for beginners to use compered to others while having high reliability. 

With this setup you can run low or high risk depending on the leverage you choose. No matter how you use this you bear all financial responsibility.
