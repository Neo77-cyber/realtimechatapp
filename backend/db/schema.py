from pydantic import BaseModel




class Message(BaseModel):
    user: int
    body: str
    