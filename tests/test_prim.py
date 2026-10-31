import random
from pathlib import Path

import networkx as nx
import pytest

from prim import load_graph, prim, total_weight

GRAPH_FILE = Path(__file__).resolve().parent.parent / "graph.txt"


def reference_weight(graph):
    return total_weight(nx.minimum_spanning_tree(graph, algorithm="kruskal"))


def test_sample_graph_is_minimum_spanning_tree():
    graph = load_graph(GRAPH_FILE)
    mst = prim(graph)
    assert nx.is_tree(mst)
    assert set(mst.nodes) == set(graph.nodes)
    assert total_weight(mst) == pytest.approx(reference_weight(graph))


@pytest.mark.parametrize("seed", range(20))
def test_random_connected_graphs(seed):
    rng = random.Random(seed)
    graph = nx.connected_watts_strogatz_graph(25, 4, 0.3, seed=seed)
    for u, v in graph.edges:
        graph[u][v]["weight"] = rng.randint(1, 50)

    mst = prim(graph)
    assert nx.is_tree(mst)
    assert total_weight(mst) == reference_weight(graph)


def test_disconnected_graph_gives_spanning_forest():
    graph = nx.Graph()
    graph.add_edge("a", "b", weight=1)
    graph.add_edge("b", "c", weight=2)
    graph.add_edge("a", "c", weight=5)
    graph.add_edge("x", "y", weight=3)

    forest = prim(graph)
    assert nx.is_forest(forest)
    assert nx.number_connected_components(forest) == 2
    assert total_weight(forest) == 6


def test_duplicate_edges_keep_cheapest(tmp_path):
    file = tmp_path / "g.txt"
    file.write_text("a b 9\nb a 2\nb c 4\n")
    graph = load_graph(file)
    assert graph["a"]["b"]["weight"] == 2
