from fastapi import FastAPI, WebSocket, Depends, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "dWd_sAxf65ED-6Yyfi6J0JnXM1tNtDmYa6rl479LlYg"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client["realtime_app"]
collection = db["realtimes"]

class User(BaseModel):
    username: str
    password_hash: str

class ChatMessage(BaseModel):
    sender: str
    recipient: str
    message: str

class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: ChatMessage):
        for connection in self.active_connections:
            await connection.send_json(message.dict())

connection_manager = WebSocketConnectionManager()


def convert_objectid_to_str(data):
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    return data

async def get_user(username: str):
    return  collection.find_one({"username": username})

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def authenticate_user(user: User, password: str):
    if not user or not verify_password(password, user.password_hash):
        return False
    else:
        return user

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")
        return User(**user)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    
async def authenticate_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")
        return User(**user)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

@app.post('/register')
async def register(username: str, password: str):
    existing_user = await get_user(username)
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already exists')
    hashed_password = password_context.hash(password)
    user = User(username=username, password_hash=hashed_password)
    collection.insert_one(user.dict())
    return {"message": "Registered successfully"}

@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user["username"]}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": "Protected route accessed successfully."}

@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user["username"]}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str, current_user: User = Depends(authenticate_token)):
    await websocket.accept()

    recipient_user = await get_user(username)
    if not recipient_user:
        raise HTTPException(status_code=404, detail="Recipient user not found.")

    while True:
        message = await websocket.receive_json()
        chat_message = ChatMessage(sender=current_user.username, recipient=username, message=message["message"])
        result = collection.insert_one(chat_message.dict())
        message_id = str(result.inserted_id)
        await websocket.send_json({"message": "Message received", "message_id": message_id})




@app.get("/messages/{username}")
async def get_chat_messages(username: str, current_user: User = Depends(authenticate_token)):
    
    if username == current_user.username:
        raise HTTPException(status_code=400, detail="Cannot retrieve messages for your own username.")
    
    
    recipient = await get_user(username)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient user not found.")
    
    messages = collection.find(
        {"$or": [
            {"sender": current_user.username, "recipient": username},
            {"sender": username, "recipient": current_user.username}
        ]}
    )
    messages = [ChatMessage(sender=msg["sender"], recipient=msg["recipient"], message=msg["message"]) for msg in messages]
    return messages

    


@app.post("/messages")
async def create_message(
    message: str,
    recipient: str,
    current_user: User = Depends(authenticate_token)
):
    recipient_user = await get_user(recipient)
    if not recipient_user:
        raise HTTPException(status_code=404, detail="Recipient user not found.")

    if current_user.username == recipient:
        raise HTTPException(status_code=400, detail="Cannot send a message to yourself.")

    chat_message = ChatMessage(sender=current_user.username, recipient=recipient, message=message)
    result = collection.insert_one(chat_message.dict())
    message_id = str(result.inserted_id)
    return {"message": "Message sent successfully", "message_id": message_id}






