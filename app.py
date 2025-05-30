from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
db = client['github_events']
collection = db['events']

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    # Extract the relevant information from the webhook payload
    event_type = request.headers.get('X-GitHub-Event')
    
    if event_type in ['push', 'pull_request']:
        event_data = {
            'request_id': request.headers.get('X-GitHub-Delivery'),
            'timestamp': datetime.utcnow().isoformat(),
            'author': data['sender']['login'] if 'sender' in data else None
        }
        
        if event_type == 'push':
            event_data['action'] = 'PUSH'
            event_data['to_branch'] = data['ref'].split('/')[-1]
            event_data['from_branch'] = None
            
        elif event_type == 'pull_request':
            action = data['action']
            if action == 'opened':
                event_data['action'] = 'PULL_REQUEST'
            elif action == 'closed' and data['pull_request']['merged']:
                event_data['action'] = 'MERGE'
            else:
                return jsonify({'status': 'ignored'}), 200
                
            event_data['from_branch'] = data['pull_request']['head']['ref']
            event_data['to_branch'] = data['pull_request']['base']['ref']
        
        # Store in MongoDB
        collection.insert_one(event_data)
        return jsonify({'status': 'success'}), 200
    
    return jsonify({'status': 'ignored'}), 200

@app.route('/events', methods=['GET'])
def get_events():
    # Get the latest events from MongoDB
    events = list(collection.find({}, {'_id': 0}).sort('timestamp', -1).limit(10))
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 