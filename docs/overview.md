# Project Overview

## Results

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
