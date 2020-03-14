from django.test import TestCase
from django.urls import reverse
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


class RegisterPageTests(TestCase):
    """Registration page functionality testing"""

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_register_page_exists(self):
        """Check that the page loads successfully"""
        self.assertEquals(self.response.status_code, 200)

    def test_register_template(self):
        """Check that the intended template is being used"""
        self.assertTemplateUsed(
            self.response, template_name='account/signup.html')
        self.assertContains(self.response, 'Register')

    def test_register_form_contains_csrf(self):
        """The form contains csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class ProfilePageTests(TestCase):
    """User profile page functionality testing"""

    def setUp(self):
        url = reverse('account_profile')
        self.public_response = self.client.get(url)

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

        # create user account
        user = get_user_model().objects.create_user(**self.account)
        self.client.login(username=user.username)

    def test_page_not_accessible_by_public(self):
        """The page should only be accessible when the user is logged in"""
        self.assertRedirects(self.public_response,
                             '/accounts/login/?next=/accounts/profile/')

        self.assertTemplateNotUsed(
            self.public_response, template_name='account/profile.html')

    def test_page_accessible_when_logged_in(self):
        """The page should be accessible when the user is logged in"""
        self.client.login(email='test_user@test.com',
                          password='really_tough_password1!')
        url = reverse('account_profile')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='account/profile.html')

    def test_user_update_successful(self):
        """Profile submission should result in updated database values"""
        # simulated data for post submission
        data = self.account
        # remove unnecessary inputs (i.e. these are not accessible on form)
        del(data['username'], data['email'], data['password'])
        # change the field values
        data['first_name'] = 'Sir Test'
        data['post_code'] = 'New Postcode'

        # account login
        self.client.login(email='test_user@test.com',
                          password='really_tough_password1!')

        # submit form to update profile with new data
        url = reverse('account_profile')
        response = self.client.post(url, data, follow=True)

        # perform tests
        self.assertContains(response, 'Your profile has been updated')

        # check that the user object has been updated
        user = get_user_model().objects.get(email='test_user@test.com')

        self.assertEquals(user.first_name, data['first_name'])
        self.assertEquals(user.post_code, data['post_code'])
