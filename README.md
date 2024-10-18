# tRNA

* [Proposal](proposal.md)
* [Plan](plan.md)

## Conda Setup

Running the code in this project requires **Make** and **Bioconda**.

To install Make in your conda environment:

```
conda install make
```

To configure your conda to use the Bioconda channel: (see also the [Bioconda documentation](https://bioconda.github.io/index.html))

```
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
```

While in this directory, run the following conda commands to create the required conda environment:

```
conda create -n trna python=3.12
conda install bioconda::bowtie2
conda install bioconda::bwa
conda install -c conda-forge ete3
conda install bioconda::fasttree
conda install conda-forge::tectonic
```

## Docker Setup

In order to run process_trnas.sh (`make bulk_process`), the following Docker images will need to be installed.

```
docker pull biocontainers/clustal-omega:v1.2.1_cv5
```

```
docker pull biocontainers/mafft:v7.407-2-deb_cv1
```

```
docker pull biocontainers/t-coffee:v12.00.7fb08c2-4-deb_cv1
```

Docker Desktop must be running in the background for process_trnas.sh to work (see [Docker's instructions](https://docs.docker.com/engine/install/) on installing Docker Desktop).

## EDA

To run the EDA for BWA:

```
make eda_bwa
```

To run the EDA for Bowtie 2:

```
make eda_bowtie2
```

To clean the output from the EDA:

```
make clean_eda
```

Because BWA and Bowtie 2 have different formats for FASTA indexing, the `make clean_eda` command should be run in between different EDAs.

See [plan.md](plan.md) for a discussion of the results of this EDA. We have not yet implemented visualizations of alignments, so we display our results in a textual format instead of with figures.

## Process tRNA

To run bulk process script:

```
make bulk_process
```

TODO:

```
make clean_bulk_process
```

![Flowchart of process_trnas.sh logic](figs/DS5500-process_trnas-flow.jpg)

_Flow chart made with Miro_

## Comments on Reproducibility

* Because of bioconda settings, creating conda environment from file does not reliably work
* Right now specific to OS X because of shell script
* Have plans to port to Python script in order to improve cross-platform reproducibility
