# Prim's Minimum Spanning Tree

[![CI](https://github.com/BernardoFerrazG/prim_algorithm/actions/workflows/ci.yml/badge.svg)](https://github.com/BernardoFerrazG/prim_algorithm/actions/workflows/ci.yml)

A from-scratch implementation of **Prim's algorithm** for computing the minimum spanning tree (MST) of an undirected, weighted graph, with a CLI and side-by-side visualisation of the original graph and its MST.

NetworkX is used only as the graph container and for drawing. The algorithm is implemented by hand and validated against NetworkX's Kruskal implementation in the test suite.

## How it works

1. Start the tree from any vertex and push all of its edges onto a **min-heap**.
2. Pop the cheapest edge. If it reaches a vertex that is not in the tree yet, add the edge and that vertex, then push the new vertex's edges.
3. Repeat until the heap is empty.
4. If the graph is disconnected, the process restarts from an unvisited vertex, producing a **minimum spanning forest**.

| | |
| --- | --- |
| Time | `O(E log V)` |
| Space | `O(V + E)` |

## Usage

```bash
pip install -r requirements.txt
python prim.py                 # uses graph.txt and opens the plots
python prim.py --no-plot       # text output only
python prim.py -g my_graph.txt
```

The input is a whitespace-separated edge list, one `u v weight` per line (see [`graph.txt`](graph.txt)). Edges are treated as undirected; if a pair appears twice, the cheaper edge is kept.

Example output:

```
Minimum spanning tree edges:
  1 - 5  (weight 1)
  6 - 8  (weight 1)
  1 - 3  (weight 2)
  3 - 4  (weight 2)
  7 - 8  (weight 2)
  2 - 4  (weight 4)
  6 - 5  (weight 7)
Total weight: 19
```

## Tests

```bash
pip install pytest
pytest
```

The suite checks that the result is a spanning tree with the same total weight as NetworkX's Kruskal MST, on the sample graph and on 20 random connected graphs. It also covers disconnected graphs (spanning forest) and duplicate edges. CI runs it on every push.

## Project structure

```
prim.py              # graph loading, Prim's algorithm, CLI and plotting
graph.txt            # sample graph
tests/               # pytest suite
```
