# This program reads in information from a file containing foods and their
# nutritional information and helps the user calculate exactly how many
# calories are in a recipe they are making.
# file is in the following format:
# name, calories, #calories, fat, #fat, protein, #protein, carbohydrate,
# #carbohydrate, fiber, #fiber, sugars, #sugars
# all of the # items are the amount of that item, in GRAMS.


def main():
    introduction()
    food_list = sort_file("Food List.txt")
    food_dict = get_food_dict(food_list)
    next_task = int(input("What would you like to do next? "))
    while next_task != 3:
        if next_task == 1:
            # creates the recipe
            recipe = create_recipe(food_dict)
            if len(recipe) >= 1:
                print("Real fast before we calculate all of the nutritional information,")
                print("I want to make sure we have all of your ingredients and")
                print("their amounts correct. This is what I have for you so far:")
                print()
                # checks whether the user input the correct recipe they want
                correct = recipe_checker(recipe)
                # Allows them to change it until it is correct
                while correct == False:
                    correct = change_recipe(food_dict, recipe)
                print()
                print("Awesome, now that we have your recipe, lets calculate the nutritional information you need to know about your recipe. But first, we need a bit more information to do the calculations.")
                print()
                servings = float(input("How many servings are there in your recipe? (type a number): "))
                print()
                # Gets a list of all the nutritional ingredients from recipe
                nutrition_info = get_nutritional_info(food_dict, recipe, servings)
                # outputs the information
                nutritional_output(nutrition_info, servings, recipe)
        # Once they are finished, asks if they want to add that recipe to
        # their recipe booklet for later use.
        if next_task == 0:
            add_to_dictionary(food_dict)
            return True
        print("Here are those options again for you...")
        decisions()
        next_task = int(input("What would you like to do next? "))


# Briefuly describes what the prorgram does to the user.
# PARAMS:   none
# RETURNS:  none
def introduction():
    print("Hey there! Welcome to the nutritional calculator / recipe creator!")
    print()
    print("This program makes it easy to figure out exactly how many calories")
    print("are in your homemade recipes! Just input an ingredient, how much")
    print("of that ingredient you used, and the weight measurement")
    print("you used (ounces, grams, or pounds).")
    print()
    decisions()


# Outputs the possible options that the user can do.
# PARAMS:   none
# RETURNS:  none
def decisions():
    print("1)  creates a new recipe to gather nutrition info.")
    print("    It also can output the recipe, (along with the")
    print("    instructions) to a file of your choice. Also asks the user if")
    print("    they have a particular calorie count in mind and will alert")
    print("    the user if they have surpassed this amount for the recipe")
    print()
    print("2)  picks random ingredients for you to experiment")
    print("    with to try and create a very unique recipe ")
    print()
    print("3)  quit the program")
    print()


# This function opens the file with all of the ingredients, and puts it into
# a list of foods.
# PARAMS:   'file_name' is the name of the file witht he foods. (Food_List.txt)
# RETURNS:   'food_list' which is a list of lists, where each list is a food
# item
def sort_file(file_name):
    food_list = []
    file = open(file_name)
    food = file.readlines()
    # splits the file into a 2D list and strips whitespace and splits on commas
    for i in range(len(food)):
        food_info = food[i].strip().split(",")

        food_list.append(food_info)
    # gets rid of the extra space at the beginning of each word in the list
    for i in range(len(food_list)):
        for j in range(len(food_list[i])):
            food_list[i][j] = food_list[i][j].strip()
    # turns the numbers into integers to be used in later calculations
    for i in range(len(food_list)):
        for j in range(2, len(food_list[i]), 2):
            food_list[i][j] = float(food_list[i][j])

    return food_list


# This function takes the food_list and makes a dictionary of another dictionary
# with the food name as the key, and the second dictionary its values. Where
# each value is information on that piece of food.
# PARAMS:   'food-list' which is a list of lists, where each list is a food
# item
# RETURNS:  'food_dict' which is a dictionary of another dictionary
# with the food name as the key, and the second dictionary as its
# values where each value is information on that piece of food
def get_food_dict(food_list):
    food_dict = {}
    for i in range(len(food_list)):
        food_name = food_list[i][0]
        if food_name not in food_dict:
            food_dict[food_name] = {}
            for j in range(1, len(food_list[i]), 2):
                info = food_list[i][j]
                amount = food_list[i][j + 1]
                food_dict[food_name][info] = amount

    return food_dict


# This function takes the amounts from the recipe the user made and calculates
# the calories per serving for the whole recipe.
# PARAMS:   'food_dict' which is the dictionary of dictionaries with the food
# name as the key of the dictionarym and its information on that piece of food
# as the value, which is also a dictionary, 'recipe' which is list of tuples,
# each tuple is like this (ingredient, amount, weight type), weight type can
# be grams, pounds, or ounces, 'servings' is the number of servings that the
# recipe makes.
# RETURNS:  'nutrition_list' which is a list of the total number of calories,
# fat, protein, carbohydrates, fiber, and sugars in a list (in that order)
# divided by the number of servings to give you the amount of each item per
# serving.
def get_nutritional_info(food_dict, recipe, servings):
    nutrition_list = [0] * 6
    for i in range(len(recipe)):
        unit = recipe[i][2]
        amount = recipe[i][1]
        ingredient = recipe[i][0]
        info = food_dict[ingredient]
        if unit[0].lower() == "g":
            multiplier = 1
        elif unit[0].lower() == "o":
            multiplier = 28.349
        else:
            multiplier = 453.592
        # CONVERTS TO APPROPRIATE WEIGHT UNIT AND REPLACE THE NUTRITION_LIST WITH THE CALCULATED AMOUNTS
        nutrition_list[0] += food_dict[ingredient]["calories"] * (amount * multiplier)
        nutrition_list[1] += food_dict[ingredient]["fat"] * (amount * multiplier)
        nutrition_list[2] += food_dict[ingredient]["protein"] * (amount * multiplier)
        nutrition_list[3] += food_dict[ingredient]["carbohydrates"] * (amount * multiplier)
        nutrition_list[4] += food_dict[ingredient]["fiber"] * (amount * multiplier)
        nutrition_list[5] += food_dict[ingredient]["sugars"] * (amount * multiplier)
    for i in range(len(nutrition_list)):
        nutrition_list[i] = round(nutrition_list[i] / servings, 1)

    return nutrition_list


# This function outputs the recipe to a recipe book if you would like to make
# that recipe again so you don't have to run the program again.
# PARAMS:   'nutrition_info' is the list of the amount of each type (calories,
# protein, etc) in that recipe, 'servings' is the amount of servings in the
# whole recipe, 'recipe' is the ingredients in the recipe and their amounts,
# they are in a list and stored as (ingredient, amount, weight_type).
# RETURNS:  none, simply outputs to a file.)
def output_recipe(nutrition_info, servings, recipe):
    out_file = open("recipe book.txt", "a")
    name = input("What would you like to call this recipe? ")
    print("Recipe Name: " + str(name.title()), file=out_file)
    print(file=out_file)
    print("Ingredients:", file=out_file)
    print(file=out_file)

    for i in range(0, len(recipe)):
        ingredient = recipe[i][0]
        amount = recipe[i][1]
        unit = recipe[i][2]
        if unit[0].lower() == "g":
            multiplier = 1
            ounces = amount / 28.349
        elif unit[0].lower() == "o":
            multiplier = 28.349
            ounces = amount
        else:
            multiplier = 453.592
            ounces = amount * 16
        grams = round(amount * multiplier, 1)
        ounces = round(ounces, 1)
        print(str(ingredient.title()) + " " * (30 - len(ingredient)) + ": " + str(grams) + " grams / " + str(ounces) + " ounces", file=out_file)
    print(file=out_file)
    print()
    print()
    print("Calories.           : " + str(nutrition_info[0]), file=out_file)
    print("Total Fat           : " + str(nutrition_info[1]) + " grams", file=out_file)
    print("Total Protein.      : " + str(nutrition_info[2]) + " grams", file=out_file)
    print("Total Carbohydrates : " + str(nutrition_info[3]) + " grams", file=out_file)
    print("Total Fiber         : " + str(nutrition_info[4]) + " grams", file=out_file)
    print("Total Sugars        : " + str(nutrition_info[5]) + " grams", file=out_file)
    print(file=out_file)
    print("Servings per recipe: " + str(servings), file=out_file)
    print(file=out_file)
    print("___________________________________________________________________", file=out_file)
    print(file=out_file)
    print()

    out_file.close()


# This function prints all of the information about the recipe to the console.
# it then prompsts whether or not the user would like to add this recipe
# to their recipe book.
# PARAMS:   'nutrition_info' is the list of the amount of each type (calories,
# protein, etc) in that recipe, 'servings' is the amount of servings in the
# whole recipe, 'recipe' is the ingredients in the recipe and their amounts,
# they are in a list and stored as (ingredient, amount, weight_type).
# RETURNS:  none, simply outputs to the console (and potentially a file).
def nutritional_output(nutrition_info, servings, recipe):
    print("Here is the nutritional information of your recipe! (PER SERVING)")
    print()
    print()
    print("Calories.           : " + str(nutrition_info[0]))
    print("Total Fat           : " + str(nutrition_info[1]) + " grams")
    print("Total Protein.      : " + str(nutrition_info[2]) + " grams")
    print("Total Carbohydrates : " + str(nutrition_info[3]) + " grams")
    print("Total Fiber         : " + str(nutrition_info[4]) + " grams")
    print("Total Sugars        : " + str(nutrition_info[5]) + " grams")
    print()
    print()
    print("Servings per recipe: " + str(servings))
    print()
    print()
    output = int(input("Would you like to add this recipe to your recipe / nutrition book? (type '1' for yes, '2' for no) "))
    if output == 1:
        output_recipe(nutrition_info, servings, recipe)
        print("done!")
        print()
        print()


# This function prompts the user for the ingredients they wish to use. It then
# asks for how much they used, and a type of weight unit, which is either
# pounds, ounces, or grams. It then builds a list of tuples with that info.
# PARAMS: 'food_dict' which is the dicionary with an ingredient as the key and
# a dictionary as its value where each piece of information about that
# ingredient is stored.
# RETURNS: 'recipe_list' which is a list of tuples containing the information
# about each ingredient in the recipe in the format of a tuple (ingredient,
# amount, weight_type).
def create_recipe(food_dict):
    recipe_list = []
    print()
    print()
    print()
    print("Let's get started!")
    print()
    ingredient = input("What's the first ingredient? (Type 'done' if finished): ").lower()
    while ingredient != "done":
        # This code creates a list of any of the food items in the dictionary
        # that contain the ingredient. i.e: 'tomato' and 'tomato sauce'.
        # It then tells the user there are a few items in the list that
        # contain the ingredient and ask for them to clarify before moving on.
        temp_food = []
        for key in food_dict:
            newkey = key.lower().split()
            if ingredient in newkey:
                temp_food.append(key)
        if len(temp_food) >= 2:
            print("Hmm, it looks like a few things have " +
                  str(ingredient) + ".")
            print()
            for i in range(len(temp_food)):
                print(str(i + 1) + ") " + str(temp_food[i]))
            print()
            ingredient = int(input
                             ("Which one of these did you mean (type the number): "))

            ingredient = temp_food[ingredient - 1]

        if ingredient in food_dict:
            print("How much will you use? ", end="")
            amount = float(input("(number without units): "))

            weight_type = input("What unit of weight? (grams, ounces, or pounds): ")
            recipe_list.append((ingredient, amount, weight_type))
            print()
        else:
            print("Hmm, can't seem to find that ingredient, lets try again..")
            print()

        print("What is the next ingredient? ", end="")
        ingredient = input("(type 'done' if you are finished with your recipe): ")
    print()
    print()
    print()
    return recipe_list


# Might make a function that makes sure the user types a correct float for the
# amount and other instances, but not as of yet.
def is_float(amount):
    pass


# This function goes through the recipe once the user has created it and asks
# the user to make sure it is correct. If not, it asks the user what they want
# to change about the recipe.
# PARAMS:   'recipe' is the ingredients in the recipe and their amounts,
# they are in a list and stored as (ingredient, amount, weight_type).
# RETURNS:  'True' if the recipe is now correct, 'False' if the recipe is still
# incorrect and they want to make more changes.
def recipe_checker(recipe):
    print()
    print()
    for i in range(0, len(recipe)):
        ingredient = recipe[i][0]
        amount = recipe[i][1]
        weight_unit = recipe[i][2]
        print(str(i + 1) + ") " + str(ingredient.title()) +
              " " * (35 - len(ingredient)) + str(amount)
              + " " + str(weight_unit))
    print()
    print()
    correct = int(input(
        "Does this look correct? (type '1' for yes, '2' for no): "))
    print()
    print()
    if correct == 1:
        return True
    else:
        return False


# This function performs the actual changes to the recipe if it is not correct.
# PARAMS:   'food_dict' which is the dicionary with an ingredient as the key
# and a dictionary as its value where each piece of information about that
# ingredient is stored. 'recipe' is the ingredients in the recipe and their
# amounts, they are in a list and stored as (ingredient, amount, weight_type).
# RETURNS: 'False' if the recipe still isn't correct and they want to make
# more changes, 'True' if the recipe is now correct.
def change_recipe(food_dict, recipe):
    print("I'm sorry there's a mistake on your recipe")
    print()
    for i in range(len(recipe)):
        ingredient = recipe[i][0]
        print(str(i + 1) + ") " + str(ingredient))
    print(str(i + 2) + ") add another ingredient to your recipe")
    print()
    print("Which one of these ingredients would you like to change? Or, you can add an ingredient to your recipe.", end="")
    change = int(input(" Type the number of the ingredient/action above): "))
    print()
    if change == i + 2:
        add_ingredient = add_single_ingredient(food_dict, recipe)
        while add_ingredient == False:
            add_ingredient = add_single_ingredient(food_dict, recipe)
    else:
        print("1) remove ingredient from the recipe.")
        print("2) change the amount of the ingredient in the recipe.")
        print("3) change the measure of weight (grams, ounces, pounds).")
        print()
        do_change = int(input("What would you like to change about your ingredient? (type a number from above): "))
        print()

        if do_change == 1:
            recipe.pop(change - 1)

        elif do_change == 2:
            amount = float(input("What do you want the new amount to be? (number only, not a word or measurement): "))
            ingredient = recipe[change - 1][0]
            new_amount = amount
            weight_unit = recipe[change - 1][2]
            new_tuple = (ingredient, new_amount, weight_unit)
            recipe[change - 1] = new_tuple

        elif do_change == 3:
            weight_unit = input("What do you want the new weight measurement to be?: ")
            ingredient = recipe[change - 1][0]
            amount = recipe[change - 1][1]
            new_weight_unit = weight_unit
            new_tuple = (ingredient, amount, new_weight_unit)
            recipe[change - 1] = new_tuple
        # This is secret option to add an element to the food list, more for
        # developers to use.
        elif do_change == 4:
            add_single_ingredient(food_dict, recipe)

    for i in range(0, len(recipe)):
        ingredient = recipe[i][0]
        amount = recipe[i][1]
        weight_unit = recipe[i][2]
        print(str(i + 1) + ") " + str(ingredient.title()) +
              " " * (35 - len(ingredient)) + str(amount)
              + " " + str(weight_unit))
    print()
    print("Here is your updated list..")
    print()
    print("Is that all that you wanted to change? Or was there", end="")
    correct = int(input(" something else you wanted to change? (type 1 to make more changes or 2 if your recipe is the way you want it): "))
    print()
    print()
    if correct == 1:
        return False
    elif correct == 2:
        return True


# This function adds a single ingredient to the recipe, if the user forgot
# to type the recipe correctly the first time.
# PARAMS:   'food_dict' which is the dicionary with an ingredient as the key
# and a dictionary as its value where each piece of information about that
# ingredient is stored, 'recipe' is the ingredients in the recipe and their
# amounts, they are in a list and stored as (ingredient, amount, weight_type).
# RETURNS: 'True' if the ingredient is in the list, 'False' if the ingredient
# is not in the list.
def add_single_ingredient(food_dict, recipe):
    temp_food = []
    ingredient = input("What is the name of the ingredient you would like to add? ").lower()
    for key in food_dict:
        newkey = key.lower().split()
        if ingredient in newkey:
            temp_food.append(key)

    if len(temp_food) >= 2:
        print("Hmm, it looks like a few things have " +
              str(ingredient) + ".")
        print()
        for i in range(len(temp_food)):
            print(str(i + 1) + ") " + str(temp_food[i]))
        print()
        ingredient = int(input
                         ("Which one of these did you mean (type the number): "))

        ingredient = temp_food[ingredient - 1]

    if ingredient in food_dict:
        print("How much will you use? ", end="")
        amount = float(input("(number without units): "))

        weight_type = input("What unit of weight? (grams, ounces, or pounds): ")
        recipe.append((ingredient, amount, weight_type))
        print()
        return True
    else:
        print("Hmm, can't seem to find that ingredient, sorry...")
        print()
        return False


# This function adds items to the list of foods file to increase the amount of
# foods, making this program more useful. Just for developers.
# PARAMS:   'food_dict' which is the dicionary with an ingredient as the key
# and a dictionary as its value where each piece of information about that
# ingredient is stored.
# RETURNS:  'none'
def add_to_dictionary(food_dict):
    ingredient = input("What ingredient would you like to add to your food list? (type 'done' to quit): ").lower()

    out_file = open("food list.txt", "a")
    while ingredient != "done":

        calories = float(input("how many calories per gram? "))
        fat = float(input("how much fat per gram? "))
        protein = float(input("how much protein per gram? "))
        carbohydrates = float(input("how many carbs per gram? "))
        fiber = float(input("how much fiber per gram? "))
        sugars = float(input("how much sugar per gram? "))

        print(str(ingredient) + str(","), "calories" + str(", ") + str(calories) + str(","), "fat" + str(", ") + str(fat) + str(","), "protein" + str(", ") + str(protein) + str(","), "carbohydrates" + str(", ") + str(carbohydrates) + str(","), "fiber" + str(", ") + str(fiber) + str(","), "sugars, " + str(sugars), file=out_file)

        ingredient = input("What ingredient would you like to add to your food list? (type 'done' to quit): ").lower()
    out_file.close()


main()
