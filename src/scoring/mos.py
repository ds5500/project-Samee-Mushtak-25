import glob
import msa_latex_utils as msalu

def mos_report(files):
    alignments = {}
    for file in files:
        file_split = file.split('/')
        file_key = file_split[-2] + '/' + file_split[-1]
        alignments[file_key] = msalu.read_alignment_file(file)

    aligned_residue_sets = {}
    for label, alignment in alignments.items():
        l = alignment.alignment_len
        w = alignment.alignment_width

        aligned_residue_set = set()
        for i in range(l):
            for j in range(i+1, l):
                res_a_no = 0
                res_b_no = 0
                for k in range(w):
                    res_a = alignment.seqs[i].seq[k]
                    res_b = alignment.seqs[j].seq[k]
                    if res_a != '-':
                        res_a_no += 1
                    if res_b != '-':
                        res_b_no += 1
                    if res_a != '-' and res_b != '-':
                        aligned_residue_set.add( (i, res_a_no, j, res_b_no) )
        aligned_residue_sets[label] = aligned_residue_set

    set_pairs = 0
    total_overlap_score = 0
    for label_a, aligned_residue_set_a in aligned_residue_sets.items():
        for label_b, aligned_residue_set_b in aligned_residue_sets.items():
            if label_a != label_b:
                set_pairs += 1
                total_overlap_score += 2 * len(aligned_residue_set_a.intersection(aligned_residue_set_b)) / \
                    (len(aligned_residue_set_a) + len(aligned_residue_set_b))
    print('Average overlap score:')
    print(total_overlap_score / set_pairs)

    for label_a, aligned_residue_set_a in aligned_residue_sets.items():
        print(f'{label_a} MOS:')
        den = len(aligned_residue_set_a) * (len(aligned_residue_sets) - 1)
        num = 0
        for label_b, aligned_residue_set_b in aligned_residue_sets.items():
            if label_a != label_b:
                for pair in aligned_residue_set_a:
                    if pair in aligned_residue_set_b:
                        num += 1
        print(num / den)

# input_dir = 'scoring/alignments/'
# mos_report(glob.iglob(input_dir + '*.clustal*'))