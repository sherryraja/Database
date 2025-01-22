from datetime import datetime
from neo4j import GraphDatabase

# Example data to store
sensor_id = "sensor_01"
message = "Temperature exceeded threshold"
timestamp = datetime.now().isoformat()

# Function to store or update the latest data in Neo4j
def save_to_neo4j(sensor_id, message, timestamp):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))  # Check password

    with driver.session() as session:
        query = """
        MERGE (a:Alert {sensor_id: $sensor_id})
        SET a.message = $message, a.timestamp = $timestamp
        RETURN a
        """
        result = session.run(query, sensor_id=sensor_id, message=message, timestamp=timestamp)
        
        if result.single():
            print(f"Data for sensor '{sensor_id}' updated successfully.")
        else:
            print(f"Data for sensor '{sensor_id}' stored successfully.")

    driver.close()

# Call the function to store the latest alert data
save_to_neo4j(sensor_id, message, timestamp)
