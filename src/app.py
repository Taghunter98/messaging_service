import requests
import json
import argparse
import os
from dotenv import load_dotenv

# Connect to REST API
load_dotenv('/home/josh/Documents/Projects/blog_rest_api/db/db_config.env')
API_BASE_URL = os.getenv('BASE_URL')

def fetch_messages(receiver_id):
    url = f"{API_BASE_URL}/messages/check"
    payload = {"receiver_id": receiver_id}
    
    try:
        response = requests.get(url, params=payload)
        response.raise_for_status() # Raise exception for HTTP
        data = response.json()
        for message in data:
            print(f"\t\n\nMessage from: {data.get('sender_id')}at {data.get('timestamp')}\nMessage: {data.get('message')}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching messages: {e}")
        return None
    
if __name__ == '__main__':
    receiver_id = 1
    messages = fetch_messages(receiver_id)
    print(messages)
