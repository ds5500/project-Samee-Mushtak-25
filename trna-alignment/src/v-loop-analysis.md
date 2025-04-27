---
title: V-Loop Analysis
---

# V-Loop Analysis

The below graph shows the distribution of "anomalous" V loop secondary structures. The predominant secondary structure, -(((****)))**-, occurs in over 1000 sequences, so it is omitted from this graph.

## Archaeal tRNA-Leu

<!--
<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plot_secondary_structure_stats(arch_leu_secondary_structure_stats_old, {width}))}
    </div>
</div>
-->

<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plot_secondary_structure_stats(arch_leu_secondary_structure_stats, {width}))}
    </div>
</div>

## Archaeal tRNA-Ser

The sequences of tRNA-Ser are more diverse, so there is no one "predominant" secondary structure among them. The below graph shows the secondary structures for all tRNA V arms in the dataset.

<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plot_secondary_structure_stats(arch_ser_secondary_structure_stats, {width}))}
    </div>
</div>

```js
const arch_leu_secondary_structure_stats = [
    {
        "length": 13,
        "secondary_structure": "-(((***)))**-",
        "count": 3,
        "order": 1
    },
    {
        "length": 13,
        "secondary_structure": "-((*****))**-",
        "count": 18,
        "order": 2
    },
    {
        "length": 13,
        "secondary_structure": "-*((****))**-",
        "count": 5,
        "order": 3
    },
    {
        "length": 14,
        "secondary_structure": "-(((***)))***-",
        "count": 2,
        "order": 4
    },
    {
        "length": 14,
        "secondary_structure": "-((******))**-",
        "count": 1,
        "order": 5
    },
    {
        "length": 15,
        "secondary_structure": "-((((****))))*-",
        "count": 6,
        "order": 6
    },
    {
        "length": 15,
        "secondary_structure": "-(((*****)))**-",
        "count": 13,
        "order": 7
    },
    {
        "length": 16,
        "secondary_structure": "-((((****))))**-",
        "count": 3,
        "order": 8
    },
    {
        "length": 16,
        "secondary_structure": "-((((*****))))*-",
        "count": 4,
        "order": 9
    },
]
const arch_leu_secondary_structure_stats_old = [
    {
        "length" : 14,
        "secondary_structure": "-((((***))))*-",
        "count": 1,
        "order": 2
    },
    {
        "length" : 15,
        "secondary_structure": "-((((***))))**-",
        "count": 7,
        "order": 5
    },
    {
        "length" : 16,
        "secondary_structure": "-((((****))))**-",
        "count": 3,
        "order": 7
    },
    {
        "length" : 16,
        "secondary_structure": "-((((*****))))*-",
        "count": 4,
        "order": 8
    },
    {
        "length" : 13,
        "secondary_structure": "-(((***)))**-",
        "count": 1,
        "order": 0
    },
    {
        "length" : 15,
        "secondary_structure": "-(((*****)))**-",
        "count": 12,
        "order": 6
    },
    {
        "length" : 13,
        "secondary_structure": "-((*****))**-",
        "count": 25,
        "order": 1
    },
    {
        "length" : 14,
        "secondary_structure": "-((*****))***-",
        "count": 1,
        "order": 3
    },
    {
        "length" : 14,
        "secondary_structure": "-((******))**-",
        "count": 1,
        "order": 4
    }
]

const arch_ser_secondary_structure_stats = [
    {
        "length": 13,
        "secondary_structure": "-(((***)))**-",
        "count": 12,
        "order": 1
    },
    {
        "length": 13,
        "secondary_structure": "-(((****)))*-",
        "count": 14,
        "order": 2
    },
    {
        "length": 14,
        "secondary_structure": "-((((***))))*-",
        "count": 59,
        "order": 3
    },
    {
        "length": 14,
        "secondary_structure": "-(((*****)))*-",
        "count": 29,
        "order": 4
    },
    {
        "length": 15,
        "secondary_structure": "-((((***))))**-",
        "count": 3,
        "order": 5
    },
    {
        "length": 15,
        "secondary_structure": "-((((****))))*-",
        "count": 280,
        "order": 6
    },
    {
        "length": 15,
        "secondary_structure": "-(((******)))*-",
        "count": 18,
        "order": 7
    },
    {
        "length": 15,
        "secondary_structure": "-*(((****)))**-",
        "count": 1,
        "order": 8
    },
    {
        "length": 16,
        "secondary_structure": "-(((((***)))))*-",
        "count": 244,
        "order": 9
    },
    {
        "length": 16,
        "secondary_structure": "-((((*****))))*-",
        "count": 90,
        "order": 10
    },
    {
        "length": 16,
        "secondary_structure": "-*((((***))))**-",
        "count": 1,
        "order": 11
    },
    {
        "length": 16,
        "secondary_structure": "-*((((****))))*-",
        "count": 2,
        "order": 12
    },
    {
        "length": 17,
        "secondary_structure": "-(((((****)))))*-",
        "count": 81,
        "order": 13
    },
    {
        "length": 17,
        "secondary_structure": "-((((******))))*-",
        "count": 2,
        "order": 14
    },
    {
        "length": 17,
        "secondary_structure": "-*((((****))))**-",
        "count": 7,
        "order": 15
    },
    {
        "length": 18,
        "secondary_structure": "-((((((***))))))*-",
        "count": 3,
        "order": 16
    },
    {
        "length": 18,
        "secondary_structure": "-(((((*****)))))*-",
        "count": 14,
        "order": 17
    }
]
```

```js
function plot_secondary_structure_stats(data, width={}) {
    return Plot.plot({
        padding: 0,
        marginLeft: 150,
        x: {label: "Count"},
        y: {label: "Secondary Structure"},
        marks: [
            Plot.barX(data, {
                x: "count",
                y: (d) => `${d.secondary_structure} (${d.length})`,
                // y: "secondary_structure",
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