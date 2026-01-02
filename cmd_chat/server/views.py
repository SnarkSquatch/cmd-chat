from dataclasses import asdict
from uuid import uuid4
import json

import rsa
from sanic import Sanic, Request, response, Websocket
from sanic.response import HTTPResponse, json as json_response

from .models import Message, UserSession
from .logger import logger
from .helpers import (
    require_auth,
    extract_pubkey,
    get_client_ip,
    get_param,
    verify_password,
    send_state,
    utcnow,
)


async def get_key(request: Request, app: Sanic) -> HTTPResponse:
    if err := require_auth(request, app):
        return err

    pubkey_bytes = extract_pubkey(request)
    if not pubkey_bytes:
        return response.text("Bad request: pubkey is required", status=400)

    try:
        public_key = rsa.PublicKey.load_pkcs1(pubkey_bytes)
        if public_key.n.bit_length() < 2048:
            raise ValueError("RSA key must be at least 2048 bits")
    except Exception as e:
        logger.warning(f"Invalid public key: {e}")
        return response.text(f"Bad pubkey: {e}", status=400)

    username = get_param(request, "username") or "unknown"

    if await app.ctx.session_store.username_exists(username):
        return response.text(f"Username '{username}' is already taken", status=409)

    session = UserSession(
        user_id=str(uuid4()),
        ip=get_client_ip(request),
        username=get_param(request, "username") or "unknown",
        fernet_key=app.ctx.fernet_key,
    )
    await app.ctx.session_store.add(session)

    try:
        encrypted_key = rsa.encrypt(app.ctx.fernet_key, public_key)
        logger.info(f"Key exchange: user={session.username}, session={session.user_id}")

        return response.raw(
            encrypted_key,
            content_type="application/octet-stream",
            headers={"X-User-Id": session.user_id},
        )
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        return response.text("Key encryption failed", status=500)


async def chat_ws(request: Request, ws: Websocket, app: Sanic) -> None:
    user_id = request.args.get("user_id")

    if not user_id:
        await ws.close(code=4002, reason="user_id required")
        return

    if not verify_password(request.args.get("password"), app.ctx.admin_password):
        await ws.close(code=4001, reason="Unauthorized")
        return

    session = await app.ctx.session_store.get(user_id)
    if not session:
        await ws.close(code=4002, reason="Invalid session")
        return

    manager = app.ctx.connection_manager
    await manager.connect(user_id, ws)

    try:
        await send_state(ws, app)

        async for data in ws:
            if data is None:
                break

            await app.ctx.session_store.update_activity(user_id)

            message = Message(
                text=str(data),
                user_ip=session.ip,
                username=session.username,
            )
            await app.ctx.message_store.add(message)

            await manager.broadcast(
                json.dumps(
                    {
                        "type": "message",
                        "data": asdict(message),
                    }
                )
            )

    except Exception as e:
        logger.error(f"WebSocket error for {user_id}: {e}")
    finally:
        await manager.disconnect(user_id)
        await manager.broadcast(
            json.dumps(
                {
                    "type": "user_left",
                    "user_id": user_id,
                }
            )
        )


async def health(request: Request, app: Sanic) -> HTTPResponse:
    return json_response(
        {
            "status": "ok",
            "messages": await app.ctx.message_store.count(),
            "users": await app.ctx.session_store.count(),
            "timestamp": utcnow().isoformat(),
        }
    )


async def clear_messages(request: Request, app: Sanic) -> HTTPResponse:
    if err := require_auth(request, app):
        return err
    await app.ctx.message_store.clear()
    return json_response({"status": "cleared"})
