---
title: Sequence Homology Network
---

# Sequence Homology Network

Code for this diagram adapted from [Force-directed graph by Mike Bostock](https://observablehq.com/@d3/force-directed-graph/2).

```js
function graph_svg() {
  // Specify the dimensions of the chart.
  const width = 1200;
  const height = 1600;

  // Specify the color scale.
  const color = d3.scaleOrdinal(d3.schemeCategory10);

  const node_color_map = {
    13 : "#FF0000",
    14 : "#808080",
    15 : "#0000FF",
    16 : "#FFA500"
  };
  
  const edge_color_map = {
    "penultimate_transition" : "#FFA500",
    "penultimate_transversion" : "#0000FF",
    "point_mutation" : "#06402B",
    "stem_pair_mutation" : "#FF00FF",
    "indel" : "#FF0000",
    "adhoc" : "#FFC0CB"
  };

  // The force simulation mutates links and nodes, so create a copy
  // so that re-evaluating this cell produces the same result.
  const links = graph_data.edges.map(d => ({...d}));//.filter((d) => d.type !== 'stem_pair_mutation');
  const nodes = graph_data.nodes.map(d => ({...d}));

  // Create a simulation with several forces.
  const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.sequence))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(width / 2, height / 2))
      .on("tick", ticked);

  simulation.tick(300);
  
  // Create the SVG container.
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto;");

  // Add a line for each link, and a circle for each node.
  const link = svg.append("g")
    .selectAll()
    .data(links)
    .join("line")
      .attr("stroke", d => edge_color_map[d.type])
      .attr("stroke-opacity", 0.7)
      .attr("stroke-width", 3);

  const node = svg.append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 0.5)
    .selectAll()
    .data(nodes)
    .join("circle")
      .attr("r", d => 3 + Math.sqrt(d.count))
      .attr("fill", d => node_color_map[d.length]);

  console.log(links);

  link.append("title")
    .text(d => `${d.source.sequence} <- ${d.type} -> ${d.target.sequence}`);

  node.append("title")
      .text(d => d.sequence);

  // Add a drag behavior.
  node.call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

  // Set the position attributes of links and nodes each time the simulation ticks.
  function ticked() {
    link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

    node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
  }

  // Reheat the simulation when drag starts, and fix the subject position.
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }

  // Update the subject (dragged node) position during drag.
  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }

  // Restore the target alpha so the simulation cools after dragging ends.
  // Unfix the subject position now that it’s no longer being dragged.
  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }

  // When this cell is re-run, stop the previous simulation. (This doesn’t
  // really matter since the target alpha is zero and the simulation will
  // stop naturally, but it’s a good practice.)
  invalidation.then(() => simulation.stop());

  return svg.node();
}
```

<div class="grid grid-cols-1">
    ${graph_svg()}
</div>

Hover over a node or edge to see more details. Drag a node to move it around. The color of a node represents the length of the corresponding sequence, and the size of a node represents its prevalence among the archaeal sequences of GtRNAdb. The color of an edge corresponds to the class of genetic mutation that describes the relationship between two connected sequences. Pink edges represent "adhoc" mutations (non-standard terminology), which are three point mutations with no obvious biochemical interpretation.

This is a network depicting genetic relationships between the 150 distinct tRNALeu V arm sequences which we extracted from GtRNAdb. 142 out of the 150 sequences are in the main connected component. Within this connected component, we can observe four clusters. In the center, there are two clusters consisting predominantly of 14 nucleotide sequences, which we call Cluster 14A and Cluster 14B. Cluster 14A can be identified by the representative sequence UCCCGUAGGGUUC, and Cluster 14B can be identified by the representative sequence UGGCGUAGGCCUGC. Cluster 14A appears to have a higher density of sequences related by penultimate transition mutations, while Cluster 14B has a higher density of sequences related by penultimate transversion mutations. These two clusters are connected by paired mutations in the V arm stem.

On the periphery, there are two more clusters. The cluster of red nodes corresponds to 13 nucleotide sequences and the cluster of blue noeds corresponds to 15 nucleotide sequences. The 13 nucleotide cluster appears to be more closely related to Cluster 14A, while the 15 nucleotide cluster appears to be more closely related to Cluster 14B. All four 16 nucleotide sequences were not able to be clustered, as were three 13 nucleotide sequences and 1 15 nucleotide sequence.

A future goal is to determine how the 8 unincorporated sequences are related to the main component. Figuring this out should give a complete picture of the evolutionary relationships between archaeal tRNALeu sequences. From this foundation, our next step would be to perform the same analysis for tRNASer sequences. If we are able to combine the networks for tRNALeu and tRNAser in a coherent manner, we would have the means to understand the history of V arms for the entire domain Archaea. From there, our analysis could expand to the bacterial, eukaryotic, and even mitochondrial V arm sequences.

The main complication expected in expanding our analysis to other domains of species is the increased diversity of V arm sequences in species more evolutionarily derived from the latest universal common ancestor (LUCA). Even with archaeal tRNASer, our brute force secondary structure determination algorithm is not sufficient to capture the variety of structures that are observed in these species, and we expect these complications to be more prevalent for bacterial and eukaryotic sequences. This is why an important preliminary step before expanding our analysis will be to improve our secondary structure algorithm.

Another challenge is the difficulty of incorporating sequences that are distantly related into the network. Using fundamental knowledge of genetics/biochemistry, we were able to connect 142 out of 150 of tRNALeu sequences, but the 8 remaining sequences are at least 4 point mutations from all other sequences in the network, so there is no single obvious genetic mutation that can explain their connection to the rest of the sequences. This will be more of a problem as we expand our analysis to other domains with more diverse sequences. This problem can be addressed by connecting to nodes which have the lowest Hamming distance between them, but this is not fully satisfactory from a biological perspective. Techniques from the field of BioNLP may be of relevance to this problem.

```js
const graph_data = FileAttachment("data/adhoc_graph.json").json()
```