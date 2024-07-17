import yfinance as yf
from utils.scoring import criteria_1, criteria_2
from utils.postgres import *
import math


def update_stock_info_1():
    column_placeholders = ', '.join(["symbol", "market", "sector","industry"]+keys_numeric)
    values_placeholders = ', '.join(f'%({key})s' for key in ["symbol", "market", "sector","industry"]+keys_numeric)
    exclude_placeholders = ', '.join(f"{key} = COALESCE(EXCLUDED.{key}, info_1.{key})" for key in ["market", "sector","industry"]+keys_numeric)
    sql_command = f"""
        INSERT INTO info_1 ({column_placeholders})  
        VALUES ({values_placeholders})  
        ON CONFLICT (symbol) DO UPDATE
        SET {exclude_placeholders};
    """ 
    data_to_insert = []  
    for symbol, market in query_symbol():
        tickerData = yf.Ticker(symbol)
        info = tickerData.info
        info_dict = {
            'symbol': symbol,
            'market': market,
        }

        for key in ["sector","industry"]:
            info_dict[key] = info.get(key)

        for key in keys_numeric:
            if isinstance(info.get(key), (float, int)) and not (math.isnan(info.get(key)) or math.isinf(info.get(key))):
                info_dict[key] = info.get(key)
            else:
                info_dict[key] = None

        data_to_insert.append(info_dict)

        if len(data_to_insert)>=1000:
            batch_insert(sql_command, data_to_insert)
            data_to_insert = []

    if data_to_insert:
        batch_insert(sql_command, data_to_insert)


def update_stock_info_2():
    data_to_insert = query_median('industry')
    data_to_insert = [{key: value for key, value in zip(['industry'] + keys_numeric, avg)} for avg in data_to_insert]
    column_placeholders = ', '.join(['industry'] + keys_numeric)
    values_placeholders = ', '.join(f'%({key})s' for key in ['industry'] + keys_numeric)
    exclude_placeholders = ', '.join([f"{key} = EXCLUDED.{key}" for key in keys_numeric])
    sql_command = f"""
        INSERT INTO info_2 ({column_placeholders})  
        VALUES ({values_placeholders})  
        ON CONFLICT (industry) DO UPDATE
        SET {exclude_placeholders};
    """
    batch_insert(sql_command, data_to_insert)


def update_stock_info_3():
    data_to_insert = query_median('sector')
    data_to_insert = [{key: value for key, value in zip(['sector'] + keys_numeric, avg)} for avg in data_to_insert]
    column_placeholders = ', '.join(['sector'] + keys_numeric)
    values_placeholders = ', '.join(f'%({key})s' for key in ['sector'] + keys_numeric)
    exclude_placeholders = ', '.join([f"{key} = EXCLUDED.{key}" for key in keys_numeric])
    sql_command = f"""
        INSERT INTO info_3 ({column_placeholders})  
        VALUES ({values_placeholders})  
        ON CONFLICT (sector) DO UPDATE
        SET {exclude_placeholders};
    """
    batch_insert(sql_command, data_to_insert)


def update_stock_score():
    data_to_insert = list(map(lambda x:{key: value for key, value in zip(['symbol','industry','sector'] + keys_numeric, x)}, query_info('info_1')))
    sector = list(map(lambda x:{key: value for key, value in zip(['sector'] + keys_numeric, x)}, query_info('info_3')))
    sector = {x['sector']: x for x in sector}
    industry = list(map(lambda x:{key: value for key, value in zip(['industry'] + keys_numeric, x)}, query_info('info_2')))
    industry = {x['industry']: x for x in industry}
    data_to_insert = list(map(lambda x:{'symbol':x['symbol'], 'score':(criteria_1(x)*1.0 + criteria_2(x,industry[x['industry']])*1.0 + criteria_2(x,sector[x['sector']])*1.0)*(100/72)}, data_to_insert))
    sql_command = f"""
        UPDATE info_1
        SET score = %(score)s
        WHERE symbol = %(symbol)s;
    """
    batch_insert(sql_command, data_to_insert)
    
    sql_command = f"""
        UPDATE info_2
        SET score = %(score)s
        WHERE industry = %(industry)s;
    """
    industry_score = list(map(lambda x:{key: value for key, value in zip(['industry','score'], x)}, query_avg_score('industry')))
    batch_insert(sql_command, industry_score)
    
    sql_command = f"""
        UPDATE info_3
        SET score = %(score)s
        WHERE sector = %(sector)s;
    """
    sector_score = list(map(lambda x:{key: value for key, value in zip(['sector','score'], x)}, query_avg_score('sector')))
    batch_insert(sql_command, sector_score)