#pip install flask mysql-connector-python

from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# database config
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'database': 'your_database',
    'raise_on_warnings': True
}


# create route table
def create_table():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS routes (
            route_id INT AUTO_INCREMENT PRIMARY KEY,
            source_node_id INT,
            destination_node_id INT,
            route_nodes TEXT,
            rough_length FLOAT,
            FOREIGN KEY (source_node_id) REFERENCES nodes(node_id),
            FOREIGN KEY (destination_node_id) REFERENCES nodes(node_id)
        )
        """
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")


# query route nodes
@app.route('/routes', methods=['GET'])
def get_all_routes():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM routes")
        routes = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(routes)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# get unique route node
@app.route('/routes/<int:route_id>', methods=['GET'])
def get_route(route_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM routes WHERE route_id = %s", (route_id,))
        route = cursor.fetchone()
        cursor.close()
        conn.close()
        if route:
            return jsonify(route)
        else:
            return jsonify({"message": "Route not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# create route nodes
@app.route('/routes', methods=['POST'])
def create_route():
    data = request.get_json()
    source_node_id = data.get('source_node_id')
    destination_node_id = data.get('destination_node_id')
    route_nodes = data.get('route_nodes')
    rough_length = data.get('rough_length')
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = "INSERT INTO routes (source_node_id, destination_node_id, route_nodes, rough_length) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (source_node_id, destination_node_id, route_nodes, rough_length))
        conn.commit()
        new_route_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "Route created successfully", "route_id": new_route_id}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# update route nodes
@app.route('/routes/<int:route_id>', methods=['PUT'])
def update_route(route_id):
    data = request.get_json()
    source_node_id = data.get('source_node_id')
    destination_node_id = data.get('destination_node_id')
    route_nodes = data.get('route_nodes')
    rough_length = data.get('rough_length')
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        update_query = "UPDATE routes SET source_node_id = %s, destination_node_id = %s, route_nodes = %s, rough_length = %s WHERE route_id = %s"
        cursor.execute(update_query, (source_node_id, destination_node_id, route_nodes, rough_length, route_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Route not found"}), 404
        cursor.close()
        conn.close()
        return jsonify({"message": "Route updated successfully"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# delete route nodes
@app.route('/routes/<int:route_id>', methods=['DELETE'])
def delete_route(route_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        delete_query = "DELETE FROM routes WHERE route_id = %s"
        cursor.execute(delete_query, (route_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Route not found"}), 404
        cursor.close()
        conn.close()
        return jsonify({"message": "Route deleted successfully"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


if __name__ == '__main__':
    create_table()
    app.run(debug=True)
    
