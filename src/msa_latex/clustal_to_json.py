import json
import argparse
import msa_latex_utils as msalu

def print_json_file(alignment_file):
    alignment = msalu.read_alignment_file(alignment_file)

    mapper = { 'A':0, 'T':1, 'U':1, 'C':2, 'G':3, 'B':4, 'N':4 }

    data = []
    for i in range(alignment.alignment_len):
        base_num = 1
        for j in range(alignment.alignment_width):
            pt = {}
            base = alignment.seqs[i].seq[j]
            if base != '-':
                pt['seq_idx'] = i
                pt['seq_label'] = alignment.seqs[i].label
                pt['base_idx'] = j+1
                pt['base_label'] = base
                pt['base_color'] = mapper[base]
                pt['base_num'] = base_num
                data.append(pt)
                base_num += 1

    for i in range(alignment.alignment_width):
        consensus_base = alignment.seqs[0].seq[i]
        consensus = True
        for j in range(alignment.alignment_len):
            pt = {}
            if consensus and alignment.seqs[j].seq[i] != consensus_base:
                consensus = False
            if j == alignment.alignment_len - 1:
                pt['seq_idx'] = alignment.alignment_len
                pt['seq_label'] = 'Consensus'
                pt['base_idx'] = i+1
                pt['base_label'] = '⏺' if consensus else ' '
                pt['base_color'] = -1
                pt['base_num'] = i+1
                data.append(pt)
    print(json.dumps(data, ensure_ascii=False))

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Path to input alignment file in clustal format')
args = parser.parse_args()

if not args.file:
    raise RuntimeError("File name is required")

print_json_file(args.file)