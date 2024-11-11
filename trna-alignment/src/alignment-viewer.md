---
title: Alignment Viewer
---

# Alignment Viewer

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

```js
function alignmentPlot(data, showSplitters, width={}) {
    // Find maximum index in alignment
    // Because Python code generates bases in a sequential order, we can break early
    let max_idx = 0;
    for (let i = 0; i < data.length; ++i) {
        let d = data[i];
        if (d.base_idx > max_idx) {
            max_idx = d.base_idx;
        }
        else {
            break;
        }
    }
    // List of integers from 1 to max_idx to use as tick labels
    let int_ticks = [];
    for (let i = 5; i < max_idx - 1; i += 5) {
        int_ticks.push(i);
    }
    int_ticks.push(max_idx);

    let marks = [
        Plot.cell(data, {
            x: "base_idx",
            y: "seq_label",
            sort: {
                y: "data",
                reduce: ([d]) => d.seq_idx
            },
            fill: "base_color"
        }),
        Plot.text(data, {
            x: "base_idx",
            y: "seq_label",
            sort: {
                y: "data",
                reduce: ([d]) => d.seq_idx
            },
            text: "base_label",
            fill: "black",
            title: (d) => `${d.seq_label}: Base #${d.base_num}=${d.base_label}`
        })
    ];
    if (showSplitters) {
        marks.push(
            Plot.ruleX(splits, {
                stroke: "red"
            })
        );
    }

    return Plot.plot({
        padding: 0,
        marginLeft: 100,
        width: 2000,
        height: 1500,
        grid: true,
        x: {
            axis: "top",
            label: "",
            ticks: int_ticks
        },
        y: {label: ""},
        color: {
            domain: [0, 1, 2, 3, 4],
            range: ["#177E89", "#DB3A34", "#FFC857", "#BBDBB4", "#FF00FF"]
        },
        marks: marks
    })
}
```

```js
function unalignedPlot(data, width={}) {
    // Consensus is not meaningful for unaligned sequences
    data = data.filter((d) => d.seq_label !== 'Consensus');
    // Find maximum length of sequence
    let max_num = 0;
    for (let i = 0; i < data.length; ++i) {
        let d = data[i];
        if (d.base_num > max_num) {
            max_num = d.base_num;
        }
        // Cannot break early anymore because diff sequences have diff lengths
    }
    // List of integers from 1 to max_idx to use as tick labels
    let int_ticks = [];
    for (let i = 5; i < max_num - 1; i += 5) {
        int_ticks.push(i);
    }
    int_ticks.push(max_num);

    return Plot.plot({
        padding: 0,
        marginLeft: 100,
        width: 2000,
        height: 1500,
        grid: true,
        x: {
            axis: "top",
            label: "",
            ticks: int_ticks
        },
        y: {label: ""},
        color: {
            domain: [0, 1, 2, 3, 4],
            range: ["#177E89", "#DB3A34", "#FFC857", "#BBDBB4", "#FF00FF"]
        },
        marks: [
            Plot.cell(data, {
                x: "base_num",
                y: "seq_label",
                sort: {
                    y: "data",
                    reduce: ([d]) => d.seq_idx
                },
                fill: "base_color"
            }),
            Plot.text(data, {
                x: "base_num",
                y: "seq_label",
                sort: {
                    y: "data",
                    reduce: ([d]) => d.seq_idx
                },
                text: "base_label",
                fill: "black",
                title: (d) => `${d.seq_label}: Base #${d.base_num}=${d.base_label}`
            }),
        ]
    })
}
```

```js
const aln_filt = aln.filter((e) => e.seq_label === 'Consensus')
```

<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => isAligned ? alignmentPlot(aln, showSplitters, {width}) : unalignedPlot(aln, {width}))}
    </div>
</div>