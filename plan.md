# Plan

## Approach

### Phase 1: Automated pipeline for aligning tRNA sequences

The automated ingestion of tRNA sequences from GtRNAdb can be facilitated using a web-crawling framework such as [Scrapy](https://scrapy.org/). To align these tRNA sequences with respect to a reference primordial sequence, we will focus on using sequence alignment libraries which are found in the [Bioconda](https://bioconda.github.io/) channel of conda. This includes, but is not limited to,

* [Bowtie 2](https://bowtie-bio.sourceforge.net/bowtie2/index.shtml)
* [BWA](https://bio-bwa.sourceforge.net/)
* [HMMER 2](http://hmmer.org/documentation.html)
* [MACSE](https://www.agap-ge2pop.org/macse/)

The alignments produced by these algorithms will be compared to ground truth alignments[^1] produced by Dr. Lei Lei and Dr. Zachary Burton using standard metrics of [genetic distance](https://www.sciencedirect.com/topics/immunology-and-microbiology/genetic-distance). If one of these algorithms produces sufficiently accurate alignments (the threshold for which will be determined through discussions with Dr. Jennifer Spillane), then we will use that algorithm to produce alignments for tRNA sequences outside of our ground truth set and proceed to the next phase of the project. Otherwise, we will consider other algorithms and/or pre-/postprocessing steps to improve the quality of the alignments.

### Phase 2: 3-dimensional phylogenetic tree visualization

To begin with, we will use the alignments created in the first phase of this project to create a standard phylogenetic tree using Python libraries like [ETE Toolkit](http://etetoolkit.org/) or [Phylo](https://biopython.org/wiki/Phylo). We will then use [NetworkX](https://networkx.org/documentation/stable/index.html) to treat the phylogenetic tree as an abstract graph and embed the graph in three dimensions. This visualization could be enhanced with t-SNE or hierarchical clustering, using genetic distance as the metric.

## Project Management

### Milestones

| Week | Milestone                 | Date   |
| ---  | ---                       | ---    |
| 3    | Proposal v1               | 20 Sep |
| 4    | Checkin 1                 | 27 Sep |
| 5    | Checkin 2                 |  4 Oct |
| 6    | Checkin 3                 | 11 Oct |
| 7    | Project v1 due            | 18 Oct |
| 8    | Project v1 presentations  | 25 Oct |
| 9    | Proposal v2               |  1 Nov |
| 10   | Checkin 1                 |  8 Nov |
| 11   | Checkin 2                 | 15 Nov |
| 12   | Checkin 3                 | 22 Nov |
| 14   | Presentations             |  5 Dec |
| 15   | Final submission          | 12 Dec |

### Risks

* If none of the existing alignment algorithms exhibit acceptable performance for this alignment task, additional research will need to be done on how to specialize or modify these algorithms. It may also be necessary to consider developing custom algorithms for this alignment task.
* There may be methodological flaws in my approach to create the 3D visualization. For example, it is unclear whether using t-SNE on low-dimensional data will produce any meaningful results as it is typically used to visualize high-dimensional data.

## EDA

To assess the feasibility of using existing command line alignment utilities for our project, we tested [BWA](https://bio-bwa.sourceforge.net/) on a FASTA file of mature tRNAs found on the GtRNAdb[^2]. This FASTA file served as the reference genome. We also manually created a FASTAQ file with fourth sequences:
1. TEST.THR: A Threonine tRNA with one deletion
2. TEST.LYS: A Lysine tRNA with no modifications
3. TEST.GARBAGE: A long arbitrary sequence of base pairs that should not align with any of the tRNAs in the reference genome
4. TEST.COMMON: A sequence that is three-base pairs long and which is expected to occur in multiple tRNAs

Below is (part of) the output [SAM file](https://samtools.github.io/hts-specs/SAMv1.pdf) produced by BWA:

```
...
@HD	VN:1.5	SO:unsorted	GO:query
@PG	ID:bwa	PN:bwa	VN:0.7.18-r1243-dirty	CL:bwa mem eda/reference/metaCupr1-mature-tRNAs.fa eda/eda.fq
TEST.THR	0	Metallosphaera_cuprina_Ar-4_tRNA-Thr-CGT-1-1	1	60	10M1D62M	*	0	0	GCCGCTGTAGTCAGCTGGTAGAGCGCCGGCCTCGTAAGCCGGTGGTCGCGGGTTCAAATCCCGCCGGCGGCT	AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA	NM:i:1	MD:Z:10^C62	AS:i:65	XS:i:0
TEST.LYS	0	Metallosphaera_cuprina_Ar-4_tRNA-Lys-TTT-1-1	1	60	77M	*	0	0	GGGCCCGTAGCTCAGCTAGGTAGAGCGGCGGGCTTTTAACCCGTAGGCCCCGGGTTCGAATCCCGGCGGGCCCGCCA	AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA	NM:i:0	MD:Z:77	AS:i:77	XS:i:27
TEST.GARBAGE	4	*	0	0	*	*	0	0	GTGTGAGCCTTAGGCTTCGCGGAATCGGCTAGCTAGATGTAGGGGAGCGTTCTTCTCCGGCGCGGGCGATTATGAGGCTACG	AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA	AS:i:0	XS:i:0
TEST.COMMON	4	*	0	0	*	*	0	0	GCG	AAA	AS:i:0	XS:i:0
```

The above output shows that TEST.THR was aligned to Metallosphaera_cuprina_Ar-4_tRNA-Thr-CGT-1-1, TEST.LYS was aligned to TEST.LYS, and TEST.GARBAGE and TEST.COMMON were not aligned to any tRNA in the reference. Additionally, the CIGAR string for TEST.THR, 10M1D62M, indicates that 1 deletion was detected and that the remaining 10 + 62 = 72 base pairs were a match. Similarly, the CIGAR string for TEST.LYS, 77M, indicates that all 77 base pairs of that sequence were a match.

Next, to assess the replicability of our sequencing results across multiple alignment algorithms, we performed the same test using [Bowtie 2](https://bowtie-bio.sourceforge.net/bowtie2/index.shtml). Below is (part of) the output SAM file produced by Bowtie 2:

```
@HD	VN:1.5	SO:unsorted	GO:query
...
@PG	ID:bowtie2	PN:bowtie2	VN:2.5.4	CL:"/Users/smushtak/miniconda3/envs/trna/bin/bowtie2-align-s --wrapper basic-0 -x eda/reference/metaCupr1 -S eda/eda_bowtie2.sam -U eda/eda.fq"
TEST.THR	0	Metallosphaera_cuprina_Ar-4_tRNA-Thr-CGT-1-1	1	42	10M1D62M	*	0	0	GCCGCTGTAGTCAGCTGGTAGAGCGCCGGCCTCGTAAGCCGGTGGTCGCGGGTTCAAATCCCGCCGGCGGCT	AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA	AS:i:-8	XN:i:0	XM:i:0	XO:i:1	XG:i:1	NM:i:1	MD:Z:10^C62	YT:Z:UU
TEST.LYS	0	Metallosphaera_cuprina_Ar-4_tRNA-Lys-TTT-1-1	1	42	77M	*	0	0	GGGCCCGTAGCTCAGCTAGGTAGAGCGGCGGGCTTTTAACCCGTAGGCCCCGGGTTCGAATCCCGGCGGGCCCGCCA	AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA	AS:i:0	XN:i:0	XM:i:0	XO:i:0	XG:i:0	NM:i:0	MD:Z:77	YT:Z:UU
TEST.GARBAGE	4	*	0	0	*	*	0	0	GTGTGAGCCTTAGGCTTCGCGGAATCGGCTAGCTAGATGTAGGGGAGCGTTCTTCTCCGGCGCGGGCGATTATGAGGCTACG	AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA	YT:Z:UU
TEST.COMMON	16	Metallosphaera_cuprina_Ar-4_tRNA-Ser-GCT-1-1	75	1	3M	*	0	0	CGC	AAA	AS:i:0	XS:i:0	XN:i:0	XM:i:0	XO:i:0	XG:i:0	NM:i:0	MD:Z:3	YT:Z:UU
```

The test sequences from the FASTAQ file were aligned to the same tRNAs in the reference, and for those sequences which were successfully aligned, they had identical CIGAR strings as to what was found in the BWA alignment, confirming that alignments can be replicated by different algorithms. The major difference between the BWA alignment and the Bowtie 2 alignment is that the TEST.COMMON sequence is aligned to a tRNA in the reference. Since for our project the size of the test sequences is expected to be comparable to the size of the reference genome of primordial tRNA, the potential for false discoveries of this kind should be low, but it is something we will be aware of going forward.

## github-pages

* tRNA alignments can be displayed on a webpage in a simple textual format, using CSS styling to highlight regions of alignment.
* We will consider using a 3D plotting library supported by [Observable](https://observablehq.com/) to create the 3D visualization. Examples:
  * [d3-3d](https://github.com/Niekes/d3-3d)
  * [Apache ECharts](https://echarts.apache.org/examples/en/editor.html?c=scatter3D-dataset&gl=1)
  * [MorphCharts](https://morphcharts.com/#getting-started-layouts-scatter)

[^1]: Ground truth alignments exist for the following species: *Homo sapiens*, *Caenorhabditis elegans*, *Arabidopsis thaliana*, *Alphaproteobacteria*, *Haloferax volcanii*, *Drosophila melanogaster*, *Methanosarcina barkeri*, *Cyanobacterium aponinum*, *Chlorobium chlorochromati*
[^2]: Because most alignment utilities handle DNA sequences and not RNA sequences, we used `sed` to replace all Uracils in the sequences with Thymines (i.e, replacing all "U"s with "T"s). For future analysis, we may consider using genomic FASTAs.
