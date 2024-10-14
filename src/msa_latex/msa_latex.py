import argparse
import msa_latex_utils as msalu

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Path to input alignment file in clustal format')
parser.add_argument('-s', '--species', help='Species of the tRNA in the alignemnt')
parser.add_argument('-a', '--algorithm', help='Algorithm used to produce the alignment')
args = parser.parse_args()

if not args.file:
    raise RuntimeError("File name is required")

if not args.species:
    raise RuntimeError("Species name is required")

if not args.algorithm:
    raise RuntimeError("Algorithm name is required")

# TODO: Optionally read colors from a config file
# Such a config could include more configuration/customization options
# NB: It might be more extensible to make this a dictionary
# and have msalu.define_macros() iterate through the keys of the dictionary
# TODO: Input validation of colors strings: /[0-9A-F]{6}/
doc_colors = msalu.DocumentColors(
    adenine_color='177E89',
    uracil_color='DB3A34',
    cytosine_color='FFC857',
    guanine_color='BBDBB4',
    anticodon_color='FF00FF',
    blank_color='FFFFFF'
)

config = msalu.Config(args, doc_colors)
msalu.print_tex_file(config)