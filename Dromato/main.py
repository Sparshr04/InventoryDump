import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def create_graph_from_osm(city_name):
    print(f"Downloading map data for {city_name}...")
    graph = ox.graph_from_place(city_name, network_type='drive')
    print(f"Graph for {city_name} created!")
    return graph

def apply_dijkstra(graph, source_node, target_node):
    try:
        path = nx.shortest_path(graph, source=source_node, target=target_node, weight='length')
        path_length = nx.shortest_path_length(graph, source=source_node, target=target_node, weight='length')
        return path, path_length
    except nx.NetworkXNoPath:
        return None, None
    
def dijkstra_animation(graph, source_node, target_node):
    
    fig, ax = plt.subplots(figsize=(10, 10))
    pos = {node: (data['x'], data['y']) for node, data in graph.nodes(data=True)} 
    path, _ = apply_dijkstra(graph, source_node, target_node)
    
    x_min, x_max = min(pos[node][0] for node in pos), max(pos[node][0] for node in pos)
    y_min, y_max = min(pos[node][1] for node in pos), max(pos[node][1] for node in pos)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    
    explored_nodes = set()  
    trial_nodes = set() 
    
    def update(frame):
        ax.clear()
        ox.plot_graph(graph, ax=ax, show=False, close=False, node_size=10, edge_linewidth=0.5)
        
        if frame < len(path):
            current_node = path[frame]
            explored_nodes.add(current_node)
            
            nx.draw_networkx_nodes(graph, pos, nodelist=explored_nodes, ax=ax, node_color='red', node_size=30)
            
            subgraph = graph.subgraph(explored_nodes)
            nx.draw_networkx_edges(subgraph, pos, ax=ax, edge_color='blue', width=2)
        
        if frame < len(path):
            trial_nodes.add(path[frame])
            nx.draw_networkx_nodes(graph, pos, nodelist=trial_nodes, ax=ax, node_color='green', node_size=30, alpha=0.5)
        
        return ax

    ani = FuncAnimation(fig, update, frames=len(path), repeat=False, interval=1000)
    plt.title(f"Shortest Path from Node {source_node} to Node {target_node}")
    plt.show()

def main():
    city_name = input("Enter the city name: ")
    graph = create_graph_from_osm(city_name)

    print("Graph created. Select nodes. ")
    source_node = int(input("Enter the source node: "))
    target_node = int(input("Enter the target node: "))

    print("Calculating shortest path...")
    path, path_length = apply_dijkstra(graph, source_node, target_node)

    if path:
        print(f"Shortest path: {path}")
        print(f"Path length: {path_length} meters")
        
        print("Animating the path...")
        dijkstra_animation(graph, source_node, target_node)
    else:
        print("No path found between the specified nodes.")

if __name__ == "__main__":
    main()
