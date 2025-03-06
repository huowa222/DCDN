import heapq

# This function implements Dijkstra's algorithm to find the shortest path and its distance from the start node to the end node in a graph.
def dijkstra(graph, start, end):
    # Initialize a dictionary to store the distance from each node to the start node, with the initial value set to infinity.
    distances = {node: float('inf') for node in graph}
    # Set the distance from the start node to itself to 0.
    distances[start] = 0
    # Initialize a priority queue to store the nodes to be explored and their distances to the start node, with the initial value being (0, start node).
    priority_queue = [(0, start)]
    # Initialize a dictionary to store the previous node of each node, with the initial value set to None.
    previous_nodes = {node: None for node in graph}

    # When the priority queue is not empty, perform the following operations in a loop.
    while priority_queue:
        # Pop the node closest to the start node and its distance from the priority queue.
        current_distance, current_node = heapq.heappop(priority_queue)

        # If the current node is the end node, construct the path and return the path and the shortest distance.
        if current_node == end:
            route = []
            while current_node is not None:
                route.append(current_node)
                current_node = previous_nodes[current_node]
            route.reverse()
            return route, distances[end]

        # If the currently popped distance is greater than the recorded distance from this node to the start node, skip this loop.
        if current_distance > distances[current_node]:
            continue

        # Traverse all the neighbor nodes of the current node and the weights of their edges.
        for neighbor, weight in graph[current_node].items():
            # Calculate the distance from the start node to the neighbor node via the current node.
            distance = current_distance + weight

            # If the calculated distance is less than the recorded distance from the neighbor node to the start node, update the distance and the previous node, and add the neighbor node to the priority queue.
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # If no path is found, return None and an infinite distance.
    return None, float('inf')
