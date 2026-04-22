import csv
import json
import os
import re

TOTAL_CSV  = os.path.join(os.path.dirname(__file__), '..', '000892952 - 人口、世帯数、人口動態（市区町村別）【総計】.csv')
FOREIGN_CSV = os.path.join(os.path.dirname(__file__), '..', '000892960 - 人口、世帯数、人口動態（市区町村別）【外国人住民】.csv')
OUT_PATH   = os.path.join(os.path.dirname(__file__), '..', 'data', 'population.json')

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

with open(TOTAL_CSV, encoding='utf-8-sig', newline='') as f:
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
            'male': safe_int(row[3]),
            'female': safe_int(row[4]),
            'population': pop,
            'households': safe_int(row[6]),
            'moveInDomestic': safe_int(row[7]),
            'moveInOverseas': safe_int(row[8]),
            'moveInTotal': safe_int(row[9]),
            'births': safe_int(row[10]),
            'moveOutDomestic': safe_int(row[13]),
            'moveOutOverseas': safe_int(row[14]),
            'moveOutTotal': safe_int(row[15]),
            'deaths': safe_int(row[16]),
            'changeCount': safe_int(row[19]),
            'changeRate': safe_float(row[20]),
            'naturalCount': safe_int(row[21]),
            'naturalRate': safe_float(row[22]),
            'socialCount': safe_int(row[23]),
            'socialRate': safe_float(row[24]),
            'foreign': None,
        }

foreign_added = 0

with open(FOREIGN_CSV, encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f)
    for _ in range(6):
        next(reader)

    for row in reader:
        if len(row) < 29:
            continue
        code6 = row[0].strip()
        if not code6.isdigit() or len(code6) != 6:
            continue

        name = row[2].strip()
        if is_gun_aggregate(name):
            continue

        code5 = code6[:5]
        if code5 not in result:
            continue

        pop = safe_int(row[5])
        if pop is None:
            continue

        result[code5]['foreign'] = {
            'male': safe_int(row[3]),
            'female': safe_int(row[4]),
            'population': pop,
            'households': safe_int(row[6]),
            'moveInDomestic': safe_int(row[7]),
            'moveInOverseas': safe_int(row[8]),
            'moveInTotal': safe_int(row[9]),
            'births': safe_int(row[10]),
            'moveOutDomestic': safe_int(row[15]),
            'moveOutOverseas': safe_int(row[16]),
            'moveOutTotal': safe_int(row[17]),
            'deaths': safe_int(row[18]),
            'changeCount': safe_int(row[23]),
            'changeRate': safe_float(row[24]),
            'naturalCount': safe_int(row[25]),
            'naturalRate': safe_float(row[26]),
            'socialCount': safe_int(row[27]),
            'socialRate': safe_float(row[28]),
        }
        foreign_added += 1

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, separators=(',', ':'))

print(f'Output: {len(result)} municipalities (skipped {skipped} gun aggregates)')
print(f'Foreign data added: {foreign_added} municipalities')
print(f'Written to: {OUT_PATH}')
