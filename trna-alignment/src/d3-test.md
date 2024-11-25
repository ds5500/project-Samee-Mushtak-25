---
title: D3 TEST
---

# Alignment Viewer

```js echo
function onclick_test() {
  let aln_cell = aln.map(cell_transformer_aligned);

  const width = 1050;
  const height = 800;
  const margin = { top: 20, bottom: 20, left: 100, right: 20 };

  const container = htl.html`<div id="container">
    <fieldset>
      <div class="input-container">
        <input type="checkbox" id="align-checkbox" name="align" checked/>
        <label for="align-checkbox">Align</label>
      </div>
    </fieldset>
    <div id="svg-container">
    </div>
  </div>`;

  const align_checkbox = d3
    .select(container)
    .select("input#align-checkbox");

  const x_domain = Array.from(new Set(aln.map((d) => d.base_idx))).sort(d3.ascending);
  const y_domain = Array.from(new Set(aln.map((d) => d.seq_label)));
  
  const x = d3
    .scaleBand()
    .domain(x_domain)
    .range([0, width]);

  const y = d3
    .scaleBand()
    .domain(y_domain)
    .range([0, height]);

  const c = d3
    .scaleOrdinal()
    .domain([-1, 0, 1, 2, 3, 4])
    .range(["none", "#177E89", "#DB3A34", "#FFC857", "#BBDBB4", "#FF00FF"]);

  const svg = d3
    .select(container)
    .select("div#svg-container")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);

  const g = svg
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

  g.append("g")
    .call(
      d3.axisLeft(y)
        .tickSizeOuter(0)
    );
  
  g.append("g")
    .call(
      d3.axisTop(x)
        .tickValues(calculate_ticks(aln, 5))
        .tickSizeOuter(0)
    );
  
  const g_cell = g
    .append("g")
    .attr("id", "g-alignment-cells")
    .selectAll("rect")
    .data(aln_cell)
    .join("rect")
    .classed("alignment-cell", true)
    .attr("x", (d) => x(d.idx))
    .attr("y", (d) => y(d.seq_label))
    .attr("width", x.bandwidth())
    .attr("height", y.bandwidth())
    .attr("fill", (d) => c(d.base_color));

  align_checkbox
    .on("click", (_,__) => {
      aln_cell = align_checkbox.property("checked")
        ? aln.map(cell_transformer_aligned)
        : aln.map(cell_transformer_unaligned);
      g_cell
        .selectAll("rect.alignment-cell")
        .data(aln_cell)
        .join("rect")
        .attr("x", (d) => x(d.idx))
        .attr("y", (d) => y(d.seq_label))
        .attr("width", x.bandwidth())
        .attr("height", y.bandwidth())
        .attr("fill", (d) => c(d.base_color));
    });

  return container;
}
```

<div class="grid grid-cols-1">
    ${onclick_test()}
</div>

```js echo
function d3_alignment_viewer() {
  const width = 1050;
  const height = 800;
  const margin = { top: 20, bottom: 20, left: 100, right: 20 };

  const container = htl.html`<div id="container">
    <fieldset>
      <div class="input-container">
        <input type="checkbox" id="align-checkbox" name="align" checked/>
        <label for="align-checkbox">Align</label>
      </div>
      <div class="input-container">
        <input type="checkbox" id="splitter-checkbox" name="splitter"/>
        <label for="splitter-checkbox">Show splitters</label>
      </div>
    </fieldset>
    <div id="svg-container">
    </div>
  </div>`;

  const align_checkbox = d3
    .select(container)
    .select("input#align-checkbox");

  const splitter_checkbox = d3
    .select(container)
    .select("input#splitter-checkbox");
  
  const x_domain = Array.from(new Set(aln.map((d) => d.base_idx))).sort(d3.ascending);
  const y_domain = Array.from(new Set(aln.map((d) => d.seq_label)));
  
  const x = d3
    .scaleBand()
    .domain(x_domain)
    .range([0, width]);

  const y = d3
    .scaleBand()
    .domain(y_domain)
    .range([0, height]);

  const c = d3
    .scaleOrdinal()
    .domain([-1, 0, 1, 2, 3, 4])
    .range(["none", "#177E89", "#DB3A34", "#FFC857", "#BBDBB4", "#FF00FF"]);

  const svg = d3
    .select(container)
    .select("div#svg-container")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);
    // .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
    // .attr("preserveAspectRatio", "xMinYMin meet");

  const g = svg
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

  g.append("g")
    .call(
      d3.axisLeft(y)
        .tickSizeOuter(0)
    );
  
  g.append("g")
    .call(
      d3.axisTop(x)
        .tickValues(calculate_ticks(aln, 5))
        .tickSizeOuter(0)
    );
  
  const g_cell = g
    .append("g")
    .attr("id", "g-alignment-cells")
    .selectAll("rect")
    .data(aln.map(cell_transformer_aligned))
    .join("rect")
    .attr("x", (d) => x(d.idx))
    .attr("y", (d) => y(d.seq_label))
    .attr("width", x.bandwidth())
    .attr("height", y.bandwidth())
    .attr("fill", (d) => c(d.base_color));

  const g_text = g
    .append("g")
    .attr("id", "g-alignment-text")
    .selectAll("text")
    .data(aln)
    .join("text")
    // 0.3 is a horizontal offset so text is not too close to left of box
    .attr("x", (d) => x(d.base_idx) + 0.3)
    // 2 is a vertical offset so text is not too close to bottom of box
    .attr("y", (d) => y(d.seq_label) + y.bandwidth() - 2)
    // How to make these offsets dynamic based on width and height?
    .attr("fill", "black")
    .attr("font-family", "monospace")
    .text((d) => d.base_label);

  const g_rule = g
    .append("g")
    .attr("id", "g-alignment-rules");

  align_checkbox
    .on("click", (_,__) => {
      // Splitters should only be displayed if the sequences are aligned
      splitter_checkbox.property("disabled", !align_checkbox.property("checked"));
      /*
      g_cell
        .selectAll("rect")
        .data(
          align_checkbox.property("checked")
            ? aln.map(cell_transformer_aligned)
            : aln.map(cell_transformer_unaligned),
          (d) => `${d.seq_label},${d.num}`)
        .join("rect")
        .attr("x", (d) => x(d.idx))
        .attr("y", (d) => y(d.seq_label))
        .attr("width", x.bandwidth())
        .attr("height", y.bandwidth())
        .attr("fill", (d) => c(d.base_color));
      */
    });
  
  splitter_checkbox
    .on("click", (_,__) => {
      g_rule
        .selectAll("line")
        .data(splitter_checkbox.property("checked") ? splits : [], (d) => d)
        .join("line")
        .attr("x1", d => x(d+1))
        .attr("x2", d => x(d+1))
        .attr("y1", y(y_domain[0]) - 0.4 * y.bandwidth())
        .attr("y2", y(y_domain[y_domain.length-1]) + 0.4 * y.bandwidth())
        .attr("stroke-width", 3)
        .attr("stroke", "blue");
    });

  return container;
}
```

<div class="grid grid-cols-1">
    ${d3_alignment_viewer()}
</div>

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
const splits_pre = alignment_selection.splits.json();
```


```js
let splits = [];
for (let i = 0; i < splits_pre.length; ++i) {
    splits.push(splits_pre[i]-0.5);
}
```

```js
function cell_transformer_aligned(d) {
  return {
    "seq_label" : d.seq_label,
    "num" : d.base_num,
    "idx" : d.base_idx,
    "base_color" : d.base_color
  }
}
```

```js
function cell_transformer_unaligned(d) {
  return {
    "seq_label" : d.seq_label,
    "num" : d.base_num,
    "idx" : d.base_num,
    "base_color" : d.base_color
  }
}
```