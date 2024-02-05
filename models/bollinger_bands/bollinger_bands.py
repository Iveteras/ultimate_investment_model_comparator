# This is exactly the same script as main.ipynb. Just in shape of a function to make testes

def bb_model(asset, stop_loss_time):
    
    import pandas as pd
    import numpy as np 
    import yfinance as yf 
    from datetime import date, timedelta
    
    ######################### IMPORTING DATA #########################

    end_date = date.today()
    start_date = end_date - timedelta(365*20)

    df = yf.download(asset, start_date, end_date)
    df = df.dropna()

    ######################### Calculating bollinger bands #########################

    # Moving average and standard deviation

    df['Moving average'] = df['Adj Close'].rolling(window = 20).mean()
    df['Std dev'] = df['Adj Close'].rolling(window = 20).std()

    # Top and botton band

    df['Top band'] = df['Moving average'] + 2 * df['Std dev']
    df['Botton band'] = df['Moving average'] - 2 * df['Std dev']

    df = df.dropna()

    ######################### Long position #########################
    
    def long_position_dates(df, stop_loss_time):
        buy_dates = []
        sell_dates = []

        for i in range(1, len(df)): # Taking away the first element

            price_day_before = df.iloc[i-1]['Adj Close']
            price = df.iloc[i]['Adj Close']
            band_day_before = df.iloc[i-1]['Top band']
            band = df.iloc[i]['Top band']

            # This indicate that price crossed top band
            if (price_day_before < band_day_before) & (price >= band):

                try: # This is for those cases that it is on te last element of df
                    buy_dates.append(df.iloc[i+1].name) # buy next day

                    for j in range(1, stop_loss_time+1): # Stop loss of x days or crossed below
                        
                        try:
                            new_price_day_before = df.iloc[i+j-1]['Adj Close']
                            new_price = df.iloc[i+j]['Adj Close']
                            new_band_day_before = df.iloc[i+j-1]['Top band']
                            new_band = df.iloc[i+j]['Top band']

                            if (new_price_day_before > new_band_day_before) & (new_price <= new_band):
                                sell_dates.append(df.iloc[i+j+1].name) # sell next day
                                break
                                
                            elif j == stop_loss_time:
                                try:
                                    sell_dates.append(df.iloc[i+j+1].name)
                                except:
                                    sell_dates.append(df.iloc[-1].name) # this is for operations in the nearest x days
                        
                        except:
                            buy_dates.remove(df.iloc[i+1].name)
                except:
                    'The last element error :('
                    
        return [buy_dates, sell_dates]
    
    lp_dates = long_position_dates(df, stop_loss_time)

    lp_buy_dates = lp_dates[0]
    lp_sell_dates = lp_dates[1]

    ######################### Short position #########################

    def short_position_dates(df, stop_loss_time):
        buy_dates = []
        sell_dates = []

        for i in range(1, len(df)): # Taking away the first element

            price_day_before = df.iloc[i-1]['Adj Close']
            price = df.iloc[i]['Adj Close']
            band_day_before = df.iloc[i-1]['Botton band']
            band = df.iloc[i]['Botton band']

            if (price_day_before > band_day_before) & (price <= band):

                try: # This is for those cases that it is on te last element of df
                    sell_dates.append(df.iloc[i+1].name) # sell the next day

                    for j in range(1,stop_loss_time+1):

                        new_short_day_before = df.iloc[i+j-1]['Adj Close']
                        new_short = df.iloc[i+j]['Adj Close']
                        new_day_before = df.iloc[i+j-1]['Botton band']
                        new_day = df.iloc[i+j]['Botton band']

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

        return [buy_dates, sell_dates]
    
    sp_dates = short_position_dates(df, stop_loss_time)

    sp_buy_dates = sp_dates[0]
    sp_sell_dates = sp_dates[1]

    ######################### Comparison with buy and hold #########################

    buy_n_hold_return = ((df.iloc[-1]['Adj Close'] - df.iloc[0]['Adj Close']) / df.iloc[0]['Adj Close']) * 100

    def find_returns(df, b_dates, s_dates):

        operation_returns = []

        for i in range(len(b_dates)):
            
            buy_price = df.loc[b_dates[i]]['Adj Close']
            sell_price = df.loc[s_dates[i]]['Adj Close']

            operation_return = (sell_price - buy_price) / buy_price

            operation_returns.append(operation_return)
        
        return operation_returns

    lp_return = find_returns(df, lp_buy_dates, lp_sell_dates)
    sp_return = find_returns(df,sp_buy_dates, sp_sell_dates)

    lp_cumulative_return = ((np.cumprod(1 + np.array(lp_return)) - 1) * 100)[-1]
    sp_cumulative_return = ((np.cumprod(1 + np.array(sp_return)) - 1) * 100)[-1]
    lp_sp_cumulative_return = np.mean([lp_cumulative_return, sp_cumulative_return])

    return [buy_n_hold_return, lp_cumulative_return, sp_cumulative_return, lp_sp_cumulative_return]