from django.contrib.auth.models import User
from django.db import models

from . import choices


class Dog(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image_filename = models.ImageField(upload_to="images/dogs/")
    breed = models.CharField(max_length=250)
    age = models.IntegerField(blank=True)
    gender = models.CharField(max_length=1, choices=choices.GENDER_CHOICES)
    size = models.CharField(max_length=2, choices=choices.SIZE_CHOICES)
    pedigree = models.CharField(max_length=1, choices=choices.PEDIGREE_CHOICES)
    fur = models.CharField(max_length=1, choices=choices.FUR_CHOICES)


class UserPref(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=1, choices=choices.AGE_CHOICES)
    gender = models.CharField(max_length=1, choices=choices.GENDER_CHOICES)
    size = models.CharField(max_length=2, choices=choices.SIZE_CHOICES)
    pedigree = models.CharField(max_length=1, choices=choices.PEDIGREE_CHOICES)
    fur = models.CharField(max_length=1, choices=choices.FUR_CHOICES)


class UserDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=choices.STATUS_CHOICES)