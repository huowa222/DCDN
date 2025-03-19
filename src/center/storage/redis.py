#pip install redis
import redis

# 连接到 Redis
def connect_redis():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("成功连接到 Redis 服务器")
        return r
    except redis.exceptions.ConnectionError as e:
        print(f"连接 Redis 服务器失败: {e}")
        return None

# 添加键值对
def add_data(r, src_ip, dst_ip, lossrate, rtt, successrate, load, bandwidth):
    key = f"{src_ip}_{dst_ip}"
    value = f"{lossrate},{rtt},{successrate},{load},{bandwidth}"
    try:
        r.set(key, value)
        print(f"成功添加数据，键: {key}，值: {value}")
    except redis.exceptions.RedisError as e:
        print(f"添加数据时出错: {e}")

# 删除键值对
def delete_data(r, src_ip, dst_ip):
    key = f"{src_ip}_{dst_ip}"
    try:
        result = r.delete(key)
        if result:
            print(f"成功删除键值对，键: {key}")
        else:
            print(f"键 {key} 不存在，未进行删除操作")
    except redis.exceptions.RedisError as e:
        print(f"删除数据时出错: {e}")

# 修改键值对
def update_data(r, src_ip, dst_ip, lossrate, rtt, successrate, load, bandwidth):
    key = f"{src_ip}_{dst_ip}"
    value = f"{lossrate},{rtt},{successrate},{load},{bandwidth}"
    try:
        if r.exists(key):
            r.set(key, value)
            print(f"成功更新数据，键: {key}，新值: {value}")
        else:
            print(f"键 {key} 不存在，无法进行更新操作")
    except redis.exceptions.RedisError as e:
        print(f"更新数据时出错: {e}")

# 查询键值对
def query_data(r, src_ip, dst_ip):
    key = f"{src_ip}_{dst_ip}"
    try:
        value = r.get(key)
        if value:
            value_str = value.decode('utf-8')
            lossrate, rtt, successrate, load, bandwidth = value_str.split(',')
            print(f"查询结果：键: {key}，丢包率: {lossrate}，往返时间: {rtt}，成功率: {successrate}，负载: {load}，带宽: {bandwidth}")
        else:
            print(f"键 {key} 不存在，未查询到数据")
    except redis.exceptions.RedisError as e:
        print(f"查询数据时出错: {e}")


if __name__ == "__main__":
    redis_client = connect_redis()
    if redis_client:
        # 添加数据
        add_data(redis_client, "192.168.1.1", "192.168.1.2", 0.01, 10, 0.95, 50, 100)
        # 查询数据
        query_data(redis_client, "192.168.1.1", "192.168.1.2")
        # 更新数据
        update_data(redis_client, "192.168.1.1", "192.168.1.2", 0.02, 12, 0.93, 60, 120)
        # 再次查询数据
        query_data(redis_client, "192.168.1.1", "192.168.1.2")
        # 删除数据
        delete_data(redis_client, "192.168.1.1", "192.168.1.2")
        # 再次查询已删除的数据
        query_data(redis_client, "192.168.1.1", "192.168.1.2")
