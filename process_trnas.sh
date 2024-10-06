#!/bin/bash
# Remember to run `chmod +x process_trnas.sh` to make this script executable

# Read comma separated list of trnas
IFS=,

# bulk_output directory must exist in same directory as Makefile prior to running this script
dir=bulk_output
# trnas.txt must also be in bulk_output directory prior to running this script
# Format of each line in trnas.txt: LABEL,URL
input_trnas=$dir/trnas.txt
# FASTA containing hypothesized Type I and Type II primordial trnas
primordial_trnas=$dir/primordial_trnas.fa
# Remember to put a newline at the end of trnas.txt and primordial_trnas.fa

while read label url; do 
    working_dir=$dir/$label-data
    mkdir -p $working_dir

    # Take all characters after the last forward slash to be the filename
    fasta_fname=${url##*/}
    # $fasta_prefix assumes that $fasta_fname is of the form <PREFIX>-mature-tRNAs.fa
    # Could also use $label
    fasta_prefix=${fasta_fname%%-*}
    echo "Downloading $fasta_fname"
    curl --output $working_dir/$fasta_fname $url

    cat $primordial_trnas $working_dir/$fasta_fname > $working_dir/$fasta_fname-e
    rm $working_dir/$fasta_fname
    mv $working_dir/$fasta_fname-e $working_dir/$fasta_fname

    # TODO: Automatically remove docker containers that are created by this command
    container_name=$(date "+%Y%m%d_%H%M%S")-$label-clustalo
    container_dir=$PWD/$working_dir
    docker run --platform linux/amd64 --name $container_name -v $container_dir:/data biocontainers/clustal-omega:v1.2.1_cv5 clustalo --infile=$fasta_fname --guidetree-out=$fasta_prefix-guidetree.dnd --outfmt=clustal --resno --wrap=150 --output-order=input-order --outfile=$fasta_prefix.clustal_num --seqtype=RNA
    ete3 view -t $working_dir/$fasta_prefix-guidetree.dnd -i $working_dir/$fasta_prefix-guidetree.png
done < $input_trnas