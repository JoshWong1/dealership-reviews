from django.db import models
from django.utils.timezone import now


# Create your models here.
class CarModel(models.Model):
    Sedan, SUV, WAGON = "Sedan", "SUV", "WAGON"
    carModels = [(Sedan, "Sedan"), (SUV, "SUV"), (WAGON, "WAGON")]
    name = models.CharField(max_length=30, default = "model name")
    dealerID = models.IntegerField()
    Type = models.CharField(max_length=10, choices = carModels, default="Sedan")
    year = models.DateField()

    def __str__(self):
        return "Name: " + self.name + ", Type: " + self.Type + ", Year: " + str(self.year)

class CarMake(models.Model):
    modelId = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default = "make name")
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name + ", Description:" + self.description

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment= sentiment
        self.id = id
    