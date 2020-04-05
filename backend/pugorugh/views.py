from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from . import models
from . import serializers


class UserRegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class UserPreferencesView(generics.RetrieveUpdateAPIView):
    """
    api/user/preferences/
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        userpref = self.get_queryset().filter(user=self.request.user).first()
        return userpref


class UserDogStatusUpdateView(generics.RetrieveUpdateAPIView):
    """
    Endpoint: /api/dog/<int:pk>/<status>  (liked or disliked)
    """
    pass

class DogListView(generics.ListCreateAPIView):
    """
    Endpoint: /api/dog/
    """

    permission_class = [permissions.IsAuthenticated]
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer


class DogRetrieve(generics.RetrieveUpdateAPIView):
    """
    Endpoint: api/dog/<int:pk>/<dogstatus:status>/next/
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        status = self.kwargs.get['status'][0]
        userpref = models.UserPref.objects.get(user=self.request.user)
        dogs = models.Dog.objects.filter(Q(gender__in=userpref.gender.split(',')))

        if status == 'u':
            unset_dogs = dogs.exclude(dog_user__user_id__exact=self.request.user.id)
            return unset_dogs

    def get_object(self):
        unset_dogs = self.get_queryset()
        #dog = queryset.filter(id__gt=self.kwargs.get('pk'))[0]
        if unset_dogs:
            return unset_dogs.first()

        

class CreateDogView(generics.CreateAPIView):
    """
    Endpoint: /api/dog/add
    """
    permission_class = [permissions.IsAuthenticated]
    serializer_class = serializers.DogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteDogView(generics.DestroyAPIView):
    """
    Endpoint: /api/dog/<int:pk>/delete
    """
    permission_class = [permissions.IsAuthenticated]
    serializer_class = serializers.DogSerializer

    def perform_destroy(self, instance):
        instance.delete()

    



