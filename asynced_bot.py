from requests import get, post
import asyncio
import aiohttp
from time import perf_counter

class Bot:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.telegram.org/bot{token}/{method}"
        self.commands = {
            # '/command':func
        }

    async def get_last_update(self, offset=None):
        if offset is None:
            url = self.base_url.format(token=self.token, method='getUpdates')
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    request = await response.json()
                    request = request['result'][-1]
            return request
        else:
            url = self.base_url.format(token=self.token, method='getUpdates')+f"?offset={offset}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    request = await response.json()
                    request = request['result'][-1]
            return request

    def parser(self, req):
        try:
            last_name = req["message"]["from"]["last_name"]
        except KeyError:
            last_name = "unknown"

        dict = {
            "text": req["message"]["text"],
            "user_id": req["message"]["from"]["id"],
            "username": req["message"]["from"]["username"],
            "first_name": req["message"]["from"]["first_name"],
            "last_name": last_name
        }
        return dict

    @staticmethod
    def get_message(req):
        context = req['text']
        return context

    @staticmethod
    def get_username(req):
        context = req["username"]
        return context

    @staticmethod
    def get_first_name(req):
        context = req["first_name"]
        return context

    @staticmethod
    def get_last_name(req):
        try:
            context = req["last_name"]
        except KeyError:
            context = "Unknown"
        return context

    @staticmethod
    def get_user_id(req):
        context = req["user_id"]
        return context

    async def send_message(self, user_id, text):
        url = self.base_url.format(token=self.token, method='sendMessage')+f"?chat_id={user_id}&text={text}"
        async with aiohttp.ClientSession() as session:
            await session.post(url)
                # request = response.json()
        #       request = request['result']
        # return request

    def command_adder(self, command, func):
        self.commands.update({command: func})

    async def command_handler(self, parser):
        command = parser['text']
        for i in self.commands:
            if i == command:
                await self.commands[i](self, parser)

    async def run(self):
        req = await self.get_last_update()
        old_offset = req['update_id']
        loop = asyncio.get_event_loop()

        while True:
            x = perf_counter()
            req = await self.get_last_update()
            y = perf_counter()
            print('Updater : ',y-x)
            new_offset = req['update_id']
            if new_offset != old_offset:
                old_offset = new_offset
                parser = self.parser(req)
                x = perf_counter()
                await self.command_handler(parser)
                y = perf_counter()
                print("Handler", y - x)