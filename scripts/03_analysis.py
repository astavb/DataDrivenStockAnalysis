# 03_analysis.py
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

IN_FILE = "data/cleaned_csv/all_stocks.csv"
OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(IN_FILE, parse_dates=['Date'])
if 'Daily Return' not in df.columns:
    df['Daily Return'] = df.groupby('Symbol')['Close'].pct_change()

yr = df[['Symbol','Yearly Return']].drop_duplicates().dropna()
top10 = yr.sort_values('Yearly Return', ascending=False).head(10)
bot10 = yr.sort_values('Yearly Return', ascending=True).head(10)

print("Top 10 gainers:\n", top10.to_string(index=False))
print("\nTop 10 losers:\n", bot10.to_string(index=False))

num_symbols = df['Symbol'].nunique()
num_green = (yr['Yearly Return'] > 0).sum()
num_red = (yr['Yearly Return'] <= 0).sum()
avg_price = df['Close'].mean()
avg_volume = df['Volume'].dropna().astype(float).mean() if 'Volume' in df.columns else None
print(f"\nMarket summary: symbols={num_symbols}, green={num_green}, red={num_red}, avg_price={avg_price:.2f}, avg_volume={avg_volume}")

# Volatility
vol = df.groupby('Symbol')['Daily Return'].std().dropna().sort_values(ascending=False)
top_vol = vol.head(10)
plt.figure(figsize=(10,6))
top_vol.plot(kind='bar')
plt.title("Top 10 Most Volatile Stocks (std of daily returns)")
plt.ylabel("Std Dev (Daily Return)")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "top10_volatile.png"))
plt.close()

# Cumulative returns top 5
top5_symbols = yr.sort_values('Yearly Return', ascending=False).head(5)['Symbol'].tolist()
plt.figure(figsize=(10,6))
for s in top5_symbols:
    sdf = df[df['Symbol']==s].sort_values('Date').set_index('Date')
    sdf['Cumulative Return'] = (1 + sdf['Daily Return'].fillna(0)).cumprod() - 1
    plt.plot(sdf.index, sdf['Cumulative Return'], label=s)
plt.legend()
plt.title("Cumulative Return - Top 5 Stocks")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "cumulative_top5.png"))
plt.close()

# Correlation heatmap of returns
pivot = df.pivot_table(index='Date', columns='Symbol', values='Close')
corr = pivot.pct_change().corr()
plt.figure(figsize=(12,10))
sns.heatmap(corr, cmap='coolwarm', center=0, vmax=1, vmin=-1)
plt.title("Correlation matrix (returns)")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "correlation_heatmap.png"))
plt.close()

# Sector-wise performance if mapping exists
sector_map_path = "data/sector_map.csv"
if os.path.exists(sector_map_path):
    sm = pd.read_csv(sector_map_path)
    if 'Symbol' in sm.columns and 'Sector' in sm.columns:
        merged = yr.merge(sm, on='Symbol', how='left')
        sector_perf = merged.groupby('Sector')['Yearly Return'].mean().dropna().sort_values(ascending=False)
        plt.figure(figsize=(10,6))
        sector_perf.plot(kind='bar')
        plt.title("Average Yearly Return by Sector")
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR, "sector_performance.png"))
        plt.close()
    else:
        print("sector_map.csv must have columns: Symbol, Sector")
else:
    print("No sector_map.csv found — skipping sector charts.")

# Month-wise top 5 gainers/losers
df['Month'] = df['Date'].dt.to_period('M')
monthly = df.groupby(['Month','Symbol']).agg(open=('Open','first'), close=('Close','last')).reset_index()
monthly['Monthly Return'] = (monthly['close'] / monthly['open']) - 1

months = monthly['Month'].unique()
for m in months:
    mdf = monthly[monthly['Month']==m].dropna(subset=['Monthly Return'])
    top5m = mdf.sort_values('Monthly Return', ascending=False).head(5)
    bot5m = mdf.sort_values('Monthly Return', ascending=True).head(5)

    f1 = os.path.join(OUT_DIR, f"top5_{m}_gainers.png")
    f2 = os.path.join(OUT_DIR, f"top5_{m}_losers.png")
    plt.figure(figsize=(8,4)); plt.bar(top5m['Symbol'], top5m['Monthly Return']); plt.title(f"Top5 Gainers {m}"); plt.xticks(rotation=45); plt.tight_layout(); plt.savefig(f1); plt.close()
    plt.figure(figsize=(8,4)); plt.bar(bot5m['Symbol'], bot5m['Monthly Return']); plt.title(f"Top5 Losers {m}"); plt.xticks(rotation=45); plt.tight_layout(); plt.savefig(f2); plt.close()

print("Charts saved in", OUT_DIR)
