eda_bwa: eda/reference/metaCupr1-mature-tRNAs.fa
	bwa index eda/reference/metaCupr1-mature-tRNAs.fa
	bwa mem eda/reference/metaCupr1-mature-tRNAs.fa eda/eda.fq > eda/eda_bwa.sam
	cat eda/eda_bwa.sam

eda_bowtie2: eda/reference/metaCupr1-mature-tRNAs.fa
	bowtie2-build eda/reference/metaCupr1-mature-tRNAs.fa eda/reference/metaCupr1
	bowtie2 -x eda/reference/metaCupr1 -U eda/eda.fq -S eda/eda_bowtie2.sam
	cat eda/eda_bowtie2.sam

eda/reference/metaCupr1-mature-tRNAs.fa:
	mkdir -p eda/reference
	curl --output eda/reference/metaCupr1-mature-tRNAs.fa https://gtrnadb.ucsc.edu/genomes/archaea/Meta_cupr_Ar_4/metaCupr1-mature-tRNAs.fa
	sed -i -e 's/U/T/g' eda/reference/metaCupr1-mature-tRNAs.fa

clean_eda:
	rm -rf eda/reference