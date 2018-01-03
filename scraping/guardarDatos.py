from food.models import Tag, RecipeBook, Recipe, Ingredient
from datetime import datetime
from django.db.transaction import atomic

path = "recipes.csv"
@atomic
def populatTag():
    print("Loading artists...")
    Tag.objects.all().delete()

    file = open(path , "r", encoding="utf8")

    line = file.readline()
    print("Esta es la linea: " + line)
    while line:
        occ = line.split(",")
        title = occ[0].strip()
        image = occ[1].strip()
        ingredients = occ[2].strip()
        tags = occ[3].strip()
        cook_url = occ[4].strip()

    if(title!="title"):
        RecipeBook.objects.create()
        Recipe.objects.create(title=title, )

    print("Esto son los tags" + tags)
    print("---------------------------------------------------------")
