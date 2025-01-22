from pymongo import MongoClient
from datetime import datetime, timezone
import time

def save_to_mongo(sensor_id, message):
    try:
        print("Connecting to MongoDB...")  # Debug message
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.server_info()  # Trigger connection exception if MongoDB is not available
        print("Connected to MongoDB successfully!")  # Debug message

        db = client['home_security']
        collection = db['alerts']

        while True:
            # Prepare the data with UTC timestamp
            data = {
                "sensor_id": sensor_id,
                "message": message,
                "timestamp": datetime.now(timezone.utc)  # Get UTC time
            }

            # Insert the data into MongoDB
            result = collection.insert_one(data)
            print(f"Data inserted successfully with ID: {result.inserted_id}")

            # Fetch the latest data inserted based on timestamp
            latest_data = collection.find().sort('timestamp', -1).limit(1)
            
            # Print the latest data stored in the database
            for record in latest_data:
                print(f"Latest Data: Sensor ID: {record['sensor_id']}, Message: {record['message']}, Timestamp: {record['timestamp']}")

            # Wait for 5 seconds before the next insertion
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()  # Ensure the database connection is closed properly

# Call the function to start inserting messages every 5 seconds
save_to_mongo("sensor_01", "Intruder detected")
