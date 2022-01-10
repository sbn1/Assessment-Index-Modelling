import datetime as dt
import pandas as pd
import numpy as np
from pandas.tseries.offsets import BDay

class IndexModel:
    def __init__(self) -> None:
        
        self.index = pd.DataFrame(columns=['Date','Value'])
        

    def calc_index_level(self, start_date: dt.date, end_date: dt.date) -> None:
       
        stocks = pd.read_csv('data_sources/stock_prices.csv')

        stocks['Date'] = pd.to_datetime(stocks['Date'],format="%d/%m/%Y")
        stocks.set_index('Date', inplace=True)
        
        business_days = pd.date_range(start_date, end_date, freq="B")
        business_month_begins = pd.date_range(start_date, end_date, freq="BMS")
        
        self.index = pd.DataFrame(columns=['Value','Date'])
        self.index['Date'] = [i.date() for i in business_days]
        self.index.set_index('Date',inplace=True)
        
        poz_1=1 
        poz_2=1
        poz_3=1      
        
        for day in business_days:
            if ( day in business_month_begins):
                
                sorted_previous_day = np.argsort(stocks[stocks.index == day-BDay(1)].values).ravel().tolist()
                                
                poz_1 =sorted_previous_day[-1]
                poz_2 =sorted_previous_day[-2]
                poz_3= sorted_previous_day[-3]
                

            self.index[self.index.index == day]=stocks[stocks.index == day][stocks.columns[poz_1]]*0.5 +\
                stocks[stocks.index == day][stocks.columns[poz_2]]*0.25 + \
                stocks[stocks.index == day][stocks.columns[poz_3]]*0.25
                
        self.index[self.index.index == start_date] = 100
        
        
    def export_values(self, file_name: str) -> None:   
        self.index.to_csv(file_name)
        
