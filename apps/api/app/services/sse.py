import asyncio
import json
from collections.abc import AsyncGenerator

import redis.asyncio as aioredis

from app.core.config import settings


class EventBus:
    def __init__(self) -> None:
        self._redis: aioredis.Redis | None = None

    async def _get_redis(self) -> aioredis.Redis:
        if self._redis is None:
            self._redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        return self._redis

    async def publish_event(self, task_id: str, event_type: str, data: dict) -> None:
        r = await self._get_redis()
        payload = json.dumps({"event": event_type, "data": data})
        await r.publish(f"task:{task_id}", payload)

    async def subscribe_events(self, task_id: str) -> AsyncGenerator[str, None]:
        r = await self._get_redis()
        pubsub = r.pubsub()
        await pubsub.subscribe(f"task:{task_id}")
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message and message["type"] == "message":
                    payload = json.loads(message["data"])
                    yield f"event: {payload['event']}\ndata: {json.dumps(payload['data'])}\n\n"
                    if payload["event"] == "complete":
                        break
                else:
                    await asyncio.sleep(0.1)
        finally:
            await pubsub.unsubscribe(f"task:{task_id}")
            await pubsub.close()

    async def close(self) -> None:
        if self._redis:
            await self._redis.close()


event_bus = EventBus()
