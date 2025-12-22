import requests
import pandas as pd
import numpy as np

from quantus.database import DataBase


db = DataBase()


def crawl_price(date):

    date_str_format = pd.to_datetime(date).strftime('%Y%m%d')

    # TWSE
    url = "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date=%s&type=ALL&response=json"%(date_str_format)
    r = requests.get(url)

    if '沒有符合' in r.json()['stat']:
        dfs = pd.DataFrame()
    else:
        tables = r.json()['tables']
        data = [t for t in tables if 'data' in t.keys() and len(t['data']) > 500][0]
        sii = pd.DataFrame(data['data'],columns=data['fields'])
        sii.columns = sii.columns.to_series().apply(lambda s:s.replace(' ','')).tolist()

        cols = ['開盤價','最高價','最低價','收盤價','成交股數','成交金額','成交筆數']

        sii = sii.astype(str).replace(',','',regex=True)

        for col in cols:
            sii[col] = pd.to_numeric(sii[col],errors='coerce')

        sii = sii[['證券代號'] + cols]

        # TPEX
        url = "https://www.tpex.org.tw/www/zh-tw/afterTrading/dailyQuotes"
        payload = {
            'date':pd.to_datetime(date).strftime('%Y/%m/%d'),
            'response':'json'
        }
        r = requests.post(url,data=payload)
        tables = r.json()['tables']
        data = [t for t in tables if 'data' in t.keys() and len(t['data']) > 500][0]
        otc = pd.DataFrame(data['data'],columns=data['fields'])
        otc.columns = otc.columns.to_series().apply(lambda s:s.replace(' ','').replace('(元)','')).tolist()
        otc = otc.rename(columns={'代號':'證券代號','收盤':'收盤價','開盤':'開盤價','最高':'最高價','最低':'最低價'})

        otc = otc.astype(str).replace(',','',regex=True)
        for col in cols:
            otc[col] = pd.to_numeric(otc[col],errors='coerce')

        otc = otc[['證券代號'] + cols]

        # merge
        dfs = pd.concat([sii,otc])
        dfs['date'] = pd.to_datetime(date)
        dfs = dfs.mask(dfs == 0,np.nan)

        return dfs