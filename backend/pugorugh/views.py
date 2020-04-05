from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import authentication
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

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
    authentication_class = [authentication.TokenAuthentication]
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        userpref = self.get_queryset().filter(user=self.request.user).first()
        return userpref

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class DogListView(generics.ListCreateAPIView):
    """
    Endpoint: /api/dog/
    """

    permission_class = [permissions.IsAuthenticated]
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer


class CreateDogView(generics.CreateAPIView):
    """
    Endpoint: /api/dog/add
    """

    permission_class = [permissions.IsAuthenticated]
    authentication_class = [authentication.TokenAuthentication]
    serializer_class = serializers.DogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteDogView(generics.DestroyAPIView):
    """
    Endpoint: /api/dog/<int:pk>/delete
    """

    permission_class = [permissions.IsAuthenticated]
    authentication_class = [authentication.TokenAuthentication]
    serializer_class = serializers.DogSerializer

    def perform_destroy(self, instance):
        instance.delete()


class UserDogStatusUpdateView(generics.RetrieveUpdateAPIView):
    """
    Endpoint: /api/dog/<int:pk>/<status>  (liked or disliked)
    """

    permission_class = [permissions.IsAuthenticated]
    authentication_class = [authentication.TokenAuthentication]
    serializer_class = serializers.DogSerializer


class DogRetrieve(generics.RetrieveUpdateAPIView):
    """
    Endpoint: api/dog/<int:pk>/<dogstatus:status>/next/
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()
