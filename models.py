from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, receiver_id: str | None = None):
        if receiver_id:
            for connection in self.active_connections:
                x = str(connection.url).split("ws/")[1]
                if x.split("/")[0] == receiver_id:
                    await connection.send_text(message)
        else:
            for connection in self.active_connections:
                await connection.send_text(message)


manager = ConnectionManager()

