from food.models import Tag, RecipeBook, Recipe, Ingredient
from django.db.transaction import atomic
from django.core.exceptions import ObjectDoesNotExist
import re


@atomic
def populate():
    print("Loading Data...")
    Recipe.objects.all().delete()
    Ingredient.objects.all().delete()
    Tag.objects.all().delete()
    RecipeBook.objects.all().delete()

    file = open("scraping/recipes.csv", "r", encoding='latin-1')
    i = 0
    line = file.readline()

    while line:
        print("--------------------------------------------------------------------------------------")
        print(line)
        # El csv se esta guardando una linea en blanco, por lo que hacemos el contador para solo coger
        # las impares que tienen linea
        i = i+1

        if i != 1:
            if i%2!=0:
                recipebook = ""
                occ = line.split(";")
                print(occ)
                title = occ[0].strip()
                image = occ[1].strip()
                # Elimino el primer elemento de los ingredientes ya que es un elemento en blanco,
                # al empezar el string por "|"
                ing = occ[2].strip().split("|")
                tags = occ[3].strip().replace("[", "").replace("]", "").replace("'", "").split(",")
                cook_url = occ[4].strip()
                recipebookTitle = occ[6].strip()
                try:
                    recipeBook = RecipeBook.objects.get(title=recipebookTitle)
                except ObjectDoesNotExist:
                    recipeBook = RecipeBook.objects.create(title=recipebookTitle, link=cook_url)

                recipe = Recipe.objects.create(title=title, image=image, recipe_book=recipeBook)

                for tag in tags:
                    try:
                        t = Tag.objects.get(name=tag)
                    except ObjectDoesNotExist:
                        t = Tag.objects.create(name=tag)
                    recipe.tags.add(t)

                for ingredient in ing:
                    Ingredient.objects.create(name=ingredient, recipe=recipe)
        line = file.readline()
    print("Se ha populado " + str(Recipe.objects.count()) + "recetas.")
    return Recipe.objects.count()
