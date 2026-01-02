import asyncio
from typing import Optional

from .models import Message, UserSession
from .logger import logger


class MessageStore:
    def __init__(self):
        self._messages: list[Message] = []
        self._lock = asyncio.Lock()

    async def add(self, message: Message) -> None:
        async with self._lock:
            self._messages.append(message)
            logger.info(f"Message added: {message.id} from {message.username}")

    async def get_all(self) -> list[Message]:
        async with self._lock:
            return self._messages.copy()

    async def clear(self) -> None:
        async with self._lock:
            count = len(self._messages)
            self._messages.clear()
            logger.info(f"Cleared {count} messages")

    async def count(self) -> int:
        async with self._lock:
            return len(self._messages)


class UserSessionStore:
    def __init__(self):
        self._sessions: dict[str, UserSession] = {}
        self._lock = asyncio.Lock()

    async def add(self, session: UserSession) -> None:
        async with self._lock:
            self._sessions[session.user_id] = session
            logger.info(f"Session created: {session.user_id} ({session.username})")

    async def get(self, user_id: str) -> Optional[UserSession]:
        async with self._lock:
            return self._sessions.get(user_id)

    async def update_activity(self, user_id: str) -> None:
        async with self._lock:
            if session := self._sessions.get(user_id):
                session.update_activity()

    async def remove(self, user_id: str) -> None:
        async with self._lock:
            if user_id in self._sessions:
                del self._sessions[user_id]
                logger.info(f"Session removed: {user_id}")

    async def cleanup_stale(self, timeout_seconds: int = 3600) -> int:
        async with self._lock:
            stale_ids = [
                uid for uid, s in self._sessions.items() if s.is_stale(timeout_seconds)
            ]
            for uid in stale_ids:
                del self._sessions[uid]
            if stale_ids:
                logger.info(f"Cleaned up {len(stale_ids)} stale sessions")
            return len(stale_ids)

    async def get_all(self) -> list[UserSession]:
        async with self._lock:
            return list(self._sessions.values())

    async def count(self) -> int:
        async with self._lock:
            return len(self._sessions)

    async def username_exists(self, username: str) -> bool:
        async with self._lock:
            return any(s.username == username for s in self._sessions.values())
