import asyncio
import aiohttp
from functools import wraps


class Bot:
    def __init__(self, token):
        self.url = "https://api.telegram.org/bot{key}/{method}"
        self.token = token

    async def get_update(self, session):
        async with session.get(self.url.format(key=self.token, method='getUpdates')) as resp:
            result = await resp.json()
        return result["result"][-1]

    async def message_reciver(self):
        async with aiohttp.ClientSession() as session:
            return await self.get_update(session)

    async def message_sender(self, chat_id, message_text):
        url = self.url.format(key=self.token, method="sendMessage")
        async with aiohttp.ClientSession() as session:
            result = await session.post(f'{url}?chat_id={chat_id}&text={message_text}')
        result = result.json()
        return await result

    @staticmethod
    def command_handler(command):
        def inner_decorator(func):
            @wraps(func)
            def wrapper(message):
                print(message)
                if message.lower() == command.lower():
                    return func(message)
                else:
                    return "This Command is not Supported"
            return wrapper
        return inner_decorator
