import csv

aa = 'Leu'
sec_structs = {}

with open(f'stats/{aa}-vloop-stats.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = len(row['secondary_structure'])
        if sec_structs.get(key):
            sec_structs[key].append(row)
        else:
            sec_structs[key] = [row]

sec_structs_sorted = dict(
        sorted(
            sec_structs.items()
            )
        )

for struct_len, rows in sec_structs_sorted.items():
    fname = f'logo_fastas/{aa}/{aa}-vloop_{struct_len}_S_N{len(rows)}.fa'
    print(fname)

    with open(fname, 'w') as f:
        for row in rows:
            f.write(f">{row['label']}\n")
            f.write(f"{row['seq']}\n")
