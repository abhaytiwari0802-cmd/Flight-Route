"""Additional tests for data manager and CSV handling."""
import pytest
from src.data_manager import DataManager
from src.models import Airport, FlightRoute


def test_add_and_delete_route(tmp_path):
    dm = DataManager(airports_csv=tmp_path/'airports.csv', routes_csv=tmp_path/'routes.csv')
    dm.add_airport(Airport('A1','A1 Name','City1'))
    dm.add_airport(Airport('A2','A2 Name','City2'))
    r = FlightRoute('A1','A2', 123.4, 90)
    df = dm.add_route(r)
    assert not df.empty
    df2 = dm.delete_route(0)
    assert df2.empty


def test_invalid_route_distance(tmp_path):
    dm = DataManager(airports_csv=tmp_path/'airports.csv', routes_csv=tmp_path/'routes.csv')
    dm.add_airport(Airport('A1','A1 Name','City1'))
    dm.add_airport(Airport('A2','A2 Name','City2'))
    with pytest.raises(ValueError):
        FlightRoute('A1','A2', -10)
