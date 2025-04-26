import csv

aa = 'Ser'
sec_structs = {}

with open(f'stats/{aa}-vloop-stats.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row['secondary_structure']
        if sec_structs.get(key):
            sec_structs[key].append(row)
        else:
            sec_structs[key] = [row]

sec_structs_sorted = dict(
        sorted(
            sec_structs.items(), key=lambda x : (len(x[0]), x[0])
            )
        )

i = 0
prev_len = 0
for struct, rows in sec_structs_sorted.items():
    if len(struct) == prev_len:
        i += 1
    else:
        prev_len = len(struct)
        i = 0

    fname = f'logo_fastas/{aa}/{aa}-vloop_{len(struct)}_{chr(65+i)}_N{len(rows)}.fa'
    print(fname)
    print(struct)

    with open(fname, 'w') as f:
        for row in rows:
            f.write(f">{row['label']}\n")
            f.write(f"{row['seq']}\n")
