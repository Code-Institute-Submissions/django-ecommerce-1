import uuid
from django.db import models
from django.urls import reverse


class Product(models.Model):
    """Store product model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=10)
    description = models.TextField()
    image = models.ImageField()
    is_live = models.BooleanField(default=True)

    def __str__(self):
        """return product title by default"""
        return self.title

    def get_absolute_url(self):
        """define default url for an instance of product model"""
        return reverse('product_detail', args=[str(self.id)])
