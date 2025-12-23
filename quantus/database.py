import os
import pandas as pd
import gdown

from quantus import COLAB_ENV,CONNECTED,DB_PATH


class DataBase:

    def __init__(self):

        # connect to Google Drive
        if COLAB_ENV & (not CONNECTED):
            from google.colab import drive
            drive.mount('/content/drive')

        # check & create DataBase
        if not os.path.exists(DB_PATH):
            gdown.download_folder(id='1gklTGXtOWtM9_u3aH-FcBsiV8UQCvhSZ',output=DB_PATH)

        self.path = DB_PATH

    def exists(self,file_name):

        return os.path.exists(f"{self.path}/{file_name}.pickle")

    def get(self,file_name):

        return pd.read_pickle(f"{self.path}/{file_name}.pickle")

    def get_klines(self,stock_id):

        ohlcv = pd.DataFrame({name:self.get(fname)[stock_id] for name,fname in [('close','收盤價'),('open','開盤價'),('high','最高價'),('low','最低價'),('volume','成交股數')]})

        return ohlcv

