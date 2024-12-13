import os
import sys
import argparse
import subprocess
import requests


def download_fastas(fasta_urls, fastas_dir):
    with open(fasta_urls, "r") as file:
        for url in file:
            url = url.strip()
            fasta_fname = os.path.basename(url)
            if not os.path.exists(fastas_dir):
                os.makedirs(fastas_dir, exist_ok=True)

            response = requests.get(url, verify=False)

            if response.status_code != 200:
                print(f"Failed to download {url}")
                continue

            with open(os.path.join(fastas_dir, fasta_fname), "wb") as f:
                f.write(response.content)


def is_high_quality_sequence_id(s, aa):
    return f"tRNA-{aa}" in s and not any(
        score in s for score in [
            f"Sc: {i}.{j}" for i in range(0,55) for j in range(0,10)
        ])

def extract_by_isotype(fastas_dir, aa):
    output_file = f"{aa}.fa"
    with open(output_file, "w") as out_f:
        for fasta_file in os.listdir(fastas_dir):
            if fasta_file.endswith(".fa"):
                fasta_path = os.path.join(fastas_dir, fasta_file)
                with open(fasta_path, "r") as in_f:
                    lines = in_f.readlines()
                    i = 0
                    while i < len(lines):
                        if is_high_quality_sequence_id(lines[i], aa):
                            out_f.write(lines[i].split()[0] + "\n")
                            i += 1
                            while i < len(lines) and lines[i][0] != ">":
                                out_f.write(lines[i].strip())
                                i += 1
                            out_f.write("\n")
                        else:
                            i += 1


def extract_t_sls():
    with open("Leu-aligned.txt", "r") as leu_in, open(
        "Leu-extract.txt", "w"
    ) as leu_out:
        for line in leu_in:
            if any(char.isalpha() for char in line):
                if "tRNA" in line:
                    leu_out.write(line)
                else:
                    leu_out.write(line[46:62] + "\n")

    with open("Ser-aligned.txt", "r") as ser_in, open(
        "Ser-extract.txt", "w"
    ) as ser_out:
        for line in ser_in:
            if any(char.isalpha() for char in line):
                if "tRNA" in line:
                    ser_out.write(line)
                else:
                    ser_out.write(line[46:65] + "\n")

    with open("Leu-aligned.txt", "r") as leu_in, open(
        "Leu-extract.txt", "w"
    ) as leu_out:
        for line in leu_in:
            if any(char.isalpha() for char in line):
                if "tRNA" in line:
                    leu_out.write(line)
                else:
                    leu_out.write(line[47:65] + "\n")


def main():
    parser = argparse.ArgumentParser(description="Process tRNAs")
    parser.add_argument(
        "type", choices=["A", "B", "F"], help="Type of processing to perform"
    )
    args = parser.parse_args()

    fasta_urls = "fasta_urls_all_archaea.txt"
    fastas_dir = "source_fastas_all_archaea"
    alns_dir = "gtrnadb_alns"
    cms_dir = "cms"

    if args.type in ["A", "F"]:
        download_fastas(fasta_urls, fastas_dir)

    if args.type in ["B", "F"]:
        for aa in ["Leu", "Ser"]:
            extract_by_isotype(fastas_dir, aa)
            # Additional processing can be added here

    extract_t_sls()


if __name__ == "__main__":
    main()
