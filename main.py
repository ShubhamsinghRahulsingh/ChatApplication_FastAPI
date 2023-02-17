from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from models import manager


app = FastAPI()


templates = Jinja2Templates(directory="Templates")


@app.get("/{client_id}")
async def get(client_id: str, request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "client_id": client_id})


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    await manager.show_joining(f"{client_id} joins the chat", client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"{client_id} sends: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_left(f"{client_id} left the chat")


@app.get("/{client_id}/{receiver_id}")
async def get(request: Request, client_id: str, receiver_id: str):
    return templates.TemplateResponse("chat.html", {"request": request, "client_id": client_id, "receiver_id": receiver_id})


@app.websocket("/ws/{client_id}/{receiver_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, receiver_id: str):
    await manager.connect(websocket)
    await manager.show_joining(f"{client_id} joins the chat", client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"{client_id} send: {data}", receiver_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_left(f"{client_id} left the chat")