#!/bin/bash

# fasta_urls=fasta_urls.txt
# fastas_dir=source_fastas
dir=tRNALeu-analysis
fasta_urls=$dir/fasta_urls_all_archaea.txt
fastas_dir=$dir/source_fastas_all_archaea
alns_dir=$dir/gtrnadb_alns
cms_dir=$dir/cms

if [[ $# -ne 1 ]]; then
    echo "Exactly one arugment should be passed" >&2
    exit 2
fi

if [[ $1 != "A" && $1 != "B" && $1 != "F" ]]; then
    echo "Argument must be either 'A', 'B', or 'F'" >&2
    exit 2
fi

# DOWNLOAD FASTAS
if [[ $1 == "A" || $1 == "F" ]]; then
    while read url; do
        # Take all characters after the last forward slash to be the filename
        fasta_fname=${url##*/}
        curl --output $fastas_dir/$fasta_fname $url
    done < $fasta_urls
fi

if [[ $1 == "B" || $1 == "F" ]]; then
    for aa in Leu; do
        # EXTRACT BY ISOTYPE
        # Assuming each tRNA sequence takes up at most 2 rows or 2*60=120 base pairs
        # This is not always the case, but these longer sequences should almost certainly be low quality
        # and would be caught in manual review after the first pass
        # awk "/tRNA-$aa/ {n=3} n-- > 0 {if (n==1) {printf} else {print \$1}}" $fastas_dir/*.fa > $aa.fa
        # awk "/tRNA-$aa/,/^[AUCG]{1,59}\$/ {if (\$1 ~ /^[AUCG]{60}\$/) {printf} else {print \$1}}" $fastas_dir/*.fa > $aa.fa
        # Selects only the tRNAs of the desired isotype (Leu or Ser) and score of 55.0 or greater
        awk "/tRNA-$aa/ && !/Sc: ([0-4]?[0-9]\.[0-9]|5[0-4]\.[0-9])/ {n=3} n-- > 0 {if (n==1) {printf} else {print \$1}}" $fastas_dir/*.fa > $dir/$aa.fa
        # BUILD COVARIANCE MODEL FROM STO ALIGNMENT FILE FROM GtRNAdb
        cmbuild -F $cms_dir/arch-$aa.cm $alns_dir/arch-$aa.sto
        # ALIGN
        cmalign $cms_dir/arch-$aa.cm $dir/$aa.fa | awk "/^[A-Z]/ {print \$1; print \$2}; /^#=GR/ {print \$4} /^#=GC/ {print \$3}" > $dir/$aa-aligned.txt
        # EXTRACT T SLS (hard-coded numbers, need to manually verify each run)
        # awk '/[a-zA-Z]/ {if ($0 ~ /tRNA/) {print} else {print substr($0, 47, 16)}}' Leu-aligned.txt > Leu-extract.txt
        # awk '/[a-zA-Z]/ {if ($0 ~ /tRNA/) {print} else {print substr($0, 47, 19)}}' Ser-aligned.txt > Ser-extract.txt
        awk '/[a-zA-Z]/ {if ($0 ~ /tRNA/) {print} else {print substr($0, 48, 18)}}' $dir/$aa-aligned.txt > $dir/$aa-extract.txt
        # After this, I remove the last line from $aa-extract.txt (which is the consensus sequence)
        # And use vim macro to merge every two lines into a single comma-separated line of seq label,aligned seq
        awk 'NR % 2 == 1 { label = $0; next } { print label "," $0 }' $dir/$aa-extract.txt > $dir/$aa-extract.csv
    done
fi

# Steps:
# Download
# Extract by isotype and align with cmalign
# MANUALLY Identify poorly aligned sequences (these tend to have scores << 50)
# MANUALLY Remove problematic sequences from the original fasta in source_fastas folder
# Re-extract and re-align
