from IPython import get_ipython
import os


__version__ = '0.1.7'

COLAB_ENV = 'google.colab' in str(get_ipython())
CONNECTED = os.path.exists('/content/drive/MyDrive')
DB_PATH = '/content/drive/MyDrive/quantus_db' if COLAB_ENV else 'quantus_db'