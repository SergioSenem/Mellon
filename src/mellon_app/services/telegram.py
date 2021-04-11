import json
import requests
from django.conf import settings
from .chat import ChatService


class TelegramService:

    def __init__(self):
        self.token = settings.BOT_TOKEN
        self.url = settings.TELEGRAM_URL.format(self.token)
        self.chat_service = ChatService()
        self.command_handlers = {
            "/start": self.start_command_handler,
            "/help": self.help_command_handler,
            "/set": self.link_chat_handler
        }

    def manage_request(self, request):
        params = json.loads(request)
        chat_id = self.get_chat_id(params)
        command, text = self.get_command(params)
        handler = self.command_handlers.get(command)
        if handler:
            handler(chat_id, text)

    @staticmethod
    def get_chat_id(params):
        return params.get("message").get("chat").get("id")

    def get_command(self, params):
        text = self.get_text(params)
        command = text.split(' ', 1)[0]
        return command, text

    @staticmethod
    def get_text(params):
        return params.get("message").get("text")

    def start_command_handler(self, chat_id, command):
        hello_message = "Olá!"
        self.send_message(chat_id, hello_message)

    def help_command_handler(self, chat_id, command):
        help_message = "Help!"
        self.send_message(chat_id, help_message)

    def link_chat_handler(self, chat_id, command):
        code = self.get_code(command)
        if self.chat_service.link_user_by_code(code, chat_id):
            self.send_message(chat_id, "Usuário associado")
        else:
            self.send_message(chat_id, "Código inválido!")

    def send_message(self, chat_id, text):
        data = {'chat_id': chat_id, 'text': text}
        requests.post('{0}/sendMessage'.format(self.url), data=data)

    @staticmethod
    def get_code(command):
        code = command.replace('/set', '')
        code = code.replace(' ', '')
        return code
