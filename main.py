from build_network import *

def main():

    no_node=input("Please input the number of nodes in the network")
    no_edge=input("Please input the max number of edges a newly added nodes can have")
    build(int(no_node), int(no_edge))

if __name__ == "__main__":
    main()