# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from django.contrib.auth import login, authenticate, logout

from profiles.forms import RegisterForm, LoginForm
from profiles.models import Profile, Search
from scraping.populate import populate
from food.models import Recipe

import contentBased.contentBased as cB
import pandas as pd

import random


def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'index.html', {'username': request.user.username})
        else:
            recipes_csv = []
            recipes = []
            user = request.user
            user_profile = Profile.objects.get(user__username=user)
            search_profile = Search.objects.filter(profile=user_profile)
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
                        data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";",
                                           encoding='latin-1')
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
                    print(search_profile)
                    for search in random_search:
                        ingredients_str = search.tags
                        print(ingredients_str)

                        # Recomender system (content based)
                        data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";",
                                           encoding='latin-1')
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


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(index)
            else:
                form = LoginForm()
                return render(request, 'registration/login.html', {'form': form, 'error': 'Datos incorrectos, vuelva a introducirlos'})
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


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
            user_profile = Profile(user=user, name=name, last_name=last_name, email=email)
            user_profile.save()

            login(request, user)
            return redirect(index)
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def profile(request):
    user = request.user
    user_profile = Profile.objects.get(user__username=user)
    user_searches = list(Search.objects.filter(profile=user_profile))
    if len(user_searches) < 5:
        user_last_searches = list(reversed(user_searches))
    else:
        user_last_searches = list(reversed(user_searches[len(user_searches)-5: len(user_searches)]))

    context = {
        'user': user,
        'profile': user_profile,
        'searches': user_last_searches}

    return render(request, 'profile.html', context)


def search(request):
    if request.method == 'GET':
        search_id = request.GET.get('id', '')
        user_search = Search.objects.get(id=search_id)
        ingredients_str = user_search.tags
        # Recomender system (content based)
        data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";", encoding='latin-1')
        data.head(3)
        content_based = cB.ContentBased()
        content_based.fit(data, 'recipe_str')
        predict = content_based.predict([ingredients_str])
        recipes_predict = predict.get('title').values
        recipe_list_predict = recipes_predict.tolist()
        recipes = []
        for recipe in recipe_list_predict:
            queryset_list = Recipe.objects.filter(title=recipe)
            if queryset_list.count() != 0:
                recipes = recipes + list(queryset_list)

        if len(recipes) > 4:
            recipes_temp = recipes
            recipes = recipes_temp[0:3]

        return render(request, 'recipes.html', {'recipes': recipes})
    else:
        return redirect(index)


def populatedb(request):
    number = populate()
    return render(request, 'populate.html', {'number': number})
