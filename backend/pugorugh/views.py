from django.contrib.auth import get_user_model

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
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        userpref = self.get_queryset().filter(user=self.request.user).first()
        return userpref
        
        
