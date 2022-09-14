from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default='')

    def __str__(self):
        return "Name: " + self.name + \
                'Description: ' + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    TYPES = (
            ("SEDAN", "Sedan"), 
            ("SUV", "SUV"), 
            ("WAGON", "Wagon"), 
            ("COUPE", "Coupe")
        )

    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    car_type = models.CharField(max_length=50,choices=TYPES)
    year = models.DateField()
    dealer_id = models.IntegerField()
    
    def __str__(self):
        return "Name: " + self.name + \
                " Make: "+ self.make.name + \
                " Type: " + self.car_type + \
                " Year: " + str(self.year) + \
                " Dealer ID: " + str(self.dealer_id)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id) -> None:
        # Dealership Id
        self.dealership = dealership
        # Purchased from Dealer
        self.purchase = purchase
        # Reviewer Name
        self.name = name
        # Review id
        self.id = id
        # Review
        self.review = review
        # Purchase Date
        self.purchase_date = purchase_date
        # Car Make
        self.car_make = car_make
        # Car Model
        self.car_model = car_model
        # Car Year
        self.car_year = car_year
        # Review sentiment (Watson NLU)
        self.sentiment = sentiment
        
    def __str__(self) -> str:
        return "Review: " + self.review + \
            " Review By: " + self.name + \
            " Sentiment: " + self.sentiment