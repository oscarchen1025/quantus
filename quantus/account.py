import shioaji as sj
import pandas as pd

from quantus.database import DataBase


db = DataBase()


class Account:

    def __init__(self,api_key,secret_key,simulation=False):

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
        snapshots = self.api.snapshots([contract for contract in contracts if contract is not None])

        df = pd.DataFrame(s.__dict__ for s in snapshots)
        df['ts'] = pd.to_datetime(df['ts'])
        df = df.rename(columns={'code':'證券代號'})

        return df