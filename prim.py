import networkx as nx
import matplotlib.pyplot as plt

def create_graph(file_path):
    G = nx.read_weighted_edgelist(file_path, create_using= nx.Graph)
    return G


def prim(graph):

    mst = nx.Graph()  
    visited = set()  

    initial_node = list(graph.nodes())[0]
    visited.add(initial_node)

    edges = [(data['weight'], u, v) 
             for u, v, data in graph.edges(data=True) 
             if u == initial_node or v == initial_node]

    edges.sort()

    while len(visited) < graph.number_of_nodes():

        for weight, u, v in edges:
            if u not in visited or v not in visited:
                best_edge = (weight, u, v)
                break
        
        weight, u, v = best_edge
        if u not in visited:
            new_node = u
        else:
            new_node = v
        
        visited.add(new_node)
        mst.add_edge(u, v, weight=weight)

        for u2, v2, data in graph.edges(data=True):
            if (u2 == new_node or v2 == new_node) and (u2 not in visited or v2 not in visited):
                edges.append((data['weight'], u2, v2))
        
        edges = [(p, u, v) for p, u, v in edges if u not in visited or v not in visited]
        edges.sort()

    return mst

def draw_graph(graph):

    pos = nx.spring_layout(graph) 
    nx.draw(graph, pos, with_labels=True)
    labels = nx.get_edge_attributes(graph, 'weight')  
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()

def main():

    file_path = 'graph.txt'
    G = create_graph(file_path)

    print("Original Graph:")
    draw_graph(G)

    mst = prim(G)

    print("Minimum Spanning Tree:")
    draw_graph(mst)


main()
