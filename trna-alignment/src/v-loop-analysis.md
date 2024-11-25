---
title: V-Loop Analysis
---

# V-Loop Analysis

## Archaea

### tRNA-Leu

<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plot_secondary_structure_stats(arch_leu_secondary_structure_stats, {width}))}
    </div>
</div>

### tRNA-Ser

```js
const arch_leu_secondary_structure_stats = [
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