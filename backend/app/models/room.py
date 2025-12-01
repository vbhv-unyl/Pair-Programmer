# app/models/room.py
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True, index=True)
    code = Column(Text, default="", nullable=False)
    language = Column(String, default="python", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
