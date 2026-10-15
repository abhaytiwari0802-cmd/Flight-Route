"""Visualization helpers for network plotting using NetworkX and Matplotlib."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[1] / 'outputs'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def draw_network(G: nx.Graph, highlight_path=None, out: Path = OUTPUT_DIR / 'network.png'):
    plt.figure(figsize=(10,8))
    pos = nx.spring_layout(G, seed=42)
    # draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(G, pos)
    # draw edges
    normal_edges = [e for e in G.edges()]
    nx.draw_networkx_edges(G, pos, edgelist=normal_edges, edge_color='gray')
    # edge labels: distance
    edge_labels = {(u,v): f"{d.get('distance_km',0)}" for u,v,d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # highlight path if provided
    if highlight_path and len(highlight_path) > 1:
        path_edges = list(zip(highlight_path, highlight_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2.5)
    plt.title('Airport Network (simulated data)')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out
