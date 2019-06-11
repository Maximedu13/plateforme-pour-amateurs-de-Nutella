from django.db import models
ARTISTS = {
  'francis-cabrel': {'name': 'Francis Cabrel'},
  'lej': {'name': 'Elijay'},
  'rosana': {'name': 'Rosana'},
  'maria-dolores-pradera': {'name': 'María Dolores Pradera'},
}


ALBUMS = [
  {'name': 'Sarbacane', 'artists': [ARTISTS['francis-cabrel']]},
  {'name': 'La Dalle', 'artists': [ARTISTS['lej']]},
  {'name': 'Luna Nueva', 'artists': [ARTISTS['rosana'], ARTISTS['maria-dolores-pradera']]}
]

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    nutriscore = models.CharField(max_length=1)
    stores = models.CharField(max_length=200, null=False)
    image = models.URLField(null=False, default='image')
    brand = models.CharField(max_length=100, null=False)
    calories = models.IntegerField(null=True)
    lipids = models.FloatField(null=True)
    sugars = models.FloatField(null=True)
    proteins = models.FloatField(null=True)
    salts = models.FloatField(null=True)
    url_off = models.URLField(null=False)

    def __str__(self):
        return self.name