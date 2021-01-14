from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from core.helpers.random_string import random_string

class UserClient:
    CLIENT = None
    USER = None
    RAW_PASSWORD = None
    RAW_TOKEN = None
    AUTH_URI = reverse('token_obtain_pair')

    def __init__(self):
        self.create_client()
        self.create_user()
        self.authenticate_user()

    def create_client(self):
        self.CLIENT = APIClient()

    def create_user(self):
        self.USER = User.objects.create(
            username=random_string(10),
        )
        self.USER.is_active = True
        self.RAW_PASSWORD = random_string(10)
        self.USER.set_password(self.RAW_PASSWORD) 
        self.USER.save()

    def set_client_token(self, jwt_token):
        self.RAW_TOKEN = jwt_token
        
        formatted_token = self.format_token(jwt_token)
        self.CLIENT.credentials(HTTP_AUTHORIZATION=formatted_token)

    def format_token(self, jwt_token):
        return f"Bearer {jwt_token}"

    def get_token_from_credentials(self, credentials):
        res = self.CLIENT.post(self.AUTH_URI, data=credentials, format='json')
        jwt_token = res.data['access']
        
        return jwt_token

    def authenticate_user(self):
        credentials = {
            'username': self.USER.username,
            'password': self.RAW_PASSWORD
        }

        jwt_token = self.get_token_from_credentials(credentials)

        self.set_client_token(jwt_token=jwt_token)

    def do_post(self, uri, payload):
        return self.CLIENT.post(uri, payload, format='json')