import glob
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

def sop_report(files):
    alignments = {}

    for file in files:
        file_split = file.split('/')
        file_key = file_split[-2] + '/' + file_split[-1]
        alignments[file_key] = msalu.read_alignment_file(file)

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

# input_dir = 'scoring/alignments/'
# sop_report(glob.iglob(input_dir + '*.clustal*'))