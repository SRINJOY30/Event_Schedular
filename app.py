from flask import Flask, jsonify, request
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'events.json'

# ---------- Utility Functions ----------

def load_events():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_events(events):
    with open(DATA_FILE, 'w') as f:
        json.dump(events, f, indent=2)

def get_event(event_id):
    events = load_events()
    for event in events:
        if event['id'] == event_id:
            return event
    return None

# ---------- Routes ----------

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Event Scheduler API is running!"})

# Create event
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    required = ['title', 'description', 'start_time', 'end_time']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        datetime.fromisoformat(data['start_time'])
        datetime.fromisoformat(data['end_time'])
    except ValueError:
        return jsonify({'error': 'Invalid datetime format (use ISO e.g. 2025-06-28T19:00:00)'}), 400

    new_event = {
        "id": str(uuid.uuid4()),
        "title": data['title'],
        "description": data['description'],
        "start_time": data['start_time'],
        "end_time": data['end_time']
    }
    events = load_events()
    events.append(new_event)
    save_events(events)
    return jsonify(new_event), 201

# Get all events (sorted by start_time)
@app.route('/events', methods=['GET'])
def get_events():
    events = load_events()
    events.sort(key=lambda x: x['start_time'])
    return jsonify(events)

# Get single event
@app.route('/events/<event_id>', methods=['GET'])
def get_single_event(event_id):
    event = get_event(event_id)
    if event:
        return jsonify(event)
    return jsonify({'error': 'Event not found'}), 404

# Update event
@app.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    events = load_events()
    event = get_event(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    data = request.get_json()
    for key in ['title', 'description', 'start_time', 'end_time']:
        if key in data:
            event[key] = data[key]

    for i, e in enumerate(events):
        if e['id'] == event_id:
            events[i] = event
            break

    save_events(events)
    return jsonify(event)

# Delete event
@app.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    events = load_events()
    new_events = [e for e in events if e['id'] != event_id]
    if len(events) == len(new_events):
        return jsonify({'error': 'Event not found'}), 404
    save_events(new_events)
    return jsonify({'message': 'Event deleted successfully'}), 200

# ---------- Run ----------
if __name__ == '__main__':
    app.run(debug=True)
