import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from plot_graph import *


def getInverseHarmonicMean(graph, node):
    # calculate the IHM of an existing node in a graph
    sum_inverse_degrees = 0
    for n in graph.neighbors(node):
        sum_inverse_degrees += 1 / graph.degree(n)
    IHM = sum_inverse_degrees / graph.degree(node)
    return IHM


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


def preferentialAttachment(max_nodes, max_edges, loner=False, max_p=1.0):
    # v_1 notes: this version follows the The Barabási–Albert model which uses a linear preferential attachment
    # https://en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model

    # loner behavior == True: if the new node did not form an edge with prev. nodes,
    # then the node will not form any edges

    # max_p: specify a maximum number for p
    # because for first few nodes, this (G.degree(node) / G.number_of_edges()) ratio is very high

    # initialize empty graph
    G = nx.Graph()
    # initialize first two nodes and edge
    G.add_nodes_from([0, 1])
    G.add_edge(0, 1)
    for i in range(2, max_nodes):
        # from a list of existing nodes sorted by their degrees (descending order)
        # get their preference (prob. of forming edge with new node by dividing their degrees by
        # sum of degrees of all pre-existing edges

        node_list = sorted(G.degree, key=lambda x: x[1], reverse=True)
        # insert new node
        G.add_node(i)
        # print('---Inserted node %d---' % i)
        # print(node_degree_list)
        for node, degrees in node_list:
            if (G.degree(node) / (2 * G.number_of_edges())) >= max_p:
                p = max_p
            else:
                p = G.degree(node) / (2 * G.number_of_edges())
            # print("the p value for node %d is: %f" % (node, p))
            if random.random() <= p:
                G.add_edge(node, i)
                # print('edge between %d and %d created' % (node, i))
        if not loner and G.degree(i) == 0:
            rand_node = np.random.randint(0, i - 1)
            G.add_edge(rand_node, i)
            # print('did not form edge with prev. nodes, will add %d to rand. node %d' % (i, rand_node))
        # if max number of edges exceeded, end the program
        if G.number_of_edges() >= max_edges:
            # print("exceeded max edges")
            break
    plotGraph(G)


def preferentialAttachment_2ndOrder(max_nodes, max_edges, loner=False, max_p=1.0):
    # v2 Goals: Implement the "Two-level network model" (proposed by Dangalchev)
    # formula: https://www.sciencedirect.com/science/article/pii/S0378437104001402

    # max_p: specify a maximum number for p
    # because for first few nodes, this (G.degree(node) / G.number_of_edges()) ratio is very high

    # coef should be [0,1]

    #           degree of node i + C * sum of degrees of i's neighbors
    # We adopt p = ----------------------------------------------------------
    #              sum of degrees of all pre-existing nodes + C * sum of degrees^2 of all pre-existing nodes
    # note that when c = 0, this equation is same as the Barabasi-ALbert model
    # initialize empty graph
    G = nx.Graph()
    # initialize first two nodes and edge
    G.add_nodes_from([0, 1])
    G.add_edge(0, 1)
    for i in range(2, max_nodes):
        # from a list of existing nodes sorted by their degrees (descending order)
        # get their preference (prob. of forming edge with new node by dividing their degrees by total edges
        existing_node_list = sorted(G.degree, key=lambda x: x[1], reverse=True)
        # insert new node
        G.add_node(i)
        print('---Inserted node %d---' % i)
        # iterate through a list of existing nodes sorted in descending order by number of degree
        for node, degrees in existing_node_list:
            sum_neighbors_degree = 0
            sum_neighbors_degree_squared = 0
            for neighbor in G.neighbors(node):
                sum_neighbors_degree += G.degree(neighbor)
                sum_neighbors_degree_squared += pow(G.degree(neighbor), 2)
            # calculate the prob. (p) that new node (i) will form edge with node (node)
            p = (G.degree(node) + coef * sum_neighbors_degree) / (
                        2 * G.number_of_edges() + coef * sum_neighbors_degree_squared)
            if p >= max_p: p = max_p
            print("the p value for node %d is: %f" % (node, p))
            if random.random() <= p:
                G.add_edge(node, i)
                print('edge between %d and %d created' % (node, i))
        if not loner and G.degree(i) == 0:
            rand_node = np.random.randint(0, i - 1)
            G.add_edge(rand_node, i)
            # print('did not form edge with prev. nodes, will add %d to rand. node %d' % (i, rand_node))
        # nx.draw(G, with_labels=True)
        # plt.show()
    plotGraph(G)
    return []


def preferentialAttachment_MDA(max_nodes, m0, m):
    # uncertainty: what if the mediator doesn't have m neighbors?
    # - current behavior: if total neighbors < m, use total neighbors

    # initialize a graph with m0 nodes connected in an arbitrary fashion
    G = preferentialAttachment(m0, 100)
    for new_node in range(m0 + 1, max_nodes):
        # first obtain a list of connected nodes in the existing graph
        connected_nodes_list = []
        for n in G.degree:
            if n[1] != 0: connected_nodes_list.append(n[0])
        # insert new node
        G.add_node(new_node)
        print('---Inserted node %d---' % new_node)
        # picking a random node from list of connected nodes as mediator
        # for n in connected_nodes_list:
        #     N = len(list(G.neighbors(n)))
        #     p = (G.degree(n) / N) * getInverseHarmonicMean(G, n)
        mediator = random.choice(connected_nodes_list)
        print("this is the randomly chosen connected node: %d" % mediator)

        # pick m of mediator's neighbors with uniform probability
        all_neighbors_list = list(G.neighbors(mediator))
        print("this is the list of all of mediator's neighbors: ", all_neighbors_list)
        m_neighbors_list = []
        # randomly select min(m, total_num_of_neighbors) nodes without replacement
        for n in range(min(m, G.degree(mediator))):
            neighbor = random.choice(all_neighbors_list)
            all_neighbors_list.remove(neighbor)
            m_neighbors_list.append(neighbor)
        print("this is list of m randomly selected neighbors of mediator: ", m_neighbors_list)
        # connect the new node with the nodes in m_neighbors_list
        for n in m_neighbors_list:
            G.add_edge(n, new_node)
            print('edge between %d and %d created' % (n, new_node))
        # nx.draw(G, with_labels=True)
        # plt.show()

    plotGraph(G)
    return []


preferentialAttachmentV1(100)
