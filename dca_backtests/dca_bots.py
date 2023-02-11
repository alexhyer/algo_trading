"""
@author: Alex Hyer
https://github.com/alexhyer
"""

import pickle

settings_1 = """
ma_1 = 400
ma_2 = 100
ma_3 = 40
derive_rate = 10
dca_amount_1 = 15 
dca_amount_2 = 30 
dca_amount_3 = 55
dca_perc_1 = 0.1
dca_perc_2 = 0.1
dca_perc_3 = 0.1
stop_loss = 0.1
take_profit = 1
lose_wait_time = 4000
win_wait_time = 0 

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
"""
indicator_type_1 = "indicators = [0,0,0,0,0]"
indicator_calc_1 = """
indicator_1 = 0
indicator_2 = 0
indicator_3 = 0
indicator_4 = 0
indicator_5 = 0
"""
open_conditions_1 = {
    'long': '0==1',
    'short': '0==1'
}

dca_bot_1 = [settings_1,indicator_type_1,indicator_calc_1,open_conditions_1]

dca_bots_data = [dca_bot_1]

with open("dca_bots_data.pickle", "wb") as f:
    pickle.dump(dca_bots_data, f)
    
    
