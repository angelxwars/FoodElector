# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)


class RecipeBook(models.Model):
    title = models.CharField(max_length=50)
    link = models.URLField()
    image = models.URLField(null=True)


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    image = models.URLField()
    tags = models.ManyToManyField(Tag)
    link = models.URLField(null=True)
    recipe_book = models.ForeignKey(RecipeBook, on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
