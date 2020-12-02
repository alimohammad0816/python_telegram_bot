import requests
token = '1330763196:AAEPyj60bkRiYCkEDHdL1LXCMCTkiwibh08'
telegram_api = "https://api.telegram.org/bot1330763196:AAH47cMaX3sIyJkxYZHZtjvXrkN6ZOZ8PA0/"

users = {
    'alireza':{
        "username":"alireza",
        "first_name":"ali",
        "last_name":"reza",
        "id":123456,
        "card":[]
    }
}

products = {
    '1' : {"name":"book","price":1000},
    '2' : {"name":"laptop","price":2000},
    '3' : {"name":"ps5","price":3000},
    '4' : {"name":"xbox series x","price":4000},
    '5' : {"name":"pc","price":5000},
    '6' : {"name":"car","price":6000},
    '7' : {"name":"keyboard","price":7000}
}
def telegram_bot_future():
    new_req = new_req = requests.get(f"{telegram_api}getUpdates").json()
    new_req = new_req["result"]
    old_len = len(new_req)
    while True:
    # get new update every second
        new_req = requests.get(f"{telegram_api}getUpdates").json()
        new_req = new_req["result"]
    # if we got new message
        if old_len < len(new_req):
            old_len = len(new_req)
            new_req = new_req[-1]
            new_req_text = new_req["message"]["text"]

            #user info
            username =new_req['message']["from"]['username']
            username = f"@{username}"
            id = new_req['message']["from"]['id']
            first_name = new_req['message']["from"]['first_name']
            try:
                last_name = new_req['message']["from"]['last_name']
            except KeyError:
                last_name = "نامشخص"

            if new_req_text == "/start":
                text = '''
                سلام به ربات ما خوش آمدید،
                برای استفاده از امکانات ربات ابتدا ثبتنام کنید.
                برای ثبتنام از دستور /signUp استفاده کنید
                '''
                requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
            elif new_req_text.lower() == '/signup':
                if username not in users:
                    users.update({
                        username:{
                        "username":username,
                        'id':id,
                        'first_name':first_name,
                        'last_name':last_name,
                        'card':[]
                    }
                    })
                    text = f"ثبتنام شما انجام شد، نام شما {first_name} ،نام خانوادگی شما {last_name} ،نام کاربری شما {username}"

                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
                else:
                    text = "شما قبلا در این ربات ثبتنام کرده اید..."
                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
            elif new_req_text.lower() == '/updateaccount':
                if username in users:
                    users.update({
                        username:{
                        "username":username,
                        'id':id,
                        'first_name':first_name,
                        'last_name':last_name,
                        
                    }
                    })
                    text = f"بروز رسانی پروفایل شما انجام شد ، نام شما {first_name} ،نام خانوادگی شما {last_name} ،نام کاربری شما {username}"

                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
                else:
                    text = "شما در گذشته ثبتنام نکرده اید."
            elif new_req_text.lower() == "/deleteaccount":
                if username in users:
                    text = "حساب کاربری شما حذف خواهد شد، ادامه می دهید؟برای متوقف کردن عملیات /exit و برای ادامه  /yesdeleteaccount را وارد کنید."
                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
                else:
                    text = "شما در گذشته ثبتنام نکرده اید."
                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
            elif new_req_text.lower() == "/yesdeleteaccount":
                if username in users:
                    users.pop(username)
                    text = 'حساب شما با موفقیت پاک شد.'
                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
            elif new_req_text.lower() == "/products":
                text = 'محصولات ما :'
                requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
                for i in products:
                    product_id = i
                    product = products[i]['name']
                    text = f"نام محصول {product} آیدی محصول {product_id}"
                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
                
                text = 'برای افزودن محصول به سبد خرید /additem محصول را وارد کنید.'
            elif new_req_text == '/additem':
                text = 'برای افزودن محصول به سبد خرید /id محصول را وارد کنید.'
                requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
            elif new_req_text == '/1':
                if username in users:
                    users[username]['card'].append(products['1'])
                    text = f"{products['1']['name']}اضافه شد"
                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
            elif new_req_text == '/2':
                if username in users:
                    users[username]['card'].append(products['2'])
                    text = f"{products['2']['name']}اضافه شد"
                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
            elif new_req_text == '/3':
                if username in users:
                    users[username]['card'].append(products['3'])
                    text = f"{products['3']['name']}اضافه شد"
                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
            elif new_req_text == '/4':
                if username in users:
                    users[username]['card'].append(products['4'])
                    text = f"{products['4']['name']}اضافه شد"
                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
            elif new_req_text == '/5':
                if username in users:
                    print(users[username])
                    users[username]['card'].append(products['5'])
                    text = f"{products['5']['name']}اضافه شد"
                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
            elif new_req_text == '/6':
                if username in users:
                    users[username]['card'].append(products['6'])
                    text = f"{products['6']['name']}اضافه شد"
                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
            elif new_req_text == '/7':
                if username in users:
                    users[username]['card'].append(products['7'])
                    text = f"{products['7']['name']}اضافه شد"
                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
            elif new_req_text == '/mycard':
                if username in users:
                    text = 'محصولات موجود در سبد خرید شما'
                    requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
                    for i in users[username]['card']:
                        text = f"{i['name']}"
                        requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
            elif new_req_text == '/del_1':
                if username in users:
                    # print(users[username]["card"])
                    product_id = new_req_text.split('_')
                    product_name = products[product_id[1]]['name']
                    for i in users[username]["card"]:
                        # print(i)
                        if product_name == i['name']:
                            
                            text = f'{i["name"]}با موفقیت حذف شد'
                            requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")
                            break
            else:
                id = new_req['message']["from"]['id']
                text = f"دوست عزیز دستورات شما قابل فهم برای ربات نیست، لطفا از دستورات پیش فرض ربات استفاده کنید."
                requests.post(f"{telegram_api}sendMessage?chat_id={id}&text={text}")


run = telegram_bot_future()

# from flask import Flask
# from flask_restful import Resource,Api

# app = Flask(__name__)
# api = Api(app)

# class telegram_bot_api(Resource):
#     pass

# api.add_resource(telegram_bot_api,'/')

# if __name__ == '__main__':
#     app.run(debug=True)