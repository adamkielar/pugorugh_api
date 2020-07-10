from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import (
    APIClient,
    APIRequestFactory,
    APITestCase,
    force_authenticate,
)

from pugorugh.models import Dog, UserPref, UserDog
from pugorugh.views import (UserRegisterView, UserPreferencesView,
                            DogListAddView, DeleteDogView,
                            UserDogStatusUpdateView, DogRetrieve)


class APIViewsTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.apiclient = APIClient()
        self.user = User.objects.create(username="adam", password="testpass")
        self.dog = Dog.objects.create(
            name="Kamzik",
            image_filename="21.jpg",
            breed="Border Coli",
            age=11,
            gender="m",
            size="m",
            pedigree="y",
            fur="s",
        )
        self.user_dog = UserDog.objects.create(user=self.user,
                                               dog=self.dog,
                                               status="l")

    def test_user_register_view(self):
        view = UserRegisterView.as_view()
        data = {"username": "adam2", "password": "testpass2"}
        request = self.factory.post("register-user", data)
        user = User.objects.all().first()
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_preferences_view_get(self):
        view = UserPreferencesView.as_view()
        request = self.factory.get("preferences")
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_preferences_view_post(self):
        view = UserPreferencesView.as_view()
        data = {
            "id": "1",
            "age": "b,y,a,s",
            "gender": "m,f",
            "size": "s,m,l,xl",
            "pedigree": "y,n",
            "fur": "l,s",
        }
        request = self.factory.post("preferences", data)
        force_authenticate(request, user=self.user)
        user_pref = UserPref.objects.all().count()
        self.assertTrue(user_pref)
        self.assertEqual(user_pref, 1)

    def test_dog_list_add_view_post(self):
        view = DogListAddView.as_view()
        data = {
            "name": "Marta",
            "image_filename": "20.jpg",
            "breed": "Border Coli",
            "age": 24,
            "gender": "f",
            "size": "xl",
            "pedigree": "n",
            "fur": "s",
        }
        request = self.factory.post("dog-list", data)
        force_authenticate(request, user=self.user)
        dog = Dog.objects.all().count()
        self.assertEqual(dog, 1)

    def test_delete_dog_view(self):
        view = DeleteDogView.as_view()
        dog = Dog.objects.all().count()
        self.assertEqual(dog, 1)
        dog_id = Dog.objects.get(id=self.dog.id)
        response = self.apiclient.delete("delete-dog", pk=dog_id)
        self.apiclient.force_authenticate(user=self.user)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_userdog_status_update_view(self):
        view = UserDogStatusUpdateView.as_view()
        dog_id = Dog.objects.get(id=self.dog.id)
        user_dog = UserDog.objects.filter(user=self.user,
                                          dog=dog_id,
                                          status=self.user_dog.status)
        self.assertEqual(user_dog.count(), 1)
        data = {
            "pk": self.dog.id,
            "status": "liked",
        }
        request = self.factory.put("dog-update", data)
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.dog.id, status=self.user_dog.status)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user_dog.status, "liked")

    def test_dog_retrieve_view(self):
        view = DogRetrieve.as_view()
        dog_id = Dog.objects.get(id=self.dog.id)
        user_dog = UserDog.objects.filter(user=self.user,
                                          dog=dog_id,
                                          status=self.user_dog.status)
        request = self.factory.get("dog-retrieve")
        force_authenticate(request, user=self.user)
        response = view(request, status=self.user_dog.status, pk=self.dog.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
