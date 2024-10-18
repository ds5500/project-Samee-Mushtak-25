# Project Overview

## Results

[!Pyrococcus furiosus alignment with Clustal Omega](alignments-20241018/Pyr_fur-CO.png)

[!Pyrococcus furiosus alignment with MAFFT](alignments-20241018/Pyr_fur-MAFFT.png)

[!Haloferax volcanii alignment with Clustal Omega](alignments-20241018/Halo_vol-CO.png)

[!Haloferax volcanii alignment with MAFFT](alignments-20241018/Halo_vol-MAFFT.png)

[!Chlorobium chlorochromatii alignment with Clustal Omega](alignments-20241018/Chlo_chlo-CO.png)

[!Chlorobium chlorochromatii alignment with MAFFT](alignments-20241018/Chlo_chlo-MAFFT.png)

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
