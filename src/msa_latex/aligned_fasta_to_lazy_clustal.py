import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Path to input alignment file in clustal format')
args = parser.parse_args()

if args.file:
    aligned_fasta = args.file
else:
    raise RuntimeError("File name is required")

print('LAZY CLUSTAL O(1.2.1) multiple sequence alignment')
print()

seq = ''
with open(aligned_fasta) as f:
    for line in f:
        if line[0] == '>':
            print(seq)
            # Ignore starting '>' and ending newline
            # print(line[1:-1], end=' ')
            start_idx = line.index('tRNA')
            if ' ' in line:
                end_idx = line.index(' ')
                print(line[start_idx:end_idx], end=' ')
            else:
                print(line[start_idx:-1], end=' ')
            seq = ''
        else:
            # Ignore ending newline
            seq = seq + line[:-1]
print(seq)