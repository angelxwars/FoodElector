# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pandas as pd
import sys
from django.shortcuts import render
from food.forms import IngredientForm
import contentBased.contentBased as cB
from food.models import Recipe, Ingredient, RecipeBook, Tag
from profiles.models import Profile


# Create your views here.


def ingredients(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        busqueda = request.POST.get('ingredients', '')
        usuario = request.user
        user = Profile.objects.get(user__username=usuario)
        search = user.searches
        searchesToSet = search + ", " +  busqueda
        setattr(user, 'searches', searchesToSet)
        user.save()
        if form.is_valid():
            recetario = list()
            ingredients_str = form.cleaned_data.get('ingredients')
            # Recomender system (content based)
            data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";")
            data.head(3)
            content_based = cB.ContentBased()
            content_based.fit(data, 'recipe_str')
            predict = content_based.predict([ingredients_str])
            recipes = predict.get('title').values
            #Cojemos los objetos de django, para obtener la id de las recetas
            #Tengo que repopular, porque hay recetas que no guarda
            for recipe in recipes:
                try:
                    a = Recipe.objects.get(title=recipe)
                    recetario.append(a)
                except:
                    a = Recipe.objects.filter(title=recipe)
                    receta = a[0]
                    recetario.append(a[0])
            return render(request, 'recipes.html', {'recipes': recetario})
        else:
            if busqueda != '':
                recetario = list()
                ingredients_str = busqueda
                # Recomender system (content based)
                data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";")
                data.head(3)
                content_based = cB.ContentBased()
                content_based.fit(data, 'recipe_str')
                predict = content_based.predict([ingredients_str])
                recipes = predict.get('title').values
                # Cojemos los objetos de django, para obtener la id de las recetas
                # Tengo que repopular, porque hay recetas que no guarda
                for recipe in recipes:
                    try:
                        a = Recipe.objects.get(title=recipe)
                        recetario.append(a)
                    except:
                        a = Recipe.objects.filter(title=recipe)
                        recetario.append(a[0])
                return render(request, 'recipes.html', {'recipes': recetario})
    else:
        form = IngredientForm()
    return render(request, 'ingredients.html', {'form': form})

def description(request):
    if request.method == 'GET':
        id = request.GET.get('id', '')
        recipe = Recipe.objects.get(id=id)
        ingredients = Ingredient.objects.select_related().filter(recipe=recipe.id)
        return render(request, 'description.html', {'recipe': recipe, 'ingredients':ingredients})
    else:
        form = IngredientForm()
    return render(request, 'ingredients.html', {'form': form})

def recipe_book(request):
    books = RecipeBook.objects.all
    return render(request, 'recipe_book.html', {'books': books})

def recipes(request):
    try:
        bookTitle = request.GET.get('book','')
        book = RecipeBook.objects.get(title=bookTitle)
        recipes = Recipe.objects.select_related().filter(recipe_book=book.id)
    except:
        recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})

def tags(request):
    tags = Tag.objects.all
    return render(request, 'tags.html', {'tags': tags})


def tag(request):
    tagName = request.GET.get('name', '')
    recipes = Recipe.objects.filter(tags__name=tagName)
    return render(request, 'recipes.html', {'recipes': recipes})