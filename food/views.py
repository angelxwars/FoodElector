# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pandas as pd
import sys
from django.shortcuts import render
from food.forms import IngredientForm
import contentBased.contentBased as cB
from food.models import Recipe, Ingredient, RecipeBook


# Create your views here.


def ingredients(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
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
                    print ("Fallo en: " + recipe)


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
        for recipe in recipes:
            print( recipe.title)
    except:
        recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})