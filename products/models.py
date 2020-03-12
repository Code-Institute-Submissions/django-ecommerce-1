from django.db import models


class Product(models.Model):
    """Store product model"""
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=10)
    description = models.TextField()
    image = models.ImageField()
    is_live = models.BooleanField(default=True)

    def __str__(self):
        return self.title
