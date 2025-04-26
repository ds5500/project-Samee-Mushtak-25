# Project Overview

## Results

### _Pyrococcus furiosus_ alignment with Clustal Omega

![Pyrococcus furiosus alignment with Clustal Omega](../figs/alignments-20241018/Pyr_fur-CO.png)

* Key regions of the tRNA (5' acceptor stem, andticodon loop, variable loop, 3' CCA tail) visually appear to be well aligned

### _Pyrococcus furiosus_ alignment with MAFFT

![Pyrococcus furiosus alignment with MAFFT](../figs/alignments-20241018/Pyr_fur-MAFFT.png)

* The variable loops of the Leu and Ser tRNAs do not align with the variable loop of the primordial type II tRNA

### _Haloferax volcanii_ alignment with Clustal Omega

![Haloferax volcanii alignment with Clustal Omega](../figs/alignments-20241018/Halo_vol-CO.png)

* Abnormally long post D loop in NNN tRNA
* Some tRNAs are missing the 3' CCA tail

### _Haloferax volcanii_ alignment with MAFFT

![Haloferax volcanii alignment with MAFFT](../figs/alignments-20241018/Halo_vol-MAFFT.png)

* This MAFFT alignment is less wide than the above Clustal Omega alignment

### _Chlorobium chlorochromatii_ alignment with Clustal Omega

![Chlorobium chlorochromatii alignment with Clustal Omega](../figs/alignments-20241018/Chlo_chlo-CO.png)

* Portions of some non-type II tRNAs are aligning in the type II variable loop region
* 3' CCA tail are not aligning well

### _Chlorobium chlorochromatii_ alignment with MAFFT

![Chlorobium chlorochromatii alignment with MAFFT](../figs/alignments-20241018/Chlo_chlo-MAFFT.png)

* Alignment in variable loop region looks better, and correctly captures that Tyr tRNA is type II in bacteria (see https://www.preprints.org/manuscript/202209.0189/v1)

We are looking for a more methodologically sound way to generate phylogenetic trees from alignment files as the guidetrees produced by alignment algorithms are quick heuristics that do not truly take evolutionary distance in account.

## Challenges

* There is not a universally best alignment algorithm. Different algorithms can perform well on different species, and even varying parameters of the same algorithm can yield markedly different results.
* tRNA sequences that are more evolutionarily derived seem to be harder to align.

## Next Steps

* Try more alignment algorithms
    * T-Coffee, MUSCLE, ProbconsRNA
    * Also, try varying parameters used in existing algorithms
* Developing metrics for assessing the quality of alignments
    * Focusing on metrics that are independent of a reference alignment since these are time-consuming to construct
* Improve pipeline script
    * Port to Python for cross-platform reproducibility
    * Use web crawler to automatically find FASTA URLs from GtRNAdb
* Improve visualizations, allowing for interactivity
    * Considering [Observable Framework](https://observablehq.com/framework/) or [Streamlit](https://streamlit.io/)
