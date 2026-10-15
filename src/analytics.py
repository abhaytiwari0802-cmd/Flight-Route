"""Analytics functions using NumPy and Pandas, and plotting helpers."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[1] / 'outputs'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def route_statistics(routes_df: pd.DataFrame) -> dict:
    """Compute simple statistics for route distances.

    Returns a dict with min, max, mean, median and numpy array of distances.
    """
    distances = routes_df['distance_km'].replace('', np.nan).dropna().astype(float).values
    stats = {}
    if distances.size == 0:
        stats = {'count': 0}
        return stats
    arr = np.array(distances)
    stats['count'] = arr.size
    stats['min'] = float(np.min(arr))
    stats['max'] = float(np.max(arr))
    stats['mean'] = float(np.mean(arr))
    stats['median'] = float(np.median(arr))
    stats['distances'] = arr
    return stats


def plot_distance_bar(routes_df: pd.DataFrame, out: Path = OUTPUT_DIR / 'distances_bar.png') -> Path:
    df = routes_df.copy()
    df['label'] = df['source'] + '-' + df['destination']
    df = df.sort_values('distance_km')
    plt.figure(figsize=(10,6))
    plt.bar(df['label'], df['distance_km'])
    plt.xticks(rotation=90)
    plt.ylabel('Distance (km)')
    plt.title('Route distances')
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out


def plot_histogram(routes_df: pd.DataFrame, out: Path = OUTPUT_DIR / 'distances_hist.png') -> Path:
    arr = routes_df['distance_km'].dropna().astype(float).values
    plt.figure(figsize=(8,5))
    plt.hist(arr, bins=10)
    plt.xlabel('Distance (km)')
    plt.ylabel('Number of routes')
    plt.title('Distribution of route distances')
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out


def plot_scatter_distance_time(routes_df: pd.DataFrame, out: Path = OUTPUT_DIR / 'distance_time_scatter.png') -> Path:
    df = routes_df.copy()
    df = df[df['travel_time_min'] != '']
    if df.empty:
        return None
    df['distance_km'] = df['distance_km'].astype(float)
    df['travel_time_min'] = df['travel_time_min'].astype(float)
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df, x='distance_km', y='travel_time_min', hue='source')
    plt.xlabel('Distance (km)')
    plt.ylabel('Estimated travel time (min)')
    plt.title('Distance vs Travel Time')
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out


def interactive_bar_plot(routes_df: pd.DataFrame, out: Path = OUTPUT_DIR / 'distances_bar.html') -> Path:
    df = routes_df.copy()
    df['label'] = df['source'] + '-' + df['destination']
    fig = px.bar(df, x='label', y='distance_km', title='Interactive Route Distances')
    fig.write_html(out)
    return out
