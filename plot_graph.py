import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from pylab import rcParams
from pyvis.network import Network

def plotGraph(G):
    # plotGraphWithDegree(G)
    # plotGraphWithNodeSizeDependOnNodeDegree(G)
    # plotGraphWithNodeColorDependOnNodeDegree(G)
    plotGraphCombined(G)
    # interactiveGraph(G)
    # interactiveGraphExtended(G)

def plotGraphWithDegree(G):
    # polt netwrok with nodes' degree labeled
    degree_labels = {}
    for node in G.nodes():
        degree_labels[node] = G.degree(node);
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=False)
    nx.draw_networkx_labels(G, pos, labels=degree_labels, font_size=10, font_color='white')
    plt.show()

def plotGraphWithNodeSizeDependOnNodeDegree(G):
    # plot network with nodes' size depend on nodes' degree
    D = dict(G.degree)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_size=10, font_color='white',
            nodelist=D.keys(), node_size=[v * 100 for v in D.values()])
    plt.show()

def plotGraphWithNodeColorDependOnNodeDegree(G):
    # plot network with nodes' color depend on nodes' degree.
    # coolwarm: Red (Higher degree) --- Blue (Lower degree)
    D = dict(G.degree)
    low, *_, high = sorted(D.values())
    norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)
    rcParams['figure.figsize'] = 12, 7
    pos = nx.spring_layout(G)
    nx.draw(G, pos,
            nodelist=D,
            node_size=1000,
            node_color=[mapper.to_rgba(i)
                        for i in D.values()],
            with_labels=True,
            font_color='white')
    plt.show()

def plotGraphCombined(G):
    # plot graph combined the above 3: Nodes' color, size depend on nodes' degree, labeled with degree
    degree_labels = {}
    for node in G.nodes():
        degree_labels[node] = G.degree(node);
    D = dict(G.degree)
    low, *_, high = sorted(D.values())
    norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)
    rcParams['figure.figsize'] = 12, 7
    pos = nx.spring_layout(G)
    nx.draw(G, pos,
            nodelist=D.keys(),
            node_size=[v * 100 for v in D.values()],
            # nodelist=D,
            # node_size=1000,
            node_color=[mapper.to_rgba(i)
                        for i in D.values()],
            with_labels=False,
            )
    nx.draw_networkx_labels(G, pos, labels=degree_labels, font_size=10, font_color='white')
    plt.show()

def interactiveGraph(G):
    # plot simple interactive graph using pyvis
    nt = Network("500px", "1000px")
    nt.from_nx(G)
    nt.show("nx.html")

def interactiveGraphExtended(G):
    # plot interactive graph using pyvis, with degree, no of node labeled, size depends on nodes' degree
    nt = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    nt.barnes_hut(spring_strength=0.006)
    for node in G:
        nt.add_node(node, label=G.degree(node), title="I am node "+str(node), value=G.degree(node))
    for edge in G.edges:
        nt.add_edge(int(edge[0]), int(edge[1]), color='white')
    nt.show("nx.html")