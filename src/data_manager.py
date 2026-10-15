"""Data manager: load and save airports and routes using pandas."""
from pathlib import Path
import pandas as pd
from typing import Tuple
from .models import Airport, FlightRoute

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
AIRPORTS_CSV = DATA_DIR / 'airports.csv'
ROUTES_CSV = DATA_DIR / 'routes.csv'


class DataManager:
    """Manages CSV persistence for airports and routes.

    Uses pandas to read/write CSV files and performs validation.
    """

    def __init__(self, airports_csv: Path = AIRPORTS_CSV, routes_csv: Path = ROUTES_CSV):
        self.airports_csv = airports_csv
        self.routes_csv = routes_csv
        self._ensure_data_files()

    def _ensure_data_files(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not self.airports_csv.exists():
            pd.DataFrame(columns=['code', 'name', 'city']).to_csv(self.airports_csv, index=False)
        if not self.routes_csv.exists():
            pd.DataFrame(columns=['source', 'destination', 'distance_km', 'travel_time_min']).to_csv(self.routes_csv, index=False)

    def load_airports(self) -> pd.DataFrame:
        df = pd.read_csv(self.airports_csv, dtype=str).fillna('')
        df['code'] = df['code'].str.strip().str.upper()
        return df

    def load_routes(self) -> pd.DataFrame:
        df = pd.read_csv(self.routes_csv, dtype={'source':str,'destination':str,'distance_km':float,'travel_time_min':float}).fillna('')
        df['source'] = df['source'].str.strip().str.upper()
        df['destination'] = df['destination'].str.strip().str.upper()
        return df

    def save_airports(self, df: pd.DataFrame):
        df.to_csv(self.airports_csv, index=False)

    def save_routes(self, df: pd.DataFrame):
        df.to_csv(self.routes_csv, index=False)

    # Airport operations
    def add_airport(self, airport: Airport):
        df = self.load_airports()
        if airport.code in df['code'].values:
            raise ValueError(f"Airport code {airport.code} already exists")
        df = df.append({'code':airport.code,'name':airport.name,'city':airport.city}, ignore_index=True)
        self.save_airports(df)
        return df

    def update_airport(self, code: str, name: str = None, city: str = None):
        df = self.load_airports()
        code = code.strip().upper()
        if code not in df['code'].values:
            raise KeyError(f"Airport {code} not found")
        if name is not None:
            df.loc[df['code']==code,'name'] = name
        if city is not None:
            df.loc[df['code']==code,'city'] = city
        self.save_airports(df)
        return df

    def delete_airport(self, code: str):
        code = code.strip().upper()
        df = self.load_airports()
        if code not in df['code'].values:
            raise KeyError(f"Airport {code} not found")
        df = df[df['code'] != code]
        # remove related routes
        routes = self.load_routes()
        routes = routes[(routes['source'] != code) & (routes['destination'] != code)]
        self.save_airports(df)
        self.save_routes(routes)
        return df, routes

    # Route operations
    def add_route(self, route: FlightRoute):
        airports = self.load_airports()
        if route.source not in airports['code'].values or route.destination not in airports['code'].values:
            raise KeyError("Source or destination airport code not found")
        if route.distance_km <= 0:
            raise ValueError("Distance must be positive")
        df = self.load_routes()
        # Prevent exact duplicate
        duplicate = df[(df['source']==route.source)&(df['destination']==route.destination)&(df['distance_km']==route.distance_km)]
        if not duplicate.empty:
            raise ValueError("Duplicate route detected")
        df = df.append({'source':route.source,'destination':route.destination,'distance_km':route.distance_km,'travel_time_min':route.travel_time_min}, ignore_index=True)
        self.save_routes(df)
        return df

    def update_route(self, index: int, distance_km: float = None, travel_time_min: float = None):
        df = self.load_routes()
        if index < 0 or index >= len(df):
            raise IndexError('Route index out of range')
        if distance_km is not None and distance_km <= 0:
            raise ValueError('distance_km must be positive')
        if distance_km is not None:
            df.at[index,'distance_km'] = float(distance_km)
        if travel_time_min is not None:
            df.at[index,'travel_time_min'] = float(travel_time_min)
        self.save_routes(df)
        return df

    def delete_route(self, index: int):
        df = self.load_routes()
        if index < 0 or index >= len(df):
            raise IndexError('Route index out of range')
        df = df.drop(df.index[index]).reset_index(drop=True)
        self.save_routes(df)
        return df
