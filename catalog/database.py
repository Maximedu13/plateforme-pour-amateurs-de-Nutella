
import requests
import json
import re
from catalog.models import Category, Product

def insert():
        global categories, category
        categories = ['Huile d‘olive d‘Aix-en-Provence', 'Sauces au roquefort', 'Œufs', 'Beurres', \
        'Muffins au chocolat', 'Bœuf', 'Beurres de cacahuètes', 'Saumons', 'Croissants au beurre']
        jac = "Beurres, Pommes noisettes et Huile d‘olive d‘Aix-en-Provence"
        for category in categories:
                Category.objects.get_or_create(name=category)
        cats = Category.objects.all()
        formatted_cats = ["{}".format(cat.name) for cat in cats]
        for cat in formatted_cats:
                r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0= \
                        categories&tag_contains_0=contains&tag_0=" + cat + \
                        "&sort_by=unique_scans_n&page_size=1000&axis_x=energy&axis_y=products_n&action= \
                        display&json=1")
                result = json.loads(r.text)
                print(result["products"][0]["nutrition_grade_fr"])
                for i in range(len(result["products"])):
                        try:    
                                name = result["products"][i]["product_name_fr"]
                                description = result["products"][i]["generic_name"]
                                nutriscore = result["products"][i]["nutrition_grade_fr"]
                                stores = result["products"][i]["stores"]
                                image = result["products"][i]["image_small_url"]
                                brand = result["products"][i]["brands"]
                                calories = float(result["products"][i]["nutriments"]["energy_100g"])
                                # Kilojoules(kJ) to calories(cal)
                                calories /= 4.184
                                lipids = result["products"][i]["nutriments"]["fat_100g"]
                                sugars = result["products"][i]["nutriments"]["sugars_100g"]
                                proteins = result["products"][i]["nutriments"]["proteins_100g"]
                                salts = result["products"][i]["nutriments"]["salt_100g"]
                                url_off = result["products"][i]["url"]
                                category_id = result["products"][i]["categories"]
                                for category in categories:
                                        regex(category_id_id)
                                        print(id)
                                Product.objects.get_or_create(name=name, description=description, nutriscore=nutriscore,\
                                stores=stores, image=image, brand=brand, calories=calories, lipids=lipids, \
                                sugars=sugars, proteins=proteins, salts=salts, url_off=url_off, category_id=3)
                        except:
                                pass

def regex(string):
        match = re.search(category, string)
        if match:
                global id
                id = categories.index(match.group(0)) + 1