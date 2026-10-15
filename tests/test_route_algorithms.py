"""Tests for route algorithms and data manager."""
import pytest
import networkx as nx
from src.route_algorithms import dijkstra, build_adj_from_nx
from src.data_manager import DataManager
from src.models import FlightRoute, Airport


def test_dijkstra_direct_route():
    # simple two-node graph
    adj = {'A': {'B': 100}, 'B': {'A': 100}}
    path, dist = dijkstra(adj, 'A', 'B')
    assert path == ['A','B']
    assert dist == 100


def test_dijkstra_via_intermediate():
    adj = {'A': {'B': 50}, 'B': {'A':50,'C':50}, 'C': {'B':50}}
    path, dist = dijkstra(adj, 'A', 'C')
    assert path == ['A','B','C']
    assert dist == 100


def test_dijkstra_no_path():
    adj = {'A':{}, 'B':{}}
    with pytest.raises(Exception):
        dijkstra(adj, 'A', 'B')


def test_data_manager_csv_load_and_duplicate_airport(tmp_path):
    dm = DataManager(airports_csv=tmp_path/'airports.csv', routes_csv=tmp_path/'routes.csv')
    # add airport
    dm.add_airport(Airport('TST','Test Airport','Test City'))
    with pytest.raises(ValueError):
        dm.add_airport(Airport('TST','Test Airport','Test City'))
