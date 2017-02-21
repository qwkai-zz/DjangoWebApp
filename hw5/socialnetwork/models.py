from __future__ import unicode_literals

from django.db import models

# Create your models here.
# User class for built-in authentication module
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


# Data model for a todo-list item
class Post(models.Model):
    text = models.CharField(max_length=160)
    user = models.ForeignKey(User, default=None)
    create_time = models.DateTimeField()

    def __unicode__(self):
        return 'id=' + str(self.id) + ',text="' + self.text + '"'

class Profile(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField(null=True,blank=True)
    bio = models.CharField(max_length=430, blank=True)
    picture = models.FileField(upload_to="images", blank=True)
    following = models.ManyToManyField("self",symmetrical=False)

#example code from 
#https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.age=0
        instance.profile.bio="Say something..."

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()