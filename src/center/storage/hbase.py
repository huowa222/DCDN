#pip install happybase
import happybase
import time

# Connect to the HBase instance
connection = happybase.Connection('localhost')

# Name of the table
table_name = 'link_history'
column_family = 'cf'

# Check if the table exists, if not, create it
if table_name not in connection.tables():
    connection.create_table(
        table_name,
        {column_family: dict()}
    )

# Get the table object
table = connection.table(table_name)

# Function to add a record to the HBase table
def add_record(link_id, source_node_id, destination_node_id, bandwidth, packet_rtt, packet_loss, successrate, workload):
    # Generate a unique row key (using timestamp and link_id)
    row_key = f"{int(time.time() * 1000)}_{link_id}"
    data = {
        f"{column_family}:link_id": str(link_id),
        f"{column_family}:source_node_id": str(source_node_id),
        f"{column_family}:destination_node_id": str(destination_node_id),
        f"{column_family}:bandwidth": str(bandwidth),
        f"{column_family}:packet_rtt": str(packet_rtt),
        f"{column_family}:packet_loss": str(packet_loss),
        f"{column_family}:successrate": str(successrate),
        f"{column_family}:workload": str(workload)
    }
    # Put the data into the table
    table.put(row_key, data)


# Simulate frequently adding historical records
for i in range(10):
    link_id = f"link_{i}"
    source_node_id = f"source_{i}"
    destination_node_id = f"destination_{i}"
    bandwidth = 100 + i
    packet_rtt = 10 + i
    packet_loss = 0.01 + i
    successrate = 0.9 + i
    workload = 50 + i

    add_record(link_id, source_node_id, destination_node_id, bandwidth, packet_rtt, packet_loss, successrate, workload)
    print(f"Record {i} added successfully.")


# Close the connection
connection.close()
