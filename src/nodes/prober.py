import time
import psutil
import pika
from scapy.all import sr1, IP, ICMP
import json


# Configure message queue connection information
MQ_CONFIG = {
    'host': 'localhost',
    'port': 5672,
    'username': 'guest',
    'password': 'guest',
    'queue': 'network_metrics'
}

# List of target nodes
TARGET_NODES = ['192.168.1.100', '192.168.1.101']

# Probe parameters
PACKET_COUNT = 10
TIMEOUT = 1


def calculate_network_metrics(target):
    """
    Calculate network metrics (packet loss rate, success rate, RTT) for the target node.
    :param target: The IP address of the target node.
    :return: A dictionary containing packet loss rate, success rate, and average RTT.
    """
    sent_packets = 0
    received_packets = 0
    total_rtt = 0

    for _ in range(PACKET_COUNT):
        sent_packets += 1
        start_time = time.time()
        packet = IP(dst=target) / ICMP()
        reply = sr1(packet, timeout=TIMEOUT, verbose=0)
        if reply:
            received_packets += 1
            end_time = time.time()
            rtt = end_time - start_time
            total_rtt += rtt

    # Calculate packet loss rate
    packet_loss_rate = (sent_packets - received_packets) / sent_packets if sent_packets > 0 else 0

    # Calculate success rate
    success_rate = received_packets / sent_packets if sent_packets > 0 else 0

    # Calculate average RTT
    average_rtt = total_rtt / received_packets if received_packets > 0 else 0

    return {
        'packet_loss_rate': packet_loss_rate,
        'success_rate': success_rate,
        'average_rtt': average_rtt
    }


def get_machine_load():
    """
    Get the load information (CPU usage and memory usage) of the local machine.
    :return: A dictionary containing CPU usage and memory usage.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    return {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage
    }


def upload_to_message_queue(data):
    """
    Upload data to the message queue.
    :param data: The data dictionary to be uploaded.
    """
    credentials = pika.PlainCredentials(MQ_CONFIG['username'], MQ_CONFIG['password'])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=MQ_CONFIG['host'], port=MQ_CONFIG['port'], credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=MQ_CONFIG['queue'])
    message = json.dumps(data)
    channel.basic_publish(exchange='', routing_key=MQ_CONFIG['queue'], body=message)
    print(f" [x] Sent {message} to message queue")
    connection.close()


if __name__ == "__main__":
    machine_load = get_machine_load()
    for target in TARGET_NODES:
        network_metrics = calculate_network_metrics(target)
        combined_data = {
            'target': target,
            **network_metrics,
            **machine_load
        }
        upload_to_message_queue(combined_data)

```
