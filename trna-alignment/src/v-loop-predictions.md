---
title: V Loop Predictions
---

```js
const vloop_stats = FileAttachment("data/Leu-Vloop-stats.csv").csv({typed:true})
```

# V Loop Predictions

The below table shows predicted secondary structures for all archaeal tRNALeu V loop sequences. These secondary structures were determined via brute forcing through all feasible stem lengths and offsets and determining the most probable combination. For future work, we aim to implement more nuanced secondary structure determination algorithms, such as Nussinov's algorithm and Zuker's algorithm.

In the last column of the table, hyphens represent the start and end of the V loop sequences, parentheses represent nucleotides in the stem of the V loop sequence, and asterisks represent unpaired nucleotides, either within the loop of the V loop or after the 3' stem.

```js
Inputs.table(vloop_stats)
```