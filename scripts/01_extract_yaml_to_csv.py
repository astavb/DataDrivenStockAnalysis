# 01_extract_yaml_to_csv.py
import os
import yaml
import pandas as pd
from glob import glob

RAW_DIR = "data/raw_yaml"
OUT_DIR = "data/cleaned_csv"
os.makedirs(OUT_DIR, exist_ok=True)

def load_yaml_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return yaml.safe_load(f)
        except Exception as e:
            print(f"YAML parse error {path}: {e}")
            return None

all_rows = []
yaml_paths = glob(os.path.join(RAW_DIR, "**", "*.yml"), recursive=True) + glob(os.path.join(RAW_DIR, "**", "*.yaml"), recursive=True)
yaml_paths = list(dict.fromkeys(yaml_paths))

for yp in yaml_paths:
    data = load_yaml_file(yp)
    if not data:
        continue
    rows = []
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        keys = list(data.keys())
        if keys and isinstance(data[keys[0]], list):
            for k in keys:
                for entry in data[k]:
                    entry_copy = dict(entry)
                    entry_copy['Symbol'] = entry_copy.get('Symbol', k)
                    rows.append(entry_copy)
        else:
            for k, v in data.items():
                if isinstance(v, dict):
                    inside_keys = list(v.keys())
                    if inside_keys and isinstance(v[inside_keys[0]], dict):
                        date = k
                        for sym, rec in v.items():
                            rec_copy = dict(rec)
                            rec_copy['Symbol'] = rec_copy.get('Symbol', sym)
                            rec_copy['Date'] = rec_copy.get('Date', date)
                            rows.append(rec_copy)
                    else:
                        rec = v
                        rec_copy = dict(rec)
                        rec_copy['Symbol'] = rec_copy.get('Symbol', k)
                        rows.append(rec_copy)

    for r in rows:
        row = dict(r)
        if 'data' in row and isinstance(row['data'], dict):
            for k, v in row['data'].items():
                row[k] = v
            row.pop('data', None)
        all_rows.append(row)

if not all_rows:
    print("No rows extracted. Put your YAML files inside data/raw_yaml/.")
else:
    df_all = pd.DataFrame(all_rows)

    rename_map = {}
    for c in df_all.columns:
        lc = c.lower()
        if lc in ("close", "closing"):
            rename_map[c] = "Close"
        if lc in ("open",):
            rename_map[c] = "Open"
        if lc in ("high",):
            rename_map[c] = "High"
        if lc in ("low",):
            rename_map[c] = "Low"
        if lc in ("volume", "vol"):
            rename_map[c] = "Volume"
        if lc in ("symbol", "ticker"):
            rename_map[c] = "Symbol"
        if lc in ("date", "dt"):
            rename_map[c] = "Date"
    df_all = df_all.rename(columns=rename_map)

    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col in df_all.columns:
            df_all[col] = pd.to_numeric(df_all[col], errors='coerce')

    if "Date" in df_all.columns:
        df_all['Date'] = pd.to_datetime(df_all['Date'], errors='coerce')

    df_all = df_all.dropna(subset=['Symbol', 'Date', 'Close']).sort_values(['Symbol', 'Date'])

    for sym, g in df_all.groupby('Symbol'):
        outp = os.path.join(OUT_DIR, f"{sym}.csv")
        g.to_csv(outp, index=False)
    master_csv = os.path.join(OUT_DIR, "all_stocks_raw.csv")
    df_all.to_csv(master_csv, index=False)
    print(f"Wrote {len(df_all)} rows. Per-symbol CSVs in {OUT_DIR}. Master: {master_csv}")
