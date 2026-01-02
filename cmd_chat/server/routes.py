from sanic import Sanic, Request, Websocket

from . import views


def register_routes(app: Sanic) -> None:
    @app.route("/get_key", methods=["GET", "POST"])
    async def get_key_route(request: Request):
        return await views.get_key(request, app)

    @app.websocket("/ws/chat")
    async def chat_ws_route(request: Request, ws: Websocket):
        await views.chat_ws(request, ws, app)

    @app.get("/health")
    async def health_route(request: Request):
        return await views.health(request, app)

    @app.delete("/clear")
    async def clear_route(request: Request):
        return await views.clear_messages(request, app)
