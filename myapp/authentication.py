from datetime import timedelta, datetime
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.utils import timezone
from boardworld import settings


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if token.created + timedelta(hours=settings.TOKEN_LIFE) < timezone.now():
            token.delete()
            raise exceptions.AuthenticationFailed('Token expired')
        return user, token