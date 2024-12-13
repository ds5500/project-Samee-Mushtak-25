eda_bwa: eda/reference/metaCupr1-mature-tRNAs.fa
	bwa index eda/reference/metaCupr1-mature-tRNAs.fa
	bwa mem eda/reference/metaCupr1-mature-tRNAs.fa eda/eda.fq > eda/eda_bwa.sam
	cat eda/eda_bwa.sam

eda_bowtie2: eda/reference/metaCupr1-mature-tRNAs.fa
	bowtie2-build eda/reference/metaCupr1-mature-tRNAs.fa eda/reference/metaCupr1
	bowtie2 -x eda/reference/metaCupr1 -U eda/eda.fq -S eda/eda_bowtie2.sam
	cat eda/eda_bowtie2.sam

eda_clustalo:
	mkdir -p eda/clustalo-data
	cp eda/pyrococcus-furiosus/pyrococcus-furiosus.fasta eda/clustalo-data
	docker run --platform linux/amd64 --name $(shell date "+%Y%m%d_%H%M%S")_eda_clustalo -v $(PWD)/eda/clustalo-data:/data biocontainers/clustal-omega:v1.2.1_cv5 clustalo --infile=pyrococcus-furiosus.fasta --guidetree-out=pyrococcus-furiosus-guidetree.dnd --outfmt=clustal --resno --wrap=100 --output-order=input-order --outfile=pyrococcus-furiosus.clustal_num --seqtype=RNA
	ete3 view -t eda/clustalo-data/pyrococcus-furiosus-guidetree.dnd -i eda/clustalo-data/pyrococcus-furiosus-guidetree.png

eda_tcoffee:
	mkdir -p eda/tcoffee-data
	cp eda/pyrococcus-furiosus/pyrococcus-furiosus-query.fasta eda/tcoffee-data
	docker run --platform linux/amd64 --name $(shell date "+%Y%m%d_%H%M%S")_eda_tcoffee -v $(PWD)/eda/tcoffee-data:/data biocontainers/t-coffee:v12.00.7fb08c2-4-deb_cv1 t_coffee -in=pyrococcus-furiosus-query.fasta -method=mafft_msa muscle_msa probconsRNA_msa -output=score_html clustalw_aln fasta_aln score_ascii phylip -maxnseq=150 -maxlen=100 -case=upper -seqnos=on -outorder=input -run_name=eda -tree -mode=rcoffee -method_limits=consan_pair 5 150

eda_mafft:
	mkdir -p eda/mafft-data
	cp eda/pyrococcus-furiosus/pyrococcus-furiosus.fasta eda/mafft-data
	docker run --platform linux/amd64 --name $(shell date "+%Y%m%d_%H%M%S")_eda_mafft -v $(PWD)/eda/mafft-data:/data biocontainers/mafft:v7.407-2-deb_cv1 mafft --inputorder --anysymbol --kimura 1 --auto pyrococcus-furiosus.fasta > eda/mafft-data/pyrococcus-furiosus-aligned.fasta
	FastTree -nt -gtr -gamma eda/mafft-data/pyrococcus-furiosus-aligned.fasta > eda/mafft-data/pyrococcus-furiosus.tre
	ete3 view -t eda/mafft-data/pyrococcus-furiosus.tre -i eda/mafft-data/pyrococcus-furiosus-guidetree.png

bulk_process:
	./src/shell_scripts/process_trnas.sh

metal_reports:
	python src/metal_scoring.py -r full_seq
	python src/metal_scoring.py -r ac_loop
	python src/metal_scoring.py -r v_loop

trna_leu_analysis:
	python tRNALeu-analysis/scraper.py
	./tRNALeu-analysis/extract_type_ii.sh F
	python tRNALeu-analysis/archLeu-v-loop-stats.py

homology_network: tRNALeu-analysis/Leu-Vloop-stats.csv
	python src/homology_network.py

eda/reference/metaCupr1-mature-tRNAs.fa:
	mkdir -p eda/reference
	curl --output eda/reference/metaCupr1-mature-tRNAs.fa https://gtrnadb.ucsc.edu/genomes/archaea/Meta_cupr_Ar_4/metaCupr1-mature-tRNAs.fa
	sed -i -e 's/U/T/g' eda/reference/metaCupr1-mature-tRNAs.fa

release:
	zip -r bulk_output.zip bulk_output/
	zip -d bulk_output.zip bulk_output/.DS_Store
	for d in bulk_output/*/; do zip -d bulk_output.zip $$d.DS_Store; done
	unzip -l bulk_output.zip

clean_eda:
	rm -rf eda/reference

clean_bulk:
	rm -r bulk_output/*/

clean_leu:
	rm tRNALeu-analysis/fasta_urls_all_archaea.txt
	rm tRNALeu-analysis/Leu*
	rm tRNALeu-analysis/source_fastas_all_archaea/*

