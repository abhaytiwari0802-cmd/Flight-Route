"""Graph construction and helper utilities using NetworkX."""
import networkx as nx
import pandas as pd
from typing import Tuple, List


class GraphManager:
    """Builds an undirected weighted graph from route data.

    Stores NetworkX graph and provides helpers for visualization and queries.
    """

    def __init__(self, airports_df: pd.DataFrame, routes_df: pd.DataFrame):
        self.airports_df = airports_df
        self.routes_df = routes_df
        self.G = nx.Graph()
        self.build_graph()

    def build_graph(self):
        self.G.clear()
        # Add nodes with labels
        for _, row in self.airports_df.iterrows():
            self.G.add_node(row['code'], name=row.get('name',''), city=row.get('city',''))
        # Add edges
        for _, r in self.routes_df.iterrows():
            s = r['source']
            d = r['destination']
            try:
                w = float(r['distance_km'])
            except Exception:
                continue
            if s not in self.G.nodes or d not in self.G.nodes:
                continue
            # undirected; store travel_time if available
            attr = {'distance_km': w}
            if 'travel_time_min' in r and r['travel_time_min']!='':
                try:
                    attr['travel_time_min'] = float(r['travel_time_min'])
                except Exception:
                    pass
            self.G.add_edge(s, d, **attr)

    def nodes(self) -> List[str]:
        return list(self.G.nodes)

    def edges(self) -> List[Tuple[str,str]]:
        return list(self.G.edges(data=True))

    def to_networkx(self):
        return self.G
