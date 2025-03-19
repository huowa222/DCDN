#pip install redis
import redis

# Connect to Redis
def connect_redis():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("Successfully connected to the Redis server")
        return r
    except redis.exceptions.ConnectionError as e:
        print(f"Failed to connect to the Redis server: {e}")
        return None

# Add a key-value pair
def add_data(r, src_ip, dst_ip, lossrate, rtt, successrate, load, bandwidth):
    key = f"{src_ip}_{dst_ip}"
    value = f"{lossrate},{rtt},{successrate},{load},{bandwidth}"
    try:
        r.set(key, value)
        print(f"Successfully added data, key: {key}, value: {value}")
    except redis.exceptions.RedisError as e:
        print(f"An error occurred while adding data: {e}")

# Delete a key-value pair
def delete_data(r, src_ip, dst_ip):
    key = f"{src_ip}_{dst_ip}"
    try:
        result = r.delete(key)
        if result:
            print(f"Successfully deleted the key-value pair, key: {key}")
        else:
            print(f"The key {key} does not exist, no deletion operation was performed")
    except redis.exceptions.RedisError as e:
        print(f"An error occurred while deleting data: {e}")

# Modify a key-value pair
def update_data(r, src_ip, dst_ip, lossrate, rtt, successrate, load, bandwidth):
    key = f"{src_ip}_{dst_ip}"
    value = f"{lossrate},{rtt},{successrate},{load},{bandwidth}"
    try:
        if r.exists(key):
            r.set(key, value)
            print(f"Successfully updated data, key: {key}, new value: {value}")
        else:
            print(f"The key {key} does not exist, unable to perform the update operation")
    except redis.exceptions.RedisError as e:
        print(f"An error occurred while updating data: {e}")

# Query a key-value pair
def query_data(r, src_ip, dst_ip):
    key = f"{src_ip}_{dst_ip}"
    try:
        value = r.get(key)
        if value:
            value_str = value.decode('utf-8')
            lossrate, rtt, successrate, load, bandwidth = value_str.split(',')
            print(f"Query result: key: {key}, packet loss rate: {lossrate}, round-trip time: {rtt}, success rate: {successrate}, load: {load}, bandwidth: {bandwidth}")
        else:
            print(f"The key {key} does not exist, no data was found")
    except redis.exceptions.RedisError as e:
        print(f"An error occurred while querying data: {e}")


if __name__ == "__main__":
    redis_client = connect_redis()
    if redis_client:
        # Add data
        add_data(redis_client, "192.168.1.1", "192.168.1.2", 0.01, 10, 0.95, 50, 100)
        # Query data
        query_data(redis_client, "192.168.1.1", "192.168.1.2")
        # Update data
        update_data(redis_client, "192.168.1.1", "192.168.1.2", 0.02, 12, 0.93, 60, 120)
        # Query data again
        query_data(redis_client, "192.168.1.1", "192.168.1.2")
        # Delete data
        delete_data(redis_client, "192.168.1.1", "192.168.1.2")
        # Query the deleted data again
        query_data(redis_client, "192.168.1.1", "192.168.1.2")
