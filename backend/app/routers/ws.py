# app/api/ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.ws_manager import ws_manager
from app.core.redis_client import redis_client
import json

router = APIRouter()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await ws_manager.connect(room_id, websocket)

    # Load initial state from Redis
    cached = await redis_client.get(f"room:{room_id}")
    if cached:
        try:
            await websocket.send_json({"type": "sync", **json.loads(cached)})
        except json.JSONDecodeError:
            pass  # Ignore corrupted cache

    try:
        while True:
            try:
                data = await websocket.receive_text()
                if not data:
                    continue  # skip empty messages
                msg = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "Invalid JSON"})
                continue

            if msg.get("type") == "code_change":
                code = msg.get("code", "")
                language = msg.get("language", "python")
                
                # Update Redis
                await redis_client.set(
                    f"room:{room_id}",
                    json.dumps({"code": code, "language": language})
                )

                # Broadcast to other clients
                await ws_manager.broadcast(room_id, msg, websocket)

    except WebSocketDisconnect:
        await ws_manager.disconnect(room_id, websocket)
