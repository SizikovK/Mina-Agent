from aiogram import BaseMiddleware
from datetime import datetime, timedelta
from typing import Callable, Awaitable, Any, Dict
from aiogram.types import TelegramObject, Message
from collections import defaultdict, deque
import logging

log = logging.getLogger(__name__)

class SpamMiddleware(BaseMiddleware):
    def __init__(
        self, 
        rate_limit: int = 3, 
        time_interval: timedelta = timedelta(seconds=5)
    ):
        self.rate_limit = rate_limit
        self.time_interval = time_interval
        self.processed_messages = defaultdict[int, deque[datetime]](deque)


    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message, 
        data: Dict[str, Any]
    ) -> Any:
        if event.from_user is None:
            return await handler(event, data)

        user_id = event.from_user.id
        now = datetime.now()
        user_messages = self.processed_messages[user_id]
        threshold = now - self.time_interval

        while user_messages and user_messages[0] < threshold:
            user_messages.popleft()

        user_messages.append(now)
        count = len(user_messages)

        if count > self.rate_limit:
            log.info(f"User {user_id} has reached the rate limit. Count: {count}")
            await event.reply(text="Притормози, я читать не успеваю")
            return

        return await handler(event, data)
