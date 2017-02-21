from __future__ import unicode_literals

from django.db import models

# Create your models here.
# User class for built-in authentication module
from django.contrib.auth.models import User

# Data model for a todo-list item
class Post(models.Model):
    text = models.CharField(max_length=160)
    user = models.ForeignKey(User, default=None)
    create_time = models.DateTimeField()

    def __unicode__(self):
        return 'id=' + str(self.id) + ',text="' + self.text + '"'
