from requests import get, post


class Bot:
    def __init__(self, token):
        self.url = "https://api.telegram.org/bot{key}/{method}"
        self.token = token

    def get_update(self):
        result = get(self.url.format(key=self.token, method='getUpdates'))
        result = result.json()
        return result["result"][-1]

    def message_sender(self, chat_id, message_text):
        url = self.url.format(key=self.token, method="sendMessage")
        result = post(f'{url}?chat_id={chat_id}&text={message_text}')
        result = result.json()
        return result["result"]

    @staticmethod
    def command_handler(command):
        def inner_decorator(func):
            def wrapper(obj):
                if obj.message == command:
                    return func(obj)
                else:
                    return "This Command is not Supported"
            return wrapper
        return inner_decorator


if __name__ == '__main__':
    t = Bot('1330763196:AAH3HHUfzfU4MSufuSWnbEZIQiQ--jy0Oug')
