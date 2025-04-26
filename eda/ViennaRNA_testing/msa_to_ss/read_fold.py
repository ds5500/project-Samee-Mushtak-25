import csv
import os
import sys

def computeTRNADetails(aa, label, seq, structure, score_str, unique=False):
    trna = {}
    if not unique:
        trna['label'] = label
        trna['species'] = label[:label.index('_tRNA')].replace('_', ' ')
        trna['anticodon'] = label[label.index(f'{aa}-') + 4:label.index(f'{aa}-') + 7].replace('T','U')

    trna['seq'] = seq
    trna['length'] = len(seq)

    trna['stem_start_idx'] = structure.index('(')
    trna['stem_length'] = structure.count('(')
    trna['n_unpaired_bases'] = structure[structure.index('('):structure.rindex(')')].count('.')
    trna['secondary_structure'] = structure
    trna['free_energy'] = float(score_str)

    return trna

def main2(args):
    aa = 'Ser'
    fold_filepath = f'folds/{aa}-vloop.fold'

    if not os.path.isfile(fold_filepath):
        exit("Fold file does not exist at the provided location")

    with open(fold_filepath, 'r') as fold_file:
        lines = [line.strip() for line in fold_file.readlines()]

    trnas = []
    trna_counts = {}
    for i in range(len(lines) // 3):
        label = lines[3*i][1:]
        seq = lines[3*i+1]
        split = lines[3*i+2].index(' ')
        structure = lines[3*i+2][:split]
        score_str = lines[3*i+2][split+2:-1]
        trna = computeTRNADetails(aa, label, seq, structure, score_str, unique=True)
        # trnas.append(trna)
        if seq not in trna_counts:
            trnas.append(trna)
        trna_counts[seq] = trna_counts.get(seq, 0) + 1
    
    for trna in trnas:
        trna['count'] = trna_counts[trna['seq']]

    with open(f'stats/{aa}-vloop-stats-unique.csv', 'w', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, trnas[0].keys())

        writer.writeheader()
        writer.writerows(trnas)

def main(args):
    aa = 'Ser'
    fold_filepath = f'folds/{aa}-vloop.fold'

    if not os.path.isfile(fold_filepath):
        exit("Fold file does not exist at the provided location")

    with open(fold_filepath, 'r') as fold_file:
        lines = [line.strip() for line in fold_file.readlines()]

    trnas = []
    for i in range(len(lines) // 3):
        label = lines[3*i][1:]
        seq = lines[3*i+1]
        split = lines[3*i+2].index(' ')
        structure = lines[3*i+2][:split]
        score_str = lines[3*i+2][split+2:-1]
        trna = computeTRNADetails(aa, label, seq, structure, score_str)

        trnas.append(trna)

    with open(f'stats/{aa}-vloop-stats.csv', 'w', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, trnas[0].keys())

        writer.writeheader()
        writer.writerows(trnas)

if __name__ == "__main__":
    main(sys.argv)
    main2(sys.argv)
