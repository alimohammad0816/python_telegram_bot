import requests

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
    #     "card": []
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

# برای هر کاربری که ثبتنام کرده ، یک وضعیت ثبت میشه که با توجه به اون داده ورودی برسی میشه.
user_state = {
    # username = state
}


# get request for new messages
def get_update(url):
    old_req = requests.get(f"{url}getUpdates").json()
    old_req = old_req["result"]
    offset = old_req[-1]['update_id']
    while True:
        req = requests.get(f"{url}getUpdates?offset={offset}").json()
        req = req["result"][-1]
        if not offset == req['update_id']:
            return req


# Signup, Update, Delete Account with Confirm.
def account(req, url):
    global user_state
    global users
    client_message = req["message"]["text"]
    username = req['message']["from"]['username']
    username = f"{username}"
    user_id = req['message']["from"]['id']
    first_name = req['message']["from"]['first_name']
    try:
        last_name = req['message']["from"]['last_name']
    except KeyError:
        last_name = "نامشخص"
    if client_message.lower() == "/signup":
        if username not in users:
            simple = {
                username: {
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "user_id": user_id,
                    "card": []
                }
            }
            users.update(simple)
            text = "ثبتنام شما با موفقیت انجام شد."
            requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
        else:
            text = "شما قبلا ثبتنام کرده اید."
            requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
    elif client_message.lower() == '/updateaccount':
        if username in users:
            simple = {
                username: {
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "user_id": user_id,
                    "card": []
                }
            }
            users.update(simple)
            text = "پروفایل شما با موفقیت آپدیت شد."
            requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
        else:
            text = "شما قبلا ثبتنام نکرده اید."
            requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
    elif client_message.lower() == '/deleteaccount':
        if username in users:
            user_state[username] = "waitforconfirm"
            text = "آیا از حذف پروفایل خود اطمینان دارید؟برای تایید بله ،و در صورت انصراف خیر را ارسال کنید."
            requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
    elif username in users:
        if username in user_state:
            if user_state[username] == 'waitforconfirm':
                if client_message == 'بله':
                    users.pop(username)
                    text = "پروفایل شما با موفقیت حذف شد."
                    requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
                elif client_message == 'خیر':
                    user_state[username] = ''
                    text = "شما از حذف پروفایل خود انصراف دادید."
                    requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
                else:
                    text = "دستور وارد شده صحیح نمیباشد، لطفا دوباره امتحان کنید."
                    requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")


# نمایش محصولات ، افزودن محصول به سبدخرید ، نمایش و مدیریت سبد خرید
def product_managing(req, url):
    global user_state
    global users
    client_message = req["message"]["text"]
    username = f"{req['message']['from']['username']}"
    user_id = req['message']["from"]['id']
    if username in users:
        if client_message.lower() == '/products':
            text = "محصولات ما : \n"
            for i in products:
                text += f"{products[i]['name']}, \n"
            requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
        elif client_message.lower() == '/mycard':
            user_card = users[username]['card']
            if user_card == []:
                text = "سبد خرید شما خالی است."
                requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
            if not user_card == []:
                text = "سبد خرید شما : \n"
                for i in user_card:
                    text += f"{i['name']}, \n"
                requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
        elif client_message.lower() == '/additem':
            user_state[username] = 'additem'
            text = 'شما در بخش خرید هستید ، برای افزودن محصولات آیدی محصول مورد نظر را وارد کنید.'
            requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
        elif username in user_state:
            print(user_state[username])
            if user_state[username] == 'additem':
                if client_message == 'خروج':
                    text = "به بخش محصولات برگشتید."
                    requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
                    user_state[username] = 'product_mode'
                    print(user_state[username])
                else:
                    item = products[client_message]
                    users[username]['card'].append(item)
                    text = f"محصول {item['name']} اضافه شد.\n"
                    text += "برای افزودن محصول جدید ،آیدی آن را وارد کنید.\n"
                    text += "برای خروج از این بخش ، کلمه خروج را ارسال کنید."
                    requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
    else:
        text = "برای استفاده از امکانات این برنامه ابتدا ثبتنام کنید. برای ثبتنام از دستور /signup استفاده کنید."
        requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")


# ثبت سفارش و پرداخت نهایی
def payment(req, url):
    pass


def executing():
    global url
    global user_state
    req = get_update(url)
    username = req['message']["from"]['username']
    user_id = req['message']['from']['id']
    client_message = req["message"]["text"]
    if client_message.lower() == '/product':
        text = "شما وارد بخش محصولات شدید.برای خارج شدن ، کلمه خروج را وارد کنید."
        requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
        user_state[username] = 'product_mode'
    if username in user_state:
        if user_state[username] == 'product_mode':
            if client_message.lower() == 'خروج':
                text = "شما به صفحه اصلی بازگشتید."
                requests.post(f"{url}sendMessage?chat_id={user_id}&text={text}")
                user_state[username] = ''
    account(req=req, url=url)
    if username in user_state:
        if user_state[username] == 'product_mode':
            product_managing(req=req, url=url)


if __name__ == "__main__":
    print("app is Running now...")
    while True:
        print(user_state)
        executing()


