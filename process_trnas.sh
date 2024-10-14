#!/bin/bash
# Remember to run `chmod +x process_trnas.sh` to make this script executable
# TODO: Error Handling

# Read comma separated list of trnas
IFS=,

# bulk_output directory must exist in same directory as Makefile prior to running this script
dir=bulk_output
# trnas.txt must also be in bulk_output directory prior to running this script
# Format of each line in trnas.txt: LABEL,URL
# TODO: Take only list of species name as input and use web crawling to find URL
input_trnas=$dir/trnas.txt
# FASTA containing hypothesized Type I and Type II primordial tRNAs
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
    # TODO: Implement caching to avoid repeated curl requests
    curl --output $working_dir/$fasta_fname $url

    # Prepend primordial tRNA sequences to tRNAs obtained from curl
    cat $primordial_trnas $working_dir/$fasta_fname > $working_dir/$fasta_fname-e
    rm $working_dir/$fasta_fname
    mv $working_dir/$fasta_fname-e $working_dir/$fasta_fname

    container_dir=$PWD/$working_dir
    clustalo_container_name=$(date "+%Y%m%d_%H%M%S")-$label-clustalo
    clustalo_dir=$working_dir/clustal-omega
    mkdir -p $clustalo_dir
    # TODO: Automatically remove docker containers that are created by this command
    docker run --platform linux/amd64 --name $clustalo_container_name -v $container_dir:/data biocontainers/clustal-omega:v1.2.1_cv5 clustalo --infile=$fasta_fname --guidetree-out=clustal-omega/$fasta_prefix-guidetree.dnd --outfmt=clustal --resno --wrap=150 --output-order=input-order --outfile=clustal-omega/$fasta_prefix.clustal_num --seqtype=RNA
    # Generate tree visualization from Newick format
    ete3 view -t $clustalo_dir/$fasta_prefix-guidetree.dnd -i $clustalo_dir/$fasta_prefix-guidetree.png
    # Visualize alignment
    python src/msa_latex/msa_latex.py -f $clustalo_dir/$fasta_prefix.clustal_num -s $fasta_prefix -a "Clustal Omega" > $clustalo_dir/$fasta_prefix.tex
    tectonic $clustalo_dir/$fasta_prefix.tex

    mafft_container_name=$(date "+%Y%m%d_%H%M%S")-$label-mafft
    mafft_dir=$working_dir/mafft
    mkdir -p $mafft_dir
    docker run --platform linux/amd64 --name $mafft_container_name -v $container_dir:/data biocontainers/mafft:v7.407-2-deb_cv1 mafft --inputorder --anysymbol --kimura 1 --auto --treeout $fasta_fname > $mafft_dir/$fasta_prefix-aligned.fasta
    mv $working_dir/$fasta_fname.tree $mafft_dir/$fasta_prefix-guidetree.tree
    # Remove numerical prefix and long suffix from IDs produced in MAFFT guidetree
    sed -E 's/^[0-9]+_//g' $mafft_dir/$fasta_prefix-guidetree.tree | sed 's/__tRNA.*$//g' > $mafft_dir/$fasta_prefix-guidetree-mod.tree
    # Generate tree visualization from Newick format
    ete3 view -t $mafft_dir/$fasta_prefix-guidetree-mod.tree -i $mafft_dir/$fasta_prefix-guidetree.png
    # Convert aligned fasta to "lazy" clustal format
    python src/msa_latex/aligned_fasta_to_lazy_clustal.py -f $mafft_dir/$fasta_prefix-aligned.fasta > $mafft_dir/$fasta_prefix-aligned.clustal
    # Visualize alignment
    python src/msa_latex/msa_latex.py -f $mafft_dir/$fasta_prefix-aligned.clustal -s $fasta_prefix -a "MAFFT" > $mafft_dir/$fasta_prefix.tex
    tectonic $mafft_dir/$fasta_prefix.tex

done < $input_trnas
