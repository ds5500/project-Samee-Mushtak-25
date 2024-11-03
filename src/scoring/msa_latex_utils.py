import argparse

class DocumentColors:
    def __init__(self, adenine_color, uracil_color, cytosine_color, guanine_color, anticodon_color, blank_color):
        self.adenine_color = adenine_color
        self.uracil_color = uracil_color
        self.cytosine_color = cytosine_color
        self.guanine_color = guanine_color
        self.anticodon_color = anticodon_color
        self.blank_color = blank_color

class AlignedSequence:
    def __init__(self, alignment_row:str, anchor:str):
        ls = alignment_row.split()
        self.full_label = ls[0]
        if anchor is not None:
            self.label = self.full_label[self.full_label.index(anchor):]
        else:
            self.label = self.full_label
        self.seq = ls[1]
        self.seq_len = len(self.seq) - self.seq.count('-')

class Alignment:
    def __init__(self, alignment_rows:list[AlignedSequence]):
        self.seqs = alignment_rows
        self.max_label_len = max([
            len(seq.label) for seq in self.seqs
        ])
        self.alignment_len = len(self.seqs)
        # Assuming all aligned sequences in alignment_rows have the same length
        self.alignment_width = len(self.seqs[0].seq)

class Config:
    def __init__(self, args:argparse.Namespace, doc_colors:DocumentColors):
        self.alignment_file = args.file
        self.species = args.species
        self.algorithm = args.algorithm
        self.document_colors = doc_colors

def print_header(doc_colors:DocumentColors):
    # TODO: Remove page numbering
    print('\\documentclass{article}')
    # Page setup could be moved into a config with the colors
    print('\\usepackage[a2paper,landscape,margin=0.5in]{geometry}')
    print('\\usepackage{xcolor}')
    print()
    define_macros(doc_colors)
    print()
    print('\\begin{document}')
    print()

def define_macros(doc_colors:DocumentColors):
    '''
    Defines the colors to be used in the document and the macros for displaying characters
    '''
    print(f'\\definecolor{{A}}{{HTML}}{{{doc_colors.adenine_color}}}')
    print(f'\\definecolor{{U}}{{HTML}}{{{doc_colors.uracil_color}}}')
    print(f'\\definecolor{{C}}{{HTML}}{{{doc_colors.cytosine_color}}}')
    print(f'\\definecolor{{G}}{{HTML}}{{{doc_colors.guanine_color}}}')
    print(f'\\definecolor{{B}}{{HTML}}{{{doc_colors.anticodon_color}}}')
    print(f'\\definecolor{{N}}{{HTML}}{{{doc_colors.anticodon_color}}}')
    print(f'\\definecolor{{-}}{{HTML}}{{{doc_colors.blank_color}}}')
    print()
    print('\\newcommand{\\rnabox}[1]{\\colorbox{#1}{\\texttt{#1}}}')
    print('\\newcommand{\\digitbox}[1]{\\colorbox{-}{\\texttt{#1}}}')
    # TODO: Make a macro for \phantom{\texttt{#1}} ?

def print_title(species:str, algorithm:str):
    print(f'\\textit{{{species.replace('_','-')}}} tRNA Alignment: {algorithm}')
    print()

def print_position_markers(label_len:int, seq_len:int):
    '''
    Prints the top two rows of the MSA. Used to identify the index of a base in the alignment.
    '''
    tens_row = [(i+1) // 10 if (i+1) % 5 == 0 else -1 for i in range(seq_len)]
    ones_row = [(i+1) % 10 if (i+1) % 5 == 0 else -1 for i in range(seq_len)]
    # Render digit label only every 5 base pairs in the alignment
    # Use hex for tens digits above 9 (seq_len >= 160 is not handled)
    mapper = lambda x : '\\digitbox{·}' if x < 0 else f'\\digitbox{{{hex(x)[-1].upper()}}}'

    print(f'\\phantom{{\\texttt{{{"x"*label_len}}}}}')
    print(''.join([mapper(digit) for digit in tens_row]))
    print()
    print('\\vspace{-0.5mm}')
    print()
    print(f'\\phantom{{\\texttt{{{"x"*label_len}}}}}')
    print(''.join([mapper(digit) for digit in ones_row]))
    print()

def print_alignment(alignment:Alignment):
    '''
    Prints alignment as colored grid of bases
    '''
    for i in range(alignment.alignment_len):
        seq = alignment.seqs[i]
        padded_label = seq.label.replace('_','-').rjust(alignment.max_label_len, '.')

        formatted_seq = ''.join([
            f'\\rnabox{{{base}}}' for base in seq.seq
        ])

        print(f'\\texttt{{{padded_label}}}')
        print(formatted_seq)
        print()
        if i == alignment.alignment_len - 1:
            print('\\vspace{-0.2mm}')
        else:
            print('\\vspace{-0.5mm}')
        print()

def print_consensus(alignment:Alignment):
    '''
    Prints consensus markers below alignment at positions where all tRNAs have the same base
    '''
    print(f'\\phantom{{\\texttt{{{"x"*alignment.max_label_len}}}}}')
    for i in range(alignment.alignment_width):
        consensus_base = alignment.seqs[0].seq[i]
        consensus = True
        for j in range(alignment.alignment_len):
            if consensus and alignment.seqs[j].seq[i] != consensus_base:
                consensus = False
            if j == alignment.alignment_len - 1:
                print(f'\\digitbox{{{"*" if consensus else ' '}}}', end='')
    print()
    print()

def print_footer():
    print('\\end{document}')

def read_alignment_file(alignment_file)->Alignment:
    alignment_seqs = []
    with open(alignment_file) as f:
        # Ignore header rows
        for i in range(3):
            f.readline()

        alignment_seqs = [
            # Start the display label from 'tRNA'
            AlignedSequence(line, anchor='tRNA')
            for line in f
            # Ignore consensus row, if it exists
            if '*' not in line
        ]

    return Alignment(alignment_seqs)

def print_tex_file(cfg:Config):
    alignment_file = cfg.alignment_file
    species = cfg.species
    algorithm = cfg.algorithm
    doc_colors = cfg.document_colors

    alignment = read_alignment_file(alignment_file)

    print_header(doc_colors)
    print_title(species, algorithm)
    print_position_markers(alignment.max_label_len, alignment.alignment_width)
    print_alignment(alignment)
    print_consensus(alignment)
    print_footer()
