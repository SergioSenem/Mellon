import requests
from django.conf import settings


class TelegramService:

    def __init__(self):
        self.token = settings.BOT_TOKEN
        self.url = settings.TELEGRAM_URL.format(self.token)

    def send_message(self, chat_id, text):
        data = {'chat_id': chat_id, 'text': text}
        requests.post('{0}/sendMessage'.format(self.url), data=data)
