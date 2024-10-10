alignment = 'pyrFur2-aligned.fasta'
species = 'Pyrococcus furiosus'
anchor = 'tRNA'
label_len = 17
seq_start = 49
seq_end = 146
seq_len = seq_end - seq_start + 1

# Right now the code depends on my custom color definitions and macros in a LaTeX file on Overleaf

print(f'\\textit{{{species}}} tRNA Alignment')
print()

tens = 0
tens_row = [(i + 1) // 10 if (i+1) % 5 == 0 else -1 for i in range(seq_len)]
ones_row = [(i+1) % 10 if (i+1) % 5 == 0 else -1 for i in range(seq_len)]
# Render digit label only every 5 base pairs in the alignment
# Use hex for tens digits above 9
mapper = lambda x : '\\colorbox{-}{\\texttt{·}}' if x < 0 else f'\colorbox{{-}}{{\\texttt{{{hex(x)[-1].upper()}}}}}'

print(f'\\phantom{{\\texttt{{{"x"*label_len}}}}}')
print(''.join([mapper(digit) for digit in tens_row]))
print()
print('\\vspace{-0.5mm}')
print()
print(f'\\phantom{{\\texttt{{{"x"*label_len}}}}}')
print(''.join([mapper(digit) for digit in ones_row]))
print()

with open(alignment) as f:
    for i in range(3):
        f.readline()

    for line in f:
        row = line.split()
        if row[0][0] != '*':
            # Get parts of string after anchor
            label = anchor + row[0].partition(anchor)[2]
            label = label.replace('_','-').rjust(label_len, '.')

            seq = ''.join([
                f'\\rnabox{{{c}}}' for c in row[1]
            ])

            print(f'\\texttt{{{label}}}')
            print(seq)
            print()
            print('\\vspace{-0.5mm}')
            print()
        else:
            print(f'\\phantom{{\\texttt{{{"x"*label_len}}}}}')
            print(''.join([
                f'\\colorbox{{-}}{{\\texttt{{{c}}}}}' for c in line[seq_start-1:seq_end]
            ]))
