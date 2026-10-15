# Flight Route Planner Using Python and Graph Algorithms

A Python-based Flight Route Planner that models airports as graph vertices and flight connections as weighted edges. The application finds the shortest-distance route between airports using Dijkstra's algorithm, while also supporting airport and route management, network visualization, data analytics, and a desktop graphical user interface.

This project is designed as a beginner-friendly academic application for a college submission. It uses Python's standard library and key syllabus topics like object-oriented programming, graph theory, CSV persistence, data analysis, and GUI programming. The sample dataset is simulated and is not connected to real-time aviation data.

---

## Abstract

The project solves a classic shortest-path problem in graph theory: given a set of airports and flight connections with distances, find the most efficient route between a source airport and a destination airport. The application also allows the user to manage airport data, maintain route records in CSV files, compare alternative routes, inspect route statistics, generate charts, and visualize the overall airport network.

---

## Problem Statement

In a transportation network, finding the best route between two locations is a common optimization problem. When airports are treated as graph nodes and flight legs as weighted edges, the path with the minimum total distance can be found using Dijkstra's algorithm.

This project demonstrates:
- Graph representation of airport networks
- Weighted shortest-path computation
- CSV-based data persistence
- Data analytics using NumPy and Pandas
- Static and interactive data visualization
- Desktop app design using Tkinter

---

## Objectives

- Represent airports and flight routes as a graph
- Find the shortest route between two airports using Dijkstra's algorithm
- Allow airport and route management through persistent CSV files
- Visualize the network connection map
- Analyze route distance data using statistics and charts
- Build a usable Tkinter desktop interface
- Keep the project beginner-friendly and suitable for viva/exam explanation

---

## Features

### Airport Management
- Add airports with unique airport codes
- View all airports
- Search airports by code, name or city
- Update airport details
- Delete airports safely while removing related routes
- Validate input and prevent duplicate airport codes

### Route Management
- Add routes between airports
- Store source, destination, distance and optional travel time
- View all available routes
- Update and delete routes
- Validate route data and distances
- Save all route changes to CSV files

### Shortest Route Finder
- Select source and destination airports
- Compute the shortest route using Dijkstra's algorithm
- View the route sequence
- View total distance in kilometers
- View number of connections
- Handle invalid input and disconnected graphs gracefully

### Alternative Route Comparison
- Identify alternative route candidates when available
- Compare route lengths
- Show that the shortest-distance route may not always be the fastest or cheapest route

### Network Visualization
- Build airport graph using NetworkX
- Display nodes and edges with distance labels
- Highlight the selected shortest route
- Save network visualizations as image files

### Analytics Dashboard
- Use NumPy for distance arrays and statistical calculations
- Use Pandas to read, filter, sort and summarize route data
- Use Matplotlib, Seaborn and Plotly to generate visual reports

### GUI
- Build a desktop application using Tkinter
- Provide navigation screens for dashboard, airports, routes, shortest-path, visualization and analytics
- Show validation messages and status updates

---

## Technology Stack

- Python 3
- Tkinter for GUI
- NetworkX for graph construction and verification
- NumPy for numerical operations
- Pandas for tabular data handling
- Matplotlib for charts and network plots
- Seaborn for statistical visualizations
- Plotly for interactive charts
- CSV files for data persistence
- pytest for automated testing

---

## Project Structure

```text
Flight-Route-Planner/
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
├── data/
│   ├── airports.csv
│   └── routes.csv
├── outputs/
│   ├── network.png
│   ├── distances_bar.png
│   ├── distances_hist.png
│   ├── distance_time_scatter.png
│   └── distances_bar.html
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── data_manager.py
│   ├── graph_manager.py
│   ├── route_algorithms.py
│   ├── analytics.py
│   ├── visualizations.py
│   └── gui.py
└── tests/
    ├── test_route_algorithms.py
    └── test_data_manager.py
