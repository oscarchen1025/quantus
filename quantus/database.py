import os
import pandas as pd

from quantus import COLAB_ENV,CONNECTED,DB_PATH


class DataBase:

    def __init__(self):

        # connect to Google Drive
        if COLAB_ENV & (not CONNECTED):
            from google.colab import drive
            drive.mount('/content/drive')

        # check & create DataBase
        if not os.path.exists(DB_PATH):
            os.mkdir(DB_PATH)

        self.path = DB_PATH

