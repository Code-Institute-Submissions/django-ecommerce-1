from django.test import SimpleTestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):
    """Test that homepage view and url work"""

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_exists(self):
        """The homepage should return http code 200, i.e. successful"""
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        """Check that homepage is using the intended template"""
        self.assertTemplateUsed(self.response, template_name='home.html')

    def test_homepage_contains_header(self):
        """Homepage should contain a header 'homepage'"""
        self.assertContains(self.response, '<h1>Homepage</h1>')
