import asyncio
import requests
import aiohttp
TOKEN = '1330763196:AAH3HHUfzfU4MSufuSWnbEZIQiQ--jy0Oug'
url = f"https://api.telegram.org/bot{TOKEN}/"

# users data
users = {
    # example user
    # 'alireza': {
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

# get new update
async def get_update(session, url):
    url = f"{url}getUpdates"
    old_req = 0
    req = 0
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


# Signup, Update, Delete Account with Confirm.
def signup(req, url):
    global users
    username = req['message']["from"]['username']
    user_id = req['message']["from"]['id']
    first_name = req['message']["from"]['first_name']
    try:
        last_name = req['message']["from"]['last_name']
    except KeyError:
        last_name = "نامشخص"
    if username not in users:
        simple = {
            username: {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "user_id": user_id,
                "card": {},
                "state": ""
            }
        }
        users.update(simple)


def update(req, url):
    global users
    username = req['message']["from"]['username']
    user_id = req['message']["from"]['id']
    first_name = req['message']["from"]['first_name']
    try:
        last_name = req['message']["from"]['last_name']
    except KeyError:
        last_name = "نامشخص"
    simple = {
        username: {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "user_id": user_id,
            "card": {},
            "state": ""
        }
    }
    users.update(simple)


def delete_account(req, url):
    global users
    username = req['message']["from"]['username']
    users.pop(username)


def get_products(products):
    text = 'محصولات ما: \n'
    for i in products:
        text += f"نام محصول :{products[i]['name']}   ,  کدمحصول :{i}\n"
    return text


def get_card(username):
    global users
    user_card = users[username]['card']
    text = 'سبد خرید شما :\n'
    if not user_card == {}:
        for i in user_card:
            text += f"نام محصول :{user_card[i]['name']}   ,  کدمحصول :{i}\n"
    else:
        text = 'سبد خرید شما خالی است.'
    return text


def add_item(username, message):
    global products
    global users
    try:
        item = {message: products[message]}
        users[username]['card'].update(item)
        return item[message]
    except KeyError:
        return False


def remove_item(username, message):
    global users
    try:
        item = {message: products[message]}
        users[username]['card'].pop(message)
        return item[message]
    except KeyError:
        return False


# محاسبه قیمت نهایی
def calc_price(username):
    card = users[username]['card']
    price_sum = 0
    for i in card:
        price_sum += card[i]['price']
    return price_sum


# پرداخت
def payment(card_number):
    if card_number.isalnum() and len(card_number) == 16:
        return True
    else:
        return False


def check_user_in(username):
    if username in users:
        return True
    else:
        return False


loop = asyncio.get_event_loop()


async def reqer(url):
    while True:
        async with aiohttp.ClientSession() as session:
            return await get_update(session, url)


async def main(url):
        req = await reqer(url)
        loop.create_task(main(url))
        username = req['message']["from"]['username']
        user_id = req['message']['from']['id']
        client_message = req["message"]["text"]
        if client_message == '/signup':
            signup(req, url)
            text = "ثبتنام شما با موفقیت انجام شد."
            async with aiohttp.ClientSession() as session:
                await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
        if not check_user_in(username):
            text = 'به ربات خوش آمدید برای استفاده از امکانات ربات ابتدا ثبتنام کنید.\n'
            text += 'برای ثبتنام از دستور /signup استفاده کنید.\n'
            text += 'در صورت عدم ثبتنام امکانات ربات برای شما فعال نخواهد شد.'
            # requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
            async with aiohttp.ClientSession() as session:
                await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
        elif check_user_in(username):
            if client_message == '/updateaccount':
                update(req, url)
                text = "پروفایل شما با موفقیت بروزرسانی شد."
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
            elif client_message == '/deleteaccount':
                users[username]['state'] = 'waitfordeleteaccount'
                text = 'آیا از حذف پروفایل خود اطمینان دارید؟'
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
            elif client_message == '/products':
                text = get_products(products)
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
            elif client_message == '/mycard':
                text = get_card(username)
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
            elif client_message == '/additem':
                users[username]['state'] = 'addingitem'
                text = 'شما در بخش افزودن محصول هستید،برای افزودن محصول کد آن را وارد کنید.'
                text += 'برای خارج شدن از این بخش، کلمه خروج را ارسال کنید.'
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
            elif client_message == '/removeitem':
                users[username]['state'] = 'removingitem'
                text = 'شما در بخش حذف محصول هستید،برای حذف محصول کد آن را وارد کنید.'
                text += 'برای خارج شدن از این بخش، کلمه خروج را ارسال کنید.'
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
            elif client_message == '/payment':
                users[username]['state'] = 'confirmingpayment'
                text = 'آیا از نهایی کردن سبد خرید خود، اطمینان دارید؟'
                text += 'برای تایید بله و برای انصراف خیر را وارد کنید.'
                async with aiohttp.ClientSession() as session:
                    await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
            # -------------from here Check states and proccess
            state = users[username]['state']
            if state == 'waitfordeleteaccount':
                if client_message == 'بله':
                    delete_account(req, url)
                    text = 'حساب شما با موفقیت پاک شد.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
                elif client_message == 'خیر':
                    text = 'شما از حذف اکانت انصراف دادید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
                    users[username]['state'] = ''
            elif state == 'addingitem':
                item = add_item(username, client_message)
                if client_message == 'خروج':
                    text = 'شما از بخش افزودن محصول، خارج شدید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
                    users[username]['state'] = ''
                elif not client_message == '/additem':
                    if item:
                        text = f"محصول {item['name']} اضافه شد.\n"
                        text += 'برای افزودن محصول دیگر کد دیگری وارد کنید یا برای خارج شدن ،خروج را ارسال کنید.'
                        async with aiohttp.ClientSession() as session:
                            await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
                    elif not item:
                        text = 'ورودی صحیح نیست، دوباره امتحان کنید.'
                        async with aiohttp.ClientSession() as session:
                            await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
            elif state == 'removingitem':
                item = remove_item(username, client_message)
                if client_message == 'خروج':
                    text = 'شما از بخش افزودن محصول، خارج شدید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
                    users[username]['state'] = ''
                elif not client_message == '/removeitem':
                    if item:
                        text = f"محصول {item['name']} حذف شد.\n"
                        text += 'برای حذف محصول دیگر کد دیگری وارد کنید یا برای خارج شدن ،خروج را ارسال کنید.'
                        async with aiohttp.ClientSession() as session:
                            await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
                    elif not item:
                        text = 'ورودی صحیح نیست، دوباره امتحان کنید.'
                        requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
            elif state == 'confirmingpayment':
                if client_message == 'بله':
                    text = 'سبد خرید ثبت شد.\n'
                    price = calc_price(username)
                    text += f'your payment : {price}\n'
                    text += 'آیا ادامه می دهید؟'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
                    users[username]['state'] = 'nextlevelforpayment'
                elif client_message == 'خیر':
                    text = 'شما از نهایی کردن سبد خرید ، خارج شدید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
                    users[username]['state'] = ''
            elif state == 'nextlevelforpayment':
                if client_message == 'بله':
                    text = 'شماره کارت خود را بدون فاصله ارسال کنید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
                    users[username]['state'] = 'finalpayment'
                elif client_message == 'خیر':
                    text = 'شما از پرداخت سبد خرید ، خارج شدید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
                    users[username]['state'] = ''
            elif state == 'finalpayment':
                pay = payment(client_message)
                if pay:
                    text = 'خرید شما با موفقیت انجام شد.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')
                    users[username]['state'] = ''
                    users[username]['card'] = {}
                if not pay:
                    text = 'شماره کارت اشتباه است، دوباره وارد کنید.'
                    async with aiohttp.ClientSession() as session:
                        await session.post(f'{url}sendMessage?chat_id={user_id}&text={text}')

loop.create_task(main(url))
if __name__ == '__main__':
    print("app is running now...")
    loop.run_forever()

