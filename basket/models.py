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
        return f'Created: {self.created_date} - Status: '
        f'{self.BASKET_STATUS[self.status-1][1]} - User: {self.user}'

    def count(self):
        """Return total number of items in basket"""
        count = self.basketitem_set.aggregate(
            count=models.Sum('quantity'))['count']

        if count is None:
            count = 0

        return count

    def total(self):
        """Return total price for the basket"""
        # get tuple which will be used to query product object for price
        products = self.basketitem_set.all().values_list('product_id',
                                                         'quantity')
        total = 0

        if products:
            for product in products:
                product_id = product[0]
                quantity = product[1]
                price = Product.objects.get(id=product_id).price

                total += quantity * price

        return total


class BasketItem(models.Model):
    """Captures detail on each item within a basket"""
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Item Total: {self.quantity * self.product.price} (Quantity: '
        f'{self.quantity}, Price: {self.product.price}) - '
        f'Product: {self.product.title} '

    def subtotal(self):
        """Return per item total's"""
        total = self.quantity * self.product.price

        if total is None:
            total = 0

        return total
