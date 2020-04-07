from django.contrib.auth.models import User
from django.test import TestCase

from pugorugh.models import Dog, UserPref, UserDog


class APIViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="adam", 
            password="drkiler",
        )
        self.dog = Dog.objects.create(
            name="Kamzik",
            breed="Border Coli",
            age=11,
            gender="m",
            size="m",
            pedigree="y",
            fur="s",
        )
        self.user_dog = UserDog.objects.create(
            user=self.user, 
            dog=self.dog, 
            status="l"
        )