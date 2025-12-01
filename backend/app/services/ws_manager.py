# app/services/ws_manager.py
from fastapi import WebSocket
from typing import Dict, List
from asyncio import Lock

class WSRoomManager:
    """
    Manages WebSocket connections per room in memory.
    Redis will store actual code/state; in-memory just handles sockets.
    """
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.locks: Dict[str, Lock] = {}

    async def connect(self, room_id: str, ws: WebSocket):
        await ws.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
            self.locks[room_id] = Lock()
        self.active_connections[room_id].append(ws)

    async def disconnect(self, room_id: str, ws: WebSocket):
        if room_id in self.active_connections:
            try:
                self.active_connections[room_id].remove(ws)
            except ValueError:
                pass  # ws was not in the list
            if len(self.active_connections[room_id]) == 0:
                del self.active_connections[room_id]
                del self.locks[room_id]

    async def broadcast(self, room_id: str, message: dict, sender: WebSocket):
        if room_id in self.active_connections:
            async with self.locks[room_id]:
                to_remove = []
                for conn in self.active_connections[room_id]:
                    if conn != sender:
                        try:
                            await conn.send_json(message)
                        except Exception:
                            # mark broken connections for removal
                            to_remove.append(conn)
                # Remove disconnected clients
                for conn in to_remove:
                    await self.disconnect(room_id, conn)

# Singleton instance
ws_manager = WSRoomManager()
