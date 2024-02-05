# This is exactly the same script as main.ipynb. Just in shape of a function to make testes

def rsi_model(asset, stop_loss_time):
    
    import pandas as pd
    import numpy as np 
    import yfinance as yf 
    from datetime import date, timedelta
    
    ######################### IMPORTING DATA #########################

    end_date = date.today()
    start_date = end_date - timedelta(365*20)

    df = yf.download(asset, start_date, end_date)
    df = df.dropna()

    ######################### Calculating asset returns #########################

    df['Return'] = df['Adj Close'].pct_change()
    df = df.dropna()

    ######################### Calculating RSI #########################

    df['Positive Returns'] = df['Return'].apply(lambda x: x if x > 0 else 0)
    df['Negative Returns'] = df['Return'].apply(lambda x: x*-1 if x <0 else 0)

    df['PAR'] = df['Positive Returns'].rolling(window = 22).mean()
    df['NAR'] = df['Negative Returns'].rolling(window = 22).mean()

    df = df.dropna()

    df['RSI'] = (100 - 100 / (1 + df['PAR']/df['NAR']))

    ######################### Long position #########################

    def long_position_dates(df, stop_loss_time):
        buy_dates = []
        sell_dates = []

        for i in range(1, len(df)): # Taking away the first element

            rsi_day_before = df.iloc[i-1]['RSI']
            rsi_today = df.iloc[i]['RSI']

            # This indicate that RSI crossed above 30
            if (rsi_day_before < 30) & (rsi_today >= 30):

                try: # This is for those cases that it is on te last element of df
                    buy_dates.append(df.iloc[i+1].name) # buy next day

                    for j in range(1, stop_loss_time+1): # Stop loss of x days or crossed above 70
                        
                        try:
                            new_rsi_day_before = df.iloc[i+j-1]['RSI']
                            new_rsi_today = df.iloc[i+j]['RSI']

                            if (new_rsi_day_before < 70) & (new_rsi_today >= 70):
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

    lp_dates = long_position_dates(df, 30)

    lp_buy_dates = lp_dates[0]
    lp_sell_dates = lp_dates[1]

    ######################### Short position #########################

    def short_position_dates(df, stop_loss_time):
        buy_dates = []
        sell_dates = []

        for i in range(1, len(df)): # Taking away the first element

            rsi_day_before = df.iloc[i-1]['RSI']
            rsi_today = df.iloc[i]['RSI']
            
            # This indicate that RSI crossed below 70
            if (rsi_day_before > 70) & (rsi_today <= 70):

                try: # This is for those cases that it is on te last element of df

                    sell_dates.append(df.iloc[i+1].name) # Sell next day

                    for j in range(1, stop_loss_time+1): # Stop loss of x days or crossed below 20
                        
                        try:
                            new_rsi_day_before = df.iloc[i+j-1]['RSI']
                            new_rsi_today = df.iloc[i+j]['RSI']

                            if (new_rsi_day_before > 20) & (new_rsi_today <= 20):
                                buy_dates.append(df.iloc[i+j+1].name) # buy next day
                                break
                                
                            elif j == stop_loss_time:
                                try:
                                    buy_dates.append(df.iloc[i+j+1].name)
                                except:
                                    buy_dates.append(df.iloc[-1].name) # this is for operations in the nearest x days
                        
                        except:
                            sell_dates.remove(df.iloc[i+1].name)
                            
                except:
                    'The last element error :('

        return [buy_dates, sell_dates]
    
    sp_dates = short_position_dates(df, 30)

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











