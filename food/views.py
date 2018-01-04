# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pandas as pd
import sys
from django.shortcuts import render
from food.forms import IngredientForm
import contentBased.contentBased as cB


# Create your views here.


def ingredients(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredients_str = form.cleaned_data.get('ingredients')

            # Recomender system (content based)
            data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";")
            data.head(3)
            content_based = cB.ContentBased()
            content_based.fit(data, 'recipe_str')
            predict = content_based.predict([ingredients_str])
            recipes = predict.get('title').values

            return render(request, 'recipes.html', {'recipes': recipes})
    else:
        form = IngredientForm()
    return render(request, 'ingredients.html', {'form': form})
