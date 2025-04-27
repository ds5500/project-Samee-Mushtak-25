---
title: Analysis of Serine V arms
---

# Analysis of Serine V Arms

```js
function graph_svg() {
  // Specify the dimensions of the chart.
  const width = 1600;
  const height = 1600;

  // Specify the color scale.
  const color = d3.scaleOrdinal(d3.schemeCategory10);

  const node_color_map = {
    13 : "#FF0000",
    14 : "#808080",
    15 : "#0000FF",
    16 : "#FFA500",
    17 : "#000000",
    18 : "#00FF00",
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

In the above network, connected components containing fewer than four nodes have been removed for visual clarity. The tRNASer V arm network consists of three medium-sized components with between 32 and 47 distinct V arm sequences in each cluster, as well as several smaller components containing fewer than 15 distinct V arm sequences. This is in contrast to the tRNALeu V arm network, which has one large component with 128 distinct sequences, one small component with 12 distinct sequences, and the remaining components have only one or two distinct sequences. Additionally, the tRNASer network components are loosely connected (low edge-to-node ratio), whereas the main component of the tRNALeu network is more densely connected. These results are expected because it is known from previous research that tRNASer V arm sequences are more genetically diverse than tRNALeu V arm sequences.

While most components have a predominant sequence length, there is one cluster which has twelve sequences with a sequence length of 14 and seventeen sequences with a sequence length of 15, as well as three sequences with a sequence length of 16. The sequences in this cluster are therefore prime candidates for further analysis to try to find connections to other clusters.

```js
const graph_data = FileAttachment("data/networks/arch-Ser-sem2-graph-trunc.json").json()
```