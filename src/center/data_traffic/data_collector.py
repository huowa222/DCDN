# pip install pika mysql-connector-python

import pika
import json
import mysql.connector
import redis

# RabbitMQ configuration
RABBITMQ_CONFIG = {
    'host': 'localhost',
    'port': 5672,
    'username': 'guest',
    'password': 'guest',
    'queue': 'network_metrics'
}

# MySQL configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'database': 'your_mysql_database'
}

#Initialize EWMA values and minimum/maximum values
ewma_values = {
'rtt': None,
'packet_loss_rate': None,
'load': None,
'success_rate': None,
'bandwidth_watermark': None
}
min_values = {
'rtt': float('inf'),
'packet_loss_rate': float('inf'),
'load': float('inf'),
'success_rate': float('inf'),
'bandwidth_watermark': float('inf')
}
max_values = {
'rtt': float('-inf'),
'packet_loss_rate': float('-inf'),
'load': float('-inf'),
'success_rate': float('-inf'),
'bandwidth_watermark': float('-inf')
}

cursor.execute(create_table_query)
connection.commit()
except mysql.connector.Error as err:
print(f"Error setting up MySQL table: {err}")
finally:
if connection.is_connected():
cursor.close()
connection.close()
def ewma_filter(value, key):
"""
Apply EWMA filtering to the value
"""
global ewma_values
if ewma_values[key] is None:
ewma_values[key] = value
else:
ewma_values[key] = ALPHA * value + (1 - ALPHA) * ewma_values[key]
return ewma_values[key]
def normalize(value, key):
"""
Normalize the value
"""
global min_values, max_values
min_values[key] = min(min_values[key], value)
max_values[key] = max(max_values[key], value)
if max_values[key] == min_values[key]:
return 0
return (value - min_values[key]) / (max_values[key] - min_values[key])


def setup_mysql_table():
    """
    Create a MySQL table for storing network metrics (if it doesn't exist).
    """
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS network_metrics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            source_ip VARCHAR(15) NOT NULL,
            dest_ip VARCHAR(15) NOT NULL,
            packet_loss_rate FLOAT NOT NULL,
            rtt FLOAT NOT NULL,
            success_rate FLOAT NOT NULL,
            load FLOAT NOT NULL,
            bandwidth_watermark FLOAT NOT NULL
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error setting up MySQL table: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def callback(ch, method, properties, body):
    """
    Process the message received from RabbitMQ and insert the data into the MySQL database.
    """
    try:
        data = json.loads(body)
        source_ip = data.get('source_ip')
        dest_ip = data.get('dest_ip')
        packet_loss_rate = data.get('packet_loss_rate')
        rtt = data.get('rtt')
        success_rate = data.get('success_rate')
        load = data.get('load')
        bandwidth_watermark = data.get('bandwidth_watermark')

        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO network_metrics (source_ip, dest_ip, packet_loss_rate, rtt, success_rate, load, bandwidth_watermark)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (source_ip, dest_ip, packet_loss_rate, rtt, success_rate, load, bandwidth_watermark)
        cursor.execute(insert_query, values)
        connection.commit()
        print(f"Successfully inserted data for {dest_ip} into MySQL.")
    except json.JSONDecodeError as err:
        print(f"Error decoding JSON from RabbitMQ: {err}")
    except mysql.connector.Error as err:
        print(f"Error inserting data into MySQL: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Connect to the Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

def callback2(ch, method, properties, body):
    """
    Process the message received from RabbitMQ and insert the data into the redis.
    """
    try:
        data = json.loads(body)
        source_ip = data.get('source_ip')
        dest_ip = data.get('dest_ip')
        packet_loss_rate = data.get('packet_loss_rate')
        rtt = data.get('rtt')
        success_rate = data.get('success_rate')
        load = data.get('load')
        bandwidth_watermark = data.get('bandwidth_watermark')

        packet_loss_rate = ewma_values(packet_loss_rate);
        rtt = ewma_values(rtt);
        success_rate = ewma_values(success_rate);
        load = ewma_values(load);

        val = a * packet_loss_rate + b * rtt + c * success_rate + d * load
        # Create (set a key-value pair)
        key = source_ip + dest_ip
        # Assume this is the weight of the edge
        r.set(key, value)

def receive_from_rabbitmq():
    """
    Receive messages from RabbitMQ.
    """
    credentials = pika.PlainCredentials(RABBITMQ_CONFIG['username'], RABBITMQ_CONFIG['password'])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_CONFIG['host'],
            port=RABBITMQ_CONFIG['port'],
            credentials=credentials
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_CONFIG['queue'])
    channel.basic_consume(
        queue=RABBITMQ_CONFIG['queue'],
        on_message_callback=callback,
        auto_ack=True
    )
    print('Waiting for messages from RabbitMQ. To exit, press Ctrl+C')
    channel.start_consuming()


if __name__ == "__main__":
    setup_mysql_table()
    receive_from_rabbitmq()
