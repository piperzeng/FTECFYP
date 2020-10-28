import networkx as nx
import collections
from operator import itemgetter
import matplotlib.pyplot as plt

# G = some networkx graph

def basicInfo(G):
    n, e = G.number_of_nodes(), G.number_of_edges()
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    dmax = max(degree_sequence)
    print("Nodes: %d. Edges: %d. Max_degree: %d" % (n,e,dmax))

def degreeHistogram(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')
    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)
    plt.show()

def degreeDistribution(G):
    degree_freq = nx.degree_histogram(G)
    degrees = range(len(degree_freq))
    plt.figure()
    plt.grid(True)
    plt.loglog(degrees[:], degree_freq[:], 'go-')
    plt.title('Social Network')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    # plt.savefig('./degree_distribution.pdf')
    plt.show()

def clusteringCoefficient(G):
    # Clustering coefficient of all nodes (in a dictionary)
    clust_coefficients = nx.clustering(G)
    ave_clust = nx.average_clustering(G)
    print("Average clustering coefficient of the graph: %d" % ave_clust)

# degreeHistogram(nx.gnp_random_graph(100, 0.02))
clusteringCoefficient(nx.gnp_random_graph(100, 0.02))