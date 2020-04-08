from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import choices


class Dog(models.Model):
    """
    Model for Dog instance.
    Rewrote save() function to convert integer age to letter.
    age_letter field added to store that letter
    """
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    image_filename = models.CharField(max_length=255, blank=True)
    breed = models.CharField(max_length=60, blank=False)
    age = models.IntegerField()
    age_letter = models.CharField(max_length=1, blank=True)
    gender = models.CharField(max_length=60, choices=choices.GENDER_CHOICES)
    size = models.CharField(max_length=60, choices=choices.SIZE_CHOICES)
    pedigree = models.CharField(max_length=60, choices=choices.PEDIGREE_CHOICES)
    fur = models.CharField(max_length=60, choices=choices.FUR_CHOICES)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.age in range(100, 200):
            self.age_letter = "s"
        elif self.age in range(50, 100):
            self.age_letter = "a"
        elif self.age in range(11, 50):
            self.age_letter = "y"
        elif self.age < 11:
            self.age_letter = "b"
        super(Dog, self).save(*args, **kwargs)



class UserPref(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=60, default="b,y,a,s")
    gender = models.CharField(max_length=60, default="m,f")
    size = models.CharField(max_length=60, default="s,m,l,xl")
    pedigree = models.CharField(max_length=60, default="y,n")
    fur = models.CharField(max_length=60, default="l,s")


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
