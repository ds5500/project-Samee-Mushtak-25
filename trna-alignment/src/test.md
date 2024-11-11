---
title: TEST
---

# TEST

```js
const species_selection = view(
    Inputs.select(
        jsons, {
            value: jsons.find( (t) => t.species === "Pyrococcus furiosus" ),
            format: (t) => t.species,
            label: "Species"
        }
    )
);
```

```js
const sel_species = species_selection.species;
```

```js
const alignment_selection = view(
    Inputs.select(
        jsons.find( (t) => t.species === sel_species ).files, {
            format: (d) => d.alignment.name,
            label: "Alignment File"
        }
    )
);
```

```js
const aln = alignment_selection.alignment.json();
const splits = alignment_selection.splits.json();
```

```js
const isAligned = view(
    Inputs.toggle({
        label: "Align",
        values: ['base_idx', 'base_num']
    })
);
```

```js
const showSplitters = view(
    Inputs.toggle({
        label: "Show splitters",
        value: false,
        disabled: !isAligned
    })
);
```

<div class="grid grid-cols-1">
    <div class="card">
        ${newPlot}
    </div>
</div>

<div class="grid grid-cols-1">
    <div class="card">
        ${myPlot}
    </div>
</div>

```js echo
const newPlot = Plot.plot({
        padding: 0,
        marginLeft: 100,
        width: 2000,
        height: 1500,
        grid: true,
        x: { axis: "top", label: "", },
        y: {label: ""},
        color: {
            domain: [0, 1, 2, 3, 4],
            range: ["#177E89", "#DB3A34", "#FFC857", "#BBDBB4", "#FF00FF"]
        },
        marks: [
            Plot.cell(aln, {
                x: "base_num", 
                y: "seq_label",
                fill: "base_color", inset: 0.5,
                render: render,
            }),
        ],
})
```

```js echo
const render = (index, scales, values, dimensions, context, next) => {
    const {x} = scales;
    const X = x.domain();
    const y0 = dimensions.height - dimensions.marginBottom; // vertical position of the y-axis
    const bars = next(index, scales, values, dimensions, context);
    const svg = context.ownerSVGElement;

    svg.update = (isAligned) => {
      d3.select(bars)
          .selectAll("rect")
        .transition().duration(2000)
          .attr("x", i => x(aln[i][isAligned]))
    };

    return bars;
}
```

```js echo
newPlot.update(isAligned);
```

```js
const myPlot = Plot.plot({
        padding: 0,
        marginLeft: 100,
        width: 2000,
        height: 1500,
        grid: true,
        x: { axis: "top", label: "", },
        y: {label: ""},
        color: {
            domain: [0, 1, 2, 3, 4],
            range: ["#177E89", "#DB3A34", "#FFC857", "#BBDBB4", "#FF00FF"]
        },
        marks: [
            Plot.cell(aln, {
                x: isAligned,
                y: "seq_label",
                fill: "base_color", inset: 0.5,
            }),
        ],
})
```

```js
const jsons = [
    {
        "species" : "Pyrococcus furiosus",
        "files" : [
            {
                "alignment" : FileAttachment("data/alignments/Pyrococcus-furiosus/pyrFur2-manual.json"),
                "splits" : FileAttachment("data/alignments/Pyrococcus-furiosus/pyrFur2-manual.splits.json")
            },
            {
                "alignment" : FileAttachment("data/alignments/Pyrococcus-furiosus/pyrFur2-clustal-omega.json"),
                "splits" : FileAttachment("data/alignments/Pyrococcus-furiosus/pyrFur2-clustal-omega.splits.json")
            },
            {
                "alignment" : FileAttachment("data/alignments/Pyrococcus-furiosus/pyrFur2-mafft.json"),
                "splits" : FileAttachment("data/alignments/Pyrococcus-furiosus/pyrFur2-mafft.splits.json")
            },
            {
                "alignment" : FileAttachment("data/alignments/Pyrococcus-furiosus/pyrFur2-mafft-kimura.json"),
                "splits" : FileAttachment("data/alignments/Pyrococcus-furiosus/pyrFur2-mafft-kimura.splits.json")
            }
        ]
    },
    {
        "species" : "Haloferax volcanii",
        "files" : [
            {
                "alignment" : FileAttachment("data/alignments/Haloferax-volcanii/haloVolc1-clustal-omega.json"),
                "splits" : FileAttachment("data/alignments/Haloferax-volcanii/haloVolc1-clustal-omega.splits.json")
            },
            {
                "alignment" : FileAttachment("data/alignments/Haloferax-volcanii/haloVolc1-mafft.json"),
                "splits" : FileAttachment("data/alignments/Haloferax-volcanii/haloVolc1-mafft.splits.json")
            },
            {
                "alignment" : FileAttachment("data/alignments/Haloferax-volcanii/haloVolc1-mafft-kimura.json"),
                "splits" : FileAttachment("data/alignments/Haloferax-volcanii/haloVolc1-mafft-kimura.splits.json")
            }
        ]
    },
    {
        "species" : "Chlorobium chlorochromatii",
        "files" : [
            {
                "alignment" : FileAttachment("data/alignments/Chlorobium-chlorochromatii/chloChlo-CAD3-clustal-omega.json"),
                "splits" : FileAttachment("data/alignments/Chlorobium-chlorochromatii/chloChlo-CAD3-clustal-omega.splits.json")
            },
            {
                "alignment" : FileAttachment("data/alignments/Chlorobium-chlorochromatii/chloChlo-CAD3-mafft.json"),
                "splits" : FileAttachment("data/alignments/Chlorobium-chlorochromatii/chloChlo-CAD3-mafft.splits.json")
            },
            {
                "alignment" : FileAttachment("data/alignments/Chlorobium-chlorochromatii/chloChlo-CAD3-mafft-kimura.json"),
                "splits" : FileAttachment("data/alignments/Chlorobium-chlorochromatii/chloChlo-CAD3-mafft-kimura.splits.json")
            }

        ]
    }
];
```
