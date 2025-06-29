# 📅 Event Scheduler API

A Python Flask-based REST API for managing scheduled events, including reminders, recurring events, and search functionality.

---

## 🚀 Features

- ✅ Create, read, update, and delete events (CRUD)
- ✅ Events stored persistently in `events.json`
- ⏰ Reminders for events starting within 1 hour (checked every minute)
- 🔁 Support for recurring events (daily, weekly, monthly)
- 🔎 Search events by title or description
- 🧪 Unit tests using Pytest

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```
git clone https://github.com/SRINJOY30/Event_Scheduler-api.git
cd Event_Scheduler
```
### 2. Install dependencies
```
pip install Flask pytest
```
Or, if you use a ```requirements.txt``` file:
```
pip install -r requirements.txt
```
### 3. Running the Application
```
python app.py
```
By default, the API runs on: [http://localhost:5000](http://127.0.0.1:5000)

---

## API Endpoints

| Method | Endpoint | Description |
|---|:---:|---:|
| GET | ```/``` | Check if API is running |
| GET | ```/events``` | List all events (sorted by start time) |
| POST | ```/events``` | Create a new event |
| GET | ```/events/<event-id>```  | Retrieve a specific event |
| PUT | ```/events/<event-id>```  | Update a specific event |
| DELETE | ```/events/<event-id>```  | Delete a specific event |
| GET | ```/events/search?<query>``` | Search by title or description |

---

## Example Request

### GET by ```/```
```
"message": "Event Scheduler API is running!"
```
### POST by ```/events```
![Post by events](https://github.com/SRINJOY30/Event_Schedular/blob/main/preview/POST.png)

### GET by ```/events```
![Get by events](https://github.com/SRINJOY30/Event_Schedular/blob/main/preview/GET.png)

### GET by ```/events/<event-id>```
![Get by event-id](https://github.com/SRINJOY30/Event_Schedular/blob/main/preview/GET%20by%20id.png)

### UPDATE by ```/events/<event-id>```
![Update by event-id](https://github.com/SRINJOY30/Event_Schedular/blob/main/preview/PUT.png)

### DELETE by ```/events/<event-id>```
![Delete by event-id](https://github.com/SRINJOY30/Event_Schedular/blob/main/preview/DELETE.png)

### Search by title or description
![Search by title](https://github.com/SRINJOY30/Event_Schedular/blob/main/preview/GET%20search%20by%20title.png)

---

## Result in   ```events.json```

### After POST and GET
![Post&Get](https://github.com/SRINJOY30/Event_Schedular/blob/main/preview/post%20json.png)

### After UPDATE by id
![Update by id](https://github.com/SRINJOY30/Event_Schedular/blob/main/preview/put%20json.png)

### After DELETE by id
![Delete by id](https://github.com/SRINJOY30/Event_Schedular/blob/main/preview/delete%20json.png)

### New event with POST
![New Event](https://github.com/SRINJOY30/Event_Schedular/blob/main/preview/new%20post%20json.png)

---

## ⏰ Reminders

### Snippit for Reminder
![Reminder](https://github.com/SRINJOY30/Event_Schedular/blob/main/preview/event%20reminder.png)

### Result
Every 60 seconds, the server checks and prints:
```
 Reminder: Upcoming Event - Attendance at 2025-06-30T09:00:00
```
---

## 🧪 Running Tests

Run unit tests with Pytest:
```
pytest test_app.py
```
### Output
![Result](https://github.com/SRINJOY30/Event_Schedular/blob/main/preview/pytest.png)

---

## 📁 Files

| File | Description |
|---|:---:|
| ```app.py``` | Main Flask app |
| ```events.json``` | JSON database file for events |
| ```test_app.py``` | Unit test cases using Pytest |
| ```requirements.txt``` | List of dependencies |
| ```README.md``` | Project documentation |

---

## Author
### Srinjoy Biswas
