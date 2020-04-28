from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserModelTests(TestCase):
    """Test user defined CustomUser model"""

    def setUp(self):
        self.User = get_user_model()
        self.account = {
            'username': 'test_user',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test_user@test.com',
            'password': 'really_tough_password1!',
            'address': '123 Coders Drive',
            'city': 'Big City',
            'country': 'Python',
            'post_code': 'PY11 2CD',
            'date_of_birth': '1981-03-01'
        }

    def test_create_user(self):
        """Check that user can be created with custom fields"""
        user = self.User.objects.create_user(**self.account)

        self.assertEqual(user.username, self.account['username'])
        self.assertEqual(user.address, self.account['address'])
        self.assertEqual(user.date_of_birth, self.account['date_of_birth'])
        self.assertTrue(user.check_password(self.account['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Check that superuser can be created with custom fields"""
        user = self.User.objects.create_superuser(**self.account)

        self.assertEqual(user.username, self.account['username'])
        self.assertEqual(user.address, self.account['address'])
        self.assertEqual(user.date_of_birth, self.account['date_of_birth'])
        self.assertTrue(user.check_password(self.account['password']))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
