import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def build(no_node, no_edge):
    G = nx.Graph(model = 'One')
    G.add_node(0, att1= 0, att2= 1)
    G.add_node(1, att1= 0, att2= 1)
    G.add_edge(0, 1, weight=1)
    p = 0.5
    for i in range(2,no_node):
        G.add_node(i, att1= 0, att2= 1)
        node_list = sorted(node for (node, val) in sorted(G.degree, key=lambda x: x[1], reverse=True))
        count = 0
        for j in node_list:
            if G.number_of_edges() != 0 :
                p = G.degree(j)/G.number_of_edges()
            if round(np.random.uniform(0,1),1)<p:
                G.add_edge(j, i, weight=1)
                count=count+1
                if count==no_edge :
                    break
        if G.degree[i] == 0:
            tmp = np.random.randint(0, i-1)
            G.add_edge(tmp, i, weight=1)
    nx.draw(G, with_labels=True)
    plt.savefig("simple_path.png")
    plt.show()

