# tRNA

* [Proposal](proposal.md)
* [Plan](plan.md)

## Setup

Running the code in this project requires **Make** and **Bioconda**.

To install Make in your conda environement:

```
conda install make
```

To configure your conda to use the Bioconda channel: (see also the [Bioconda documentation](https://bioconda.github.io/index.html))

```
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
```

## EDA

To run the EDA for BWA:

```
make eda_bwa
```

To run the EDA for Bowtie2:

```
make eda_bowtie2
```

To clean the output from the EDA:

```
make clean_eda
```

See [plan.md](plan.md) for a brief discussion of the results of this EDA.
