from django.contrib.auth import get_user_model
from django.shortcuts import Http404


from rest_framework import authentication
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from . import models
from . import serializers


class UserRegisterView(generics.CreateAPIView):
    """
    Endpoint: /api/user/
    """

    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class UserPreferencesView(generics.RetrieveUpdateAPIView):
    """
    api/user/preferences/
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        user_pref = self.queryset.filter(user=self.request.user).first()

        dogs = models.Dog.objects.filter(
            age_letter__in=self.request.user.userpref.age.split(","),
            gender__in=self.request.user.userpref.gender.split(","),
            size__in=self.request.user.userpref.size.split(","),
            pedigree__in=self.request.user.userpref.pedigree.split(","),
            fur__in=self.request.user.userpref.fur.split(","),
        )

        for dog in dogs:
            models.UserDog.objects.update_or_create(
                user=self.request.user, dog=dog, status="u"
            )
        return user_pref


class DogListAddView(generics.ListCreateAPIView):
    """
    Endpoint: /api/dog/
    Endpoint: /api/dog/add
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteDogView(generics.DestroyAPIView):
    """
    Endpoint: /api/dog/<int:pk>/delete
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = serializers.DogSerializer

    def perform_destroy(self, instance):
        instance.delete()


class UserDogStatusUpdateView(generics.UpdateAPIView):
    """
    Endpoint: /api/dog/<int:pk>/<status>  (liked or disliked or undecided)
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    queryset = models.UserDog.objects.all()
    serializer_class = serializers.UserDogSerializer

    def put(self, *args, **kwargs):
        dog_id = self.kwargs["pk"]
        status = self.kwargs["status"][0]
        try:
            user_dog = self.queryset.get(user=self.request.user, dog=dog_id)
            user_dog.status = status
            user_dog.save()
        except IndexError:
            user_dog = self.queryset.create(
                user=self.request.user, dog=dog_id, status=status
            )
        serializer = serializers.UserDogSerializer(user_dog)
        return Response(serializer.data)


class DogRetrieve(generics.RetrieveUpdateAPIView):
    """
    Endpoint: api/dog/<int:pk>/<status>/next/
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        status = self.kwargs.get("status")[0]
        user_pref = models.UserPref.objects.get(user=self.request.user.id)
        status_dogs = self.queryset.filter(
            age_letter__in=self.request.user.userpref.age.split(","),
            gender__in=self.request.user.userpref.gender.split(","),
            size__in=self.request.user.userpref.size.split(","),
            pedigree__in=self.request.user.userpref.pedigree.split(","),
            fur__in=self.request.user.userpref.fur.split(","),
        )

        if status == "u":
            status_dogs = status_dogs.filter(
                userdog__status__exact="u", userdog__user=self.request.user
            )
        elif status == "l":
            status_dogs = status_dogs.filter(
                userdog__status__exact="l", userdog__user=self.request.user
            )
        else:
            status_dogs = status_dogs.filter(
                userdog__status__exact="d", userdog__user=self.request.user
            )
        return status_dogs

    def get_object(self):
        status_dogs = self.get_queryset()
        next_dogs = status_dogs.filter(id__gt=self.kwargs.get("pk"))
        if next_dogs.exists():
            return next_dogs.first()
        if status_dogs.exists():
            return status_dogs.first()
        raise Http404()
