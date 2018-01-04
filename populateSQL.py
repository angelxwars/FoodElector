import sqlite3



path = "recipes.csv"
def populate():
    conn = sqlite3.connect('FoodElector.db')
    conn.text_factory = str
    cursor = conn.cursor()
    print("La base de datos se ha abierto correctamente")
    conn.execute("PRAGMA busy_timeout = 30000")
    print("Loading Data...")

    idRecipe = 1
    idIngredient = 1
    idTag = 1
    idRecipeTag = 1

    file = open("recipes.csv" , "r")
    i=2
    line = file.readline()
    # Creo un recipeBook, ya que no se guarda en el csv, y siempre voy a añadir este
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO FOOD_RECIPEBOOK (ID, TITLE, LINK) VALUES(?,?,?)""", (1, "Titulo", "URL"))
    while line:
        #El csv se esta guardando una linea en blanco, por lo que hacemos el contador para solo coger las impares que tienen linea
        i = i+1
        if (i%2==1):
            occ = line.split("#")
            title = occ[0].strip()
            image = occ[1].strip()
            #Elimino el primer elemento de los ingredientes ya que es un elemento en blanco, al empezar el string por |
            ing = occ[2].strip().split("|")
            a = ing[0]
            ingredients = ing.remove(a)
            tags = occ[3].strip().replace("[","").replace("]","").replace("'", "").split(",")
            cook_url = occ[4].strip()
            cursor.execute("""INSERT INTO FOOD_RECIPE (ID, TITLE, IMAGE, RECIPE_BOOK_ID) VALUES(?,?,?,?)""", (idRecipe, title, image, 1))
            for tag in tags:
                try:
                    cursor.execute("""SELECT id FROM FOOD_TAG WHERE NAME=?""", tag)
                    idTagCreado = cursor.fetchone()
                    cursor.execute("""INSERT INTO FOOD_RECIPE_TAGS (ID, RECIPE_ID, TAG_ID) VALUES(?,?,?)""", idRecipeTag, idRecipe, idTagCreado)
                except :
                    cursor.execute("""INSERT INTO FOOD_TAG (ID, NAME) VALUES(?,?)""", idTag, tag)
                    cursor.execute("""INSERT INTO FOOD_RECIPE_TAGS (ID, RECIPE_ID, TAG_ID) VALUES(?,?,?)""", idRecipeTag, idRecipe, idTag)
                    idtag = idTag+1
            for ingredient in ing:
                cursor.execute("""INSERT INTO FOOD_INGREDIENT (ID, NAME, RECIPE_ID) VALUES(?,?,?)""", idIngredient, ingredient, idRecipe)
                idIngredient = idIngredient + 1
            print("---------------------------------------------------------")
            idRecipe = idRecipe + 1

        line = file.readline()
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM food_recipe")
    print("Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()


populate()
