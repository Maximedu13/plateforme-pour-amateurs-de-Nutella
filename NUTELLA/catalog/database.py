""" algorithm to insert the products """
import json
import re
import requests
from catalog.models import Category, Product
# pylint: disable=no-member

def insert():
    """Insert categories, products in database"""
    global categories
    categories = ['Sauces au roquefort', 'Œufs', 'Beurres', \
    'Muffins au chocolat', 'Bœuf', 'Beurres de cacahuètes', 'Pâtes à tartiner au chocolat']
    for category in categories:
        Category.objects.get_or_create(name=category)
        cats = Category.objects.all()
        formatted_cats = ["{}".format(cat.name) for cat in cats]
        if not cats:
            for cat in formatted_cats:
                r = requests.get\
                    ("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0= \
                    categories&tag_contains_0=contains&tag_0=" + cat + \
                    "&sort_by=unique_scans_n&page_size=1000&axis_x=energy&axis_y= \
                    products_n&action=display&json=1")
                result = json.loads(r.text)
                for i in range(len(result["products"])):
                    try:
                        name = result["products"][i]["product_name_fr"]
                        if result["products"][i]["product_name_fr"] == "" or \
                        not result["products"][i]["product_name_fr"]:
                            name = result["products"][i]["product_name"]
                        if not result["products"][i]["product_name"]:
                            pass
                        description = result["products"][i]["generic_name"]
                        if not result["products"][i]["generic_name"]:
                            description = ""
                        nutriscore = (result["products"][i]["nutrition_grade_fr"]).upper()
                        if not result["products"][i]["nutrition_grade_fr"]:
                            nutriscore = result["products"][i]["nutrition_grades"]
                            if not result["products"][i]["nutrition_grades"]:
                                pass
                        stores = result["products"][i]["stores"]
                        image = result["products"][i]["image_small_url"]
                        brand = result["products"][i]["brands"]
                        calories = float(result["products"][i]["nutriments"]["energy_100g"])
                        # Kilojoules(kJ) to calories(cal)
                        calories /= 4.184
                        calories = calories.__round__(2)
                        lipids = result["products"][i]["nutriments"]["fat_100g"]
                        sugars = result["products"][i]["nutriments"]["sugars_100g"]
                        proteins = result["products"][i]["nutriments"]["proteins_100g"]
                        salts = result["products"][i]["nutriments"]["salt_100g"]
                        url_off = result["products"][i]["url"]
                        category_id = result["products"][i]["categories"]
                        for category in categories:
                            regex(category, category_id)
                            global id
                        Product.objects.get_or_create(name=name, description=description,
                                                      nutriscore=nutriscore, stores=stores,
                                                      image=image, brand=brand, calories=calories,
                                                      lipids=lipids, sugars=sugars,
                                                      proteins=proteins,
                                                      salts=salts, url_off=url_off, category_id=id)
                    except:
                        pass

def regex(category, string):
    """Find the category id"""
    match = re.search(category, string)
    if match:
        global id
        id = categories.index(match.group(0)) + 1

def results(product_id):
    """Interprate results"""
    id = int(product_id)
    this_product = Product.objects.get(pk=id)
    this_product.proteins = this_product.proteins.__round__(2)
    this_product.formatted_proteins = \
    "Protéines : {} g/100g".format(this_product.proteins.__round__(2))
    this_product.formatted_calories = \
    "Calories : {} kCal/100g".format(this_product.calories.__round__(2))
    this_product.salts = this_product.salts.__round__(2)
    this_product.formatted_salts = "Sel : {} g/100g".format(this_product.salts)
    this_product.formatted_lipids = "Lipides : {} g/100g".format(this_product.lipids.__round__(2))
    this_product.sugars = this_product.sugars.__round__(2)
    this_product.formatted_sugars = "Sucres : {} g/100g".format(this_product.sugars.__round__(2))
    salts_percentage = this_product.salts * 100 / 2.3
    salts_percentage = str(salts_percentage) + "%"
    proteins_percentage = this_product.proteins * 100 / 16
    proteins_percentage = str(proteins_percentage) + "%"
    sugars_percentage = this_product.sugars * 100 / 45
    sugars_percentage = str(sugars_percentage) + "%"
    lipids_percentage = this_product.lipids * 100 / 60
    lipids_percentage = str(lipids_percentage) + "%"
    calories_percentage = this_product.calories * 100 / 560
    calories_percentage = str(calories_percentage) + "%"
    low = "Peu"
    medium = "Un peu trop"
    high = "Trop"
    space = " "
    adjective_calories = "calorique"
    adjective_sugars = "sucré"
    adjective_salts = "salé"
    adjective_proteins = "protéiné"
    adjective_lipids = "lipidique"

    if this_product.calories < 560 /3:
        result_nutri_score_cal = low + space + adjective_calories
    elif this_product.calories >= 560 / 3 and this_product.calories <= 560 / 2:
        result_nutri_score_cal = medium + space + adjective_calories
    else:
        result_nutri_score_cal = high + space + adjective_calories

    if this_product.proteins < 16/3:
        result_nutri_score_pro = low + space + adjective_proteins
    elif this_product.proteins >= 16/3 and this_product.proteins <= 16/2:
        result_nutri_score_pro = "Un peu " + adjective_proteins
    else:
        result_nutri_score_pro = "Bonne source de protéines"
    if this_product.lipids < 60/3:
        result_nutri_score_lpds = low + space + adjective_lipids
    elif this_product.lipids >= 60/3 and this_product.lipids <= 60/2:
        result_nutri_score_lpds = medium + space + adjective_lipids
    else:
        result_nutri_score_lpds = high + space + adjective_lipids
    if this_product.salts < 2.3/3:
        result_nutri_score_salts = low + space + adjective_salts
    elif this_product.salts >= 2.3/3 and this_product.salts <= 2.3/2:
        result_nutri_score_salts = medium + space + adjective_salts
    else:
        result_nutri_score_salts = high + space + adjective_salts
    if this_product.sugars < 45/3:
        result_nutri_score_sugars = low + space + adjective_sugars
    elif this_product.sugars >= 45/3 and this_product.sugars <= 45/2:
        result_nutri_score_sugars = medium + space + adjective_sugars
    else:
        result_nutri_score_sugars = high + space + adjective_sugars

    message = {
        'this_product' : this_product,
        'lipids_percentage' : lipids_percentage,
        'calories_percentage' : calories_percentage,
        'salts_percentage' : salts_percentage,
        'result_nutri_score_cal' : result_nutri_score_cal,
        'result_nutri_score_pro' : result_nutri_score_pro,
        'result_nutri_score_salts' : result_nutri_score_salts,
        'result_nutri_score_sugars' : result_nutri_score_sugars,
        'result_nutri_score_lpds' : result_nutri_score_lpds,
        'proteins_percentage' : proteins_percentage,
        'sugars_percentage' : sugars_percentage
    }
    return message
