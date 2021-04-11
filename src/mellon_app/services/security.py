from datetime import datetime, timedelta
from random import randint

from django.utils import timezone

from ..models import SecurityCode


class SecurityService:

    def __init__(self):
        self.expiration_minutes = 10
        self.remove_old_security_codes()

    @staticmethod
    def get_security_code(code):
        return SecurityCode.objects.filter(code=code, expiration_date__gt=timezone.now()).first()

    def get_or_create_security_code(self, user_id):
        code = self.get_user_active_code(user_id)
        return code if code else self.generate_security_code(user_id)

    @staticmethod
    def get_user_active_code(user_id):
        return SecurityCode.objects.filter(user_id=user_id, expiration_date__gt=timezone.now()).first()

    def generate_security_code(self, user_id):
        code = SecurityCode()
        code.user_id = user_id
        code.code = self.generate_code()
        code.expiration_date = self.get_expiration_date()
        code.save()
        return code

    @staticmethod
    def remove_old_security_codes():
        SecurityCode.objects.filter(expiration_date__lt=timezone.now()).delete()

    @staticmethod
    def generate_code():
        number = randint(10000, 99999)
        return str(number)

    def get_expiration_date(self):
        now = timezone.now()
        delta = timedelta(minutes=self.expiration_minutes)
        return now + delta
