import paho.mqtt.client as mqtt
import json
import time
from random import choice, randint

# Connect to the broker
client = mqtt.Client()
client.connect("localhost", 1883, 60)

# Topics for simulation
topics = ["home/security/intrusion", "home/security/fire", "home/security/gas"]

while True:
    # Simulated sensor data
    data = {
        "sensor_id": f"sensor_{randint(1, 10)}",
        "message": choice(["Intrusion detected", "Smoke detected", "Gas leak detected"]),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    # Publish data to a random topic
    client.publish(choice(topics), json.dumps(data))
    print(f"Published: {data}")
    time.sleep(5)
