import paho.mqtt.client as mqtt
import json
from mysql_handler import save_to_mysql  # Import MySQL handler
from mongodb_handler import save_to_mongo  # Import MongoDB handler
from neo4j_handler import save_to_neo4j  # Import Neo4j handler

# This function will be called when a message is received from the MQTT broker
def on_message(client, userdata, msg):
    # Print the received message
    print(f"Received `{msg.payload.decode()}` on topic `{msg.topic}`")

    # Parse the incoming JSON message
    try:
        data = json.loads(msg.payload.decode())
    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")
        return  # If the message is not valid JSON, skip it

    # Extract data from the parsed JSON
    sensor_id = data.get('sensor_id')
    message = data.get('message')
    timestamp = data.get('timestamp')

    # Ensure all required data is present
    if not all([sensor_id, message, timestamp]):
        print("Incomplete message data. Skipping insert.")
        return

    # Save the data to MySQL
    try:
        save_to_mysql(sensor_id, message, timestamp)
    except Exception as e:
        print(f"Error saving to MySQL: {e}")

    # Save the data to MongoDB
    try:
        save_to_mongo(sensor_id, message, timestamp)
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")

    # Save the data to Neo4j
    try:
        save_to_neo4j(sensor_id, message, timestamp)
    except Exception as e:
        print(f"Error saving to Neo4j: {e}")

# Set up the MQTT client
client = mqtt.Client()

# Assign the message callback function
client.on_message = on_message

# Connect to the MQTT broker
try:
    client.connect("localhost", 1883, 60)
except Exception as e:
    print(f"Error connecting to MQTT broker: {e}")
    exit(1)  # Exit if connection fails

# Subscribe to all security topics
client.subscribe("home/security/#")

# Start the loop to process incoming messages
client.loop_forever()
