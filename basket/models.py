from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from products.models import Product
from checkout.models import Order, OrderItem

# Create your models here.


class BasketException(Exception):
    """Capture basket related exceptions"""


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

    def create_order(self, order_details, stripe_id=None):
        """Convert active basket into an order in the checkout app"""
        # check user exists
        items = self.basketitem_set.all()
        number_of_items = items.count()
        user = self.user

        if not user:
            # called with no user
            raise BasketException(
                'Order cannot be generated as there is no associated user')

        if not number_of_items:
            # called with no items in basket
            raise BasketException('Order cannot be generated as the basket '
                                  'is empty')

        if not stripe_id:
            # stripe_id is confirmation of payment, required field
            raise BasketException('Order cannot be created as there was a '
                                  'problem identifying the payment.')

        # create order
        order_data = {
            'user': user,
            # billing data is populated from user profile
            'billing_name': user.first_name + ' ' + user.last_name,
            'billing_address': user.address,
            'billing_city': user.city,
            'billing_country': user.country,
            'billing_post_code': user.post_code,
            # user can add shipping information if different from billing
            'shipping_name': order_details.get('shipping_name'),
            'shipping_address': order_details.get('shipping_address'),
            'shipping_city': order_details.get('shipping_city'),
            'shipping_country': order_details.get('shipping_country'),
            'shipping_post_code': order_details.get('shipping_post_code'),
            # store stripe payment id
            'stripe_id': stripe_id
        }

        order = Order.objects.create(**order_data)

        # since stripe_id is NOT None, payment has been received
        order.status = Order.PAID
        order.save()

        # loop through basket contents and add to orderitem object
        for item in items:
            for single_item in range(item.quantity):
                # input each item as a single item
                # an item with a quantity of three will be inputted three times
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price
                )

        # update basket so it can no longer be modified
        self.status = Basket.PROCESSED
        self.save()

        return order


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
