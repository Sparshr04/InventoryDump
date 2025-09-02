import osmnx as ox
import folium

city_name = input("Enter location: ")
graph = ox.graph_from_place(city_name, network_type='drive')

nodes, edges = ox.graph_to_gdfs(graph)

# Create a map centered on the city
city_center = nodes[['y', 'x']].mean()
m = folium.Map(location=[city_center['y'], city_center['x']], zoom_start=12)

for _, row in nodes.iterrows():
    folium.CircleMarker(
        location=(row['y'], row['x']),
        radius=2,
        popup=f"Node ID: {row.name}",
        color='blue',
    ).add_to(m)

m.save("map.html")
print("Hell Yeah! Saving Successful...")
