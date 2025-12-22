from IPython import get_ipython
import os


__version__ = '0.1.0'

COLAB_ENV = 'google.colab' in str(get_ipython())
CONNECTED = os.path.exists('/content/drive/MyDrive')
DB_PATH = '/content/drive/MyDrive/Quantus_db' if COLAB_ENV else 'Quantus_db'