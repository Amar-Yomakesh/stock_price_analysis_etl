import requests
import pandas as pd
import sqlalchemy
from configparser import ConfigParser
import pathlib


config = ConfigParser()
script_path=pathlib.Path(__file__).parent.resolve()
config_file='configuration.ini'

config.read(f"{script_path}/config/{config_file}")
try:
    db_user=config.get("database","db_user")
    db_password=config.get("database","db_password")
    db_host=config.get("database","db_host")
    db_name=config.get("database","db_name")
    wazirx_url=config.get("wazirx","url")
except:
    print('properties are not found! exiting')
    exit()

def crypto_price_capture():
    try:
        connection_obj=sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(db_user, db_password, 
                                                      db_host, db_name))
    except:
        print("Database connection not successful! exiting")
        exit(0)
    try:
        crypto = requests.get(url=f'{wazirx_url}',verify=False)
    except:
        print("wazirx api connection not successful! exiting")
        exit(0)
    crypto_raw_data = crypto.json()
    #initialise database column variables
    high_list = list()
    low_list = list()
    last_list = list()
    open_list =  list()
    volume_list = list()
    sell_list = list()
    buy_list = list()
    at_list = list()
    crypto_id_list = list()

    #collected json data into database column data
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

    #conver to dataframe
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

    #insert into database
    ## add id column
    crypto_pricing_df['id'] = pd.read_sql_query('select ifnull(max(id),0)+1 from crypto_hourly_price',connection_obj).iloc[0,0]+range(len(crypto_pricing_df))
    crypto_pricing_df.to_sql(con=connection_obj,name='crypto_hourly_price',if_exists='append',index=False,dtype={ 'high' : sqlalchemy.FLOAT, 'low' : sqlalchemy.FLOAT, 'last' : sqlalchemy.FLOAT, 
                                                                                                                'open' : sqlalchemy.FLOAT, 'volume' : sqlalchemy.FLOAT, 'sell' : sqlalchemy.FLOAT, 'buy' : sqlalchemy.FLOAT, 'at': sqlalchemy.Integer, 'crypto_id' : sqlalchemy.String(15) })
    return ("total number of records :" + str(crypto_pricing_df.shape[0]))
    