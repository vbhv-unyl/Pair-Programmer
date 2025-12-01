# app/services/room_service.py
import uuid
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.room import Room
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate
from app.core.redis_client import redis_client


class RoomService:

    @staticmethod
    async def create_room(payload: RoomCreate, db: AsyncSession) -> RoomResponse:
        room_id = str(uuid.uuid4())[:8]

        new_room = Room(
            id=room_id,
            code="",
            language=payload.language
        )

        db.add(new_room)
        await db.commit()
        await db.refresh(new_room)

        # store in redis
        await redis_client.set(
            f"room:{room_id}",
            json.dumps({"code": "", "language": payload.language})
        )

        return RoomResponse(
            room_id=room_id,
            code="",
            language=payload.language,
            created_at=new_room.created_at,
            updated_at=new_room.updated_at
        )

    @staticmethod
    async def get_room(room_id: str, db: AsyncSession):
        # try redis
        cached = await redis_client.get(f"room:{room_id}")

        if cached:
            cached_data = json.loads(cached)

            # fetch timestamps from DB
            result = await db.execute(select(Room).where(Room.id == room_id))
            db_room = result.scalars().first()
            if not db_room:
                return None

            return RoomResponse(
                room_id=room_id,
                code=cached_data["code"],
                language=cached_data["language"],
                created_at=db_room.created_at,
                updated_at=db_room.updated_at
            )

        # fallback: database
        result = await db.execute(select(Room).where(Room.id == room_id))
        room = result.scalars().first()

        if not room:
            return None

        await redis_client.set(
            f"room:{room_id}",
            json.dumps({"code": room.code, "language": room.language})
        )

        return RoomResponse(
            room_id=room.id,
            code=room.code,
            language=room.language,
            created_at=room.created_at,
            updated_at=room.updated_at
        )
