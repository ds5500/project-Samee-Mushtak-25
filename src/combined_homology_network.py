import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import json

# Could split this into two functions:
# purine_transition and pyrimidine_transition
def penultimate_transition(node_a, node_b):
  seq_a = node_a[0]
  seq_b = node_b[0]
  transition_map = {
      'A':'G',
      'G':'A',
      'U':'C',
      'C':'U'
  }

  # No insertions or deletions
  if len(seq_a) != len(seq_b):
    return False

  # Last base must match (I think this is always C but better to check)
  # Penultimate base must be a transition point mutation
  # This appears to be a common mutation (especially U <-> C),
  # so we want to highlight it
  if (seq_a[-1] != seq_b[-1]) or (seq_a[-2] != transition_map[seq_b[-2]]):
    return False

  # Check that the remaining bases are the same
  for i in range(len(seq_a)-2):
    if seq_a[i] != seq_b[i]:
      return False

  return True

# Any mutation in the penultimate base that is not a transition
def penultimate_transversion(node_a, node_b):
  seq_a = node_a[0]
  seq_b = node_b[0]
  # No insertions or deletions
  if len(seq_a) != len(seq_b):
    return False

  # Last base must match (I think this is always C but better to check)
  if (seq_a[-1] != seq_b[-1]):
    return False

  # Check that the remaining bases, except the penultimate, are the same
  for i in range(len(seq_a)-2):
    if seq_a[i] != seq_b[i]:
      return False

  return True

# Check for a mutation (not insertion/deletion) in a single base
# Should this only look for point mutations outside the stem?
# Right now this would pick up a C->U mutation in the stem, which is probably
# closer to a paired mutation because G can bind either C or U.
def point_mutation(node_a, node_b):
  seq_a = node_a[0]
  seq_b = node_b[0]
  # No insertions or deletions
  if len(seq_a) != len(seq_b):
    return False

  n_mutations = 0
  for i in range(len(seq_a)):
    if seq_a[i] != seq_b[i]:
      n_mutations += 1

  return n_mutations == 1

# Check for base pair mutation in the stem
# need secondary structure info from dataframe
def stem_pair_mutation(node_a, node_b):
  seq_a = node_a[0]
  seq_b = node_b[0]
  secondary_structure_a = node_a[1]
  secondary_structure_b = node_b[1]

  # No insertions or deletions
  if len(seq_a) != len(seq_b):
    return False
  # This check is might be too agressive
  # Need to consider if/when it makes sense to analyze paired mutations in stem
  # if secondary structure is not exactly the same
  # Currently our algorithm does not produce stems with bulge loops, simplifying the algorithm
  # The algorithm relies on the secondary structure being of the form:
    # [START -][UNPAIRED BASES *][FIVE' STEM (][LOOP BASES *][THREE' STEM )][UNPAIRED BASES *][END -]
  if secondary_structure_a != secondary_structure_b:
    return False

  fivep_stem_start = secondary_structure_a.find('(')
  fivep_stem_end = secondary_structure_a.rfind('(')
  threep_stem_start = secondary_structure_a.find(')')
  threep_stem_end = secondary_structure_a.rfind(')')

  n_changed_fivep = 0
  fivep_changed_pos = -1
  n_changed_threep = 0
  threep_changed_pos = -1

  for i in range(len(seq_a)):
    if i >= fivep_stem_start and i <= fivep_stem_end:
      if seq_a[i] != seq_b[i]:
        n_changed_fivep += 1
        fivep_changed_pos = i - fivep_stem_start
        if n_changed_fivep > 1:
          return False
    elif i >= threep_stem_start and i <= threep_stem_end:
      if seq_a[i] != seq_b[i]:
        n_changed_threep += 1
        threep_changed_pos = threep_stem_end - i
        if n_changed_threep > 1:
          return False
    else:
      if seq_a[i] != seq_b[i]:
        return False

  if n_changed_fivep == 1 and n_changed_threep == 1 and fivep_changed_pos == threep_changed_pos:
    return True
  elif n_changed_fivep == 0 or n_changed_threep == 0:
    return True
  else:
    return False

# Check for insertion/deletion
def indel(node_a, node_b):
  seq_a = node_a[0]
  seq_b = node_b[0]

  # WLOG seq_a longer than seq_b
  if len(seq_a) < len(seq_b):
    seq_a, seq_b = seq_b, seq_a

  # Consider only single-base deletions
  if len(seq_a) == len(seq_b) + 1:
    for i in range(len(seq_a)):
      if seq_a[:i] + seq_a[i+1:] == seq_b:
        return True

  return False

def construct_edge_list(node_list, func_dict):
  edge_list = []
  edge_type = []

  for i in range(len(node_list)-1):
    for j in range(i+1, len(node_list)):
      for typ, func in func_dict.items():
        if func(node_list[i], node_list[j]):
          edge_list.append((node_list[i], node_list[j]))
          edge_type.append(typ)
          # We should only add an edge once
          # func_dict is sorted in order of decreasing priority
          break

  return edge_list, edge_type

# vloop_stats = pd.read_csv('tRNALeu-analysis/Leu-Vloop-stats.csv')
vloop_stats = pd.read_csv('eda/ViennaRNA_testing/msa_to_ss/stats/combined-vloop-stats.csv')

unique_seqs = vloop_stats[['length', 'seq', 'secondary_structure', 'isotype']].value_counts().sort_index()
frequent_seqs = unique_seqs
sequence_counts = list(frequent_seqs)
node_list = [(row[1],row[2],row[3]) for row in frequent_seqs.index]

point_mut_func_dict = {
  'penultimate_transition': penultimate_transition,
  'penultimate_transversion': penultimate_transversion,
  'point_mutation': point_mutation
  # 'stem_pair_mutation': stem_pair_mutation,
  # 'indel': indel
}

indel_func_dict = {
  'penultimate_transition': penultimate_transition,
  'penultimate_transversion': penultimate_transversion,
  'point_mutation': point_mutation,
  # 'stem_pair_mutation': stem_pair_mutation,
  'indel': indel
}

paired_mut_func_dict = {
  'penultimate_transition': penultimate_transition,
  'penultimate_transversion': penultimate_transversion,
  'point_mutation': point_mutation,
  'stem_pair_mutation': stem_pair_mutation,
  'indel': indel
}

point_mut_edge_list, point_mut_edge_types = construct_edge_list(node_list, point_mut_func_dict)
indel_edge_list, indel_edge_types = construct_edge_list(node_list, indel_func_dict)
paired_mut_edge_list, paired_mut_edge_types = construct_edge_list(node_list, paired_mut_func_dict)

# G.remove_nodes_from(list(nx.isolates(G)))

G1 = nx.Graph()
G1.add_nodes_from(node_list)
G1.add_edges_from(point_mut_edge_list)

G2 = nx.Graph()
G2.add_nodes_from(node_list)
G2.add_edges_from(indel_edge_list)

G3 = nx.Graph()
G3.add_nodes_from(node_list)
G3.add_edges_from(paired_mut_edge_list)

def edge_color_mapper(edge_type):
  color_map = {
      'penultimate_transition': 'orange',
      'penultimate_transversion': 'b',
      'point_mutation': 'g',
      'indel': 'r',
      'stem_pair_mutation': 'm',
      'adhoc': 'rebeccapurple'
  }
  return color_map[edge_type]

def node_color_mapper(sequence_length):
  color_map = {
      13: 'r',
      14: 'gray',
      15: 'b',
      16: 'orange',
      17: 'y',
      18: 'k'
  }
  return color_map[sequence_length]

plt.figure(figsize=(8,8))
G = G3
# original_edges = list(G.edges)
large_ccs = [cc for cc in nx.connected_components(G) if len(cc) > 3]
filtered_nodes = []
for cc in large_ccs:
    for node in cc:
        filtered_nodes.append(node)

G = G.subgraph(filtered_nodes).copy()
# print(len(G.edges))

# edge_types = point_mut_edge_types
# edge_types = indel_edge_types
# edge_types = paired_mut_edge_types
edge_types = []
for edge in G.edges:
    if edge in paired_mut_edge_list:
        edge_types.append(
                paired_mut_edge_types[
                    paired_mut_edge_list.index(edge)
                    ]
                )
    elif (edge[1], edge[0]) in paired_mut_edge_list:
        swapped_edge = (edge[1], edge[0])
        # print('SWAPPED')
        edge_types.append(
                paired_mut_edge_types[
                    paired_mut_edge_list.index(swapped_edge)
                    ]
                )
    else: 
        print(f'MISSED: {edge}')
seed = 1
def node_color_by_isotype(isotype):
    if isotype == 'Leu':
        return 'r'
    elif isotype == 'Ser':
        return 'b'
    else:
        return 'k'

nx.draw_networkx_nodes(G, pos=nx.spring_layout(G, seed=seed),
                       node_size=[3*sequence_counts[node_list.index(node)] for node in G.nodes],
                       # node_size=[400 if sequence_counts[node_list.index(node)] > 100 else 4 for node in G.nodes],
                       # node_color=[node_color_mapper(len(node[0])) for node in G.nodes],
                       node_color=[node_color_by_isotype(node[2]) for node in G.nodes],
                       alpha=[0.4 if len(node[0]) == 14 else 0.8 for node in G.nodes])
nx.draw_networkx_edges(G, pos=nx.spring_layout(G, seed=seed),
                       edge_color=[edge_color_mapper(t) for t in edge_types],
                       alpha=0.5,
                       width=2)
plt.savefig('figs/sem2/combined_network.png')

sequence_to_anticodon_map = vloop_stats.groupby('seq')['anticodon'].agg(set)

def node_to_dictionary(node, node_list, sequence_counts, sequence_to_anticodon_map):
  return {
      'sequence': f'{node[0]}-{node[2]}',
      'secondary_structure': node[1],
      'length': len(node[0]),
      'count': sequence_counts[node_list.index(node)],
      'anticodon_list': list(sequence_to_anticodon_map[node[0]]),
      'isotype': node[2]
  }

def edge_to_dictionary(edge, edge_type):
  return {
      'source': f'{edge[0][0]}-{edge[0][2]}',
      'target': f'{edge[1][0]}-{edge[1][2]}',
      'type': edge_type
  }

node_json_list = [node_to_dictionary(node, list(G.nodes), sequence_counts, sequence_to_anticodon_map) for node in list(G.nodes)]
edge_json_list = [edge_to_dictionary(edge, edge_type) for edge, edge_type in zip(list(G.edges), edge_types)]
graph_json = {
  'nodes': node_json_list,
  'edges': edge_json_list
}
json_string = json.dumps(graph_json)
print(json_string)
