import requests
import json
import argparse
import os
from dotenv import load_dotenv

# Connect to REST API
load_dotenv('/home/josh/Documents/Projects/messaging_service/src/variables.env')
API_BASE_URL = os.getenv('BASE_URL')

def fetch_messages(receiver_id):
    url = f"{API_BASE_URL}/messages/check"
    payload = {"receiver_id": receiver_id}
    
    try:
        response = requests.get(url, params = payload)
        response.raise_for_status() # Raise exception for HTTP
        data = response.json()
        print(json.dumps(data, indent = 4))
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching messages: {e}")
        return None
    
def send_message(sender_id, receiver_id, content):
    url = f"{API_BASE_URL}/messages/send"
    
    response = requests.post(url, json={
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "content": content
    })
        
    if response.status_code == 200:
            print("Message sent successfully.")
    else:
        try:
            print(f"Failed to send: {response.json()}")
        except ValueError:
            print("Response is not in JSON format.")

def get_chat_history(chat_id):
    url = f"{API_BASE_URL}/messages/history"
    
    payload = {"chat_id": chat_id}
    
    try:
        response = requests.get(url, params = payload)
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent = 4))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching chat history: {e}")
        return None
    
if __name__ == '__main__':
    # CLI argument parser
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--get", type=int, nargs=1, help="Get all messages with <user_id>")
    parser.add_argument("--send", nargs=3, help="Send a message from <sender_id> to <reciever_id> and <content>")
    parser.add_argument("--chat", type=str, nargs=1, help="Get chat history for <chat_id>")
    args = parser.parse_args() # Parse arguments
    
    
    # Arguments
    if args.get:
        receiver_id = args.get[0]
        print(f"Fetching messages for receiver_id: {receiver_id}...")
        messages = fetch_messages(receiver_id)
        
    elif args.send:
        sender_id = int(args.send[0])
        receiver_id = int(args.send[1])
        content = args.send[2]
        print(f"Sending message from sender_id: {sender_id} to receiver_id: {receiver_id} with content: {content}...")
        send_message(sender_id, receiver_id, content)
        
    elif args.chat:
        chat_id = args.chat[0]
        print(f"Fetching chat history for id: {chat_id}...")
        get_chat_history(chat_id)
