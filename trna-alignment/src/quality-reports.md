---
title: Quality Reports
---

# Quality Reports

## MetAl Scoring

Scores calculated using Benjamin Blackburne's MetAl command line utility compiled from [source](https://github.com/benb/MetAl). See original paper: [https://doi.org/10.1093/bioinformatics/btr701](https://doi.org/10.1093/bioinformatics/btr701)


```js
const dists = [
    {"dist" : "d_ssp", "dist_literal" : "Symmetrized Sum of Pairs Distance"},
    {"dist" : "d_pos", "dist_literal" : "Positional Encoding Distance"},
    {"dist" : "d_simple", "dist_literal" : "Homology Distance"}
];
```

```js
const region_selection = view(
    Inputs.select(
        region_jsons, {
            value: region_jsons.find( (t) => t.region === "Full Sequence" ),
            format: (t) => t.region,
            label: "Region"
        }
    )
);
```

```js
const dist_selection = view(
    Inputs.select(
        dists, {
            value: dists.find( (t) => t.dist === "d_ssp" ),
            format: (t) => t.dist_literal,
            label: "Species"
        }
    )
);
```

```js
const region_dist_data = region_selection.data;
```

```js
function plot_dists(data, width={}) {
    return Plot.plot({
        padding: 0,
        grid: true,
        aspectRatio: 1,
        marginLeft: 120,
        marginTop: 90,
        x: {
            domain: ["Manual", "Clustal Omega", "MAFFT", "MAFFT-Kimura", "Infernal"],
        },
        y: {
            domain: ["Manual", "Clustal Omega", "MAFFT", "MAFFT-Kimura", "Infernal"],
        },
        color: {type: "linear", scheme: "GnBu"},
        marks: [
            Plot.axisX({
                anchor: "top",
                fontSize: 14,
                label: "Algorithm 1",
                tickRotate: -30
            }),
            Plot.axisY({
                anchor: "left",
                fontSize: 14,
                label: "Algorithm 2",
                tickRotate: -30
            }),
            Plot.cell(data, {
                x : "col_label",
                y : "row_label",
                fill : dist_selection.dist + "_inv",
                inset: 0.5
            }),
            Plot.text(data, {
                x : "col_label",
                y : "row_label",
                text : dist_selection.dist,
                fill: "black",
                fontSize: 24
            })
        ]
    })
}
```

<div class="grid grid-cols-1">
    ${resize((width) => plot_dists(region_dist_data, {width}))}
</div>

In the above heatmaps, a lower numerical score corresponds to a higher similarity between two alignments. The first row/column correspond to a manual alignment taken to be the gold-standard, and the other rows/columns correspond to algorithmic alignments.

From the above, we can see that the middling performance observed in the full sequence is primarily the result of poor performance in the V loop region. The V loop region of tRNAs is currently not well understood, so it will be the focus of our analysis henceforth.

## Sum-of-Pairs Scoring

### _Pyrococcus furiosus_

```js
const sop_score_data = [
    {
        "algo": "Manual",
        "score": 18764,
        "order": 0
    },
    {
        "algo": "Clustal Omega",
        "score": 18827,
        "order": 1
    },
    {
        "algo": "MAFFT L-INS-i",
        "score": 15212,
        "order": 2
    },
    {
        "algo": "MAFFT L-INS-i w/ Kimura",
        "score": 18581,
        "order": 3
    }
]
```

```js
function plot_sop_scores(data, width={}) {
    return Plot.plot({
        padding: 0,
        marginLeft: 150,
        x: {label: "Score"},
        y: {label: "Algorithm"},
        marks: [
            Plot.barX(data, {
                x: "score",
                y: "algo",
                sort: {
                    y: "data",
                    reduce: ([d]) => d.order
                },
                inset: 1
            })
        ]
    })
}
```

<!--
<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plot_sop_scores(sop_score_data, {width}))}
    </div>
</div>
-->

```js
const sop_cost_data = [
    {
        "algo": "Manual",
        "cost": 30490,
        "order": 0
    },
    {
        "algo": "Clustal Omega",
        "cost": 30477,
        "order": 1
    },
    {
        "algo": "MAFFT L-INS-i",
        "cost": 32505,
        "order": 2
    },
    {
        "algo": "MAFFT L-INS-i w/ Kimura",
        "cost": 30621,
        "order": 3
    }
]
```

```js
function plot_sop_costs(data, width={}) {
    return Plot.plot({
        padding: 0,
        marginLeft: 150,
        x: {label: "Cost"},
        y: {label: "Algorithm"},
        marks: [
            Plot.barX(data, {
                x: "cost",
                y: "algo",
                sort: {
                    y: "data",
                    reduce: ([d]) => d.order
                },
                inset: 1
            })
        ]
    })
}
```

<div class="grid grid-cols-2">
    <div class="card">
        ${resize((width) => plot_sop_scores(sop_score_data, {width}))}
    </div>
    <div class="card">
        ${resize((width) => plot_sop_costs(sop_cost_data, {width}))}
    </div>
</div>

## Multiple Overlap Scoring

```js
const pyr_fur_mos_score_data = [
    {
        "algo": "Manual",
        "score": 0.901200508293205,
        "order": 0
    },
    {
        "algo": "Clustal Omega",
        "score": 0.9100704846183093,
        "order": 1
    },
    {
        "algo": "MAFFT L-INS-i",
        "score": 0.7983138457447251,
        "order": 2
    },
    {
        "algo": "MAFFT L-INS-i w/ Kimura",
        "score": 0.9107400122771632,
        "order": 3
    }
];
const halo_volc_mos_score_data = [
    {
        "algo": "Clustal Omega",
        "score": 0.8289635838530937,
        "order": 1
    },
    {
        "algo": "MAFFT L-INS-i",
        "score": 0.8895253607184923,
        "order": 2
    },
    {
        "algo": "MAFFT L-INS-i w/ Kimura",
        "score": 0.8885055777149332,
        "order": 3
    }
];
const chlo_chlo_mos_score_data = [
    {
        "algo": "Clustal Omega",
        "score": 0.9372615619385168,
        "order": 1
    },
    {
        "algo": "MAFFT L-INS-i",
        "score": 0.957567688062561,
        "order": 2
    },
    {
        "algo": "MAFFT L-INS-i w/ Kimura",
        "score": 0.9570462449308672,
        "order": 3
    }
];
```

```js
function plot_mos_scores(data, width={}) {
    return Plot.plot({
        padding: 0,
        marginLeft: 150,
        x: {label: "Score", domain: [0,1]},
        y: {label: "Algorithm"},
        marks: [
            Plot.barX(data, {
                x: "score",
                y: "algo",
                sort: {
                    y: "data",
                    reduce: ([d]) => d.order
                },
                inset: 1
            }),
            Plot.ruleX([0.8], {
                stroke: "red"
            })
        ]
    })
}
```

### _Pyrococcus furiosus_
<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plot_mos_scores(pyr_fur_mos_score_data, {width}))}
    </div>
</div>

### _Haloferax volcanii_
<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plot_mos_scores(halo_volc_mos_score_data, {width}))}
    </div>
</div>

### _Chlorobium chlorochromatii_
<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plot_mos_scores(chlo_chlo_mos_score_data, {width}))}
    </div>
</div>

```js
const full_seq_metal_scores_data = FileAttachment("data/quality-reports/full_seq_metal_scores.json").json()
const ac_loop_metal_scores_data = FileAttachment("data/quality-reports/ac_loop_metal_scores.json").json()
const v_loop_metal_scores_data = FileAttachment("data/quality-reports/v_loop_metal_scores.json").json()
```

```js
const region_jsons = [
    {
        "region" : "Full Sequence",
        "data" : FileAttachment("data/quality-reports/full_seq_metal_scores.json").json()
    },
    {
        "region" : "Ac Loop",
        "data" : FileAttachment("data/quality-reports/ac_loop_metal_scores.json").json()
    },
    {
        "region" : " V Loop",
        "data" : FileAttachment("data/quality-reports/v_loop_metal_scores.json").json()
    }
];
```