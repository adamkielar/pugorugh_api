from django.contrib.auth.models import User
from django.test import TestCase

from pugorugh.models import Dog, UserPref, UserDog


class UserDogModelTests(TestCase):
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

    def test_user_creation(self):
        self.assertEqual(str(self.user), "adam")

    def test_dog_creation(self):
        self.assertEqual(str(self.dog), self.dog.name)

    def test_userpref_creation(self):
        self.assertEqual(UserPref.objects.all().count(), 1)

    def test_userdog_creation(self):
        self.assertEqual(UserDog.objects.all().count(), 1)
