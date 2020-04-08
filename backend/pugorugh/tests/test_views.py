from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from pugorugh.models import Dog, UserPref, UserDog


class APIViewsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="adam", password="testpass",)
        self.dog = Dog.objects.create(
            name="Kamzik",
            breed="Border Coli",
            age=11,
            gender="m",
            size="m",
            pedigree="y",
            fur="s",
        )
        self.user_dog = UserDog.objects.create(user=self.user, dog=self.dog, status="l")

        self.token = Token.objects.create(user=self.user)
        self.token = Token.objects.get(user__username="adam")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_account_create_endpoint(self):
        self.client.credentials()
        url = "/api/user/"
        data = {"username": "adam", "password": "testpass"}
        response = self.client.get(reverse("register-user"))
        self.assertEqual(response.status_code, 200)
        #response = self.client.post(url, data, format="json")
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)
