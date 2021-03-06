# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.

class Messeges(models.Model):
        messege= models.TextField(blank=True,default='')
        count=models.IntegerField(default=0)
        users= models.ManyToManyField(User,related_name="msgList")
        def __str__(self):              # __unicode__ on Python 2
                return self.messege

class Seen(models.Model):
        users=models.ManyToManyField(User,related_name="Unneccessary")
        count=models.IntegerField(default=0)
        curr_user=models.ForeignKey(User,related_name="UserSeenList")
        def __str__(self):              # __unicode__ on Python 2
                return self.count