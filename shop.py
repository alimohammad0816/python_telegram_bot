import asyncio
import aiohttp
from bot import Bot
from time import strftime, perf_counter


class Main:
    bot = Bot('1330763196:AAFZYZy8u9FZCv1K2POYyPQt2IChxMvh-iQ')
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
    user = bot.user

    def __init__(self):

        # user = self.bot.user
        pass

    @Bot.command_handler('/signup')
    def signup(self):
        for i in self.user:
            if i not in self.users:
                simple = {
                    i: {
                        "username": self.user[i]['username'],
                        "first_name": self.user[i]['first_name'],
                        "last_name": self.user[i]['last_name'],
                        "user_id": i,
                        "card": {},
                        "state": ""
                    }
                }
                self.users.update(simple)
                return True
            else:
                return False

    @Bot.command_handler('/updateaccount')
    def update(self):
        for i in self.user:
            if i in self.users:
                simple = {
                    i: {
                        "username": self.user[i]['username'],
                        "first_name": self.user[i]['first_name'],
                        "last_name": self.user[i]['last_name'],
                        "user_id": i,
                        "card": {},
                        "state": ""
                    }
                }
                self.users.update(simple)
                return True
            else:
                return False

    @Bot.command_handler('/deleteaccount')
    def delete_account(self):
        if self.user_id in self.users:
            self.users.pop(self.user_id)
            return True
        else:
            return False

    @Bot.command_handler('/procuts')
    def get_products(self):
        text = 'محصولات ما: \n'
        for i in self.products:
            text += f"نام محصول :{self.products[i]['name']}   ,  کدمحصول :{i}\n"
        return text

    @Bot.command_handler('/mycard')
    def get_user_card(self):
        user_card = self.users[self.user_id]['card']
        text = 'سبد خرید شما :\n'
        if not user_card == {}:
            for i in user_card:
                text += f"نام محصول :{user_card[i]['name']}   ,  کدمحصول :{i}\n"
        else:
            text = 'سبد خرید شما خالی است.'
        return text

    @Bot.command_handler('/additem')
    def add_item(self):
        try:
            item = {self.message: Bot.products[self.message]}
            self.users[self.user_id]['card'].update(item)
            return item[self.message]
        except KeyError:
            return False

    @Bot.command_handler('/removeitem')
    def remove_item(self):
        try:
            item = {self.message: self.products[self.message]}
            self.users[self.user_id]['card'].pop(self.message)
            return item[self.message]
        except KeyError:
            return False

    @Bot.command_handler('/calc_price')
    def calc_price(self):
        if not self.users[self.user_id]['card'] == {}:
            card = self.users[self.user_id]['card']
            price_sum = 0
            for i in card:
                price_sum += card[i]['price']
            return price_sum
        else:
            text = 'سبد خرید شما خالی است.'
            return text

    @Bot.command_handler('/payment')
    def payment(self):
        card_number = self.message
        if card_number.isalnum() and len(card_number) == 16:
            return True
        else:
            return False

    def check_user_in(self):
        if self.user_id in self.users:
            return True
        else:
            return False

    def run(self):
        while True:
            for i in self.user:
                user_id = self.user[i]['user_id']
            x = perf_counter()
            if self.signup():
                text = "your Signup is Done!"
                self.bot.message_sender(user_id, text)
            elif self.update():
                y = perf_counter()
                print(y - x)
                text = "your update is Done!"
                self.bot.message_sender(user_id, text)


# class Main:
#     async def runing(self):
#         req = await self.requester(self.url)
#         instance = Bot.collector(req)
#         state = ''
#         if instance.message == '/signup':
#             instance.signup()
#             text = "ثبتنام شما با موفقیت انجام شد."
#             async with aiohttp.ClientSession() as session:
#                 await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#         if not instance.check_user_in():
#             text = 'به ربات خوش آمدید برای استفاده از امکانات ربات ابتدا ثبتنام کنید.\n'
#             text += 'برای ثبتنام از دستور /signup استفاده کنید.\n'
#             text += 'در صورت عدم ثبتنام امکانات ربات برای شما فعال نخواهد شد.'
#             async with aiohttp.ClientSession() as session:
#                 await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#         elif instance.check_user_in:
#             if instance.message == '/updateaccount':
#                 instance.update()
#                 text = "پروفایل شما با موفقیت بروزرسانی شد."
#                 async with aiohttp.ClientSession() as session:
#                     await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#             elif instance.message == '/deleteaccount':
#                 Bot.users[instance.user_id]['state'] = 'waitfordeleteaccount'
#                 text = 'آیا از حذف پروفایل خود اطمینان دارید؟'
#                 async with aiohttp.ClientSession() as session:
#                     await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#             elif instance.message == '/products':
#                     text = Bot.get_products()
#                     async with aiohttp.ClientSession() as session:
#                         await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#             elif instance.message == '/mycard':
#                 text = instance.get_user_card()
#                 async with aiohttp.ClientSession() as session:
#                     await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#             elif instance.message == '/additem':
#                 Bot.users[instance.user_id]['state'] = 'addingitem'
#                 text = 'شما در بخش افزودن محصول هستید،برای افزودن محصول کد آن را وارد کنید.'
#                 text += 'برای خارج شدن از این بخش، کلمه خروج را ارسال کنید.'
#                 async with aiohttp.ClientSession() as session:
#                     await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#             elif instance.message == '/removeitem':
#                 Bot.users[instance.user_id]['state'] = 'removingitem'
#                 text = 'شما در بخش حذف محصول هستید،برای حذف محصول کد آن را وارد کنید.'
#                 text += 'برای خارج شدن از این بخش، کلمه خروج را ارسال کنید.'
#                 async with aiohttp.ClientSession() as session:
#                     await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#             elif instance.message == '/payment':
#                 Bot.users[instance.user_id]['state'] = 'confirmingpayment'
#                 text = 'آیا از نهایی کردن سبد خرید خود، اطمینان دارید؟'
#                 text += 'برای تایید بله و برای انصراف خیر را وارد کنید.'
#                 async with aiohttp.ClientSession() as session:
#                     await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#             # -------------from here Check states and proccess
#             elif Bot.users[instance.user_id]['state'] == 'waitfordeleteaccount':
#                 if instance.message == 'بله':
#                     text = 'حساب شما با موفقیت پاک شد.'
#                     async with aiohttp.ClientSession() as session:
#                         await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#                     instance.delete_account()
#                 elif instance.message == 'خیر':
#                     text = 'شما از حذف اکانت انصراف دادید.'
#                     async with aiohttp.ClientSession() as session:
#                         await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#                     Bot.users[instance.user_id]['state'] = ''
#             elif Bot.users[instance.user_id]['state'] == 'addingitem':
#                 item = instance.add_item()
#                 if instance.message == 'خروج':
#                     text = 'شما از بخش افزودن محصول، خارج شدید.'
#                     async with aiohttp.ClientSession() as session:
#                         await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#                     Bot.users[instance.user_id]['state'] = ''
#                 elif not instance.message == '/additem':
#                     if item:
#                         text = f"محصول {item['name']} اضافه شد.\n"
#                         text += 'برای افزودن محصول دیگر کد دیگری وارد کنید یا برای خارج شدن ،خروج را ارسال کنید.'
#                         async with aiohttp.ClientSession() as session:
#                             await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#                     elif not item:
#                         text = 'ورودی صحیح نیست، دوباره امتحان کنید.'
#                         async with aiohttp.ClientSession() as session:
#                             await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#             elif Bot.users[instance.user_id]['state'] == 'removingitem':
#                 item = instance.remove_item()
#                 if instance.message == 'خروج':
#                     text = 'شما از بخش افزودن محصول، خارج شدید.'
#                     async with aiohttp.ClientSession() as session:
#                         await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#                     Bot.users[instance.user_id]['state'] = ''
#                 elif not instance.message == '/removeitem':
#                     if item:
#                         text = f"محصول {item['name']} حذف شد.\n"
#                         text += 'برای حذف محصول دیگر کد دیگری وارد کنید یا برای خارج شدن ،خروج را ارسال کنید.'
#                         async with aiohttp.ClientSession() as session:
#                             await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#                     elif not item:
#                         text = 'ورودی صحیح نیست، دوباره امتحان کنید.'
#                         async with aiohttp.ClientSession() as session:
#                             await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#             elif Bot.users[instance.user_id]['state'] == 'confirmingpayment':
#                 if instance.message == 'بله':
#                     text = 'سبد خرید ثبت شد.\n'
#                     price = instance.calc_price()
#                     text += f'your payment : {price}\n'
#                     text += 'آیا ادامه می دهید؟'
#                     async with aiohttp.ClientSession() as session:
#                         await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#                     Bot.users[instance.user_id]['state'] = 'nextlevelforpayment'
#                 elif instance.message == 'خیر':
#                     text = 'شما از نهایی کردن سبد خرید ، خارج شدید.'
#                     async with aiohttp.ClientSession() as session:
#                         await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#                     Bot.users[instance.user_id]['state'] = ''
#             elif Bot.users[instance.user_id]['state'] == 'nextlevelforpayment':
#                 if instance.message == 'بله':
#                     text = 'شماره کارت خود را بدون فاصله ارسال کنید.'
#                     async with aiohttp.ClientSession() as session:
#                         await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#                     Bot.users[instance.user_id]['state'] = 'finalpayment'
#                 elif instance.message == 'خیر':
#                     text = 'شما از پرداخت سبد خرید ، خارج شدید.'
#                     async with aiohttp.ClientSession() as session:
#                         await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#                     Bot.users[instance.user_id]['state'] = ''
#             elif Bot.users[instance.user_id]['state'] == 'finalpayment':
#                 pay = instance.payment()
#                 if pay:
#                     text = 'خرید شما با موفقیت انجام شد.'
#                     async with aiohttp.ClientSession() as session:
#                         await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')
#                     Bot.users[instance.user_id]['state'] = ''
#                     Bot.users[instance.user_id]['card'] = {}
#                 if not pay:
#                     text = 'شماره کارت اشتباه است، دوباره وارد کنید.'
#                     async with aiohttp.ClientSession() as session:
#                         await session.post(f'{self.url}sendMessage?chat_id={instance.user_id}&text={text}')


a = Main()
a.run()
