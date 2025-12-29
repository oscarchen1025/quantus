import shioaji as sj
import pandas as pd
from IPython.display import display

from quantus.database import DataBase


db = DataBase()


class Account:

    def __init__(self,api_key,secret_key,simulation=True):

        api = sj.Shioaji(simulation)
        accounts = api.login(api_key,secret_key)

        self.api = api
        self.accounts = accounts

    def api_testing(self):

        if self.api.simulation:

            contract = self.api.Contracts.Stocks["2890"]

            order = sj.order.StockOrder(
                action='Buy',
                price=contract.limit_down,
                quantity=1,
                price_type='LMT',
                order_type='ROD',
            )

            trade = self.api.place_order(contract=contract,order=order)

            print('Auth success !')

    def get_snapshot_data(self,stock_ids:list=None):

        stock_ids = stock_ids or db.get('收盤價',exclude_etf=True).tail(200).dropna(how='all',axis=1).columns

        contracts = [self.api.Contracts.Stocks[stock_id] for stock_id in stock_ids]
        contracts = [contract for contract in contracts if contract is not None]
        snapshots = self.api.snapshots(contracts)

        info = pd.DataFrame(s.__dict__ for s in contracts).set_index('code')
        df = pd.DataFrame(s.__dict__ for s in snapshots).set_index('code')

        df['ts'] = pd.to_datetime(df['ts'])
        df.insert(0,'name',info['name'])

        return df

    def get_realtime_data(self):

        df = self.get_snapshot_data()
        df['date'] = pd.to_datetime(df['ts'].apply(lambda s:s.strftime('%Y-%m-%d')))
        df['volume'] = df['total_volume'] * 1000

        stocks = {}
        for name,file_name in [('close','收盤價'),('open','開盤價'),('high','最高價'),('low','最低價'),('volume','成交股數')]:
            
            stocks[name] = pd.concat([db.get(file_name,exclude_etf=True),df.pivot_table(name,'date',df.index).iloc[[-1]]]).groupby(level=0).nth[-1]

        return stocks

    def display_stocks_info(self,conditions):

        stock_ids = conditions.iloc[-1][conditions.iloc[-1]].index.tolist()

        df = self.get_snapshot_data(stock_ids)

        df['kbar_rate'] = round((df['close'] / df['open'] - 1) * 100,2)
        df = df[['name','close','total_volume','change_rate','volume_ratio','kbar_rate']]

        for n,col in [(5,'week'),(20,'month'),(240,'year')]:
            
            close = db.get('收盤價')[stock_ids]
            df[f"1{col}"] = round(close.pipe(lambda s:s / s.shift(n) - 1).iloc[-1] * 100,2)

        df['ytd'] = round(close.loc[str(close.index.year[-1])].pipe(lambda s:s.iloc[-1] / s.iloc[0] - 1) * 100,2)

        display(
            df.style
            .bar(color=['#049981c3','#cd323fc3'],width=100,height=20,align='zero',subset=['change_rate','kbar_rate','1week','1month','1year','ytd'])
            .bar(color=['#049981','#3b8ae8'],width=50,height=25,align='zero',subset=['volume_ratio'])
            .format(lambda s:str(round(s,2)) + ' %',subset=['change_rate','kbar_rate','volume_ratio','1week','1month','1year','ytd'])
            .format(lambda s:s,subset=['close','total_volume'])
        )