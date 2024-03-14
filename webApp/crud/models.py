# Create your models here.
from django.db import models


# declaring schema of table in databases
# Create your models here.
class Cars(models.Model):
    # Auto-incrementing primary key field:
    car_id = models.AutoField(primary_key=True)

    # Other fields for the Cars model:
    car_name = models.CharField(max_length=100)
    car_brand = models.CharField(max_length=10)
    car_model = models.CharField(max_length=30)

    # The __str__ method to represent the object as a string, usually useful in the Django admin or shell
    def __str__(self):
        return f"{self.car_brand} {self.car_model} (ID: {self.car_id})"
