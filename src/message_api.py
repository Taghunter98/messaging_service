from flask import Flask, request, jsonify
import mysql.connector
import ssl
import os
from dotenv import load_dotenv

load_dotenv('/home/josh/Documents/Projects/messaging_service/src/variables.env') # File path

app = Flask(__name__) # Create app

# Load .env variables
DB_HOST = os.getenv('DB_HOST')         # Host endpoint
DB_USER = os.getenv('DB_USER')         # Username
DB_PASSWORD = os.getenv('DB_PASSWORD') # Password
DB_NAME = os.getenv('DB_NAME')         # Database name
DB_SSL_PATH = os.getenv('DB_SSL_PATH') # SSL file - required
BASE_URL = os.getenv('BASE_URL')       # Base URL for the REST API

# Connection and mySQL execution functions
def database_connection():
    connection = mysql.connector.connect (
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        ssl_ca=DB_SSL_PATH,
    )
    return connection

def mysql_error(e):
    return jsonify({"error": str(e)}), 500

# Helper method to execute cursor for POST requests
def execute_cursor(connection, script, values):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(script, (values))
    connection.commit()
    cursor.close()
    connection.close()

# Helper method to fetchall for GET requests
def execute_cursor_fetchall(cursor, script, values):
    if not isinstance(values, (list, tuple)):
        values = (values,)
    cursor.execute(script, (values))
    return cursor.fetchall()


@app.route('/users', methods=['POST'])
def create_user():
    
    # Get data
    data = request.get_json()
    name = data.get('username')
    email = data.get('email')
    password = data.get('password_hash')
    
    # Check if data
    if not name or not email or not password:
        print("You need a name, email and password to create an account.")
    
    try:
        connection = database_connection()
        
        script = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        """
        values = (name, email, password)
        
        execute_cursor(connection, script, values)
    
        return jsonify({"message": f"User {name} was created successfully."}), 201
    
    except mysql.connector.Error as e:
        return mysql_error(e)


@app.route('/messages/send', methods=['POST'])
def send_message():
    
    # Get data
    data = request.get_json()
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    
    try:
        connection = database_connection()
        message_id = f"{min(sender_id, receiver_id)}/{max(receiver_id, sender_id)}" # Chat id generation 
        
        script = """
        INSERT INTO messages (sender_id, receiver_id, message, chat_id)
        VALUES (%s, %s, %s, %s)
        """
        values = (sender_id, receiver_id, content, message_id)
        
        execute_cursor(connection, script, values)
    
        return jsonify({"message": f"Messsage {message_id} was created successfully."}), 200
    
    except mysql.connector.Error as e:
        return mysql_error(e)

@app.route('/messages/check', methods=['GET'])
def get_message():
    
    # Get user ID
    receiver_id = request.args.get('receiver_id')
    
    try:
        connection = database_connection()
        cursor = connection.cursor(dictionary=True)
        
        script = """
        SELECT * FROM messages
        WHERE receiver_id = %s AND is_read = 0;
        """
        cursor.execute(script, (receiver_id,))
        messages = cursor.fetchall()
        message_count = len(messages)
        
        # Send notification message
        if message_count == 1:
            message = f"You have {message_count} new message."
        else:
            message = f"You have {message_count} new messages."
        
        if messages:
            # Add read tag to message
            update_script = """
            UPDATE messages
            SET is_read = 1
            WHERE receiver_id = %s AND is_read = 0;
            """
            cursor.execute(update_script, (receiver_id,))
            connection.commit()
        else:
            return jsonify({"message": "You have no new messages."}), 200
              
        cursor.close()
        connection.close()
        
        return jsonify({"messages": messages, "message_count": message}), 200
    except mysql.connector.Error as e:
        return mysql_error(e)


@app.route('/messages/history', methods=['GET'])
def get_history():
    # Get data
    chat_id= request.args.get('chat_id')
    
    try:
        connection = database_connection()
        cursor = connection.cursor()
        
        script = """
        SELECT * FROM messages
        WHERE chat_id = %s;
        """
        
        cursor.execute(script, (chat_id,))
        messages = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({"messages": messages}), 200
    
    except mysql.connector.Error as e:
        return mysql_error(e)
        


# Start app
if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)