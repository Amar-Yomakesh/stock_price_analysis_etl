import requests
import pandas as pd
import sqlalchemy

db_user='admin'
db_password='admin123!'
db_host='172.24.48.1'
db_name='stocks'
connection_obj=sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(db_user, db_password, 
                                                      db_host, db_name))

def crypto_price_capture():
    crypto = requests.get(url='https://api.wazirx.com/api/v2/tickers',verify=False)
    crypto_raw_data = crypto.json()
    print(crypto_raw_data)

    high_list = list()
    low_list = list()
    last_list = list()
    open_list =  list()
    volume_list = list()
    sell_list = list()
    buy_list = list()
    at_list = list()
    crypto_id_list = list()

    for crypto_id in crypto_raw_data:
        high_list.append(crypto_raw_data[crypto_id]['high'])
        low_list.append(crypto_raw_data[crypto_id]['low'])
        last_list.append(crypto_raw_data[crypto_id]['last'])
        open_list.append(crypto_raw_data[crypto_id]['open'])
        volume_list.append(crypto_raw_data[crypto_id]['volume'])
        sell_list.append(crypto_raw_data[crypto_id]['sell'])
        buy_list.append(crypto_raw_data[crypto_id]['buy'])
        at_list.append(crypto_raw_data[crypto_id]['at'])
        crypto_id_list.append(crypto_id)

    crypto_pricing_df = pd.DataFrame({
        'high':high_list,
        'low' : low_list,
        'last' : last_list,
        'open' : open_list,
        'volume' : volume_list,
        'sell' : sell_list,
        'buy' : buy_list,
        'at':at_list,
        'crypto_id' : crypto_id_list
    })

    db_user='admin'
    db_password='admin123!'
    db_host='172.24.48.1'
    db_name='stocks'
    connection_obj=sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                format(db_user, db_password, 
                                                        db_host, db_name))
    crypto_pricing_df['id'] = pd.read_sql_query('select ifnull(max(id),0)+1 from crypto_hourly_price',connection_obj).iloc[0,0]+range(len(crypto_pricing_df))
    crypto_pricing_df.to_sql(con=connection_obj,name='crypto_hourly_price',if_exists='append',index=False,dtype={ 'high' : sqlalchemy.FLOAT, 'low' : sqlalchemy.FLOAT, 'last' : sqlalchemy.FLOAT, 
                                                                                                                'open' : sqlalchemy.FLOAT, 'volume' : sqlalchemy.FLOAT, 'sell' : sqlalchemy.FLOAT, 'buy' : sqlalchemy.FLOAT, 'at': sqlalchemy.Integer, 'crypto_id' : sqlalchemy.String(15) })
    with connection_obj.connect() as con:
        result = con.execute(sqlalchemy.text("select count(*) from stocks.crypto_hourly_price"))
        for row in result:
            total=(row[0])
    return ("total number of records :" + str(total))
    