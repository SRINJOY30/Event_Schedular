from flask import Flask, jsonify, request
import json
import os
import uuid
from datetime import datetime, timedelta
import threading
import time

# Event Scheduler API
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

def is_due_within_one_hour(start_time):
    try:
        event_time = datetime.fromisoformat(start_time)
        now = datetime.now()
        return now <= event_time <= now + timedelta(hours=1)
    except:
        return False

def expand_recurring_events(events):
    expanded = []
    now = datetime.now()
    for event in events:
        recurring = event.get('recurring')
        if not recurring:
            expanded.append(event)
            continue

        try:
            base_time = datetime.fromisoformat(event['start_time'])
            end_time = datetime.fromisoformat(event['end_time'])
            for i in range(10):  # generate next 10 recurrences
                delta = {
                    'daily': timedelta(days=1),
                    'weekly': timedelta(weeks=1),
                    'monthly': timedelta(days=30)  # rough estimate
                }.get(recurring, timedelta(days=0))
                base_time += delta
                end_time += delta
                new_event = event.copy()
                new_event['id'] = str(uuid.uuid4())
                new_event['start_time'] = base_time.isoformat()
                new_event['end_time'] = end_time.isoformat()
                expanded.append(new_event)
        except:
            expanded.append(event)
    return expanded

# ---------- Reminders Background Thread ----------
def check_reminders():
    while True:
        events = load_events()
        for event in events:
            if is_due_within_one_hour(event['start_time']):
                print(f"⏰ Reminder: Upcoming Event - {event['title']} at {event['start_time']}")
        time.sleep(60)

reminder_thread = threading.Thread(target=check_reminders, daemon=True)
reminder_thread.start()

# ---------- Routes ----------

@app.route('/')
def home():
    return jsonify({"message": "Event Scheduler API is running!"})

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
        return jsonify({'error': 'Invalid datetime format (use ISO format)'}), 400

    new_event = {
        "id": str(uuid.uuid4()),
        "title": data['title'],
        "description": data['description'],
        "start_time": data['start_time'],
        "end_time": data['end_time'],
        "recurring": data.get('recurring')  # daily, weekly, monthly or None
    }
    events = load_events()
    events.append(new_event)
    save_events(events)
    return jsonify(new_event), 201

@app.route('/events', methods=['GET'])
def get_events():
    events = load_events()
    all_events = events + expand_recurring_events(events)
    all_events.sort(key=lambda x: x['start_time'])
    return jsonify(all_events)

@app.route('/events/<event_id>', methods=['GET'])
def get_single_event(event_id):
    event = get_event(event_id)
    if event:
        return jsonify(event)
    return jsonify({'error': 'Event not found'}), 404

@app.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    events = load_events()
    event = get_event(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    data = request.get_json()
    for key in ['title', 'description', 'start_time', 'end_time', 'recurring']:
        if key in data:
            event[key] = data[key]

    for i, e in enumerate(events):
        if e['id'] == event_id:
            events[i] = event
            break

    save_events(events)
    return jsonify(event)

@app.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    events = load_events()
    new_events = [e for e in events if e['id'] != event_id]
    if len(events) == len(new_events):
        return jsonify({'error': 'Event not found'}), 404
    save_events(new_events)
    return jsonify({'message': 'Event deleted successfully'})

@app.route('/events/search', methods=['GET'])
def search_events():
    query = request.args.get('q', '').lower()
    results = [e for e in load_events()
               if query in e['title'].lower() or query in e['description'].lower()]
    return jsonify(results)

# ---------- Run ----------
if __name__ == '__main__':
    app.run(debug=True)
