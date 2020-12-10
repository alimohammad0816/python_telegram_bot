# import urllib.request as request
from requests import get, post
import json
import asyncio
import aiohttp

class Bot:
    def __init__(self, token):
        self.url = "https://api.telegram.org/bot{key}/{method}"
        self.token = token

    async def get_update(self, session):
        async with session.get(self.url.format(key=self.token, method='getUpdates')) as resp:
            result = await resp.json()
        return result["result"][-1]

    async def message_reciver(self):
        while True:
            async with aiohttp.ClientSession() as session:
                return await self.get_update(session)

    async def message_sender(self, chat_id, message_text):
        url = self.url.format(key=self.token, method="sendMessage")
        async with aiohttp.ClientSession() as session:
            result = await session.post(f'{url}?chat_id={chat_id}&text={message_text}')
        result = result.json()
        return await result

    def handlers(self):
        pass

    def add_handler(self):
        pass

    def remove_handler(self):
        pass

loop = asyncio.get_event_loop()


if __name__ == '__main__':
    t = Bot('1330763196:AAH3HHUfzfU4MSufuSWnbEZIQiQ--jy0Oug')