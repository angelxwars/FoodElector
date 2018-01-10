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



def index(request):
    if request.user.is_authenticated:
        sugerencias = 4
        recipes = []
        user = request.user
        profile = Profile.objects.get(user__username=user)
        search = Search.objects.filter(profile=profile)
        for cb in search:
            print("busquedas: " + str(cb))
        if len(search)>0:
            try: #Intentamos hacerlo con las tres ultimas busquedas, si tiene menos busquedas saltara la excepcion, y lo haremos con la unica que tenga
                for i in range(sugerencias):
                    print("-----------------------------------------------------------  " + str(i))
                    s = search[i]
                    print(s.tags)
                    ingredients_str = s.tags
                    # Recomender system (content based)
                    data = pd.read_csv('scraping/recipes.csv', error_bad_lines=False, delimiter=";", encoding='latin-1')
                    data.head(3)
                    content_based = cB.ContentBased()
                    content_based.fit(data, 'recipe_str')
                    predict = content_based.predict([ingredients_str])
                    recipesPredict = predict.get('title').values
                    reci = recipesPredict.tolist()
                    if len(recipesPredict)>0:
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
                numerosSugeridos=[]
                randomNum = 0
                predic = recipesPredict.tolist()
                if len(predic)>sugerencias:
                    for i in range(sugerencias):
                        try:
                            while randomNum in numerosSugeridos:
                                randomNum = random.randrange(len(recipes))
                        except:
                            randomNum = random.randrange(len(recipes))
                        recipes.append(predic[randomNum])
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

            return render(request, 'index.html', {'username': request.user.username, 'recomendation':recetario})
        else: #Esto seria en el caso que sea un user nuevo sin ninguna busqueda
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
    numero = populate()
    return render(request, 'populate.html', {'numero':numero})
