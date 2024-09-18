# Plan

## Approach

### Phase 1: Automated pipeline for aligning tRNA sequences

The automated ingestion of tRNA sequences from GtRNAdb can be facilitated using a web-crawling framework such as [Scrapy](https://scrapy.org/). To align these tRNA sequences with respect to a reference primordial sequence, I will focus on using sequence alignment libraries which are found in the [Bioconda](https://bioconda.github.io/) channel of conda. This includes, but is not limited to,

* [Bowtie 2](https://bowtie-bio.sourceforge.net/bowtie2/index.shtml)
* [BWA](https://bio-bwa.sourceforge.net/)
* [HMMER 2](http://hmmer.org/documentation.html)
* [MACSE](https://www.agap-ge2pop.org/macse/)

The alignments produced by these algorithms will be compared to ground truth alignments[^1] produced by Dr. Lei Lei and Dr. Zachary Burton using standard metrics of [genetic distance](https://www.sciencedirect.com/topics/immunology-and-microbiology/genetic-distance). If one of these algorithms produces sufficiently accurate alignments (the threshold for which will be determined through discussions with Dr. Jennifer Spillane), then I will use that algorithm to produce alignments for tRNA sequences outside of our ground truth set and proceed to the next phase of the project. Otherwise, I will consider other algorithms and/or pre-/postprocessing steps to improve the quality of the alignments.

### Phase 2: 3-dimensional phylogenetic tree visualization

To begin with, I will use the alignments created in the first phase of this project to create a standard phylogenetic tree using Python libraries like [ETE Toolkit](http://etetoolkit.org/) or [Phylo](https://biopython.org/wiki/Phylo). I will then use [NetworkX](https://networkx.org/documentation/stable/index.html) to treat the phylogenetic tree as an abstract graph and embed the graph in three dimensions. This visualization could be enhanced with t-SNE or hierarchical clustering, using genetic distance as the metric.

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

## github-pages

* tRNA alignments can be displayed on a webpage in a simple textual format, using CSS styling to highlight regions of alignment.
* I will consider using a 3D plotting library supported by [Observable](https://observablehq.com/) to create the 3D visualization. Examples:
  * [d3-3d](https://github.com/Niekes/d3-3d)
  * [Apache ECharts](https://echarts.apache.org/examples/en/editor.html?c=scatter3D-dataset&gl=1)
  * [MorphCharts](https://morphcharts.com/#getting-started-layouts-scatter)

[^1] Ground truth alignments exist for the following species: *Homo sapiens*, *Caenorhabditis elegans*, *Arabidopsis thaliana*, *Alphaproteobacteria*, *Haloferax volcanii*, *Drosophila melanogaster*, *Methanosarcina barkeri*, *Cyanobacterium aponinum*, *Chlorobium chlorochromati*
