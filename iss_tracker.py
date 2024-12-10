import requests
import redis
import json
import time
from datetime import datetime

# CONFIG
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
API_URL = 'http://api.open-notify.org/iss-now.json'
POLL_INTERVAL = 5  

def connect_to_redis():
    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True  
        )
        client.ping()  
        return client
    except redis.ConnectionError as e:
        print(f"ERROR - Could not connect to Redis: {e}")
        return None

def get_iss_position():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"ERROR - fetching ISS data: {e}")
        return None

def get_stored_position(redis_client):
    try:
        data = redis_client.get('iss_position')
        return json.loads(data) if data else None
    except redis.RedisError as e:
        print(f"ERROR - retrieving data: {e}")
        return None

def store_position(redis_client, position_data):
    try:
        position_data['timestamp'] = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
        
        # SET operation
        redis_client.set('iss_position', json.dumps(position_data))
        print("\nSUCCESS - Stored new position in Redis")
        
        # GET operation
        stored_data = get_stored_position(redis_client)
        if stored_data:
            print("\nSUCCESS - Verified data in Redis:")
            print(json.dumps(stored_data, indent=2))
        return True
        
    except redis.RedisError as e:
        print(f"ERROR - storing data: {e}")
        return False

def main():
    # Connect to Redis
    redis_client = connect_to_redis()
    if not redis_client:
        return

    print(f"Starting ISS position tracking (every {POLL_INTERVAL} seconds)")
    print("Press Ctrl+C to stop...")

    try:
        updates = 0
        while True:
            position = get_iss_position()
            if position:
                store_position(redis_client, position)
                updates += 1
                print(f"Total updates: {updates}")
            
            print(f"\nWaiting {POLL_INTERVAL} seconds...")
            time.sleep(POLL_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nStopping ISS tracker...")

if __name__ == "__main__":
    main()