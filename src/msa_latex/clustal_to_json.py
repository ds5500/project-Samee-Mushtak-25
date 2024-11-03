import argparse
import msa_latex_utils as msalu

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Path to input alignment file in clustal format')
parser.add_argument('-s', '--species', help='Species of the tRNA in the alignemnt')
parser.add_argument('-a', '--algorithm', help='Algorithm used to produce the alignment')
args = parser.parse_args()

if not args.file:
    raise RuntimeError("File name is required")

# if not args.species:
    # raise RuntimeError("Species name is required")

# if not args.algorithm:
    # raise RuntimeError("Algorithm name is required")

config = msalu.JsonConfig(args)
msalu.print_json_file(config)