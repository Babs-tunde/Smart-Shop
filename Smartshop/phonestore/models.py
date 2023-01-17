from django.db import models

# Create your models here.


class Phone(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Invoice(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_address = models.TextField()
    date = models.DateField()
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return 'Invoice for ' + self.customer_name

