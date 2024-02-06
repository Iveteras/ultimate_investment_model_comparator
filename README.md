# Investment model comparator

## About 

This project consists in compare four investment models used in technical analysis and measure all the returns of each model.<br>
Models:
- [RSI](https://github.com/Iveteras/ultimate_investment_model_comparator/blob/main/models/rsi/main.ipynb) (Relative Strength Index);
- [Bollinger bands](https://github.com/Iveteras/ultimate_investment_model_comparator/blob/main/models/bollinger_bands/main.ipynb)
- [EMA](https://github.com/Iveteras/ultimate_investment_model_comparator/blob/main/models/moving_average/main.ipynb) (Exponential Moving Average)
- [Stochastic](https://github.com/Iveteras/ultimate_investment_model_comparator/blob/main/models/stochastic/main.ipynb)
  
## Technologies
```python
# Data manipulation
import pandas as pd
import numpy as np

# Dates
from datetime import date, timedelta

# Assets data
import yfinance as yf

# Charts
import matplotlib.pyplot as plt 
```
I also used POWER BI to data visualization.
## Parameters
- Every model folder has three files: 
  - **main.ipynb:** a script that demonstrate the model with one example asset;
  - ***name_of_model*.py:** is a function of the model to execute the test;
  - **test_model.ipynb:** is the model applied to 31 assets and analysis of their results.
- Stop loss time: 3, 7, 14, 21 and 30 days.
- Default asset in main.ipynb: AMZN. The choice was completely random.
- Default preiod in main.ipynb: 20 years.
- Results: Every test it returned the average of buy and hold of the asset, long position and short position.

## Phases
- Phase 1: *Coding models*
  - **Step one:** *Wrote the script of each model with the same parameters.*
  - **Step two:** *Ran all the tests and compared with Buy and hold*
  - **Step three:** *Saved each test result in [return_data](https://github.com/Iveteras/ultimate_investment_model_comparator/tree/main/return_data)*

- Phase 2: *Organize data*
  - **Step one:** *Took all returned data from the tests and got together in one single dataframe.*
  - **Step two:** *Made the TIP (Treasury Inflation-Protected) return to have a safe guideline.*

- Phase 3: *Data visualization*
  - **Step one:** *Basically the only step on this phase. Just developed all the charts.*
 
## Results
