import os
import msa_latex_utils as msalu

def cost(b1, b2):
    return 1 if b1 != b2 else 0

def score(b1, b2):
    # Blank
    if b1 == '-' and b2 == '-':
        return 0
    # Gap
    elif b1 == '-' or b2 == '-':
        return -2
    # Mismatch
    elif b1 != b2:
        return -1
    # Match
    else:
        return 1

alignments = {}
input_dir = 'scoring/alignments/'
for alignment_file in os.listdir(input_dir):
    alignments[alignment_file] = msalu.read_alignment_file(os.path.join(input_dir, alignment_file))

for label, alignment in alignments.items():
    print(label)
    sop_cost = 0
    sop_score = 0
    l = alignment.alignment_len
    w = alignment.alignment_width
    for i in range(l):
        for j in range(i+1, l):
            for k in range(w):
                sop_score += score(alignment.seqs[i].seq[k], alignment.seqs[j].seq[k])
                sop_cost += cost(alignment.seqs[i].seq[k], alignment.seqs[j].seq[k])
    print(f'Score: {sop_score}')
    print(f'Cost: {sop_cost}')