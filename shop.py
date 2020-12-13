from bot import Bot

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
bot = Bot('1330763196:AAFZYZy8u9FZCv1K2POYyPQt2IChxMvh-iQ')


def start(bot, req):
    text = "Welcome,Register to use the bot features." \
           "For /Signup click on it."
    user_id = bot.get_user_id(req)
    bot.send_message(user_id, text)


def get_products(bot, req):
    global products
    text = 'محصولات ما: \n'
    for i in products:
        text += f"نام محصول :{products[i]['name']}   ,  کدمحصول :{i}\n"
    user_id = bot.get_user_id(req)
    bot.send_message(user_id, text)


def signup(bot, req):
    global users
    user_id = bot.get_user_id(req)
    username = bot.get_username(req)
    first_name = bot.get_first_name(req)
    last_name = bot.get_last_name(req)
    simple = {
        user_id: {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "username": username
        }}
    users.update(simple)
    text = "Your account Created successfuly!"
    bot.send_message(user_id, text)


bot.command_adder("/start", start)
bot.command_adder("/products", get_products)
bot.command_adder("/signup", signup)
bot.run()
