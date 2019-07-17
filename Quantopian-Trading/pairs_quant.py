import numpy as np

#initialize - schedule function
def initialize(context):
    schedule_function(check_pairs,date_rules.every_day(),time_rules.market_close(minutes=60))
    
    context.aa = sid(45971)
    context.ual = sid(28051)
    
    context.long_on_spread = False
    context.shorting_spread = False

#check_pairs
def check_pairs(context,data):
    
    aa = context.aa
    ual = context.ual
    
    prices = data.history([aa,ual],'price',30,'1d')
    
    short_prices = prices.iloc[-1:]
    
    # SPREAD
    mavg_30 = np.mean(prices[aa] - prices[ual])
    std_30 = np.std(prices[aa] - prices[ual])
    
    mavg_1 = np.mean(short_prices[aa] - short_prices[ual])
    
    if std_30 > 0:
        zscore = (mavg_1 - mavg_30)/std_30
        
        if zscore > 1.0 and not context.shorting_spread:
            # SPREAD = AA - UAL
            # This implies that American Airlines is overvalued and its price will come down ,short the shares
            order_target_percent(aa,-0.5)
            order_target_percent(ual,0.5)
            context.shorting_spread = True
            context.long_on_spread = False
            
        elif zscore < 1.0 and not context.long_on_spread:
            # This implies that United Airlines is overvalued ,short it
            order_target_percent(ual,-0.5)
            order_target_percent(aa,0.5)
            context.shorting_spread = False
            context.long_on_spread = True
            
        elif abs(zscore) < 0.1:
            order_target_percent(aa,0)
            order_target_percent(ual,0)
            context.shorting_spread = False
            context.long_on_spread = True
            
        record(z_score = zscore)