import psycopg2
import psycopg2.extras

PostgresDB_params = {'database': 'postgres',
                    'user': 'admin',
                    'password': 'password',
                    # 'host': 'host.docker.internal',
                    'host': 'host',
                    'port': 5432}


keys_numeric = ["priceToBook","returnOnAssets","returnOnEquity","debtToEquity","enterpriseToRevenue","enterpriseToEbitda","beta","grossMargins","ebitdaMargins","operatingMargins","profitMargins","quickRatio","currentRatio","pegRatio","payoutRatio","earningsGrowth","revenueGrowth","trailingEps","forwardEps","trailingPE","forwardPE","dividendYield","marketCap","revenuePerShare"]


def query_median(col:str): 
    column_placeholders = ', '.join(
        f'PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {key})' for key in keys_numeric)
    sql_command = f"""
        SELECT {col}, {column_placeholders} 
        FROM info_1 
        WHERE {col} IS NOT NULL 
        GROUP BY {col}
        ORDER BY {col}; 
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            data = cur.fetchall()
    return data


def query_avg_score(col:str): 
    sql_command = f"""
        SELECT {col}, AVG(score)
        FROM info_1 
        WHERE {col} IS NOT NULL 
        GROUP BY {col}
        ORDER BY {col}; 
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            data = cur.fetchall()
    return data


def get_conn():
    return psycopg2.connect(**PostgresDB_params)


def query_symbol():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT symbol, market FROM symbols WHERE industry IS NOT NULL AND sector IS NOT NULL""")
            data = cur.fetchall()
    return data


def query_info(table:str):
    column_placeholders = ', '.join(['symbol','industry','sector']+keys_numeric if table=='info_1' else ['industry']+keys_numeric if table=='info_2' else ['sector']+keys_numeric if table=='info_3' else [])
    cond = 'WHERE industry IS NOT NULL AND sector IS NOT NULL' if table=='info_1' else 'WHERE industry IS NOT NULL' if table=='info_2' else 'WHERE sector IS NOT NULL' if table=='info_3' else ''
    sql_command = f"""SELECT {column_placeholders} FROM {table} {cond}"""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_command)
            data = cur.fetchall()
    return data


def batch_insert(sql_command:str, data_to_insert:list):
    with get_conn() as conn:
        with conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, sql_command, data_to_insert)
        conn.commit()
