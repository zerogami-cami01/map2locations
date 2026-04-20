import csv
import json
import os
import re

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '000892952 - 人口、世帯数、人口動態（市区町村別）【総計】.csv')
OUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'population.json')

def is_gun_aggregate(name):
    return bool(re.fullmatch(r'.+郡', name.strip()))

def safe_float(val):
    try:
        return float(val.strip())
    except (ValueError, AttributeError):
        return None

def safe_int(val):
    try:
        return int(val.strip().replace(',', ''))
    except (ValueError, AttributeError):
        return None

result = {}
skipped = 0

with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f)
    for _ in range(6):
        next(reader)

    for row in reader:
        if len(row) < 25:
            continue
        code6 = row[0].strip()
        if not code6.isdigit() or len(code6) != 6:
            continue

        name = row[2].strip()
        if is_gun_aggregate(name):
            skipped += 1
            continue

        code5 = code6[:5]
        pop = safe_int(row[5])
        if pop is None:
            continue

        result[code5] = {
            'prefecture': row[1].strip(),
            'name': name,
            # 人口（2025年1月1日現在）
            'male': safe_int(row[3]),
            'female': safe_int(row[4]),
            'population': pop,
            'households': safe_int(row[6]),
            # 住民票記載数
            'moveInDomestic': safe_int(row[7]),
            'moveInOverseas': safe_int(row[8]),
            'moveInTotal': safe_int(row[9]),
            'births': safe_int(row[10]),
            # 住民票消除数
            'moveOutDomestic': safe_int(row[13]),
            'moveOutOverseas': safe_int(row[14]),
            'moveOutTotal': safe_int(row[15]),
            'deaths': safe_int(row[16]),
            # 増減
            'changeCount': safe_int(row[19]),
            'changeRate': safe_float(row[20]),
            'naturalCount': safe_int(row[21]),
            'naturalRate': safe_float(row[22]),
            'socialCount': safe_int(row[23]),
            'socialRate': safe_float(row[24]),
        }

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, separators=(',', ':'))

print(f'Output: {len(result)} municipalities (skipped {skipped} gun aggregates)')
print(f'Written to: {OUT_PATH}')
