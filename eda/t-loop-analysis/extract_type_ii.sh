#!/bin/bash

fasta_urls=fasta_urls.txt
fastas_dir=source_fastas

# DOWNLOAD FASTAS
# while read url; do
    # Take all characters after the last forward slash to be the filename
    # fasta_fname=${url##*/}
    # curl --output $fastas_dir/$fasta_fname $url

# done < $fasta_urls

for aa in Leu Ser; do
    # EXTRACT BY ISOTYPE
    awk "/tRNA-$aa/ {n=3} n-- > 0 {if (n==1) {printf} else {print \$1}}" $fastas_dir/*.fa > $aa.fa
    # ALIGN
    cmalign archaea.cm $aa.fa | awk "/^[A-Z]/ {print \$1; print \$2}; /^#=GR/ {print \$4} /^#=GC/ {print \$3}" > $aa-aligned.txt
done

# Steps:
# Download
# Extract by isotype and align with cmalign
# MANUALLY Identify poorly aligned sequences (these tend to have scores << 50)
# MANUALLY Remove problematic sequences from the original fasta in source_fastas folder
# Re-extract and re-align