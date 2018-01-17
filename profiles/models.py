# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from food.models import Recipe

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default=None)
    last_name = models.CharField(max_length=50, default=None)
    email = models.EmailField(default=None)
    searches = models.CharField(max_length=1000, default='')
    recipes = models.ManyToManyField(Recipe)

class Search(models.Model):
    profile = models.ForeignKey(Profile, related_name='profile', on_delete=models.CASCADE)
    tags = models.CharField(max_length=280)
    date = models.DateField()

