---
title: V Loop Predictions
---

```js
const vloop_stats = FileAttachment("data/Leu-Vloop-stats.csv").csv({typed:true})
```

# V Loop Predictions

The below table shows predicted secondary structures for all archaeal tRNALeu V loop sequences. These secondary structures were determined via brute forcing through all feasible stem lengths and offsets and determining the most probable combination. For future work, we aim to implement more nuanced secondary structure determination algorithms, such as Nussinov's algorithm and Zuker's algorithm.

```js
Inputs.table(vloop_stats)
```