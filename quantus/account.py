import shioaji as sj


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