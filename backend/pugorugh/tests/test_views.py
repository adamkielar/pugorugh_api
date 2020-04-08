from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory, APITestCase, force_authenticate

from pugorugh.models import Dog, UserPref, UserDog
from pugorugh.views import UserRegisterView, UserPreferencesView


class APIViewsTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username="adam", password="testpass")
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

        #self.token = Token.objects.create(user=self.user)
        #self.token = Token.objects.get(user__username="adam")

    def test_user_register_view(self):
        view = UserRegisterView.as_view()
        data = {'username': 'adam2', 'password': 'testpass2'}
        request = self.factory.post("register-user", data)
        user = User.objects.all().first()
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_preferences_view(self):
        user = User.objects.all().first()
        view = UserPreferencesView.as_view()
        request = self.factory.get("preferences")
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

