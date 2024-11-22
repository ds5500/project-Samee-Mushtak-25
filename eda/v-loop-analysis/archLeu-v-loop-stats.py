import re
import csv

def pairs_with(base1, base2):
    return (base1 == 'A' and base2 == 'U') or \
        (base1 == 'U' and (base2 == 'A' or base2 == 'G')) or \
        (base1 == 'C' and base2 == 'G') or \
        (base1 == 'G' and (base2 == 'C' or base2 == 'U'))

def viable(seq:str, stem_start_idx:int, stem_length:int, n_unpaired_bases:int):
    for i in range(stem_length):
        left_base = seq[stem_start_idx + i]
        right_base = seq[len(seq) - 2 - n_unpaired_bases - i]
        if not pairs_with(left_base, right_base):
            return False
    
    # Need to make sure AG is in the loop between the two stems
    try:
        if seq.index('AG', stem_start_idx + stem_length, len(seq) - 1 - n_unpaired_bases - stem_length) > 0:
            return True
    except ValueError:
        return False

def calc_secondary_structure_params(seq):
    # The parameters are ordered so that if a candidate is found
    # the first solution that is found will be most probable (for Leucine)
    for stem_start_idx in [1, 2, 3]:
        # If a stem_length of 4 is viable, then it is probably correct
        for stem_length in [4, 3, 2]:
            for n_unpaired_bases in [2, 1, 0, 3]:
                if viable(seq, stem_start_idx, stem_length, n_unpaired_bases):
                    return stem_start_idx, stem_length, n_unpaired_bases
    return -1, -1, -1

def secondary_structure_from_params(seq, stem_start_idx, stem_length, n_unpaired_bases):
    secondary_structure = ['-'] * len(seq)
    for i in range(stem_start_idx - 1):
        secondary_structure[i+1] = '*'
    for i in range(stem_length):
        secondary_structure[stem_start_idx + i] = '('
        secondary_structure[len(seq) - 2 - n_unpaired_bases - i] = ')'
    for i in range(stem_start_idx + stem_length, len(seq) - 1 - n_unpaired_bases - stem_length):
        secondary_structure[i] = '*'
    for i in range(n_unpaired_bases):
        secondary_structure[len(seq)-2-i] = '*'
    return ''.join(secondary_structure)

extract_file = 'Leu-extract.txt'
output_file = 'Leu-Vloop-stats.csv'

trnas = []
with open(extract_file) as f:
    for l in f:
        args = l.strip().split(',')
        trna = {}
        label = args[0]
        trna['label'] = label
        # Species name appears before 'tRNA' in label
        trna['species'] = label[:label.index('_tRNA')].replace('_', ' ')
        # Anticodon appears after 'Leu' in label
        # Converting T to U for RNA
        trna['anticodon'] = label[label.index('Leu-') + 4:label.index('Leu-') + 7].replace('T','U')

        seq = re.sub('[^a-zA-Z]', '', args[1]).upper()
        trna['seq'] = seq
        trna['length'] = len(seq)

        trna['stem_start_idx'], trna['stem_length'], trna['n_unpaired_bases'] = calc_secondary_structure_params(seq)
        trna['secondary_structure'] = secondary_structure_from_params(
            seq, trna['stem_start_idx'], trna['stem_length'], trna['n_unpaired_bases']
        )

        if trna['stem_start_idx'] == -1:
            print(trna['label'])

        trnas.append(trna)


# print(trnas)
with open(output_file, 'w', newline='\n') as csvfile:
    writer = csv.DictWriter(csvfile, trnas[0].keys())

    writer.writeheader()
    writer.writerows(trnas)
