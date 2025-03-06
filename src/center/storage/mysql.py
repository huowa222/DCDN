import mysql.connector

# Hypothetical MySQL configuration
MYSQL_CONFIG = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'database': 'your_database'
}


def create_tables():
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()

        # Create the nodes table
        create_nodes_table_query = """
        CREATE TABLE IF NOT EXISTS nodes (
            node_id INT AUTO_INCREMENT PRIMARY KEY,
            node_name VARCHAR(255) NOT NULL,
            node_type VARCHAR(50) NOT NULL,
            status VARCHAR(20) NOT NULL
        )
        """
        cursor.execute(create_nodes_table_query)

        # Create the links table for detection
        create_links_table_query = """
        CREATE TABLE IF NOT EXISTS links (
            link_id INT AUTO_INCREMENT PRIMARY KEY,
            source_node_id INT NOT NULL,
            destination_node_id INT NOT NULL,
            bandwidth FLOAT NOT NULL,
            packet_rtt FLOAT NOT NULL,
            packet_loss FLOAT NOT NULL,
            successrate FLOAT NOT NULL,
            workload FLOAT NOT NULL,
            FOREIGN KEY (source_node_id) REFERENCES nodes(node_id),
            FOREIGN KEY (destination_node_id) REFERENCES nodes(node_id)
        )
        """
        cursor.execute(create_links_table_query)

        # Create the shortest routes table
        create_shortest_routes_table_query = """
        CREATE TABLE IF NOT EXISTS shortest_routes (
            route_id INT AUTO_INCREMENT PRIMARY KEY,
            source_node_id INT NOT NULL,
            destination_node_id INT NOT NULL,
            route_nodes TEXT NOT NULL,
            route_length FLOAT NOT NULL,
            FOREIGN KEY (source_node_id) REFERENCES nodes(node_id),
            FOREIGN KEY (destination_node_id) REFERENCES nodes(node_id)
        )
        """
        cursor.execute(create_shortest_routes_table_query)

        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# CRUD operations for the nodes table
def add_node(node_name, node_type, status):
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        insert_query = "INSERT INTO nodes (node_name, node_type, status) VALUES (%s, %s, %s)"
        values = (node_name, node_type, status)
        cursor.execute(insert_query, values)
        connection.commit()
        print(f"Node added with ID: {cursor.lastrowid}")
    except mysql.connector.Error as err:
        print(f"Error adding node: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def delete_node(node_id):
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        delete_query = "DELETE FROM nodes WHERE node_id = %s"
        cursor.execute(delete_query, (node_id,))
        connection.commit()
        print(f"Node with ID {node_id} deleted.")
    except mysql.connector.Error as err:
        print(f"Error deleting node: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def update_node(node_id, node_name, node_type, status):
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        update_query = "UPDATE nodes SET node_name = %s, node_type = %s, status = %s WHERE node_id = %s"
        values = (node_name, node_type, status, node_id)
        cursor.execute(update_query, values)
        connection.commit()
        print(f"Node with ID {node_id} updated.")
    except mysql.connector.Error as err:
        print(f"Error updating node: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_nodes():
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        select_query = "SELECT * FROM nodes"
        cursor.execute(select_query)
        nodes = cursor.fetchall()
        for node in nodes:
            print(node)
    except mysql.connector.Error as err:
        print(f"Error getting nodes: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# CRUD operations for the links table
def add_link(source_node_id, destination_node_id, bandwidth, packet_rtt, packet_loss, successrate, workload):
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        insert_query = "INSERT INTO links (source_node_id, destination_node_id, bandwidth, packet_rtt, packet_loss, successrate, workload) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (source_node_id, destination_node_id, bandwidth, packet_rtt, packet_loss, successrate, workload)
        cursor.execute(insert_query, values)
        connection.commit()
        print(f"Link added with ID: {cursor.lastrowid}")
    except mysql.connector.Error as err:
        print(f"Error adding link: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def delete_link(link_id):
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        delete_query = "DELETE FROM links WHERE link_id = %s"
        cursor.execute(delete_query, (link_id,))
        connection.commit()
        print(f"Link with ID {link_id} deleted.")
    except mysql.connector.Error as err:
        print(f"Error deleting link: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def update_link(link_id, source_node_id, destination_node_id, bandwidth, packet_rtt, packet_loss, successrate, workload):
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        update_query = "UPDATE links SET source_node_id = %s, destination_node_id = %s, bandwidth = %s, packet_rtt = %s, packet_loss = %s, successrate = %s, workload = %s WHERE link_id = %s"
        values = (source_node_id, destination_node_id, bandwidth, packet_rtt, packet_loss, successrate, workload, link_id)
        cursor.execute(update_query, values)
        connection.commit()
        print(f"Link with ID {link_id} updated.")
    except mysql.connector.Error as err:
        print(f"Error updating link: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_links():
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        select_query = "SELECT * FROM links"
        cursor.execute(select_query)
        links = cursor.fetchall()
        for link in links:
            print(link)
    except mysql.connector.Error as err:
        print(f"Error getting links: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# CRUD operations for the shortest routes table
def add_shortest_route(source_node_id, destination_node_id, route_nodes, route_length):
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        insert_query = "INSERT INTO shortest_routes (source_node_id, destination_node_id, route_nodes, route_length) VALUES (%s, %s, %s, %s)"
        values = (source_node_id, destination_node_id, route_nodes, route_length)
        cursor.execute(insert_query, values)
        connection.commit()
        print(f"Shortest route added with ID: {cursor.lastrowid}")
    except mysql.connector.Error as err:
        print(f"Error adding shortest route: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def delete_shortest_route(route_id):
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        delete_query = "DELETE FROM shortest_routes WHERE route_id = %s"
        cursor.execute(delete_query, (route_id,))
        connection.commit()
        print(f"Shortest route with ID {route_id} deleted.")
    except mysql.connector.Error as err:
        print(f"Error deleting shortest route: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def update_shortest_route(route_id, source_node_id, destination_node_id, route_nodes, route_length):
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        update_query = "UPDATE shortest_routes SET source_node_id = %s, destination_node_id = %s, route_nodes = %s, route_length = %s WHERE route_id = %s"
        values = (source_node_id, destination_node_id, route_nodes, route_length, route_id)
        cursor.execute(update_query, values)
        connection.commit()
        print(f"Shortest route with ID {route_id} updated.")
    except mysql.connector.Error as err:
        print(f"Error updating shortest route: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_shortest_routes():
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        select_query = "SELECT * FROM shortest_routes"
        cursor.execute(select_query)
        routes = cursor.fetchall()
        for route in routes:
            print(route)
    except mysql.connector.Error as err:
        print(f"Error getting shortest routes: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Example usage
if __name__ == "__main__":
    create_tables()

    # Example of adding a node
    add_node("Node1", "L1", "Available")

    # Example of getting nodes
    get_nodes()

    # Example of adding a link
    add_link(1, 1, 100.0, 10.0, 0.01, 0.99, 50.0)

    # Example of getting links
    get_links()

    # Example of adding a shortest route
    add_shortest_route(1, 1, "Node1,Node1", 10.0)

    # Example of getting shortest routes
    get_shortest_routes()
