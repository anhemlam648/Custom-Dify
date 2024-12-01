from flask import Flask, request, jsonify
import requests
import json
from flask_cors import CORS 

app = Flask(__name__)

# Config CORS
CORS(app)

# API_URL
API_URL = "http://localhost/v1/chat-messages" 

# Token
Token = 'YourToken'

# Headers
headers = {
    'Authorization': f'Bearer {Token}', 
    'Content-Type': 'application/json',
}

@app.route('/chat-messages', methods=['POST'])
def chat_messages():
    # get Json
    data = request.json
    
    # Check data
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    # get user_input
    user_input = data.get('query', 'Hello') 

    file = request.files.get('file') 
    
    if file:
        # Save or process the file
        file.save(f"./uploads/{file.filename}")
        print(f"File saved: {file.filename}")

    # Check Input
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # get Input
    inputs = data.get('inputs', {})
    
    # get response
    response_mode = data.get('response_mode', 'blocking')
    
    # get conversation_i
    conversation_id = data.get('conversation_id', '')
    
    # get user_ID
    user = data.get('user', 'abc-123') 
    
    # get files
    files = data.get('files', [])
    
    payload = {
        "inputs": inputs, 
        "query": user_input, 
        "response_mode": response_mode,  
        "conversation_id": conversation_id,  
        "user": user, 
        "files": files  
    }

    # If there was a file, attach it to the payload or pass its info
    # if file:
    #     payload['file'] = file.filename  
    # POST to API Dify
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        
        # Check
        if response.status_code == 200:
            return jsonify(response.json())  
        else:
            return jsonify({"error": "Failed to get response from API", "status_code": response.status_code}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/chat-fileUrl', methods=['POST'])
def chat_fileUrl():
    try:
        # get data from request
        data = request.get_json()

        # Get enviroment 
        user_query = data.get('query', '') 
        files_data = data.get('files', []) 

        # Process file even get url
        image_url = None
        if files_data:
            for file_info in files_data:
                if file_info.get('transfer_method') == 'remote_url':
                    image_url = file_info.get('url')
                    print(f"Received image URL: {image_url}")
        
        # response JSON
        response = {
            'answer': f"Received your message: {user_query} and image URL: {image_url if image_url else 'None'}"
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 400
# run Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3010)
