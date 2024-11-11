---
title: Quality Reports
---

# Quality Reports

Alignment quality reports for _Pyrococcus furiosus_.

## Sum-of-Pairs Scoring

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

<!--
```tex
\int_0^1 e^x d{x}
```
-->

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
const mos_score_data = [
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
]
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

<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plot_mos_scores(mos_score_data, {width}))}
    </div>
</div>