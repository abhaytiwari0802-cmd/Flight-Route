"""Implementation of Dijkstra's algorithm and alternative route discovery."""
from typing import Dict, Tuple, List, Optional
import heapq
import networkx as nx


def dijkstra(adj: Dict[str, Dict[str, float]], source: str, target: str) -> Tuple[List[str], float]:
    """Compute shortest path using Dijkstra's algorithm.

    adj: adjacency dict of dicts: {u: {v: weight, ...}, ...}
    Returns (path list, total distance)

    Time complexity: Using a binary heap (heapq) and adjacency lists, the
    complexity is O((V + E) log V) where V is number of vertices and E is
    number of edges.
    """
    source = source.strip().upper()
    target = target.strip().upper()
    if source == target:
        raise ValueError("Source and destination are the same")
    if source not in adj or target not in adj:
        raise KeyError("Unknown source or destination code")

    pq = []  # heap of (distance, node, predecessor)
    heapq.heappush(pq, (0.0, source, None))
    dist = {source: 0.0}
    prev: Dict[str, Optional[str]] = {source: None}
    visited = set()

    while pq:
        d, node, _ = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if node == target:
            break
        for neighbor, weight in adj.get(node, {}).items():
            if weight <= 0:
                continue
            nd = d + weight
            if neighbor not in dist or nd < dist[neighbor]:
                dist[neighbor] = nd
                prev[neighbor] = node
                heapq.heappush(pq, (nd, neighbor, node))

    if target not in dist:
        raise nx.NetworkXNoPath(f"No path between {source} and {target}")

    # reconstruct path
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()
    return path, dist[target]


def build_adj_from_nx(G: nx.Graph) -> Dict[str, Dict[str, float]]:
    adj = {}
    for u in G.nodes:
        adj[u] = {}
    for u, v, data in G.edges(data=True):
        w = float(data.get('distance_km', 0.0))
        adj[u][v] = w
        adj[v][u] = w
    return adj


def find_alternative_paths(G: nx.Graph, source: str, target: str, k: int = 3) -> List[Tuple[List[str], float]]:
    """Find up to k simple alternative paths using a simple k-shortest approach.

    This is a simple candidate generator: remove one edge on the found shortest
    path and recompute shortest path to get alternatives. It does not guarantee
    all possible routes but provides meaningful alternatives for comparison.
    """
    source = source.strip().upper()
    target = target.strip().upper()
    results = []
    try:
        sp = nx.shortest_path(G, source=source, target=target, weight='distance_km')
        sp_length = nx.shortest_path_length(G, source=source, target=target, weight='distance_km')
        results.append((sp, float(sp_length)))
    except Exception:
        return results

    # generate alternatives by removing each edge along shortest path and recomputing
    for i in range(len(sp)-1):
        if len(results) >= k:
            break
        u = sp[i]
        v = sp[i+1]
        if not G.has_edge(u, v):
            continue
        G.remove_edge(u, v)
        try:
            alt_path = nx.shortest_path(G, source=source, target=target, weight='distance_km')
            alt_length = float(nx.shortest_path_length(G, source=source, target=target, weight='distance_km'))
            if (alt_path, alt_length) not in results:
                results.append((alt_path, alt_length))
        except Exception:
            pass
        G.add_edge(u, v, distance_km=G.graph.get('edge_backup', {}).get((u, v), 0))
    return results
