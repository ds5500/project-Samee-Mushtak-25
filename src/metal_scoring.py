import json
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--region', help='tRNA region to analyze')
args = parser.parse_args()

if not args.region:
    raise RuntimeError("Region is required")

fasta_dir = f'eda/all_alignments/{args.region}'
fasta_files = {
    'Manual' : f'{fasta_dir}/pyrFur2-manual.fasta',
    'Clustal Omega' : f'{fasta_dir}/pyrFur2-clustal-omega.fasta',
    'MAFFT' : f'{fasta_dir}/pyrFur2-mafft-aligned.fasta',
    'MAFFT-Kimura' : f'{fasta_dir}/pyrFur2-mafft-kimura-aligned.fasta',
    'Infernal' : f'{fasta_dir}/pyrFur2-infernal.fasta'
}
options = {
    'd_pos' : '-p',
    'd_ssp' : '-n',
    'd_simple' : '-s'
}

scores_list = []
for label_a, file_a in fasta_files.items():
    for label_b, file_b in fasta_files.items():
        # print(f'{label_a},{label_b}')
        score_data = {}
        score_data['row_label'] = label_a
        score_data['col_label'] = label_b
        for metric, option in options.items():
            # https://www.geeksforgeeks.org/python-subprocess-module/
            try:
                score_report = subprocess.check_output([
                    "metal", option, file_a, file_b
                ], text=True)
                # print(score_report)
                # Score can be given in scientific notation if it is less than 0.1
                score = float(score_report.split()[-1])
                # For text label
                score_data[metric] = score
                # For coloring
                score_data[metric + '_inv'] = 1 - score
            except subprocess.CalledProcessError as e:
                print(f"Command failed with return code {e.returncode}")
        scores_list.append(score_data)

print(json.dumps(scores_list))
