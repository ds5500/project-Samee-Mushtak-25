---
title: Analysis of All V arms
---

# Analysis of All V Arms

```js
function graph_svg() {
  // Specify the dimensions of the chart.
  const width = 2200;
  const height = 2200;

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
      // .attr("fill", d => node_color_map[d.length]);
      .attr("fill", d => {
        if (d.sequence.endsWith("Leu")) {
            return "#FF0000";
        }
        else if (d.sequence.endsWith("Ser")) {
            return "#0000FF"
        }
        else {
            return "#000000"
        }
      });


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

In the above network, red nodes correspond to tRNALeu V arm sequences and blue nodes correspond to tRNASer V arm sequences. Connected components containing fewer than four nodes have been removed for visual clarity. The main point to note is that there is only one edge in this network linking a sequence in the tRNALeu V arm set to a sequence in the tRNASer V arm set. The two sequences are UGGGCGUCAG**G**CCCGC (tRNALeu) and UGGGCGUCAGCCCGC (tRNASer), which are linked by an indel mutation. This means that if there are other relations between the tRNALeu and tRNASer sequences as we hypothesize, then these relations likely involve at least three nucleotides since our analysis checks for the most common one- and two-nucleotide transformations.

Future analysis may require looking more broadly for changes in the structure of the V arms between different species rather than focusing on the specific nucleotide-level changes for each sequence. For example, one structural relation between two sequences that we do not consider in our analysis is a change in the V arm stem length. Most tRNALeu sequences have a stem length of 3, while most tRNASer sequences have a stem length of 4 or 5. By comparing sequences with similar structures aside from a difference in stem length, it may be possible to observe patterns in these sequences that are not apparent when considering only one or two nucleotides at a time.

```js
const graph_data = FileAttachment("data/networks/combined-graph.json").json()
```