# Description for the Preferential Attachment Functions
## 1. PreferntialAttachmentV1
```python
def preferentialAttachmentV1(max_nodes, loner=False):
    G = nx.Graph()
    G.add_node(0)
    G.add_node(1)
    G.add_edge(0, 1)
    p = 0.5
    # ----- Part 1 -----
    for i in range(2, max_nodes):
        # ----- Part 1.1 -----
        G.add_node(i)
        node_list = sorted(node for (node, val) in sorted(G.degree, key=lambda x: x[1], reverse=True))
        # ----- Part 1.2 -----
        for j in node_list:
            if G.number_of_edges() != 0:
                p = G.degree(j) / (2 * G.number_of_edges())
            if (round(np.random.uniform(0, 1), 1) < p) & (j != i):
                G.add_edge(j, i)
        # ----- Part 1.3 -----
        if not loner & (G.degree[i] == 0):
            tmp = node_list[0]
            G.add_edge(tmp, i)
    plotGraph(G)
    return (G)
```
### Basic Description:
User defines the maximum number of nodes in the final graph (max_nodes) as well as wheter loner behavior
should be exhibited (more on this later). The Function then returns a preferential attachment (PA) graph.

#### Part 1
```python
for i in range(2, max_nodes):
```
The loop will run $$(max_nodes -) $$
