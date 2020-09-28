import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

def preferentialAttachPipi(no_node, no_edge):
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
        # get their preference (prob. of forming edge with new node by dividing their degrees by total edges
        node_list = sorted(G.degree, key=lambda x: x[1], reverse=True)
        # insert new node
        G.add_node(i)
        print('---Inserted node %d---' % i)
        # print(node_degree_list)
        for node, degrees in node_list:
            if (G.degree(node) / G.number_of_edges()) >= max_p:
                p = max_p
            else:
                p = G.degree(node) / G.number_of_edges()
            print("the p value for node %d is: %f" % (node, p))
            if random.random() <= p:
                G.add_edge(node, i)
                print('edge between %d and %d created' % (node, i))
        if not loner and G.degree(i) == 0:
            rand_node = np.random.randint(0, i - 1)
            G.add_edge(rand_node, i)
            print('did not form edge with prev. nodes, will add %d to rand. node %d' % (i, rand_node))
        # if max number of edges exceeded, end the program
        if G.number_of_edges() >= max_edges:
            print("exceeded max edges")
            break
        # nx.draw(G, with_labels=True)
        # plt.show()
    nx.draw(G, with_labels=True)
    plt.show()
    return []

def preferentialAttachment_2ndOrder(max_nodes, max_edges, loner=False, max_p=1.0):
    # v2 Goals: Implement the "Two-level network model" (proposed by Dangalchev)
    # formula: https://en.wikipedia.org/wiki/Scale-free_network

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
        # get their preference (prob. of forming edge with new node by dividing their degrees by total edges
        node_list = sorted(G.degree, key=lambda x: x[1], reverse=True)
        # insert new node
        G.add_node(i)
        print('---Inserted node %d---' % i)
        # print(node_degree_list)
        for node, degrees in node_list:
            if (G.degree(node) / G.number_of_edges()) >= max_p:
                p = max_p
            else:
                p = G.degree(node) / G.number_of_edges()
            print("the p value for node %d is: %f" % (node, p))
            if random.random() <= p:
                G.add_edge(node, i)
                print('edge between %d and %d created' % (node, i))
        if not loner and G.degree(i) == 0:
            rand_node = np.random.randint(0, i - 1)
            G.add_edge(rand_node, i)
            print('did not form edge with prev. nodes, will add %d to rand. node %d' % (i, rand_node))
        # if max number of edges exceeded, end the program
        if G.number_of_edges() >= max_edges:
            print("exceeded max edges")
            break
        # nx.draw(G, with_labels=True)
        # plt.show()
    nx.draw(G, with_labels=True)
    plt.show()
    return []