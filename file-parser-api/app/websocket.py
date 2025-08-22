import json
import asyncio
from typing import Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.connection_info: Dict[WebSocket, Dict] = {}

    async def connect(self, websocket: WebSocket, file_id: str):
        await websocket.accept()
        if file_id not in self.active_connections:
            self.active_connections[file_id] = set()
        self.active_connections[file_id].add(websocket)
        self.connection_info[websocket] = {"file_id": file_id, "connected_at": datetime.now()}

    def disconnect(self, websocket: WebSocket, file_id: str):
        if file_id in self.active_connections:
            self.active_connections[file_id].discard(websocket)
            if not self.active_connections[file_id]:
                del self.active_connections[file_id]
        
        if websocket in self.connection_info:
            del self.connection_info[websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            self.disconnect(websocket, self.connection_info.get(websocket, {}).get("file_id", "unknown"))

    async def broadcast_progress(self, file_id: str, message: dict):
        if file_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[file_id]:
                try:
                    await connection.send_text(json.dumps({
                        "type": "progress_update",
                        "file_id": file_id,
                        "data": message,
                        "timestamp": datetime.now().isoformat()
                    }))
                except Exception:
                    disconnected.add(connection)
            
            for connection in disconnected:
                self.disconnect(connection, file_id)

    async def broadcast_file_status(self, file_id: str, message: dict):
        if file_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[file_id]:
                try:
                    await connection.send_text(json.dumps({
                        "type": "status_update",
                        "file_id": file_id,
                        "data": message,
                        "timestamp": datetime.now().isoformat()
                    }))
                except Exception:
                    disconnected.add(connection)
            
            for connection in disconnected:
                self.disconnect(connection, file_id)

    def get_connection_count(self, file_id: str) -> int:
        return len(self.active_connections.get(file_id, set()))

    def get_total_connections(self) -> int:
        return sum(len(connections) for connections in self.active_connections.values())

manager = ConnectionManager()
