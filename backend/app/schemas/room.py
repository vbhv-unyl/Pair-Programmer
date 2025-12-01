# app/schemas/room.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Used when creating a new room
class RoomCreate(BaseModel):
    language: Optional[str] = "python"


# Used when returning room info
class RoomResponse(BaseModel):
    room_id: str
    code: str
    language: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Used for updating code (not through websocket, but fallback)
class RoomUpdate(BaseModel):
    code: str
