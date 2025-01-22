import mysql.connector
import time
from datetime import datetime
from random import choice, randint

def save_to_mysql(sensor_id, message, timestamp):
    try:
        # If timestamp is a string, convert it to a datetime object
        if isinstance(timestamp, str):
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        
        # Connect to MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  # Adjust if you use different credentials
            database="home_security"
        )
        
        cursor = conn.cursor()

        # Query to insert data into the alerts table
        query = "INSERT INTO alerts (sensor_id, message, timestamp) VALUES (%s, %s, %s)"
        
        # Execute the query with the data
        cursor.execute(query, (sensor_id, message, timestamp))
        
        # Commit the transaction to the database
        conn.commit()
        
        print(f"Data inserted: {sensor_id}, {message}, {timestamp}")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        # Ensure the connection is closed even if an error occurs
        if conn.is_connected():
            conn.close()


# Simulated sensor data
def generate_sensor_data():
    sensor_ids = [f"sensor_{i}" for i in range(1, 6)]
    messages = ["Intrusion detected", "Smoke detected", "Gas leak detected"]
    
    return {
        "sensor_id": choice(sensor_ids),
        "message": choice(messages),
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


# Periodically store data every 5 seconds
def main():
    print("Starting data insertion every 5 seconds...")

    while True:
        data = generate_sensor_data()
        save_to_mysql(data["sensor_id"], data["message"], data["timestamp"])
        
        # Wait for 5 seconds before next insertion
        time.sleep(5)


if __name__ == "__main__":
    main()
