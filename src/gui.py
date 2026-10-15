"""Tkinter GUI for the Flight Route Planner.

This is a simplified but functional GUI that provides navigation to core
features: airports, routes, shortest path, visualization and analytics.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from .data_manager import DataManager
from .graph_manager import GraphManager
from .route_algorithms import build_adj_from_nx, dijkstra, find_alternative_paths
from .visualizations import draw_network
from .analytics import plot_distance_bar, plot_histogram, interactive_bar_plot, route_statistics
import threading
import webbrowser
import os

class FlightPlannerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Flight Route Planner')
        self.root.geometry('900x600')
        self.dm = DataManager()
        self._build_ui()

    def _build_ui(self):
        # Simple navigation on the left and content on the right
        self.left = ttk.Frame(self.root, width=200)
        self.left.pack(side='left', fill='y')
        self.content = ttk.Frame(self.root)
        self.content.pack(side='right', expand=True, fill='both')

        ttk.Label(self.left, text='Navigation', font=('Arial', 12, 'bold')).pack(pady=10)
        buttons = [
            ('Dashboard', self.show_dashboard),
            ('Airports', self.show_airports),
            ('Routes', self.show_routes),
            ('Shortest Route', self.show_shortest_route),
            ('Visualize Network', self.show_visualization),
            ('Analytics', self.show_analytics),
            ('Exit', self.root.quit)
        ]
        for (t, cmd) in buttons:
            b = ttk.Button(self.left, text=t, command=cmd)
            b.pack(fill='x', padx=10, pady=5)

        self.status = ttk.Label(self.root, text='Ready', relief='sunken', anchor='w')
        self.status.pack(side='bottom', fill='x')
        self.show_dashboard()

    def _set_status(self, text: str):
        self.status.config(text=text)

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def show_dashboard(self):
        self.clear_content()
        ttk.Label(self.content, text='Flight Route Planner', font=('Arial', 16, 'bold')).pack(pady=20)
        ttk.Label(self.content, text='Use the navigation buttons to manage airports, routes, compute shortest paths, visualize the network and view analytics.').pack(pady=10)

    def show_airports(self):
        self.clear_content()
        frame = ttk.Frame(self.content)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        df = self.dm.load_airports()
        cols = list(df.columns)
        tree = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=150)
        for _, r in df.iterrows():
            tree.insert('', 'end', values=list(r[c] for c in cols))
        tree.pack(expand=True, fill='both')

    def show_routes(self):
        self.clear_content()
        frame = ttk.Frame(self.content)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        df = self.dm.load_routes()
        cols = list(df.columns)
        tree = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=150)
        for _, r in df.iterrows():
            tree.insert('', 'end', values=[r.get(c,'') for c in cols])
        tree.pack(expand=True, fill='both')

    def show_shortest_route(self):
        self.clear_content()
        frame = ttk.Frame(self.content)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        airports = self.dm.load_airports()['code'].tolist()
        if not airports:
            ttk.Label(frame, text='No airports available. Add airports first.').pack()
            return
        ttk.Label(frame, text='Source:').grid(row=0, column=0, sticky='w')
        src_cb = ttk.Combobox(frame, values=airports)
        src_cb.grid(row=0, column=1, sticky='w')
        ttk.Label(frame, text='Destination:').grid(row=1, column=0, sticky='w')
        dst_cb = ttk.Combobox(frame, values=airports)
        dst_cb.grid(row=1, column=1, sticky='w')
        res_label = ttk.Label(frame, text='')
        res_label.grid(row=3, column=0, columnspan=3, sticky='w')

        def compute():
            s = src_cb.get().strip().upper()
            t = dst_cb.get().strip().upper()
            if s == '' or t == '':
                messagebox.showerror('Input error','Select both source and destination')
                return
            if s == t:
                messagebox.showinfo('Validation','Source and destination are the same')
                return
            gm = GraphManager(self.dm.load_airports(), self.dm.load_routes())
            adj = build_adj_from_nx(gm.G)
            try:
                path, dist = dijkstra(adj, s, t)
            except Exception as e:
                messagebox.showerror('Error', str(e))
                return
            res = f"Path: {' -> '.join(path)}\nTotal distance: {dist:.1f} km\nConnections: {len(path)-1}"
            res_label.config(text=res)
            # highlight network
            out = draw_network(gm.G, highlight_path=path)
            messagebox.showinfo('Result','Shortest path computed and network image saved to outputs folder')

        ttk.Button(frame, text='Compute Shortest Route', command=compute).grid(row=2, column=0, pady=10)

    def show_visualization(self):
        self.clear_content()
        frame = ttk.Frame(self.content)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        gm = GraphManager(self.dm.load_airports(), self.dm.load_routes())
        out = draw_network(gm.G)
        ttk.Label(frame, text=f'Network visualization saved to {out}').pack()

    def show_analytics(self):
        self.clear_content()
        frame = ttk.Frame(self.content)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        routes = self.dm.load_routes()
        stats = route_statistics(routes)
        if stats.get('count',0)==0:
            ttk.Label(frame, text='No route data available').pack()
            return
        ttk.Label(frame, text=f"Routes: {stats['count']}").pack()
        ttk.Label(frame, text=f"Min: {stats['min']:.1f} km, Max: {stats['max']:.1f} km, Mean: {stats['mean']:.1f} km, Median: {stats['median']:.1f} km").pack()
        bar = plot_distance_bar(routes)
        hist = plot_histogram(routes)
        ttk.Label(frame, text=f'Charts saved to outputs folder: {bar.name}, {hist.name}').pack()
        # interactive plot
        html = interactive_bar_plot(routes)
        ttk.Label(frame, text=f'Interactive chart: {html}').pack()
        ttk.Button(frame, text='Open interactive chart in browser', command=lambda: webbrowser.open('file://' + os.path.abspath(html))).pack()

    def run(self):
        self.root.mainloop()
