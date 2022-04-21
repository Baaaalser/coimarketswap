from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer



class RegistrationTest(APITestCase):
    def test_register(self):
        data = {
                "email": "testuser@mail.com",
                "username": "testuser",
                "password": "super_strong_password"
        }
        response = self.client.post("/api/auth/signup/", format="json", data=data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_register_bad_registration(self):
        data = {
                "email": "testmail.com",
                "username": "testuser",
                "password": "super_strong_password"
        }
        response = self.client.post("/api/auth/signup/", format="json", data=data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        data = {
                "email": "testuser@mail.com",
                "username": "testuser",
                "password": "super_strong_password"
        }
        self.test_register()
        response = self.client.post("/api/auth/login/", format="json", data=data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_login_bad(self):
        data = {
                "email": "testuser@mail.com",
                "username": "testuser",
                "password": "strong_password"
        }
        self.test_register()
        response = self.client.post("/api/auth/login/", format="json", data=data)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

