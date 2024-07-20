from sqlalchemy import create_engine
import pandas as pd
import requests
import dataframe_image as dfi
import time


# Database credentials
user = 'admin'
password = 'password'
host = 'host'
port = '5432'  
dbname = 'postgres'
database_url = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

line_headers = {'Authorization':'Bearer '+ 'token'}

# Create the engine
engine = create_engine(database_url)

# SQL query
query = "SELECT * FROM info_1 where (market = 'set' OR market = 'mai') order by score desc"


def line_notify(message:str, file_path:str):
    payload = {'message':message}
    with open(file_path, 'rb') as file:
        image_file = {'imageFile':file}
        requests.post("https://notify-api.line.me/api/notify", headers=line_headers , data = payload, files = image_file)
        file.close()


def daily_report():
    df = pd.read_sql_query(query, engine)
    df.set_index('symbol',inplace=True)
    dfi.export(df[['score','sector','industry']].head(10), '/tmp/daily.png', dpi = 300, table_conversion='matplotlib')
    line_notify('overall','/tmp/daily.png')
    sectors = df['sector'].unique()
    for sector in sectors:
        dfi.export(df.loc[df['sector']==sector][['score','industry']].head(10), '/tmp/daily.png', dpi = 300, table_conversion='matplotlib')
        line_notify(sector,'/tmp/daily.png')
        time.sleep(1)