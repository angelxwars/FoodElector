# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from django.contrib.auth import login, authenticate, logout

from profiles.forms import RegisterForm
from profiles.models import Profile, Search
from scraping.populate import populate
from food.models import Recipe

import contentBased.contentBased as cB
import pandas as pd

import random


"""def index(request):
    if request.user.is_authenticated:
        suggestion = 4
        recipes = []
        user = request.user
        profile = Profile.objects.get(user__username=user)
        search_profile = Search.objects.filter(profile=profile)
        annadidosB = []
        if len(search_profile) > 0:
            try: #Intentamos hacerlo con las tres ultimas busquedas, si tiene menos busquedas saltara la excepcion, y lo haremos con la unica que tenga
                for i in range(suggestion):
                    random_num = random.randint(0, len(search_profile)-1)
                    #try:
                    #if randomNume in annadidosB:
                        #while randomNume in annadidosB:
                            #randomNume = random.randint(0, len(search) - 1)
                    annadidosB.append(random_num)
                    search_random = search_profile[random_num]
                    ingredients_str = search_random.tags
                    # Recomender system (content based)
                    data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";", encoding='latin-1')
                    data.head(3)
                    content_based = cB.ContentBased()
                    content_based.fit(data, 'recipe_str')
                    predict = content_based.predict([ingredients_str])
                    recipes_predict = predict.get('title').values
                    reci = recipes_predict.tolist()
                    if len(recipes_predict) > 0:
                        #vamos a añadir una recomendacion aleatoria dentro de las que nos da el algoritmo
                        randomNum = random.randint(0, len(reci)-1)
                        if reci:
                            recipes.append(reci[randomNum])
                        print(recipes)
            except:
                recipes = []
                search = Search.objects.filter(profile=profile)
                s = search[0]
                ingredients_str = s.tags
                # Recomender system (content based)
                data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";", encoding='latin-1')
                data.head(3)
                content_based = cB.ContentBased()
                content_based.fit(data, 'recipe_str')
                predict = content_based.predict([ingredients_str])
                recipesPredict = predict.get('title').values
                #vamos a añadir una recomendacion aleatoria dentro de las que nos da el algoritmo
                numerosSugeridos = []

                predic = recipesPredict.tolist()
                if len(predic) > suggestion:
                    usados = []
                    for i in range(suggestion):
                        randomNum = random.randint(0, len(recipes))
                        if randomNum in numerosSugeridos:
                            while randomNum in numerosSugeridos:
                                randomNum = random.randint(0, len(recipes))
                        numerosSugeridos.append(randomNum)
                        print(randomNum)
                        recipes.append(predic[randomNum])
                        if len(numerosSugeridos) == len(predic):
                            break
                else:
                    recipes = predic
            recetario = []
            for recipe in recipes:
                try:
                    a = Recipe.objects.get(title=recipe)
                    recetario.append(a)
                except:
                    a = Recipe.objects.filter(title=recipe)
                    recetario.append(a[0])

            return render(request, 'index.html', {'username': request.user.username, 'recomendation': recetario})
        else: #Esto seria en el caso que sea un user nuevo sin ninguna busqueda
            return render(request, 'index.html', {'username': request.user.username})
    return render(request, 'index.html', {'username': request.user.username})"""


def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'index.html', {'username': request.user.username})
        else:
            recipes_csv = []
            recipes = []
            user = request.user
            profile = Profile.objects.get(user__username=user)
            search_profile = Search.objects.filter(profile=profile)
            if len(search_profile) > 0:
                if len(search_profile) == 1:
                    random_search = search_profile[0]
                    ingredients_str = random_search.tags
                    # Recomender system (content based)
                    data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";", encoding='latin-1')
                    data.head(3)
                    content_based = cB.ContentBased()
                    content_based.fit(data, 'recipe_str')
                    predict = content_based.predict([ingredients_str])
                    recipes_predict = predict.get('title').values
                    recipe_list = recipes_predict.tolist()
                    recipes_random = recipe_list
                    recipes_csv = recipes_csv + recipes_random
                elif len(search_profile) == 2:
                    random_search = random.choice(search_profile)
                    ingredients_str = random_search.tags
                    # Recomender system (content based)
                    data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";", encoding='latin-1')
                    data.head(3)
                    content_based = cB.ContentBased()
                    content_based.fit(data, 'recipe_str')
                    predict = content_based.predict([ingredients_str])
                    recipes_predict = predict.get('title').values
                    recipe_list = recipes_predict.tolist()
                    recipes_random = recipe_list
                    recipes_csv = recipes_csv + recipes_random
                elif len(search_profile) == 3 or len(search_profile) == 4:
                    random_search = random.sample(list(search_profile), 2)
                    for search in random_search:
                        ingredients_str = search.tags
                        # Recomender system (content based)
                        data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";", encoding='latin-1')
                        data.head(3)
                        content_based = cB.ContentBased()
                        content_based.fit(data, 'recipe_str')
                        predict = content_based.predict([ingredients_str])
                        recipes_predict = predict.get('title').values
                        recipe_list = recipes_predict.tolist()
                        recipe_random = random.sample(recipe_list, 2)
                        recipes_csv = recipes_csv + recipe_random
                else:
                    random_search = random.sample(list(search_profile), 4)
                    for search in random_search:
                        ingredients_str = search.tags
                        # Recomender system (content based)
                        data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";", encoding='latin-1')
                        data.head(3)
                        content_based = cB.ContentBased()
                        content_based.fit(data, 'recipe_str')
                        predict = content_based.predict([ingredients_str])
                        recipes_predict = predict.get('title').values
                        recipe_list = recipes_predict.tolist()
                        recipe_random = random.choice(recipe_list)
                        recipes_csv.append(recipe_random)

                for recipe in recipes_csv:
                    try:
                        a = Recipe.objects.get(title=recipe)
                        recipes.append(a)
                    except:
                        a = Recipe.objects.filter(title=recipe)
                        recipes.append(a[0])

                return render(request, 'index.html', {'username': request.user.username, 'recomendation': recipes})
            else:
                return render(request, 'index.html', {'username': request.user.username})
    return render(request, 'index.html', {'username': request.user.username})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            name = form.cleaned_data.get('name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            # Save user
            user = authenticate(username=username, password=raw_password)

            # Save profile
            profile = Profile(user=user, name=name, last_name=last_name, email=email)
            profile.save()

            login(request, user)
            return redirect(index)
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def Populate(request):
    number = populate()
    return render(request, 'populate.html', {'numero': number})
