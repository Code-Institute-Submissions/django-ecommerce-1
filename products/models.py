import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class Product(models.Model):
    """Store product model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=10)
    description = models.TextField()
    image = models.ImageField(null=True)
    is_live = models.BooleanField(default=True)

    def review_count(self):
        """Return total reviews for product"""
        count = self.reviews.aggregate(
            count=models.Count('rating'))['count']

        if count is None:
            count = 0

        return count

    def __str__(self):
        """return product title by default"""
        return self.title

    def get_absolute_url(self):
        """define default url for an instance of product model"""
        return reverse('product_detail', kwargs={'pk': str(self.id)})


class Review(models.Model):
    """Users can leave product reviews"""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    rating = models.IntegerField(choices=RATING_CHOICES, default=3)
    review = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review
