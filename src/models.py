"""Models for Airport and FlightRoute

Includes simple classes showcasing OOP concepts from the Python syllabus.
"""
from typing import Optional

class Airport:
    """Represents an airport.

    Attributes:
        code (str): IATA-like airport code, unique.
        name (str): Airport full name.
        city (str): City where the airport is located.
    """

    def __init__(self, code: str, name: str, city: str):
        self.code = code.strip().upper()
        self.name = name.strip()
        self.city = city.strip()

    def __repr__(self):
        return f"Airport({self.code}, {self.name}, {self.city})"


class FlightRoute:
    """Represents a route between two airports.

    Attributes:
        source (str): source airport code
        destination (str): destination airport code
        distance_km (float): distance in kilometers (must be positive)
        travel_time_min (Optional[float]): estimated travel time in minutes
    """

    def __init__(self, source: str, destination: str, distance_km: float, travel_time_min: Optional[float] = None):
        self.source = source.strip().upper()
        self.destination = destination.strip().upper()
        if distance_km <= 0:
            raise ValueError("distance_km must be positive")
        self.distance_km = float(distance_km)
        self.travel_time_min = float(travel_time_min) if travel_time_min is not None and travel_time_min != '' else None

    def __repr__(self):
        return f"FlightRoute({self.source} - {self.destination}, {self.distance_km} km, {self.travel_time_min} min)"
