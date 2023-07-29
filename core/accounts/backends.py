from typing import Any, Optional
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
from .models import User


class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            
    












