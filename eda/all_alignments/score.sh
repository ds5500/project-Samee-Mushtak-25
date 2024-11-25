#!/bin/bash

fasta_dir=full_seq
for file_a in $fasta_dir/*.fasta
do
    for file_b in $fasta_dir/*.fasta
    do
        echo $file_a $file_b
        metal $file_a $file_b
    done
done
