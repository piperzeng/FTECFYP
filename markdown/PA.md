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
        node_list = sorted(node for (node, val) in sorted(G.degree, key=lambda x: x[1], reverse=True))
        G.add_node(i)
        # ----- Part 1.2 -----
        for j in node_list:
            if G.number_of_edges() != 0:
                p = G.degree(j) / (2 * G.number_of_edges())
            if (round(np.random.uniform(0, 1), 1) < p):
                G.add_edge(j, i)
        # ----- Part 1.3 -----
        if not loner & (G.degree[i] == 0):
            tmp = node_list[random.choice(node_list)]
            G.add_edge(tmp, i)
    plotGraph(G)
    return (G)
```
### Basic Description:
User defines the maximum number of nodes in the final graph (max_nodes) as well as whether loner behavior should be exhibited (refer to *Part 1.3*). The Function then returns a preferential attachment (*PA*) graph.

#### Part 1
```python
for i in range(2, max_nodes):
```
The loop will run $(max\_nodes - 2)$ times, omitting nodes 0 and 1 because they are already initialized.
#### Part 1.1
```python
node_list = sorted(node for (node, val) in sorted(G.degree, key=lambda x: x[1], reverse=True))
G.add_node(i)
```
We first obtain a list of existing nodes sorted by degrees in descending order, then we add the new $node_i$ into the graph

#### Part 1.2
```python
for j in node_list:
    if G.number_of_edges() != 0:
        p = G.degree(j) / (2 * G.number_of_edges())
    if (round(np.random.uniform(0, 1), 1) < p):
        G.add_edge(j, i)
```
Now we loop through the list of existing nodes excluding $node_i$ (node_list) and calculate the probability p that the new $node_i$ will form an edge with the current existing node.
Probability $p_i$ that new $node_i$ will appending to existing $node_j$ is calculated as follows:
$$
\begin{align*}
p_i = \frac{k_i}{\sum_j k_j}\label{ref1}
\end{align*}
\\
$$
Once we have calculated the probability, we used the numpy's random.uniform() function to get a random float between [0,1] and compare that with $p_i$. If the random float is smaller than $p_i$, we connect $node_i$ with $node_j$.

#### Part 1.3

```python
if not loner & (G.degree[i] == 0):
    tmp = node_list[random.choice(node_list)]
    G.add_edge(tmp, i)
```

This is the loner behavior of the graph. If $loner == False$ , $node_i$ will connect to a random existing node in the graph if it did not form an edge with $node_j$ in *Part 1.2*. We found that the method we use to select the random node has significant effect on the final graph. In the following section we will discuss the results of different selection methods using the following parameters:

```python
preferentialAttachmentV1(100, False)
```

#### Discussion of different random node selection methods for *Part 1.3*

1. Randomly select a node from node_list using random.choice():

```python
if not loner & (G.degree[i] == 0):
    tmp = node_list[random.choice(node_list)]
    G.add_edge(tmp, i)
```

The result from this method is shown below:

![random.choice() method](./graphs/PAv1_graph1.PNG)

The highlighted node in the middle is $node_0$ , and as you can see its degree isn't very different from other nodes (the size of the node represents its relative degree).

2.  Simply choose the most connected node:

```python
if not loner & (G.degree[i] == 0):
    tmp = node_list[0]
    G.add_edge(tmp, i)
```

![random.choice() method](./graphs/PAv1_graph2.PNG)

The highlighted node is $node_0$ and its degree is significantly higher than other nodes. 

