from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import choices


class Dog(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    image_filename = models.CharField(max_length=255, blank=True)
    breed = models.CharField(max_length=60, blank=False)
    age = models.IntegerField(blank=False)
    gender = models.CharField(max_length=60, choices=choices.GENDER_CHOICES)
    size = models.CharField(max_length=60, choices=choices.SIZE_CHOICES)
    pedigree = models.CharField(max_length=60, choices=choices.PEDIGREE_CHOICES)
    fur = models.CharField(max_length=60, choices=choices.FUR_CHOICES)


class UserPref(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=7, default='b,y,a,s')
    gender = models.CharField(max_length=6, default='m,f,u')
    size = models.CharField(max_length=8, default='s,m,l,xl,u')
    pedigree = models.CharField(max_length=3, default='y,n')
    fur = models.CharField(max_length=3, default='l,s')


@receiver(post_save, sender=User)
def create_user_userpref(sender, instance=None, created=None, **kwargs):
    if created:
        UserPref.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_userpref(sender, instance, **kwargs):
    instance.userpref.save()


class UserDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=choices.STATUS_CHOICES)