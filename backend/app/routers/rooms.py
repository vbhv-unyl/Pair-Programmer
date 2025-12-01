# app/api/rooms.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.room import RoomCreate, RoomResponse
from app.services.room_service import RoomService
from app.core.database import get_db

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("", response_model=RoomResponse)
async def create_room(payload: RoomCreate, db: AsyncSession = Depends(get_db)):
    return await RoomService.create_room(payload, db)


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: str, db: AsyncSession = Depends(get_db)):
    room = await RoomService.get_room(room_id, db)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room
