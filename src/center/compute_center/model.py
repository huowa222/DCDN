```python
import redis
import networkx as nx
import matplotlib.pyplot as plt

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Create a directed graph
G = nx.DiGraph()

# Get all key-value pairs from Redis
keys = r.keys()
for key in keys:
    key_str = key.decode('utf-8')
    value_str = r.get(key).decode('utf-8')
    try:
        # Parse source_node_id and destination_node_id
        source_node_id, destination_node_id = key_str.split('+')
        weight = float(value_str)
        # Add an edge to the graph
        G.add_edge(source_node_id, destination_node_id, weight=weight)
    except ValueError:
        print(f"Unable to parse key {key_str} or value {value_str}")

# Print the nodes and edges of the graph
print("Nodes of the graph:", G.nodes())
print("Edges of the graph:", G.edges(data=True))

# Draw the graph (optional)
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()
```
