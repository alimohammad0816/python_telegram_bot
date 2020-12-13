from requests import get, post


class Bot:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.telegram.org/bot{token}/{method}"
        self.commands = {
            # '/command':func
        }

    def get_last_update(self, offset=None):
        if offset is None:
            url = self.base_url.format(token=self.token, method='getUpdates')
            request = get(url)
            request = request.json()
            request = request['result'][-1]
            return request
        else:
            url = self.base_url.format(token=self.token, method='getUpdates')+f"?offset={offset}"
            request = get(url)
            request = request.json()
            print(request)
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

    @property
    def get_message(self, req):
        context = req['text']
        return context

    @property
    def get_username(self, req):
        context = req["username"]
        return context

    @property
    def get_first_name(self, req):
        context = req["first_name"]
        return context

    @property
    def get_last_name(self, req):
        try:
            context = req["last_name"]
        except KeyError:
            context = "Unknown"
        return context

    @property
    def get_user_id(self, req):
        context = req["last_name"]
        return context

    def send_message(self, user_id, text):
        url = self.base_url.format(token=self.token, method='sendMessage')+f"?chat_id={user_id}&text={text}"
        request = post(url)
        request = request.json()
        request = request['result']
        return request

    def command_adder(self, command, func):
        self.commands.update({command: func})

    def command_handler(self, parser):
        command = parser['text']
        for i in self.commands:
            if i == command:
                self.commands[i](self, parser)

    def run(self):
        req = self.get_last_update()
        old_offset = req['update_id']
        while True:
            req = self.get_last_update()
            new_offset = req['update_id']
            if new_offset != old_offset:
                old_offset = new_offset
                parser = self.parser(req)
                self.command_handler(parser)



