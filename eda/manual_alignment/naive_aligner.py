import re

clustal_filepath = 'haloVolc1/haloVolc1-manual.clustal'

def reverse_complement_regex(seq:str):
    # Consider allowing at most one non-Watson-Crick base pair (G-U)
    # If parameter strict=True is given to function
    rev_comp = ''
    for base in reversed(seq):
        match base:
            case 'A':
                rev_comp = rev_comp + 'U'
            case 'U':
                rev_comp = rev_comp + '(A|G)'
            case 'C':
                rev_comp = rev_comp + 'G'
            case 'G':
                rev_comp = rev_comp + '(C|U)'
            case _:
                return None
    return rev_comp

seqs = {}
with open(clustal_filepath) as f:
    for line in f:
        if line.startswith('tRNA'):
            parts = line.split()
            seqs[parts[0]] = parts[1]


max_ac_start = 0
mac_t_start = 0

for label,seq in seqs.items():
    print(label)

    # Acceptor Step
    fp_stem = seq[:7]
    tp_stem_expr = reverse_complement_regex(fp_stem)
    # Cannot use because of overlapping
    tp_matches = re.finditer(tp_stem_expr, seq)
    tp_match = None
    # Get the last match
    for m in tp_matches:
        tp_match = m
    # print('5\' Acceptor Stem')
    # print(f'00: {fp_stem}')
    # print('3\' Acceptor Stem')
    # print(f'{tp_match.start()}: {tp_match.group()}')

    # Anticodon stem-loop-stem
    # Search for 5,7,5 patterns where outer 5's are reverse complementary
    # Start at index 15 because it seems unlikely for the anticodon loop to occur earlier
    ac_start = 0
    for i in range(20,len(seq)-16):
        ac_fp_stem = seq[i:i+5]
        ac_tp_stem = reverse_complement_regex(ac_fp_stem)
        # Checking for 'U' at this position based on observed consensus and to reduce regex use
        if ac_tp_stem != None and seq[i+6] == 'U':
            ac_expr = f'{ac_fp_stem}.U.{{5}}{ac_tp_stem}'
            ac_match = re.match(ac_expr, seq[i:])
            if ac_match != None:
                ac_start = i
                # print(f'{i:02}: {match.group()}')
                break
    
    # T stem-loop-stem
    # Search for 5,7,5 patterns where outer 5's are reverse complementary
    # t_start = 0
    # for j in range (len(seq)-17, ac_start, -1):
        # fp_stem = seq[j:j+5]
        # tp_stem = reverse_complement_regex(fp_stem)
        # Checking for 'U' at these position based on observed consensus and to reduce regex use
        # if tp_stem != None and seq[j+5] == 'U' and seq[j+6] == 'U':
            # expr = f'{fp_stem}UU.{{5}}{tp_stem}'
            # match = re.match(expr, seq[j:])
            # if match != None:
                # t_start = j
                # print(f'{i:02}: {match.group()}')
                # break
    
    # print('Anticodon Loop')
    # print(f'{ac_start:02}: {seq[ac_start:ac_start+17]}')
    # print('T Loop')
    # print(f'{t_start:02}: {seq[t_start:t_start+17]}')
    # print(f'{tp_match.start()-17}: {seq[tp_match.start()-17:tp_match.start()]}')

    print(f'{seq[:ac_start]}\t{seq[ac_start:min(ac_start+22,tp_match.start()-17)]}\t{seq[tp_match.start()-17:]}')