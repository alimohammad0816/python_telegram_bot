import asyncio
import aiohttp
from bot import Bot


class Bot:
    users = {
        # example user
        # 'user_id': {
        #     "username": "alireza",
        #     "first_name": "ali",
        #     "last_name": "reza",
        #     "user_id": 123456,
        #     "card": [],
        #     "state": some sate
        # }
    }
    products = {
        '1': {"name": "book", "price": 1000},
        '2': {"name": "laptop", "price": 2000},
        '3': {"name": "ps5", "price": 3000},
        '4': {"name": "xbox series x", "price": 4000},
        '5': {"name": "pc", "price": 5000},
        '6': {"name": "car", "price": 6000},
        '7': {"name": "keyboard", "price": 7000}
    }

    def __init__(self, message, user_id, username, first_name, last_name):
        self.message = message
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def collector(cls, req):
        message = req['message']['text']
        username = req['message']["from"]['username']
        user_id = req['message']["from"]['id']
        first_name = req['message']["from"]['first_name']
        try:
            last_name = req['message']["from"]['last_name']
        except KeyError:
            last_name = "نامشخص"
        return cls(message, user_id, username, first_name, last_name)

    def signup(self):
        if self.username not in Bot.users:
            simple = {
                self.user_id: {
                    "username": self.username,
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "user_id": self.user_id,
                    "card": {},
                    "state": ""
                }
            }
            Bot.users.update(simple)
            return True
        else:
            return False

    def update(self):
        if self.username in Bot.users:
            simple = {
                self.user_id: {
                    "username": self.username,
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "user_id": self.user_id,
                    "card": {},
                    "state": ""
                }
            }
            Bot.users.update(simple)
            return True
        else:
            return False

    def delete_account(self):
        if self.user_id in Bot.users:
            Bot.users.pop(self.user_id)
            return True
        else:
            return False

    @staticmethod
    def get_products():
        text = 'محصولات ما: \n'
        for i in Bot.products:
            text += f"نام محصول :{Bot.products[i]['name']}   ,  کدمحصول :{i}\n"
        return text

    def get_user_card(self):
        user_card = self.users[self.user_id]['card']
        text = 'سبد خرید شما :\n'
        if not user_card == {}:
            for i in user_card:
                text += f"نام محصول :{user_card[i]['name']}   ,  کدمحصول :{i}\n"
        else:
            text = 'سبد خرید شما خالی است.'
        return text

    def add_item(self):
        try:
            item = {self.message: Bot.products[self.message]}
            Bot.users[self.user_id]['card'].update(item)
            return item[self.message]
        except KeyError:
            return False

    def remove_item(self):
        try:
            item = {self.message: self.products[self.message]}
            Bot.users[self.user_id]['card'].pop(self.message)
            return item[self.message]
        except KeyError:
            return False

    def calc_price(self):
        if not Bot.users[self.user_id]['card'] == {}:
            card = self.users[self.user_id]['card']
            price_sum = 0
            for i in card:
                price_sum += card[i]['price']
            return price_sum
        else:
            text = 'سبد خرید شما خالی است.'
            return text

    def payment(self):
        card_number = self.message
        if card_number.isalnum() and len(card_number) == 16:
            return True
        else:
            return False

    def check_user_in(self):
        if self.user_id in Bot.users:
            return True
        else:
            return False


class Main:
    TOKEN = '1330763196:AAH3HHUfzfU4MSufuSWnbEZIQiQ--jy0Oug'
    url = f"https://api.telegram.org/bot{TOKEN}/"
    last_request = ''

    @staticmethod
    async def get_update(session, url):
        url = f"{url}getUpdates"
        old_req = ''
        req = ''
        async with session.get(url) as resp:
            old_req = await resp.json()
        old_req = old_req["result"]
        offset = old_req[-1]['update_id']
        while True:
            async with session.get(f'{url}?offset={offset}') as resp:
                req = await resp.json()
            req = req["result"][-1]
            if not offset == req['update_id']:
                return req

    async def requester(self, url):
        while True:
            async with aiohttp.ClientSession() as session:
                return await self.get_update(session, url)

    async def runing(self):
        req = await self.requester(self.url)
        instance = Bot.collector(req)
        state = ''
        if instance.message == '/signup':
            instance.signup()
            text = "ثبتنام شما با موفقیت انجام شد."
            async with aiohttp.ClientSession() as session:
                await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
        if not instance.check_user_in():
            text = 'به ربات خوش آمدید برای استفاده از امکانات ربات ابتدا ثبتنام کنید.\n'
            text += 'برای ثبتنام از دستور /signup استفاده کنید.\n'
            text += 'در صورت عدم ثبتنام امکانات ربات برای شما فعال نخواهد شد.'
            async with aiohttp.ClientSession() as session:
                await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
        elif instance.check_user_in:
            if instance.message == '/updateaccount':
                instance.update()
                text = "پروفایل شما با موفقیت بروزرسانی شد."
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
            elif instance.message == '/deleteaccount':
                Bot.users[instance.user_id]['state'] = 'waitfordeleteaccount'
                text = 'آیا از حذف پروفایل خود اطمینان دارید؟'
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
            elif instance.message == '/products':
                    text = Bot.get_products()
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
            elif instance.message == '/mycard':
                text = instance.get_user_card()
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
            elif instance.message == '/additem':
                Bot.users[instance.user_id]['state'] = 'addingitem'
                text = 'شما در بخش افزودن محصول هستید،برای افزودن محصول کد آن را وارد کنید.'
                text += 'برای خارج شدن از این بخش، کلمه خروج را ارسال کنید.'
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
            elif instance.message == '/removeitem':
                Bot.users[instance.user_id]['state'] = 'removingitem'
                text = 'شما در بخش حذف محصول هستید،برای حذف محصول کد آن را وارد کنید.'
                text += 'برای خارج شدن از این بخش، کلمه خروج را ارسال کنید.'
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
            elif instance.message == '/payment':
                Bot.users[instance.user_id]['state'] = 'confirmingpayment'
                text = 'آیا از نهایی کردن سبد خرید خود، اطمینان دارید؟'
                text += 'برای تایید بله و برای انصراف خیر را وارد کنید.'
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
            # -------------from here Check states and proccess
            elif Bot.users[instance.user_id]['state'] == 'waitfordeleteaccount':
                if instance.message == 'بله':
                    text = 'حساب شما با موفقیت پاک شد.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
                    instance.delete_account()
                elif instance.message == 'خیر':
                    text = 'شما از حذف اکانت انصراف دادید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
                    Bot.users[instance.user_id]['state'] = ''
            elif Bot.users[instance.user_id]['state'] == 'addingitem':
                item = instance.add_item()
                if instance.message == 'خروج':
                    text = 'شما از بخش افزودن محصول، خارج شدید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
                    Bot.users[instance.user_id]['state'] = ''
                elif not instance.message == '/additem':
                    if item:
                        text = f"محصول {item['name']} اضافه شد.\n"
                        text += 'برای افزودن محصول دیگر کد دیگری وارد کنید یا برای خارج شدن ،خروج را ارسال کنید.'
                        async with aiohttp.ClientSession() as session:
                            await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
                    elif not item:
                        text = 'ورودی صحیح نیست، دوباره امتحان کنید.'
                        async with aiohttp.ClientSession() as session:
                            await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
            elif Bot.users[instance.user_id]['state'] == 'removingitem':
                item = instance.remove_item()
                if instance.message == 'خروج':
                    text = 'شما از بخش افزودن محصول، خارج شدید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
                    Bot.users[instance.user_id]['state'] = ''
                elif not instance.message == '/removeitem':
                    if item:
                        text = f"محصول {item['name']} حذف شد.\n"
                        text += 'برای حذف محصول دیگر کد دیگری وارد کنید یا برای خارج شدن ،خروج را ارسال کنید.'
                        async with aiohttp.ClientSession() as session:
                            await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
                    elif not item:
                        text = 'ورودی صحیح نیست، دوباره امتحان کنید.'
                        async with aiohttp.ClientSession() as session:
                            await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
            elif Bot.users[instance.user_id]['state'] == 'confirmingpayment':
                if instance.message == 'بله':
                    text = 'سبد خرید ثبت شد.\n'
                    price = instance.calc_price()
                    text += f'your payment : {price}\n'
                    text += 'آیا ادامه می دهید؟'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
                    Bot.users[instance.user_id]['state'] = 'nextlevelforpayment'
                elif instance.message == 'خیر':
                    text = 'شما از نهایی کردن سبد خرید ، خارج شدید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
                    Bot.users[instance.user_id]['state'] = ''
            elif Bot.users[instance.user_id]['state'] == 'nextlevelforpayment':
                if instance.message == 'بله':
                    text = 'شماره کارت خود را بدون فاصله ارسال کنید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
                    Bot.users[instance.user_id]['state'] = 'finalpayment'
                elif instance.message == 'خیر':
                    text = 'شما از پرداخت سبد خرید ، خارج شدید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
                    Bot.users[instance.user_id]['state'] = ''
            elif Bot.users[instance.user_id]['state'] == 'finalpayment':
                pay = instance.payment()
                if pay:
                    text = 'خرید شما با موفقیت انجام شد.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
                    Bot.users[instance.user_id]['state'] = ''
                    Bot.users[instance.user_id]['card'] = {}
                if not pay:
                    text = 'شماره کارت اشتباه است، دوباره وارد کنید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')


async def run_bot():
    x = Main()
    while True:
        task = asyncio.create_task(x.runing())
        await task

if __name__ == '__main__':
    print("Bot is Running Now...")
    asyncio.run(run_bot())
