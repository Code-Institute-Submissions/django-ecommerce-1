from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    """Test that homepage view and url work"""

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_view_url(self):
        """The homepage should return http code 200, i.e. successful"""
        self.assertEqual(self.response.status_code, 200)

    def test_view_template(self):
        """Check that homepage is using the intended template"""
        self.assertTemplateUsed(self.response, template_name='pages/home.html')
