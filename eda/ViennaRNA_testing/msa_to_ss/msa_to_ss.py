import os
import re
import sys

def main(args):
    # if len(args) < 2:
        # exit("Provide path to MSA as argument")

    # msa_filepath = sys.argv[1]
    # aa = 'Leu'
    aa = 'Ser'
    msa_filepath = f'{aa}-aligned.txt'

    d_loop = (8,30)
    ac_loop = (31,47)
    # v_loop = (48,65)
    # t_loop = (66,84)
    v_loop = (48,67)
    t_loop = (68,84)

    if not os.path.isfile(msa_filepath):
        exit("MSA does not exist at the provided location")

    with open(msa_filepath, "r") as msa_file:
        lines = [line.strip() for line in msa_file.readlines()]

    '''
    for i in range(len(lines[-2])):
        if (i+1) % 10 == 0:
            print((i+1) // 10, end="")
        elif (i+1) % 5 == 0:
            print(",", end="")
        else:
            print(".", end="")

    print()
    print(lines[-2])
    print(lines[-1])
    '''

    regBases = re.compile('[^AUCGaucg]')
    with open (f'{aa}-extract-dloop.fa', 'w') as extract_dloop_file:
        for i in range(len(lines) // 3):
            extract_dloop_file.write(f'>{lines[3*i]}')
            extract_dloop_file.write('\n')
            seq = re.sub(regBases, '', lines[3*i+1][d_loop[0]-1:d_loop[1]])
            extract_dloop_file.write(seq.upper())
            extract_dloop_file.write('\n')

    with open (f'{aa}-extract-vloop.fa', 'w') as extract_vloop_file:
        for i in range(len(lines) // 3):
            extract_vloop_file.write(f'>{lines[3*i]}')
            extract_vloop_file.write('\n')
            seq = re.sub(regBases, '', lines[3*i+1][v_loop[0]-1:v_loop[1]])
            extract_vloop_file.write(seq.upper())
            extract_vloop_file.write('\n')

if __name__ == "__main__":
    main(sys.argv)

