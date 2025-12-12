import os, json, zlib, hashlib, glob, sys

# Find PNG
candidates = glob.glob("**/EvieCore_latest.png", recursive=True)
if not candidates:
    print("EvieCore_latest.png not found! Drop it anywhere in ~/unified")
    sys.exit(1)
png_path = candidates[0]
print(f"Found: {png_path}")

# Extract all IDAT data
with open(png_path, "rb") as f:
    raw = f.read()

if raw[:8] != b'\x89PNG\r\n\x1a\n':
    print("Not a valid PNG")


python utils/generate_seed.py
