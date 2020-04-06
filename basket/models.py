from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from products.models import Product

# Create your models here.


class Basket(models.Model):
    """Stores a user's current basket, transitioning when an order is placed"""
    IN_PROGRESS = 1
    PROCESSED = 2
    BASKET_STATUS = (
        (IN_PROGRESS, 'Open'),
        (PROCESSED, 'Processed')
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             blank=True, null=True)
    status = models.IntegerField(choices=BASKET_STATUS, default=IN_PROGRESS)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_date} - {self.id} - {self.user.email}'

    def count(self):
        """Return total number of items in basket"""
        return self.basketitem_set.aggregate(
            total=models.Sum('quantity'))['total']


class BasketItem(models.Model):
    """Captures detail on each item within a basket"""
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.basket.user.email} - basket_id: {self.basket.id} - \
            product: {self.product.title} - quantity: {self.quantity}'
