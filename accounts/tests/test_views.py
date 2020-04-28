from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class RegisterPageTests(TestCase):
    """Registration page functionality testing"""

    def setUp(self):
        self.url = reverse('account_signup')
        self.response = self.client.get(self.url)

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

    def test_register_page_submission(self):
        """Check that submission of form with valid data creates account"""
        form_details = {
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': '1981-03-01',
            'address': '123 Coders Drive',
            'city': 'Big City',
            'country': 'Python',
            'post_code': 'PY11 2CD',
            'email': 'test_user@test.com',
            'password1': 'really_tough_password1!',
            'password2': 'really_tough_password1!'
        }

        response = self.client.post(self.url, data=form_details, follow=True)

        # check account exists
        user = get_user_model().objects.get(email=form_details['email'])

        self.assertEqual(form_details['first_name'], user.first_name)
        self.assertEqual(form_details['last_name'], user.last_name)
        self.assertEqual(
            datetime.strptime(
                form_details['date_of_birth'], '%Y-%m-%d'
            ).date(),
            user.date_of_birth)
        self.assertEqual(form_details['address'], user.address)
        self.assertEqual(form_details['city'], user.city)
        self.assertEqual(form_details['country'], user.country)
        self.assertEqual(form_details['post_code'], user.post_code)
        self.assertEqual(form_details['email'], user.email)
        self.assertTrue(user.check_password(form_details['password1']))

        # check that page returns to...
        self.assertContains(
            response, 'Confirmation e-mail sent to ' + form_details['email'])


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
