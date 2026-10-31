"""Minimum spanning tree with Prim's algorithm.

The graph is read from a weighted edge list (``u v weight`` per line) and
treated as undirected. Prim's algorithm is implemented from scratch with a
binary heap; NetworkX is used only as the graph container and for drawing.
"""

from __future__ import annotations

import argparse
import heapq
from collections.abc import Hashable

import networkx as nx

Node = Hashable


def load_graph(path: str) -> nx.Graph:
    """Read an undirected, weighted graph from an edge-list file.

    If the same pair of vertices appears more than once (e.g. ``3 4`` and
    ``4 3``), the cheapest edge is kept.
    """
    graph = nx.Graph()
    with open(path, encoding="utf-8") as file:
        for line in file:
            fields = line.split()
            if not fields or fields[0].startswith("#"):
                continue
            u, v, weight = fields[0], fields[1], float(fields[2])
            if not graph.has_edge(u, v) or weight < graph[u][v]["weight"]:
                graph.add_edge(u, v, weight=weight)
    return graph


def prim(graph: nx.Graph) -> nx.Graph:
    """Return a minimum spanning forest of ``graph``.

    Each connected component is grown from an arbitrary start vertex by
    repeatedly adding the cheapest edge that leaves the current tree.
    Runs in O(E log V).
    """
    forest = nx.Graph()
    forest.add_nodes_from(graph.nodes)
    visited: set[Node] = set()
    counter = 0  # tie-breaker so nodes themselves never need to be comparable

    for start in graph.nodes:
        if start in visited:
            continue
        visited.add(start)
        heap: list[tuple[float, int, Node, Node]] = []
        for neighbor, data in graph[start].items():
            heapq.heappush(heap, (data.get("weight", 1.0), counter, start, neighbor))
            counter += 1

        while heap:
            weight, _, u, v = heapq.heappop(heap)
            if v in visited:
                continue
            visited.add(v)
            forest.add_edge(u, v, weight=weight)
            for neighbor, data in graph[v].items():
                if neighbor not in visited:
                    heapq.heappush(heap, (data.get("weight", 1.0), counter, v, neighbor))
                    counter += 1

    return forest


def total_weight(graph: nx.Graph) -> float:
    return sum(weight for _, _, weight in graph.edges(data="weight", default=1.0))


def draw_graph(graph: nx.Graph, title: str) -> None:
    import matplotlib.pyplot as plt

    plt.figure(title)
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=600)
    labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimum spanning tree (Prim).")
    parser.add_argument("-g", "--graph", default="graph.txt", help="edge-list file (default: graph.txt)")
    parser.add_argument("--no-plot", action="store_true", help="do not open the graph windows")
    args = parser.parse_args()

    graph = load_graph(args.graph)
    mst = prim(graph)

    print("Minimum spanning tree edges:")
    for u, v, weight in sorted(mst.edges(data="weight"), key=lambda edge: edge[2]):
        print(f"  {u} - {v}  (weight {weight:g})")
    print(f"Total weight: {total_weight(mst):g}")

    if not args.no_plot:
        import matplotlib.pyplot as plt

        draw_graph(graph, "Original graph")
        draw_graph(mst, "Minimum spanning tree")
        plt.show()


if __name__ == "__main__":
    main()
