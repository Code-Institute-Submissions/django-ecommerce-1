from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Product


class ProductTests(TestCase):
    """Verify that product pages work as intended"""

    def setUp(self):
        """Create a product for testing"""
        self.product_details = {
            'title': 'Doggie Treats',
            'brand': 'Pawful Intentions',
            'category': 'Dog',
            'price': 9.99,
            'stock': 11,
            'description': 'Doggie Treats',
            # simulate the content required for imagefield
            'image': SimpleUploadedFile(
                name='image.jpg',
                content=open(settings.BASE_DIR +
                             '/test/image.jpg', 'rb').read(),
                content_type='image/jpeg'
            ),
            'is_live': True
        }
        self.product = Product.objects.create(**self.product_details)
        self.list_url = reverse('product_list')
        self.detail_url = self.product.get_absolute_url()

    def test_product_created_in_db(self):
        """Check that the product in setUp was created"""
        self.assertEqual(self.product.title, self.product_details['title'])
        self.assertEqual(self.product.price, self.product_details['price'])
        self.assertEqual(self.product.is_live, self.product_details['is_live'])

    def test_product_list_page_exists(self):
        """Check that product listing page response code is 200"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_product_list_page_contains_product(self):
        """Check that product has been listed"""
        response = self.client.get(self.list_url)
        self.assertContains(response, self.product_details['title'])
        self.assertContains(response, self.product_details['price'])
        # make sure the text that displays when products is empty is not shown
        self.assertNotContains(response, 'no products to display')

    def test_product_detail_page_successful(self):
        """Check product detail view exists and works"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_displays_content(self):
        """Ensure page lists all the expected product detail"""
        response = self.client.get(self.detail_url)
        self.assertContains(response, self.product_details['title'])
        self.assertContains(response, self.product_details['brand'])
        self.assertNotContains(response, 'category')
        self.assertContains(response, self.product_details['price'])
        self.assertNotContains(response, 'stock')
        self.assertContains(response, self.product_details['description'])

    def test_product_does_not_display(self):
        """Test that product does not show when is_live is set to False"""
        # store product details in local variable and override is_live value
        product_two_details = self.product_details
        product_two_details['title'] = 'DO_NOT_DISPLAY_PRODUCT'
        product_two_details['is_live'] = False
        # create new product
        product_two = Product.objects.create(**product_two_details)
        # check listing page does not show product
        list_response = self.client.get(self.list_url)
        self.assertNotContains(list_response, product_two_details['title'])
        # check that the initial product is still there
        self.assertContains(list_response, self.product.title)
        # check product detail page is unsuccessful (i.e. doesnt show)
        detail_response = self.client.get(product_two.get_absolute_url())
        self.assertNotEqual(detail_response, 200)

    def test_list_view_template(self):
        """Check that the correct template is being used"""
        response = self.client.get(self.list_url)
        self.assertTemplateUsed(response, 'products/product_list.html')

    def test_detail_view_template(self):
        """Check that the correct template is being used"""
        response = self.client.get(self.detail_url)
        self.assertTemplateUsed(response, 'products/product_detail.html')
