# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pandas as pd
import datetime

from django.shortcuts import render

from food.forms import IngredientForm
import contentBased.contentBased as cB
from food.models import Recipe, Ingredient, RecipeBook, Tag
from profiles.models import Profile, Search


# Create your views here.

def ingredients(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        user = request.user
        profile = Profile.objects.get(user__username=user)

        if form.is_valid():
            ingredients_recipes = list()
            ingredients_str = form.cleaned_data.get('ingredients')
            recetario = Recipe.objects.filter(ingredient__name__contains=ingredients_str)

            search = Search(profile=profile, tags=ingredients_str, date=datetime.date.today())
            search.save()
            # Recomender system (content based)
            data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";", encoding='latin-1')
            data.head(3)
            content_based = cB.ContentBased()
            content_based.fit(data, 'recipe_str')
            predict = content_based.predict([ingredients_str])
            recipes_predict = predict.get('title').values
            for recipe in recipes_predict:
                a = Recipe.objects.filter(title=recipe)
                ingredients_recipes.append(a[0])
            return render(request, 'recipes.html', {'recipes': ingredients_recipes})

    else:
        form = IngredientForm()
    return render(request, 'ingredients.html', {'form': form})


def description(request):
    if request.method == 'GET':
        recipe_id = request.GET.get('id', '')
        recipe = Recipe.objects.get(id=recipe_id)
        recipe_ingredients = Ingredient.objects.select_related().filter(recipe=recipe.id)
        return render(request, 'description.html', {'recipe': recipe, 'ingredients': recipe_ingredients})
    else:
        form = IngredientForm()
    return render(request, 'ingredients.html', {'form': form})


def recipe_book(request):
    books = RecipeBook.objects.all
    return render(request, 'recipe_book.html', {'books': books})


def recipes(request):
    try:
        book_title = request.GET.get('book', '')
        book = RecipeBook.objects.get(title=book_title)
        book_recipes = Recipe.objects.select_related().filter(recipe_book=book.id)
    except:
        book_recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': book_recipes})


def tags(request):
    all_tags = Tag.objects.all
    return render(request, 'tags.html', {'tags': all_tags})


def tag(request):
    tag_name = request.GET.get('name', '')
    tag_recipes = Recipe.objects.filter(tags__name=tag_name)
    return render(request, 'recipes.html', {'recipes': tag_recipes})


def add_favourite(request):
    recipe_title = request.GET.get('title', '')
    recipe = Recipe.objects.filter(title=recipe_title)
    user = request.user
    profile = Profile.objects.get(user__username=user)
    profile.recipes.add(recipe[0])
    favourites_recipes = profile.recipes.all()
    return render(request, 'favourites.html', {'recipes': favourites_recipes})


def favourites(request):
    user = request.user
    profile = Profile.objects.get(user__username=user)
    favourites_recipes = profile.recipes.all()
    return render(request, 'favourites.html', {'recipes': favourites_recipes})
