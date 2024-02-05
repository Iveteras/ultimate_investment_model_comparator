# This is exactly the same script as main.ipynb. Just in shape of a function to make testes

def ema_model(asset, stop_loss_time, short_term, long_term):
    
    import pandas as pd
    import numpy as np 
    import yfinance as yf 
    from datetime import date, timedelta
    
    ######################### IMPORTING DATA #########################

    end_date = date.today()
    start_date = end_date - timedelta(365*20)

    df = yf.download(asset, start_date, end_date)
    df = df.dropna()

    ######################### Calculating exponentially weighted moving average (EMA) #########################

    df[f'EMA ({short_term})'] = df['Adj Close'].ewm(span=short_term, adjust=False).mean()
    df[f'EMA ({long_term})'] = df['Adj Close'].ewm(span=long_term, adjust=False).mean()

    df = df.dropna()

    buy_n_hold_return = ((df.iloc[-1]['Adj Close'] - df.iloc[0]['Adj Close']) / df.iloc[0]['Adj Close']) * 100
    ######################### Long position #########################

    def long_position_dates(df, stop_loss_time, short_term, long_term): 
        buy_dates = []
        sell_dates = []

        for i in range(1, len(df)): # Taking away the first element
            
            short_day_before = df.iloc[i-1][f'EMA ({short_term})']
            short_day = df.iloc[i][f'EMA ({short_term})']
            long_day_before = df.iloc[i-1][f'EMA ({long_term})']
            long_day = df.iloc[i][f'EMA ({long_term})']

            # This indicate that EMA short term crossed above long term EMA
            if (short_day_before < long_day_before) & (short_day >= long_day): 

                try: # This is for those cases that it is on te last element of df
                    buy_dates.append(df.iloc[i+1].name) # buy next day

                    for j in range(1,stop_loss_time+1): # Stop loss of x days or crossed below
                        
                        new_short_day_before = df.iloc[i+j-1][f'EMA ({short_term})']
                        new_short = df.iloc[i+j][f'EMA ({short_term})']
                        new_day_before = df.iloc[i+j-1][f'EMA ({long_term})']
                        new_day = df.iloc[i+j][f'EMA ({long_term})']

                        # This indicate that EMA short term crossed below long term EMA
                        if (new_short_day_before > new_day_before) & (new_short <= new_day):

                            sell_dates.append(df.iloc[i+j+1].name) # sell next day
                            break
                            
                        elif j == stop_loss_time:
                            try:
                                sell_dates.append(df.iloc[i+j+1].name)
                            except:
                                sell_dates.append(df.iloc[-1].name) # this is for operations in the nearest x days
                except:
                    'The last element error :('
                    
        return [buy_dates, sell_dates]
    
    lp_date_list = long_position_dates(df, stop_loss_time,short_term, long_term)

    lp_buy_date = lp_date_list[0]
    lp_sell_date = lp_date_list[1]

    ######################### Short position #########################

    def short_position_dates(df, stop_loss_time,short_term, long_term): 
        sell_dates = []
        buy_dates = []

        for i in range(1, len(df)): # Taking away the first element
            
            short_day_before = df.iloc[i-1][f'EMA ({short_term})']
            short_day = df.iloc[i][f'EMA ({short_term})']
            long_day_before = df.iloc[i-1][f'EMA ({long_term})']
            long_day = df.iloc[i][f'EMA ({long_term})']

            # This indicate that EMA short term crossed below long term EMA
            if (short_day_before > long_day_before) & (short_day <= long_day): 
                
                try: # This is for those cases that it is on te last element of df
                    sell_dates.append(df.iloc[i+1].name) # sell next day

                    for j in range(1,stop_loss_time+1): # Stop loss of x days or crossed below

                        new_short_day_before = df.iloc[i+j-1][f'EMA ({short_term})']
                        new_short = df.iloc[i+j][f'EMA ({short_term})']
                        new_day_before = df.iloc[i+j-1][f'EMA ({long_term})']
                        new_day = df.iloc[i+j][f'EMA ({long_term})']

                        # This indicate that EMA short term crossed above long term EMA
                        if (new_short_day_before < new_day_before) & (new_short >= new_day):

                            buy_dates.append(df.iloc[i+j+1].name) # buy next day
                            break
                            
                        elif j == stop_loss_time:
                            try:
                                buy_dates.append(df.iloc[i+j+1].name)
                            except:
                                buy_dates.append(df.iloc[-1].name) # this is for operations in the nearest x days
                except:
                    'The last element error :('
                    
        return [sell_dates, buy_dates]
    
    sp_date_list = short_position_dates(df, stop_loss_time,short_term, long_term)

    sp_sell_date = sp_date_list[0]
    sp_buy_date = sp_date_list[1]

    ######################### Comparison with buy and hold #########################

    def find_returns(df, b_dates, s_dates):

        operation_returns = []

        for i in range(len(b_dates)):
            
            buy_price = df.loc[b_dates[i]]['Adj Close']
            sell_price = df.loc[s_dates[i]]['Adj Close']

            operation_return = (sell_price - buy_price) / buy_price

            operation_returns.append(operation_return)
        
        return operation_returns
    
    lp_return = find_returns(df, lp_buy_date, lp_sell_date)
    sp_return = find_returns(df,sp_buy_date, sp_sell_date)

    lp_cumulative_return = ((np.cumprod(1 + np.array(lp_return)) - 1) * 100)[-1]
    sp_cumulative_return = ((np.cumprod(1 + np.array(sp_return)) - 1) * 100)[-1]
    lp_sp_cumulative_return = np.mean([lp_cumulative_return, sp_cumulative_return])

    return [buy_n_hold_return, lp_cumulative_return, sp_cumulative_return, lp_sp_cumulative_return]