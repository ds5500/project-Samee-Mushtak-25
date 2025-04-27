---
title: V Loop Predictions
---

```js
const leu_vloop_stats = FileAttachment("data/stats/Leu-Vloop-stats-unique.csv").csv({typed:true})
const ser_vloop_stats = FileAttachment("data/stats/Ser-Vloop-stats-unique.csv").csv({typed:true})
```

# V Loop Secondary Structure Predictions

The below tables show predicted secondary structures for all archaeal tRNALeu and tRNASer V loop sequences. The secondary structures were determined using Wuchty's algorithm, which finds secondary structures of RNA sequences with low Gibbs free energy (GFE), which corresponds to a more stable folding pattern. This is in contrast to algorithms like Nussinov's algorithm, which primarily seek to maximize the number of base pairs formed. While forming more base pairs does tend to decrease the GFE of a RNA structure, forming too many base pairs in the stem region can reduce the number of unpaired bases in the loop region, which can cause loop strain. By minimizing the GFE, Wuchty's algorithm aims to balance both of these factors when considering potential secondary structures.

However, it is not always correct to take the secondary structure which has the absolute minimum GFE because functional requirements of the tRNA structure or conditions in the cell may make this energetically optimal structure inviable. Therefore, Wuchty's algorithm (unlike Zuker's algorithm), also finds considers suboptimal secondary structures. To determine the best secondary structure from the list of suboptimal secondary structures, we use constraints to enforce the expected secondary structure based on knowledge about the structure of tRNA molecules. The constraints that we use are to force the third base in the V loop sequence to participate in a base pair and to prevent the first base in the V loop sequence from participating in a base pair.

While this algorithm does perform well on archaeal V loop sequences, it does not perform as well on the longer D loop sequences because these sequences have more possible folding patterns. Increasing the specificity of the constraints used for these sequences could help in finding plausible secondary structures for the D loop region. We expect that this problem will not exist for bacterial V loop sequences because the lengths of bacterial V loops are comparable to the lengths of archaeal V loop sequences.

With our approach, we are able to predict secondary structures for sequences which the GtRNAdb fails to predict any structure for. Additionally, for some sequences with anomalous secondary structures, the GtRNAdb underestimates the stem length which our approach does not. We conjecture that the algorithm used by the GtRNAdb is more predisposed to predicting shorter stem lengths because it uses a covariance model trained against a profile of tRNA sequences of the same isotype. For tRNALeu, a stem length of 4 occurs in only 13 out of over 1000 sequences, which means that the covariance model may be biased against predicting that a sequence has a stem length of 4. On the other hand, our approach treats each sequence independently, so the presence of more shorter stem lengths in the dataset will not skew the predictions made by Wuchty's algorithm.

## Archaeal tRNA-Leu predictions

```js
Inputs.table(leu_vloop_stats)
```

## Archaeal tRNA-Ser predictions

```js
Inputs.table(ser_vloop_stats)
```