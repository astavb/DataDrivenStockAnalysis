# 00_optional_extract_rar.py
"""
Optional helper to extract a .rar file of your dataset into data/raw_yaml.
Requires 'rarfile' package AND either unrar or bsdtar installed on your system.
Usage:
    python 00_optional_extract_rar.py /path/to/data.rar
"""
import sys, os, rarfile, shutil

RAW_DIR = "data/raw_yaml"
os.makedirs(RAW_DIR, exist_ok=True)

if len(sys.argv) < 2:
    print("Provide path to .rar file, e.g. python 00_optional_extract_rar.py data.rar")
    sys.exit(1)

rar_path = sys.argv[1]
if not os.path.exists(rar_path):
    print("RAR not found:", rar_path)
    sys.exit(1)

try:
    with rarfile.RarFile(rar_path) as rf:
        rf.extractall(RAW_DIR)
        print("Extracted into", RAW_DIR)
except rarfile.NeedFirstVolume:
    print("This looks like a multi-part archive; provide the first volume.")
except rarfile.RarCannotExec as e:
    print("Extraction backend not found. Install 'unrar' or 'bsdtar' then retry.")
except Exception as e:
    print("RAR extraction failed:", e)
