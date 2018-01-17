"""FoodElector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout
from FoodElector import settings

from profiles import views as profiles_views
from food import views as food_views

urlpatterns = [

    # General
    url(r'^admin/', admin.site.urls),
    url(r'^$', profiles_views.index, name="index"),
    url(r'^populate/$', profiles_views.populate, name='populate'),

    # User and profile
    url(r'^login/', profiles_views.login_view, name="login"),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^register/$', profiles_views.register, name='register'),
    url(r'^profile/$', profiles_views.profile, name='profile'),
    url(r'^search/$', profiles_views.search, name='search'),


    # FoodElector
    url(r'^ingredients/', food_views.ingredients, name="ingredients"),
    url(r'^description/$', food_views.description, name="description"),
    url(r'^recipebook/$', food_views.recipe_book, name="recipebook"),
    url(r'^recipes/$', food_views.recipes, name="recipes"),
    url(r'^tags/$', food_views.tags, name="tags"),
    url(r'^tag/$', food_views.tag, name="tag"),
    url(r'^addfavorite/', food_views.annadirfavoritos, name="addfavorite"),
    url(r'^favorites/', food_views.favorites, name="favorites"),
]
