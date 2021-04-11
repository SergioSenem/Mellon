from .security import SecurityService
from ..models import Chat


class ChatService:

    def __init__(self):
        self.security_service = SecurityService()

    def link_user_by_code(self, code, chat_id):
        security_code = self.security_service.get_security_code(code)
        if security_code:
            return self.create_chat(security_code, chat_id)
        return None

    @staticmethod
    def create_chat(security_code, chat_id):
        chat = Chat()
        chat.user_id = security_code.user_id
        chat.uuid = chat_id
        chat.save()
        return chat
