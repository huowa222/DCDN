```python
#
#shortestpathofthecurrenthopthroughtheresultoftheprevioushop k − 1 : • d p [ k ][ i ] = min (dp[ k − 1][ i ], min (dp[ k − 1][ j ] + adj[ j ][ i ])) 
#

import sys
import redis


def shortest_path_redis(redis_client, num_nodes, max_hops, start_node=0):
    # Initialize the dp array, where dp[k][i] represents the shortest path to reach node i with at most k hops.
    dp = [[sys.maxsize for _ in range(num_nodes)] for _ in range(max_hops + 1)]
    # The distance from the starting node to itself with 0 hops is 0.
    dp[0][start_node] = 0

    for k in range(1, max_hops + 1):
        for i in range(num_nodes):
            # The case without taking the k-th hop.
            dp[k][i] = dp[k - 1][i]
            for j in range(num_nodes):
                key = f"{j}{i}"
                weight_str = redis_client.get(key)
                if weight_str is not None:
                    weight = float(weight_str)
                    # The case of taking the k-th hop.
                    dp[k][i] = min(dp[k][i], dp[k - 1][j] + weight)

    shortest_paths = []
    for i in range(num_nodes):
        shortest_paths.append(min([dp[k][i] for k in range(max_hops + 1)]))
    return shortest_paths


# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
# Assume the number of nodes
num_nodes = 5
# Maximum number of hops
max_hops = 3
# Calculate the shortest paths
result = shortest_path_redis(redis_client, num_nodes, max_hops)
print("Shortest paths to each node:", result)

```
