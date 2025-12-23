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

