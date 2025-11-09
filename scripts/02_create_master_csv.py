# 02_create_master_csv.py
import os
import pandas as pd
from glob import glob

IN_DIR = "data/cleaned_csv"
OUT_FILE = os.path.join(IN_DIR, "all_stocks.csv")

csvs = glob(os.path.join(IN_DIR, "*.csv"))
csvs = [c for c in csvs if not os.path.basename(c).startswith("all_stocks")]
dfs = []
for c in csvs:
    try:
        d = pd.read_csv(c, parse_dates=['Date'], dayfirst=False)
    except Exception:
        d = pd.read_csv(c)
        if 'Date' in d.columns:
            d['Date'] = pd.to_datetime(d['Date'], errors='coerce')
    if 'Symbol' not in d.columns:
        sym = os.path.splitext(os.path.basename(c))[0]
        d['Symbol'] = sym
    possible = ['Date','Symbol','Open','High','Low','Close','Volume']
    present = [p for p in possible if p in d.columns]
    d = d[present]
    dfs.append(d)

if not dfs:
    print("No CSVs found in", IN_DIR)
else:
    all_df = pd.concat(dfs, ignore_index=True)
    all_df = all_df.dropna(subset=['Date','Symbol','Close'])
    all_df = all_df.sort_values(['Symbol','Date']).drop_duplicates(['Symbol','Date'])
    all_df['Close'] = pd.to_numeric(all_df['Close'], errors='coerce')
    all_df['Daily Return'] = all_df.groupby('Symbol')['Close'].pct_change()

    first_last = all_df.groupby('Symbol').agg(
        first_date=('Date','first'),
        last_date=('Date','last'),
        first_close=('Close','first'),
        last_close=('Close','last')
    ).reset_index()
    first_last['Yearly Return'] = (first_last['last_close'] / first_last['first_close']) - 1
    all_df = all_df.merge(first_last[['Symbol','Yearly Return']], on='Symbol', how='left')

    all_df.to_csv(OUT_FILE, index=False)
    print("Master cleaned file saved to", OUT_FILE)
