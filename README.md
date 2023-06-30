# Real-Time Chat App

This is a Real-Time Chat App built with FastAPI and MongoDB.

## Features

- User registration and login
- Authentication and authorization using JWT tokens
- WebSocket-based real-time messaging
- Storage of chat messages in a MongoDB database

## Requirements

- Python 3.9 or higher
- MongoDB

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/realtime-chat-app.git
   ```cd realtime-chat-app```

2. Create a virtual environment:
   ```python3 -m venv myenv```
   ```source myenv/bin/activate```

3. Install the dependencies:
   ```pip install -r requirements.txt```
   
4. Set up the MongoDB connection:  Make sure MongoDB is installed and running on your machine. Update the MongoDB connection URL in the app.py file:
  ```client = MongoClient("mongodb://localhost:27017/")```
  ```db = client["realtime_app"]```
  ```collection = db["realtimes"]```
  
5. Start the application:

  ```uvicorn app:app --reload```
  
6. Access the application in your browser at ```http://localhost:8000```.

  API Endpoints
  POST /register: Register a new user.
  POST /login: Authenticate and obtain an access token.
  GET /protected: Access a protected route.
  POST /token: Generate a new access token.
  GET /messages/{username}: Get chat messages between the authenticated user and the specified recipient.
  POST /messages: Send a chat message to a recipient.
  WebSocket Endpoint
  /ws/{username}: Establish a WebSocket connection for real-time messaging.
