# 04_to_sql.py
import pandas as pd
from sqlalchemy import create_engine

MASTER = "data/cleaned_csv/all_stocks.csv"
df = pd.read_csv(MASTER, parse_dates=['Date'])

# TODO: update your DB credentials before running
# MySQL example: mysql+pymysql://user:password@localhost/stock_analysis
CONN_STR = "mysql+pymysql://root:password@localhost/stock_analysis"

engine = create_engine(CONN_STR)
with engine.begin() as conn:
    df.to_sql('stock_data', conn, if_exists='replace', index=False)
print("Uploaded to SQL table: stock_data")
