---
title: Alignment Viewer
---

# Alignment Viewer

Code for alignment animations provided by Professor Phil Bogden.

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
        value: true
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
    ${combinedPlot}
</div>

```js
const combinedPlot = Plot.plot({
    padding: 0,
    marginLeft: 100,
    width: 2000,
    height: 1500,
    grid: true,
    x: {label: "", ticks: calculate_ticks(aln, 5)},
    y: {label: ""},
    color: {
        domain: [0, 1, 2, 3, 4],
        range: ["#177E89", "#DB3A34", "#FFC857", "#BBDBB4", "#FF00FF"]
    },
    marks: [
        Plot.axisX(calculate_ticks(aln, 5), {
            anchor: "top",
            fontSize: 24
        }),
        Plot.axisY({
            anchor: "left",
            fontSize: 24
        }),
        Plot.cell(aln, {
            x: "base_idx", 
            y: "seq_label",
            sort: {
                y: "data",
                reduce: ([d]) => d.seq_idx
            },
            fill: "base_color",
            render: render_cell
        }),
        Plot.text(aln, {
            x: "base_idx",
            y: "seq_label",
            sort: {
                y: "data",
                reduce: ([d]) => d.seq_idx
            },
            text: "base_label",
            fill: "black",
            monospace: true,
            fontSize: 24,
            title: (d) => `${d.seq_label}: Base #${d.base_num}=${d.base_label}`,
            render: render_text
        }),
        Plot.ruleX(splits.map((d) => d-0.5), {
            stroke: "blue",
            strokeWidth: 0,
            render: render_rule
        })
    ]
});
```

```js
function calculate_ticks(data, delta) {
    const max_idx = d3.max(data.map((d) => d.base_idx));
    let ticks = [];
    for (let i = delta; i < max_idx - 1; i += delta) {
        ticks.push(i);
    }
    ticks.push(max_idx);
    return ticks;
}
```

```js
const render_cell = (index, scales, values, dimensions, context, next) => {
    const {x} = scales;
    const g = next(index, scales, values, dimensions, context);
    const svg = context.ownerSVGElement;

    svg.update_cell = (isAligned) => {
      d3.select(g)
          .selectAll("rect")
        .transition().duration(1000)
          .attr("x", i => x(aln[i][isAligned ? 'base_idx' : 'base_num']))
    };

    return g;
};
```

```js
const render_text = (index, scales, values, dimensions, context, next) => {
    const {x,y} = scales;
    const g = next(index, scales, values, dimensions, context);
    const svg = context.ownerSVGElement;

    svg.update_text = (isAligned) => {
      d3.select(g)
          .selectAll("text")
        .transition().duration(1000)
            // .attr("x", i => `${x(aln[i][isAligned ? 'base_idx' : 'base_num'])}`)
            // .attr("y", i => `${y(aln[i]['seq_label'])}`)
            .attr("transform", i => 
                `translate(${x(aln[i][isAligned ? 'base_idx' : 'base_num'])}, ${y(aln[i]['seq_label'])})`
            )
    };
    // Need to filter out consensus markers in unaligned view

    return g;
};
```

```js
const render_rule = (index, scales, values, dimensions, context, next) => {
    const {x} = scales;
    const g = next(index, scales, values, dimensions, context);
    const svg = context.ownerSVGElement;
    const half_width = (x(2) - x(1)) / 2;

    svg.toggle_rule = (showSplitters) => {
        d3.select(g)
        .selectAll("line")
        .attr("stroke-width", showSplitters ? 3 : 0)
        .attr("transform", `translate(${half_width},0)`);
    };

    return g;
};
```

```js
combinedPlot.update_cell(isAligned);
combinedPlot.update_text(isAligned);
combinedPlot.toggle_rule(showSplitters);
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
            },
            {
                "alignment" : FileAttachment("data/alignments/Pyrococcus-furiosus/pyrFur2-infernal.json"),
                "splits" : FileAttachment("data/alignments/Pyrococcus-furiosus/pyrFur2-infernal.splits.json")
            },
            {
                "alignment" : FileAttachment("data/alignments/Pyrococcus-furiosus/pyrFur2-infernal-immature.json"),
                "splits" : FileAttachment("data/alignments/Pyrococcus-furiosus/pyrFur2-infernal-immature.splits.json")
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