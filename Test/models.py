#coding=utf8
from __future__ import unicode_literals
from ckeditor.fields import RichTextField
from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.
class User(models.Model):
    Audiofile = models.FileField(upload_to = './upload/')

class Blog(models.Model):
	content = UEditorField('内容', height=500, width=1200,
						   default=u'', blank=True, imagePath="uploads/images/",
						   toolbars='full', filePath='uploads/files/')