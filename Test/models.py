from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    Audiofile = models.FileField(upload_to = './upload/')

