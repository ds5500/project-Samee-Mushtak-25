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

eda/reference/metaCupr1-mature-tRNAs.fa:
	mkdir -p eda/reference
	curl --output eda/reference/metaCupr1-mature-tRNAs.fa https://gtrnadb.ucsc.edu/genomes/archaea/Meta_cupr_Ar_4/metaCupr1-mature-tRNAs.fa
	sed -i -e 's/U/T/g' eda/reference/metaCupr1-mature-tRNAs.fa

clean_eda:
	rm -rf eda/reference
