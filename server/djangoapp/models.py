from django.db import models
from django.utils.timezone import now


#CarMake model
class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name + ", Description:" + self.description

#CarModel model
class CarModel(models.Model):
    modelId = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    Sedan, SUV, WAGON = "Sedan", "SUV", "WAGON"
    carModels = [(Sedan, "Sedan"), (SUV, "SUV"), (WAGON, "WAGON")]
    name = models.CharField(max_length=30)
    dealerID = models.IntegerField()
    Type = models.CharField(max_length=10, choices = carModels, default="Sedan")
    year = models.DateField()

    def __str__(self):
        return "Name: " + self.name + ", Type: " + self.Type + ", Year: " + str(self.year)


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

class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment= None
        self.id = id
    