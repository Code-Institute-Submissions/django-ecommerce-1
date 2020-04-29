from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.urls import reverse

from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div, Fieldset, Layout
from allauth.account.forms import LoginForm, SignupForm


class CustomUserCreationForm(UserCreationForm):
    """Updated for customer user model"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'first_name',
                  'last_name', 'date_of_birth', 'address', 'city',
                  'country', 'post_code')


class CustomUserChangeForm(UserChangeForm):
    """Updated for customer user model"""
    class Meta:
        model = get_user_model()
        fields = '__all__'


class CustomSignupForm(SignupForm):
    """Override the default allauth signup form"""
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=50)
    country = forms.CharField(max_length=100)
    post_code = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(label='Date of Birth (YYYY-MM-DD)')

    def save(self, request):
        """Add additional fields to be saved"""
        user = super(CustomSignupForm, self).save(request)
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.address = self.cleaned_data['address']
        user.city = self.cleaned_data['city']
        user.country = self.cleaned_data['country']
        user.post_code = self.cleaned_data['post_code']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        # create form structure using crispy forms
        self.helper = FormHelper()
        self.helper.form_id = 'user-signup-form'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('account_signup')
        self.helper.add_input(
            Submit('submit', 'Register'))
        self.helper.layout = Layout(
            Fieldset('Personal Details',
                     Div(
                         Div('first_name', css_class='col-12 col-sm-6 '
                             'col-md-4'),
                         Div('last_name', css_class='col-12 col-sm-6 '
                             'col-md-4'),
                         Div('date_of_birth', css_class='col-12 col-md-4'),
                         css_class='row')
                     ),
            Fieldset('Billing Address',
                     Div(
                         Div('address', css_class='col-12'),
                         Div('city', css_class='col-12 col-sm-4'),
                         Div('country', css_class='col-12 col-sm-4'),
                         Div('post_code', css_class='col-12 col-sm-4'),
                         css_class='row')
                     ),
            Fieldset('Login Details',
                     Div(
                         Div('email', css_class='col-12'),
                         Div('password1', css_class='col-12 col-sm-6'),
                         Div('password2', css_class='col-12 col-sm-6'),
                         css_class='row')
                     )
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'date_of_birth',
                  'address', 'city', 'country', 'post_code')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # create form structure using crispy forms
        self.helper = FormHelper()
        self.helper.form_id = 'user-profile-form'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('account_profile')
        self.helper.add_input(
            Submit('submit', 'Update', css_class='btn btn-success'))
        self.helper.layout = Layout(
            Fieldset('Personal Details',
                     Div(
                         Field('first_name', wrapper_class='col-12 col-sm-6 '
                               'col-md-4'),
                         Field('last_name',
                               wrapper_class='col-12 col-sm-6 col-md-4'),
                         Field('date_of_birth', wrapper_class='col-12 '
                               'col-md-4'),
                         css_class='row')
                     ),
            Fieldset('Address',
                     Div(
                         Field('address', wrapper_class='col-12'),
                         Field('city', wrapper_class='col-12 col-sm-4'),
                         Field('country', wrapper_class='col-12 col-sm-4'),
                         Field('post_code', wrapper_class='col-12 col-sm-4'),
                         css_class='row')
                     )
        )


class CustomLoginForm(LoginForm):
    """Extend allauth loginform with custom form layout"""

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        # create form structure using crispy forms
        self.helper = FormHelper()
        self.helper.form_id = 'user-login-form'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('account_login')
        self.helper.add_input(
            Submit('submit', 'Login'))
        self.helper.layout = Layout(
            Fieldset('Login Details',
                     Div(
                         Field(
                             'login', wrapper_class='col-12 col-sm-9 col-md-6'
                             ' col-lg-4'),
                         css_class='row'),
                     Div(
                         Field(
                             'password', wrapper_class='col-12 col-sm-9 '
                             'col-md-6 col-lg-4'),
                         css_class='row'),
                     )
        )
